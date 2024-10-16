import yfinance as yf
import numpy as np
import networkx as nx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from scipy.signal import stft
from scipy.stats import pearsonr
from sklearn.preprocessing import StandardScaler
from librosa.feature import mfcc
import matplotlib.pyplot as plt
import os
from datetime import datetime
import logging

from time_frequency import calculate_time_frequency, plot_time_frequency
from technical_analysis import TechnicalAnalysis

# Configure logging at the top of your main.py
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a directory to store images
os.makedirs("images", exist_ok=True)

def fetch_stock_data(symbol, start_date=None, end_date=None, interval="1d"):
    stock = yf.Ticker(symbol)
    data = stock.history(start=start_date, end=end_date, interval=interval)
    return data['Close'].values

def calculate_mel_spectrogram(prices, n_fft=256, hop_length=None):
    """
    Calculates the Mel spectrogram of stock prices using STFT.

    Args:
        prices (np.ndarray): Array of stock closing prices.
        n_fft (int): Number of FFT points.
        hop_length (int, optional): Number of points between successive frames. Defaults to n_fft//4.

    Returns:
        np.ndarray: Magnitude of the STFT.
    """
    if hop_length is None:
        hop_length = n_fft // 4  # Default to 1/4 of n_fft

    logger.info(f"Initial parameters - n_fft: {n_fft}, hop_length: {hop_length}")

    # Enforce hop_length constraints
    if hop_length <= 0:
        logger.warning("hop_length <= 0. Setting hop_length to 1.")
        hop_length = 1
    elif hop_length >= n_fft:
        logger.warning(f"hop_length ({hop_length}) >= n_fft ({n_fft}). Setting hop_length to n_fft - 1.")
        hop_length = n_fft - 1

    noverlap = n_fft - hop_length

    # Ensure noverlap is less than n_fft
    if noverlap >= n_fft:
        logger.warning(f"noverlap ({noverlap}) >= n_fft ({n_fft}). Adjusting noverlap to n_fft // 2.")
        noverlap = n_fft // 2

    logger.info(f"Adjusted parameters - noverlap: {noverlap}")

    # Final check to ensure noverlap < n_fft
    if noverlap >= n_fft:
        logger.error(f"Final noverlap ({noverlap}) is not less than n_fft ({n_fft}). Setting noverlap to n_fft - 1.")
        noverlap = n_fft - 1

    try:
        freqs, times, Zxx = stft(prices, nperseg=n_fft, noverlap=noverlap)
    except ValueError as e:
        logger.error(f"STFT Calculation Error: {e}")
        raise

    return np.abs(Zxx)

def extract_mfccs(spectrogram, n_mfcc=13):
    """
    Extracts MFCC features from the mel spectrogram.

    Args:
        spectrogram (np.ndarray): Mel spectrogram.
        n_mfcc (int): Number of MFCCs to extract.

    Returns:
        np.ndarray: MFCC feature matrix.
    """
    return mfcc(S=spectrogram, n_mfcc=n_mfcc)

def create_network(mfccs, threshold=0.7):
    G = nx.Graph()
    n_weeks = mfccs.shape[1]
    
    for i in range(n_weeks):
        for j in range(i+1, n_weeks):
            corr, _ = pearsonr(mfccs[:, i], mfccs[:, j])
            if corr > threshold:
                G.add_edge(i, j, weight=corr)
    
    return G

def plot_time_series(prices, symbol, filename):
    plt.figure(figsize=(10, 4))
    plt.plot(prices)
    plt.title(f"{symbol} Stock Price")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.tight_layout()
    plt.savefig(f"images/{filename}")
    plt.close()

def plot_spectrogram(spectrogram, symbol, filename):
    plt.figure(figsize=(10, 4))
    plt.imshow(spectrogram, aspect='auto', origin='lower')
    plt.title(f"{symbol} Mel Spectrogram")
    plt.xlabel("Time")
    plt.ylabel("Frequency")
    plt.colorbar(label='Magnitude')
    plt.tight_layout()
    plt.savefig(f"images/{filename}")
    plt.close()

def plot_mfccs(mfccs, symbol, filename):
    plt.figure(figsize=(10, 6))
    plt.imshow(mfccs, aspect='auto', origin='lower', cmap='viridis')
    plt.title(f"{symbol} MFCCs")
    plt.xlabel("Time")
    plt.ylabel("MFCC Coefficients")
    plt.colorbar(label='Magnitude')
    plt.tight_layout()
    plt.savefig(f"images/{filename}")
    plt.close()

def plot_time_frequency(spectrogram, symbol, freq_resolution_multiplier=1, filename=None):
    plt.figure(figsize=(10, 4))
    plt.imshow(spectrogram, aspect='auto', origin='lower', cmap='viridis')
    plt.title(f"{symbol} Time-Frequency Representation")
    plt.xlabel("Time")
    plt.ylabel("Frequency")
    plt.colorbar(label='Magnitude')
    plt.tight_layout()

    if filename:
        plt.savefig(f"images/{filename}")
    else:
        plt.savefig(f"images/{symbol}_time_frequency_x{freq_resolution_multiplier}.png")
    plt.close()

def fetch_stock_set(set_name):
    """
    Returns a list of stock symbols based on the stock set name.

    Args:
        set_name (str): Name of the stock set ("sp500", "dow", "nasdaq100").

    Returns:
        list: List of stock symbols.

    Raises:
        ValueError: If an unknown stock set name is provided.
    """
    if set_name.lower() == "sp500":
        # Predefined list of S&P 500 symbols (for brevity, only a few are listed)
        return [
            "AAPL", "MSFT", "GOOGL", "AMZN", "FB", "BRK.B", "JPM", "JNJ",
            "V", "PG", "UNH", "DIS", "NVDA", "HD", "MA",
            # ... add more symbols as needed
        ]
    elif set_name.lower() == "dow":
        # Predefined list of Dow Jones symbols
        return [
            "AAPL", "MSFT", "JNJ", "V", "PG",
            "UNH", "DIS", "HD", "MA", "IBM",
            # ... add more symbols as needed
        ]
    elif set_name.lower() == "nasdaq100":
        # Predefined list of NASDAQ-100 symbols
        return [
            "AAPL", "MSFT", "AMZN", "FB", "GOOGL",
            "GOOG", "INTC", "CSCO", "CMCSA", "ADBE",
            # ... add more symbols as needed
        ]
    else:
        raise ValueError(f"Unknown stock set: {set_name}")

@app.get("/analyze")
async def analyze_stocks(
    symbols: str = Query(None),
    stock_set: str = Query(None),
    freq_resolution_multiplier: float = Query(1.0, ge=1.0, description="Multiplier to adjust frequency resolution"),
    section_start: int = Query(0, ge=0, description="Start index of the section"),
    section_end: int = Query(None, ge=0, description="End index of the section"),
    start_date: str = Query(None, description="Start date for data (YYYY-MM-DD)"),
    end_date: str = Query(None, description="End date for data (YYYY-MM-DD)"),
    interval: str = Query("1d", description="Data interval (1d, 1wk, 1mo)"),
    refresh: bool = Query(False, description="Force refresh of graphs")
):
    if symbols is None and stock_set is None:
        raise HTTPException(status_code=400, detail="Either symbols or stock_set must be provided")

    if stock_set:
        try:
            symbols_list = fetch_stock_set(stock_set)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        symbols_list = [symbol.strip().upper() for symbol in symbols.split(',') if symbol.strip()]

    if not symbols_list:
        raise HTTPException(status_code=400, detail="No valid symbols provided.")

    results = {}
    
    for symbol in symbols_list:
        try:
            prices = fetch_stock_data(symbol, start_date, end_date, interval)
            if len(prices) == 0:
                logger.warning(f"No price data found for symbol: {symbol}")
                continue

            # Handle section selection
            if section_end is not None:
                selected_prices = prices[section_start:section_end]
            else:
                selected_prices = prices

            if len(selected_prices) < 2:
                logger.warning(f"Not enough price data for symbol: {symbol} after section selection.")
                continue

            spectrogram = calculate_mel_spectrogram(selected_prices)

            mfccs = extract_mfccs(spectrogram)  # Ensure that mfccs is computed before normalization

            # Normalize MFCCs
            scaler = StandardScaler()
            mfccs_normalized = scaler.fit_transform(mfccs.T).T

            G = create_network(mfccs_normalized)

            # Technical Analysis
            ta = TechnicalAnalysis(selected_prices)
            ta.calculate_moving_average()
            ta.calculate_rsi()
            ta.calculate_macd()
            ta.calculate_bollinger_bands()
            indicators = ta.get_indicators()

            # Convert network to JSON-serializable format
            nodes = [{"id": n, "group": 1} for n in G.nodes()]
            links = [{"source": u, "target": v, "value": G[u][v]['weight']} for u, v in G.edges()]

            # Generate and save visualizations
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

            time_series_filename = f"{symbol}_time_series_{timestamp}.png"
            plot_time_series(selected_prices, symbol, filename=time_series_filename)

            spectrogram_filename = f"{symbol}_spectrogram_{timestamp}.png"
            plot_spectrogram(spectrogram, symbol, filename=spectrogram_filename)

            mfccs_filename = f"{symbol}_mfccs_{timestamp}.png"
            plot_mfccs(mfccs, symbol, filename=mfccs_filename)

            # Compute and plot time-frequency graph with adjusted frequency resolution
            tf_spectrogram = calculate_time_frequency(selected_prices, freq_resolution_multiplier=freq_resolution_multiplier)
            time_frequency_filename = f"{symbol}_time_frequency_x{freq_resolution_multiplier}_{timestamp}.png"
            plot_time_frequency(tf_spectrogram, symbol, freq_resolution_multiplier, filename=time_frequency_filename)

            results[symbol] = {
                "nodes": nodes,
                "links": links,
                "time_series_image": f"/images/{time_series_filename}",
                "spectrogram_image": f"/images/{spectrogram_filename}",
                "mfccs_image": f"/images/{mfccs_filename}",
                "time_frequency_image": f"/images/{time_frequency_filename}",
                "prices": selected_prices.tolist(),
                "mfccs": mfccs.tolist(),
                "section_start": section_start,
                "section_end": section_end,
                "indicators": {
                    "sma": ta.indicators.get('sma').tolist(),
                    "rsi": ta.indicators.get('rsi').tolist(),
                    "macd": {
                        "macd": ta.indicators.get('macd')['macd'].tolist(),
                        "macdsignal": ta.indicators.get('macd')['macdsignal'].tolist(),
                        "macdhist": ta.indicators.get('macd')['macdhist'].tolist(),
                    },
                    "bollinger_bands": {
                        "upperband": ta.indicators.get('bollinger_bands')['upperband'].tolist(),
                        "middleband": ta.indicators.get('bollinger_bands')['middleband'].tolist(),
                        "lowerband": ta.indicators.get('bollinger_bands')['lowerband'].tolist(),
                    }
                }
            }
        
        except ValueError as e:
            logger.error(f"ValueError for symbol {symbol}: {e}")
            continue
        except Exception as e:
            logger.error(f"Unexpected error for symbol {symbol}: {e}")
            continue

    if not results:
        raise HTTPException(status_code=400, detail="No valid data processed.")

    return results

@app.get("/images/{image_name}")
async def get_image(image_name: str):
    image_path = f"images/{image_name}"
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path)

@app.get("/technical_indicators/{symbol}")
async def get_technical_indicators(
    symbol: str,
    start_date: str = Query(None, description="Start date for data (YYYY-MM-DD)"),
    end_date: str = Query(None, description="End date for data (YYYY-MM-DD)"),
    interval: str = Query("1d", description="Data interval (1d, 1wk, 1mo)")
):
    prices = fetch_stock_data(symbol, start_date, end_date, interval)
    if len(prices) == 0:
        raise HTTPException(status_code=404, detail="No price data found for the symbol.")

    ta = TechnicalAnalysis(prices)
    ta.calculate_moving_average()
    ta.calculate_rsi()
    ta.calculate_macd()
    ta.calculate_bollinger_bands()
    indicators = ta.get_indicators()

    return {
        "symbol": symbol,
        "indicators": {
            "sma": indicators.get('sma').tolist(),
            "rsi": indicators.get('rsi').tolist(),
            "macd": {
                "macd": indicators.get('macd')['macd'].tolist(),
                "macdsignal": indicators.get('macd')['macdsignal'].tolist(),
                "macdhist": indicators.get('macd')['macdhist'].tolist(),
            },
            "bollinger_bands": {
                "upperband": indicators.get('bollinger_bands')['upperband'].tolist(),
                "middleband": indicators.get('bollinger_bands')['middleband'].tolist(),
                "lowerband": indicators.get('bollinger_bands')['lowerband'].tolist(),
            }
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

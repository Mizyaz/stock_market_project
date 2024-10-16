import logging
from scipy.signal import stft
import matplotlib.pyplot as plt
import os
import numpy as np

# Configure logging at the top of your time_frequency.py
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_time_frequency(prices, n_fft=256, hop_length=None, freq_resolution_multiplier=1):
    """
    Calculates the time-frequency representation of the stock prices using STFT.

    Args:
        prices (np.ndarray): Array of stock closing prices.
        n_fft (int): Number of FFT points.
        hop_length (int, optional): Number of points between successive frames.
        freq_resolution_multiplier (float): Multiplier to adjust frequency resolution.

    Returns:
        np.ndarray: Magnitude of the STFT.
    """
    adjusted_n_fft = int(n_fft * freq_resolution_multiplier)
    logger.info(f"Adjusted n_fft: {adjusted_n_fft} with freq_resolution_multiplier: {freq_resolution_multiplier}")

    if hop_length is None:
        hop_length = adjusted_n_fft // 4  # Default to 1/4 of adjusted_n_fft

    # Enforce hop_length constraints
    if hop_length <= 0:
        logger.warning("hop_length <= 0. Setting hop_length to 1.")
        hop_length = 1
    elif hop_length >= adjusted_n_fft:
        logger.warning(f"hop_length ({hop_length}) >= adjusted_n_fft ({adjusted_n_fft}). Setting hop_length to adjusted_n_fft - 1.")
        hop_length = adjusted_n_fft - 1

    noverlap = adjusted_n_fft - hop_length

    # Ensure noverlap is less than adjusted_n_fft
    if noverlap >= adjusted_n_fft:
        logger.warning(f"noverlap ({noverlap}) >= adjusted_n_fft ({adjusted_n_fft}). Adjusting noverlap to adjusted_n_fft // 2.")
        noverlap = adjusted_n_fft // 2

    logger.info(f"Adjusted parameters - noverlap: {noverlap}")

    # Final check to ensure noverlap < adjusted_n_fft
    if noverlap >= adjusted_n_fft:
        logger.error(f"Final noverlap ({noverlap}) is not less than adjusted_n_fft ({adjusted_n_fft}). Setting noverlap to adjusted_n_fft - 1.")
        noverlap = adjusted_n_fft - 1

    try:
        freqs, times, Zxx = stft(prices, nperseg=adjusted_n_fft, noverlap=noverlap)
    except ValueError as e:
        logger.error(f"Time-Frequency STFT Calculation Error: {e}")
        raise

    return np.abs(Zxx)

def plot_time_frequency(spectrogram, symbol, freq_resolution_multiplier=1, filename=None):
    """
    Plots and saves the time-frequency graph.

    Args:
        spectrogram (np.ndarray): Magnitude of the STFT.
        symbol (str): Stock symbol.
        freq_resolution_multiplier (float): Multiplier to adjust frequency resolution.
        filename (str, optional): Filename to save the plot.
    """
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

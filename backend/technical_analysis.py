import talib
import numpy as np
import logging

class TechnicalAnalysis:
    def __init__(self, prices: np.ndarray):
        """
        Initialize with stock closing prices.

        Args:
            prices (np.ndarray): Array of stock closing prices.
        """
        self.prices = prices
        self.indicators = {}
        self.logger = logging.getLogger(__name__)

    def calculate_moving_average(self, timeperiod: int = 20):
        """
        Calculate Simple Moving Average (SMA).

        Args:
            timeperiod (int, optional): Number of periods for SMA. Defaults to 20.
        """
        self.indicators['sma'] = talib.SMA(self.prices, timeperiod=timeperiod)
        self.logger.info(f"Calculated SMA with timeperiod={timeperiod}.")

    def calculate_rsi(self, timeperiod: int = 14):
        """
        Calculate Relative Strength Index (RSI).

        Args:
            timeperiod (int, optional): Number of periods for RSI. Defaults to 14.
        """
        self.indicators['rsi'] = talib.RSI(self.prices, timeperiod=timeperiod)
        self.logger.info(f"Calculated RSI with timeperiod={timeperiod}.")

    def calculate_macd(self, fastperiod: int = 12, slowperiod: int = 26, signalperiod: int = 9):
        """
        Calculate Moving Average Convergence Divergence (MACD).

        Args:
            fastperiod (int, optional): Fast EMA period. Defaults to 12.
            slowperiod (int, optional): Slow EMA period. Defaults to 26.
            signalperiod (int, optional): Signal line period. Defaults to 9.
        """
        macd, macdsignal, macdhist = talib.MACD(self.prices, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
        self.indicators['macd'] = {
            'macd': macd,
            'macdsignal': macdsignal,
            'macdhist': macdhist
        }
        self.logger.info(f"Calculated MACD with fastperiod={fastperiod}, slowperiod={slowperiod}, signalperiod={signalperiod}.")

    def calculate_bollinger_bands(self, timeperiod: int = 20, nbdevup: float = 2, nbdevdn: float = 2, matype: int = 0):
        """
        Calculate Bollinger Bands.

        Args:
            timeperiod (int, optional): Number of periods for Bollinger Bands. Defaults to 20.
            nbdevup (float, optional): Number of standard deviations for the upper band. Defaults to 2.
            nbdevdn (float, optional): Number of standard deviations for the lower band. Defaults to 2.
            matype (int, optional): Type of Moving Average. Defaults to 0 (SMA).
        """
        upperband, middleband, lowerband = talib.BBANDS(self.prices, timeperiod=timeperiod, nbdevup=nbdevup, nbdevdn=nbdevdn, matype=matype)
        self.indicators['bollinger_bands'] = {
            'upperband': upperband,
            'middleband': middleband,
            'lowerband': lowerband
        }
        self.logger.info(f"Calculated Bollinger Bands with timeperiod={timeperiod}, nbdevup={nbdevup}, nbdevdn={nbdevdn}, matype={matype}.")

    def get_indicators(self):
        """
        Get the calculated indicators.

        Returns:
            dict: Dictionary of indicators.
        """
        return self.indicators

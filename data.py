import yfinance as yf
from pandas import DataFrame


def get_closing_prices(tickers: list[str], start: str, end: str) -> DataFrame:
    """
    Fetches historical closing prices for a list of stock tickers over a specified date range.

    Parameters:
        tickers (list[str]): A list of stock ticker symbols (e.g., ["AAPL", "MSFT"]).
        start (str): The start date for the data in "YYYY-MM-DD" format.
        end (str): The end date for the data in "YYYY-MM-DD" format.

    Returns:
        pandas.DataFrame: A DataFrame containing the closing prices for each ticker,
        indexed by date. Rows with missing values are removed.

    Notes:
        - Uses the yfinance library to retrieve data.
        - If multiple tickers are provided, the resulting DataFrame will have
          one column per ticker.
    """
    ticker = yf.Tickers(" ".join(tickers))
    data = ticker.download(start=start, end = end)
    data = data["Close"]
    data =  data.dropna()
    return data
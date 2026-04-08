from src.data import get_closing_prices
from src.cointegration import is_cointegrated
from src.spread import compute_spread
from src.signals import generate_signals
# import itertools
# from tqdm import tqdm
import matplotlib.pyplot as plt


# tickers = [
#     "JPM","BAC","WFC","C","GS","MS",
#     "RY","TD","BMO","BNS",
#     "XOM","CVX","COP","PSX","ENB","TRP","SU",
#     "KO","PEP","PG","CL","WMT","COST",
#     "AAPL","MSFT","GOOGL","AMZN","META","NVDA",
#     "SPY","IVV","VOO","QQQ","XLK","XLF","VFH","XLE","VDE",
#     "CAT","DE","UNP","CSX",
#     "JNJ","PFE","MRK","ABBV","LLY"
# ]


def main():
    data = get_closing_prices(tickers=["GOOGL", "IVV"], start="2016-01-01", end="2020-12-31")
    

    
    cointegrated, p, beta = is_cointegrated(data["GOOGL"], data["IVV"])
    spread, z_score = compute_spread(data["GOOGL"], data["IVV"], beta)
    signals = generate_signals(z_score=z_score)

    plt.plot(z_score)
    plt.plot(signals)
    plt.show()
    
if __name__ == "__main__":
    main()

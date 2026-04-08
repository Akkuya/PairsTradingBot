from data import get_closing_prices
from cointegration import is_cointegrated
import itertools


tickers = [
    "KO", "PEP",
    "XOM", "CVX",
    "SPY", "IVV",
    "QQQ", "XLK",
    "MSFT", "AAPL"
]


def main():
    data = get_closing_prices(tickers=tickers, start="2016-01-01", end="2020-12-31")
    results = []

    for a, b in itertools.combinations(tickers, 2):
        cointegrated, p, beta = is_cointegrated(data[a], data[b])
        
        results.append((a, b,  cointegrated, p, beta))

    results.sort(key=lambda x: x[3])

    for r in results[:10]:
        print(r)
    
if __name__ == "__main__":
    main()

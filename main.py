from src.data import get_closing_prices
from src.cointegration import is_cointegrated
from src.spread import compute_spread
from src.signals import generate_signals
from src.backtest import backtest
from src.metrics import compute_metrics

def main():

    tickers = input("Enter the two tickers that you want to run the strategy on: ").split(" ")
    start = input("Enter start date: (YYYY-MM-DD): ")
    end = input("Enter END date: (YYYY-MM-DD): ")
    capital = float(input("Enter starting capital: "))
    
    cost = float(input("Enter transcation cost: "))
    
    data = get_closing_prices(tickers=tickers, start=start, end=end)
    _, _, beta = is_cointegrated(data[tickers[0]], data[tickers[1]])
    _, z_score = compute_spread(data[tickers[0]], data[tickers[1]], beta)
    signals = generate_signals(z_score=z_score)
    portfolio = backtest(signals, data, tickers[0], tickers[1], initial_capital=capital, transaction_cost=cost)
    compute_metrics(portfolio, signals, data, capital, start, end)
    
if __name__ == "__main__":
    main()

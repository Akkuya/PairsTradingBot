from pandas import Series, DataFrame
import matplotlib.pyplot as plt
from src.data import get_closing_prices

def compute_metrics(portfolio_values: Series, signals: Series, data: DataFrame, initial_capital: int) -> None:
    """
    Computes and displays performance metrics for a trading strategy.

    Parameters:
        portfolio_values (Series): Time series of portfolio value (equity curve).
        signals (Series): Trading signals used in the backtest.
        data (DataFrame): Price data for the traded assets.
        initial_capital (int): Starting portfolio value.

    Outputs:
        Prints key performance metrics and displays plots.

    Metrics:
        - Total return (%)
        - Annualized return (%)
        - Sharpe ratio
        - Sortino ratio
        - Maximum drawdown (%)

    Visualization:
        - Strategy vs SPY benchmark
        - Drawdown over time

    Notes:
        - Assumes 252 trading days per year.
        - Uses a fixed 5% annual risk-free rate.
    """
    spy_price = get_closing_prices(tickers=["SPY"], start="2016-01-01", end="2020-12-31")

    spy_normalized = (spy_price / spy_price.iloc[0]) * initial_capital

    total_return = (portfolio_values.iloc[-1] - initial_capital)/initial_capital * 100
    years = len(portfolio_values) / 252
    
    annualized_return = (1 + total_return/100) ** (1/years) - 1

    daily_returns = portfolio_values.pct_change()
    avg_return = daily_returns.mean()
    std_dev_return = daily_returns.std()
    sharpe_ratio = (avg_return - (0.05/252)) / std_dev_return
    
    negative_returns = daily_returns[daily_returns < 0]
    downside_std = negative_returns.std()
    sortino_ratio = (avg_return - (0.05/252)) / downside_std
    
    portfolio_max = portfolio_values.cummax()
    drawdown = ((portfolio_values - portfolio_max)/portfolio_max)
    max_drawdown=drawdown.min()


    
    print(f"Total Return: {total_return:.2f}%")
    print(f"Annualized Return: {annualized_return:.2f}%")
    print(f"Sharpe Ratio: {sharpe_ratio:.3f}")
    print(f"Sortino Ratio: {sortino_ratio:.3f}")
    print(f"Max Drawdown: {max_drawdown*100:.2f}%")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    ax1.plot(spy_normalized, label="SPY")
    ax1.plot(portfolio_values, label="Strategy")
    ax1.legend()
    ax1.set_title("Strategy vs SPY")

    ax2.plot(drawdown, label="Drawdown", color="red")
    ax2.set_title("Drawdown")
    ax2.legend()

    plt.tight_layout()
    plt.show()
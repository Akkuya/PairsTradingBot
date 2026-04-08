from pandas import Series
from math import floor

def backtest(signals: Series, data: Series, ticker_a: str, ticker_b: str,  initial_capital=10000, transaction_cost=0.001) -> Series:
    """
    Simulates a pairs trading strategy based on generated signals.

    Parameters:
        signals (Series): Trading signals (-1 = long spread, 1 = short spread, 0 = flat).
        data (DataFrame): Price data containing both ticker columns.
        ticker_a (str): First asset in the pair.
        ticker_b (str): Second asset in the pair.
        initial_capital (float): Starting cash for the portfolio.
        transaction_cost (float): Proportional cost per trade (e.g., 0.001 = 0.1%).

    Returns:
        Series: Portfolio value over time (equity curve).

    Notes:
        - Positions are opened/closed when signals change.
        - Capital is split equally between both assets.
        - Accounts for transaction costs on each trade.
        - Avoids lookahead bias by using shifted signals.
    """
    cash = initial_capital
    portfolio_value = cash
    portfolio_values = []

    position = {}

    for i in range(len(signals)):
        day = signals.index[i]

        prev_signal = signals.iloc[i-1] if i > 0 else 0
        current_signal = signals.iloc[i]

        price_a = data.loc[day, ticker_a]
        price_b = data.loc[day, ticker_b]

        # OPEN
        if prev_signal == 0 and current_signal != 0:
            shares_a = floor(cash / 2 / price_a)
            shares_b = floor(cash / 2 / price_b)

            position = {
                "shares_a": shares_a,
                "shares_b": shares_b,
                "direction": current_signal
            }

            if current_signal == 1:
                cash += price_a * shares_a
                cash -= price_b * shares_b
            else:
                cash -= price_a * shares_a
                cash += price_b * shares_b

            cash -= transaction_cost * (price_a * shares_a + price_b * shares_b)

        # CLOSE
        elif prev_signal != 0 and current_signal == 0:
            if position:

                shares_a = position["shares_a"]
                shares_b = position["shares_b"]
                direction = position["direction"]

                if direction == 1:
                    cash -= price_a * shares_a
                    cash += price_b * shares_b
                else:
                    cash += price_a * shares_a
                    cash -= price_b * shares_b

                cash -= transaction_cost * (price_a * shares_a + price_b * shares_b)
                
                position = {}

        # PORTFOLIO VALUE
        shares_a = position.get("shares_a", 0)
        shares_b = position.get("shares_b", 0)
        direction = position.get("direction", 0)

        if direction == 1:
            portfolio_value = cash - (price_a * shares_a) + (price_b * shares_b)
        elif direction == -1:
            portfolio_value = cash + (price_a * shares_a) - (price_b * shares_b)
        else:
            portfolio_value = cash

        portfolio_values.append(portfolio_value)
        

    return Series(portfolio_values, index=signals.index)
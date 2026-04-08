from pandas import Series

def compute_spread(series_a: Series, series_b: Series, beta: float, lookback=60) -> tuple[Series, Series]:
    """
    Computes the spread between two time series and its rolling z-score.

    Parameters:
        series_a (Series): First time series.
        series_b (Series): Second time series.
        beta (float): Hedge ratio from regression.
        lookback (int): Window size for rolling mean and std.

    Returns:
        tuple:
            - Series: Spread (series_a - beta * series_b)
            - Series: Z-score of the spread
    """
    spread:Series = series_a - beta * series_b

    rolling = spread.rolling(window=lookback)
    r_mean = rolling.mean()
    r_std = rolling.std()

    z_score = (spread - r_mean) / r_std

    return (spread, z_score)
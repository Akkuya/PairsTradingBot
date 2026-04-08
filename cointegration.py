import statsmodels.api as sm
import statsmodels.tsa.stattools as st
from pandas import Series, Float64Dtype as float, BooleanDtype as bool

def is_cointegrated(series_a: Series, series_b: Series) -> tuple[bool, float, float]:
    """
    Checks if two time series are cointegrated.

    Parameters:
        series_a: First time series.
        series_b: Second time series.

    Returns:
        tuple:
            - bool: True if cointegrated, False otherwise.
            - float: p-value from the ADF test.
            - float: Hedge ratio from the regression.

    Notes:
        - Runs a regression to find the hedge ratio.
        - Tests if the spread is stationary using the ADF test.
        - Uses a 0.05 threshold for cointegration.
    """
    ols = sm.OLS(series_a, sm.add_constant(series_b))
    model = ols.fit()
    hedge_ratio = model.params.iloc[1]
    
    spread = series_a - hedge_ratio * series_b

    adf = st.adfuller(spread)
    p_value = adf[1]

    cointegrated = p_value < 0.05
    
    return (cointegrated, p_value, hedge_ratio)



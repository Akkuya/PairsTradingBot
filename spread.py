from cointegration import is_cointegrated
from pandas import Series, Float64Dtype as float, BooleanDtype as bool

def compute_z_score(series_a: Series, series_b: Series) -> tuple[Series, Series]:
    _, _, hedge_ratio = is_cointegrated(series_a, series_b)
    spread = series_a - hedge_ratio * series_b 
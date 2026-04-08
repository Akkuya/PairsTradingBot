from pandas import Series
import numpy as np

def generate_signals(z_score: Series) -> Series:
    """
    Generates trading signals based on z-score thresholds.

    Parameters:
        z_score (Series): Z-score of the spread.

    Returns:
        Series: Trading signals where:
            -1 = long spread (z < -2)
             1 = short spread (z > 2)
             0 = no position

    Notes:
        - Signals are shifted to avoid lookahead bias.
    """
    signals = z_score.shift(1)
    
    cond_list = [signals < -2, signals > 2]
    choice_list = [-1, 1]
    signals = Series(np.select(condlist=cond_list, choicelist=choice_list, default=0), index=z_score.index)

    return signals
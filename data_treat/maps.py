import numpy as np
import pandas as pd

def map_range(
    in_series: pd.Series,
    in_min: float=None,
    in_max: float=None,
    out_min: float=0.,
    out_max: float=1.,
    invert: bool=False,
    to_int: bool=False
) -> pd.Series:
    """
    This function maps a data range to a new data range.

    Args:
        in_series (pd.Series): Series with range to be mapped.
        in_min (float, optional): Minimum for the original series to use in the
            mapping. if None, takes the minimum of the series.
            If greater than the minimum of the series, the series
            will be mapped with clipping.
        in_max (float, optional): Maximum for the original series to use in the
            mapping. if None, takes the maximum of the series.
            If less than the maximum of the series, the series
            will be mapped with clipping.
        out_min (float, optional): Minimum of the mapped series. Defaults to 0..
        out_max (float, optional): Maximum of the mapped series. Defaults to 1..
        invert (bool, optional): Whether or not the mapped
            series should be inverted with regards to the original series.
            Defaults to False.
        to_int (bool, optional): Whether or not the mapped
            series should be should be cast to int for use in e.g. color scales.
            Defaults to False.

    Returns:
        out_series (pd.Series): Mapped series.
    """

    # Sets incoming min and max to series values if none are given.
    if in_min is None:
        in_min = in_series.min()

    if in_max is None:
        in_max = in_series.max()

    # Calculate amplitudes.
    amplitude_in = in_max - in_min
    amplitude_out = out_max - out_min
    # Create a temporary normed series to apply the new scaling.
    norm_series = (in_series - in_min)/amplitude_in
    # Apply scaling.
    out_series = (norm_series + out_min) * amplitude_out
    # Apply clipping to prevent out-of-range values.
    out_series.clip(lower=out_min, upper=out_max, inplace=True)

    # If inversion is requested, do that.
    if invert:
        out_series = out_max - (out_series - out_min)

    # If casting to int is requested, do that.
    if to_int:
        out_series = out_series.astype(int)

    return out_series
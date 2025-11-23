"""
DateTime utility functions for FlowViz
Handles date format detection and parsing
"""

import pandas as pd


def detect_datetime_format(series: pd.Series) -> str | None:
    """
    Try to infer a consistent datetime format for the series.
    
    Args:
        series: Pandas Series containing potential datetime strings
        
    Returns:
        Detected datetime format string or None if no format detected
    """
    cleaned = series.dropna().astype(str).str.strip()
    if cleaned.empty:
        return None

    # Try common datetime formats
    common_formats = [
        '%Y-%m-%d',
        '%Y/%m/%d',
        '%d-%m-%Y',
        '%d/%m/%Y',
        '%m-%d-%Y',
        '%m/%d/%Y',
        '%Y-%m-%d %H:%M:%S',
        '%Y/%m/%d %H:%M:%S',
        '%d-%m-%Y %H:%M:%S',
        '%d/%m/%Y %H:%M:%S',
    ]
    
    sample = cleaned.head(50)
    
    for fmt in common_formats:
        try:
            # Try to parse the sample with this format
            pd.to_datetime(sample, format=fmt, errors='raise')
            return fmt
        except (ValueError, TypeError):
            continue
    
    return None


def parse_datetime_column(df: pd.DataFrame, col: str, date_format: str | None = None) -> pd.Series:
    """
    Parse a datetime column with optional format specification.
    
    Args:
        df: DataFrame containing the column
        col: Column name to parse
        date_format: Optional datetime format string
        
    Returns:
        Parsed datetime Series
    """
    if date_format:
        return pd.to_datetime(df[col], format=date_format, errors='coerce')
    else:
        # Remove deprecated infer_datetime_format parameter
        # Pandas now infers format by default
        return pd.to_datetime(df[col], errors='coerce')

"""
Constants used across QuantConnect trading strategies.

This module centralizes all magic numbers and configuration values
to ensure consistency and ease of maintenance across the project.
"""

# =============================================================================
# Annualization Factors
# =============================================================================
# Number of trading days in a year (used for annualizing returns, volatility, etc.)
ANN_FACTOR_TRADING_DAYS: int = 252

# Number of compounding periods per year for quarterly data
ANN_FACTOR_CARRY_QUARTERLY: int = 4

# Number of compounding periods per year for monthly data
ANN_FACTOR_CARRY_MONTHLY: int = 12


# =============================================================================
# Risk Management Defaults
# =============================================================================
# Default target annual volatility for volatility-targeted strategies
DEFAULT_TARGET_VOLATILITY: float = 0.40

# Maximum absolute signal value (prevents extreme position sizing)
DEFAULT_SIGNAL_CAP: float = 0.95

# Rolling window length for volatility calculation (in trading days)
DEFAULT_VOLATILITY_WINDOW: int = 21


# =============================================================================
# Rebalancing Frequencies
# =============================================================================
# Rebalance on a monthly basis
REBALANCE_MONTHLY: str = "monthly"

# Rebalance on a weekly basis
REBALANCE_WEEKLY: str = "weekly"


# =============================================================================
# Lookback Periods
# =============================================================================
# Short-term lookback: approximately 1 month (21 trading days)
LOOKBACK_1M: int = 21

# Medium-term lookback: approximately 3 months (63 trading days)
LOOKBACK_3M: int = 63

# Medium-term lookback: approximately 6 months (126 trading days)
LOOKBACK_6M: int = 126

# Long-term lookback: approximately 1 year (252 trading days)
LOOKBACK_1Y: int = 252


# =============================================================================
# Warmup and Initialization
# =============================================================================
# Buffer days added to lookback periods for warmup to ensure sufficient data
WARMUP_BUFFER_DAYS: int = 30


# =============================================================================
# Statistical Measures
# =============================================================================
# Lookback period for calculating skewness (1 year of data)
SKEWNESS_LOOKBACK: int = 252


# =============================================================================
# Percentile/Quantile Thresholds
# =============================================================================
# Top tercile threshold (top 33% of values)
TERCILE_TOP: float = 0.33

# Bottom tercile threshold (bottom 33% of values)
TERCILE_BOTTOM: float = 0.33

# Strategy Implementation Plan: S02 - Time-Series Momentum Enhanced (Baltas 2020)

## TL;DR

> **Baltas and Kosowski (2020) Enhanced Time-Series Momentum**
>
> **Signal**: 12-month past return sign (same as Moskowitz)
> **Enhancement**: Yang-Zhang volatility, correlation-adjusted weights
> **Sizing**: Volatility-scaled with pairwise correlation adjustment
> **Turnover Reduction**: >30% via improved volatility estimation
> **Expected Sharpe**: ~0.80 (improved from 0.75)

---

## Context

### Original Reference
Baltas, N. and Kosowski, R., 2020. "Demystifying time-series momentum strategies: Volatility estimators, trading rules and pairwise correlations." Market Momentum: Theory and Practice, Wiley.

### Key Enhancements vs. Moskowitz 2012

1. **Alternative Volatility Estimators**:
   - Standard EWMA (Equally Weighted Moving Average)
   - Yang-Zhang (YZ) realized volatility estimator
   - Rolling realized volatility

2. **Correlation-Aware Weighting**:
   - Product weighting (multiplicative signal combination)
   - Equal weighting comparison
   - Dynamic leverage based on pairwise correlations

3. **Improved Trading Rules**:
   - Continuous trend signals vs. discrete sign-based
   - Reduced turnover through better volatility estimation

### Mathematical Formulation

**Yang-Zhang Volatility Estimator:**
```
σ_YZ = √(σ_O² + k×σ_C² + (1-k)×σ_RS²)
```

Where:
- `σ_O` = overnight/open volatility
- `σ_C` = close-to-close volatility
- `σ_RS` = Rogers-Satchell volatility
- `k` = weighting parameter (typically 0.34)

**Rogers-Satchell Volatility:**
```
σ_RS² = ln(H/C) × ln(H/O) + ln(L/C) × ln(L/O)
```

**Correlation-Adjusted Weight:**
```
w_i,t* = σ_target / (Σ_j |c_ij| × σ_j,t)
```

Where `c_ij` is the pairwise correlation between assets i and j.

**EWMA Volatility:**
```
σ²_EWMA,t = (1-λ) × σ²_EWMA,t-1 + λ × (r_i,t)²
```

Where λ = 2/(n+1) for n-day window.

### Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Volatility Type | YZ or Rolling | Yang-Zhang or rolling realized volatility |
| Volatility Window | 21 days | Lookback for volatility estimation |
| Min Periods | 10 | Minimum observations for valid estimate |
| Target Volatility | 40% | Annualized volatility target |
| Signal Cap | 0.95 | Maximum leverage cap |
| Weighting | Product or Equal | Cross-signal combination method |

---

## Implementation Requirements

### Input Data
- Daily OHLC futures price data for 58 instruments
- History requirement: 21+ days for volatility, 13 months for signal
- Need OHLC data (not just close) for Yang-Zhang

### Output Signals
- Same as Moskowitz 2012: signal per instrument (-1, 0, +1)
- Position weights with correlation adjustment
- Reduced turnover vs. standard TSMOM

### LEAN Components

**Algorithm Class:**
```python
class TSMOM_Baltas2020(BaseStrategyAlgorithm):
    def __init__(self):
        self.volatility_type = 'YangZhang'  # or 'EWMA', 'Rolling'
        self.volatility_window = 21
        self.correlation_window = 63  # ~3 months
        self.target_volatility = 0.40
        self.use_correlation_adjustment = True
```

**Key Differences from Moskowitz:**
1. `CalculateVolatility()` - Support YZ, EWMA, Rolling
2. `CalculateCorrelationMatrix()` - Pairwise correlations
3. `CalculateCorrelationAdjustedWeights()` - Adjust for correlations
4. `OnEndOfMonth()` - Apply correlation adjustment

---

## Implementation Details

### Code Structure

```python
from AlgorithmImports import *
from quantconnect.Common.BaseStrategyAlgorithm import BaseStrategyAlgorithm
from quantconnect.Common.VolatilityCalculator import (
    EWMA, YangZhang, Rolling
)

class TSMOM_Baltas2020(BaseStrategyAlgorithm):
    def Initialize(self):
        self.SetStartDate(2000, 1, 1)
        self.SetCash(100000)
        
        # Baltas-specific parameters
        self.volatility_type = self.GetParameter('volatility_type', 'YangZhang')
        self.volatility_window = 21
        self.correlation_window = 63
        self.target_volatility = 0.40
        self.signal_cap = 0.95
        self.use_correlation_adjustment = True
        
        # Universe (same as Moskowitz)
        self.universe = self.GetUniverse()
        for symbol in self.universe:
            future = self.AddFuture(symbol)
            future.SetFilter(0, 182)
    
    def CalculateVolatility(self, symbol, volatility_type='YangZhang'):
        """Calculate volatility using specified method"""
        history = self.History(symbol, self.volatility_window * 2, Resolution.DAILY)
        
        if volatility_type == 'YangZhang':
            return self._calculate_yang_zhang(history)
        elif volatility_type == 'EWMA':
            returns = history['close'].pct_change().dropna()
            return EWMA(returns.values, self.volatility_window) * np.sqrt(252)
        else:  # Rolling
            returns = history['close'].pct_change().dropna()
            return returns.std() * np.sqrt(252)
    
    def _calculate_yang_zhang(self, history):
        """Yang-Zhang volatility estimator"""
        # Calculate components
        log_ho = np.log(history['high'] / history['open'])
        log_lo = np.log(history['low'] / history['open'])
        log_co = np.log(history['close'] / history['open'])
        log_oc = np.log(history['open'] / history['close'].shift(1))
        log_cc = np.log(history['close'] / history['close'].shift(1))
        
        # Rogers-Satchell volatility
        rs = log_ho * (log_ho - log_co) + log_lo * (log_lo - log_co)
        sigma_rs = np.sqrt(rs.mean())
        
        # Overnight volatility
        sigma_o = log_oc.std()
        
        # Close-to-close volatility
        sigma_c = log_cc.std()
        
        # Yang-Zhang (k = 0.34)
        k = 0.34
        sigma_yz = np.sqrt(sigma_o**2 + k * sigma_c**2 + (1 - k) * sigma_rs**2)
        
        return sigma_yz * np.sqrt(252)
    
    def CalculateCorrelationMatrix(self):
        """Calculate pairwise correlations"""
        returns_data = {}
        
        for symbol in self.universe:
            history = self.History(symbol, self.correlation_window, Resolution.DAILY)
            returns_data[symbol] = history['close'].pct_change().dropna()
        
        # Create returns DataFrame
        returns_df = pd.DataFrame(returns_data)
        
        # Calculate correlation matrix
        corr_matrix = returns_df.corr().fillna(0)
        
        return corr_matrix
    
    def CalculateCorrelationAdjustedWeight(self, symbol, base_weight, corr_matrix, volatilities):
        """Apply correlation adjustment to weight"""
        if not self.use_correlation_adjustment:
            return base_weight
        
        # Sum of absolute correlations with all other assets
        abs_corr_sum = corr_matrix[symbol].abs().sum()
        
        # Adjust weight
        if abs_corr_sum > 0:
            adjusted_weight = base_weight / abs_corr_sum
        else:
            adjusted_weight = base_weight
        
        return adjusted_weight
```

### Configuration File

```json
{
  "strategy_name": "TSMOM_Baltas2020",
  "description": "Enhanced Time-Series Momentum from Baltas and Kosowski (2020)",
  "parameters": {
    "volatility_type": "YangZhang",
    "volatility_window": 21,
    "correlation_window": 63,
    "target_volatility": 0.40,
    "signal_cap": 0.95,
    "use_correlation_adjustment": true,
    "rebalancing_freq": "monthly"
  },
  "volatility_types": ["YangZhang", "EWMA", "Rolling"],
  "enhancements": [
    "Yang-Zhang volatility estimator",
    "Correlation-adjusted weights",
    "30%+ turnover reduction"
  ],
  "expected_performance": {
    "sharpe_ratio": 0.80,
    "turnover_reduction": "30%+",
    "vs_moskowitz": "Improved post-2008"
  },
  "reference": "Baltas, N. and Kosowski, R., 2020. 'Demystifying time-series momentum strategies: Volatility estimators, trading rules and pairwise correlations.' Market Momentum: Theory and Practice, Wiley."
}
```

---

## Acceptance Criteria

### Volatility Calculation Tests
- [ ] Yang-Zhang volatility calculated using OHLC
- [ ] EWMA matches standard implementation
- [ ] Rolling volatility with configurable window
- [ ] All methods return annualized values
- [ ] Volatility types can be switched via config

### Correlation Tests
- [ ] Correlation matrix calculated for all pairs
- [ ] 63-day window (configurable)
- [ ] Handling of missing data
- [ ] Correlations in valid range [-1, 1]

### Correlation Adjustment Tests
- [ ] Weights reduced for high correlation
- [ ] Weights increased for low correlation
- [ ] Adjustment formula matches specification
- [ ] Can be disabled via config

### Performance Tests
- [ ] Turnover reduced vs. Moskowitz
- [ ] Similar or better Sharpe ratio
- [ ] Post-2008 performance improved

---

## Dependencies

### Prerequisites
- Task S01 (TSMOM Moskowitz) complete
- VolatilityCalculator with Yang-Zhang support
- Correlation calculation utilities

### Extends
- Inherits from TSMOM_Moskowitz2012
- Overrides volatility calculation
- Adds correlation adjustment

---

## Estimated Effort

- **Development**: 5 hours (extends S01)
- **Testing**: 3 hours
- **Documentation**: 1 hour
- **Total**: 9 hours

---

## Notes

### Implementation Notes
- Extends Moskowitz 2012 with enhancements
- Yang-Zhang requires OHLC data
- Correlation adjustment reduces concentration risk
- Turnover reduction is key benefit

### Key Differences from Moskowitz
1. Volatility estimator: YZ vs. EWMA
2. Correlation adjustment: Optional
3. Multiple volatility options
4. Expected turnover reduction

### References
- Paper: Baltas & Kosowski (2020)
- Builds on: Moskowitz et al. (2012)

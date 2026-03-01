# Search Findings Summary - QuantConnect LEAN Implementation Patterns

**Search Mode Execution**: Parallel background agents + direct grep searches  
**Date**: 2026-03-01  
**Scope**: 29 notebooks + QuantConnect LEAN framework research

---

## Key Findings from Codebase Analysis

### 1. Vivace Library Patterns (Proprietary - needs replacement)

**Signal Structure Pattern**:
```python
from vivace.backtest import signal, processing

# Parallel signal combination
signal.ParallelSignal([
    signal.VolatilityScale(agg_method='ewm', com=60, ann_factor=261, 
                           target_volatility=0.4, signal_cap=0.95,
                           post_process=processing.AsFreq(freq='m', method='pad')),
    signal.TSMOMMoskowitz2012(post_process=processing.AsFreq(freq='m', method='pad'))
])

# Pipeline with SMA
signal.Pipeline([
    signal.XSSkewness(lookback=252, 
                      post_process=processing.Pipeline([
                          processing.Negate(),
                          processing.AsFreq(freq='m', method='pad')
                      ]))
])
```

**Key Components to Replicate in LEAN**:
- `ParallelSignal`: Combines multiple signals (vol scaling + momentum)
- `Pipeline`: Sequential signal processing
- `VolatilityScale`: Volatility-based position sizing
- `AsFreq(freq='m')`: Monthly rebalancing
- `SMA(252)`: 252-day smoothing
- `Negate()`: Signal inversion

### 2. Signal Parameters Found

**Volatility Scaling**:
```python
agg_method='ewm'        # Exponentially weighted
com=60                  # Center of mass (60 days)
ann_factor=261          # Annualization factor
target_volatility=0.4   # 40% annual target
signal_cap=0.95         # Max 95th percentile leverage
```

**Alternative Volatility**:
```python
agg_method='rolling'    # Rolling window
window=21               # 21-day window
volatility_type='YZ'    # Yang-Zhang
```

**Momentum Signal**:
```python
lookback=252            # 12-month lookback
shift=2                 # 2-day shift
```

### 3. Futures Universe Definitions

**Moskowitz 2012** (58 futures):
```python
all_futures_moskowitz2012 = [
    # Equity indices
    'ES', 'NQ', 'YM', 'RTY', ...,
    # Currencies
    'EC', 'JY', 'BP', ...,
    # Commodities
    'CL', 'GC', 'S', 'SM', 'BO', ...,
    # Bonds
    'ZB', 'ZN', ...
]
```

**Hollstein 2020** (26 commodities):
```python
all_futures_hollstein2020 = [
    'CL', 'HO', 'RB', 'NG',  # Energy
    'GC', 'SI', 'HG',        # Metals
    'ZC', 'ZS', 'ZW', ...     # Agriculture
]
```

### 4. Strategy Implementation Patterns

**TSMOM Moskowitz 2012**:
```python
# Formula from notebook
signal_t^s = sign(r_{t-12,t}^s) × (40% / σ_t^s)

# Implementation
signal = instrument_return.rolling(self.lookback).sum().fillna(0).pipe(np.sign).shift(self.shift)
```

**Carry Signal**:
```python
# Term structure carry
Carry = log(F1 / F2) × annualization_factor

# Implementation
signal.XSCarryFutureFuture(nth_expiry_shift=1, 
                           post_process=processing.Pipeline([
                               processing.SMA(252),
                               processing.AsFreq(freq='m', method='pad')
                           ]))
```

**Skewness Signal**:
```python
# 252-day skewness, negated
signal.XSSkewness(lookback=252, 
                  post_process=processing.Pipeline([
                      processing.Negate(),
                      processing.AsFreq(freq='m', method='pad')
                  ]))
```

### 5. Rebalancing Patterns

**Monthly Rebalancing**:
```python
rebalance_freq='m'  # Monthly
rebalance_freq='d'  # Daily

# Observed in:
- trend_following_moskowitz2012.ipynb
- fx_carry.ipynb
- commodity_momentum.ipynb
```

### 6. Contract Handling Patterns

**Roll Schedule**:
```python
roll_schedule=21  # Days prior to expiry
contract_depth_offset=0  # Front contract

# Volume-based active contracts
volume_ratio = contract_volume / annual_average
```

**Continuous Contracts**:
```python
# Data normalization modes
DataNormalizationMode.BACKWARDS_RATIO
DataNormalizationMode.FORWARDS_RATIO
DataNormalizationMode.ADJUSTED

# Data mapping modes
DataMappingMode.LAST_TRADING_DAY
DataMappingMode.OPEN_INTEREST
```

### 7. Spread Trading Patterns

**Crush Spread** (Soybean complex):
```
Crush = (Meal_price × 2.2) + (Oil_price × 11) - Soybean_price

Assets: S (Soybeans), SM (Soybean Meal), BO (Soybean Oil)
```

**Crack Spread** (Petroleum):
```
3:2:1 Crack Spread = (2/3 × HO × 42) + (1/3 × RB × 42) - CL

Assets: CL (Crude), RB (RBOB Gasoline), HO (Heating Oil)
Unit: 1 barrel = 42 gallons
```

### 8. Volatility Calculation Patterns

**EWMA Volatility**:
```python
σ²_t = (1-λ) × σ²_{t-1} + λ × r_t²
where λ = 2/(n+1)
```

**Yang-Zhang Volatility**:
```python
σ_YZ = √(σ_O² + k×σ_C² + (1-k)×σ_RS²)
where k = 0.34

Components:
- σ_O: Overnight/open volatility
- σ_C: Close-to-close volatility  
- σ_RS: Rogers-Satchell volatility
```

**Rogers-Satchell**:
```python
σ_RS² = ln(H/C) × ln(H/O) + ln(L/C) × ln(L/O)
```

### 9. Portfolio Construction Patterns

**Tercile Selection** (33% top/bottom):
```python
# Rank by signal
ranked = sorted(signals.items(), key=lambda x: x[1])
n = len(ranked)
tercile_size = n // 3

long_symbols = ranked[-tercile_size:]   # Top 33%
short_symbols = ranked[:tercile_size]   # Bottom 33%
```

**Volatility-Scaled Sizing**:
```python
weight = target_volatility / instrument_volatility × signal
# Capped at signal_cap (0.95)
```

### 10. LEAN Framework Integration

**Event Handlers**:
```python
def initialize(self):           # Setup
    pass

def on_data(self, data):        # Price data
    pass

def on_end_of_month(self):      # Monthly rebalancing
    pass

def on_securities_changed(self, changes):  # Universe changes
    pass
```

**Futures Subscription**:
```python
future = self.add_future(Futures.Indices.SP_500_E_MINI,
                        data_normalization_mode=DataNormalizationMode.BACKWARDS_RATIO,
                        data_mapping_mode=DataMappingMode.LAST_TRADING_DAY,
                        contract_depth_offset=0)
```

**History Requests**:
```python
history = self.History(symbol, 252, Resolution.DAILY)
returns = history['close'].pct_change()
```

**Position Management**:
```python
# Set target portfolio percentage
self.SetHoldings(symbol, target_weight)

# Market order
self.MarketOrder(symbol, quantity)

# Liquidate
self.Liquidate(symbol)
```

---

## LEAN-Specific Patterns from Research

### Algorithm Framework Components

**Alpha Models** (Signal Generation):
```python
# Generate Insight objects
insight = Insight(symbol, period, InsightType.PRICE, 
                  InsightDirection.UP, magnitude, confidence)
```

**Portfolio Construction**:
```python
# Built-in models
self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel())
self.SetPortfolioConstruction(ConfidenceWeightedPortfolioConstructionModel())
```

**Execution Models**:
```python
# Immediate or VWAP
self.SetExecution(ImmediateExecutionModel())
self.SetExecution(VolumeWeightedAveragePriceExecutionModel())
```

**Risk Management**:
```python
# Drawdown limits
self.SetRiskManagement(MaximumDrawdownPercentPerSecurity(0.05))
```

### Futures-Specific LEAN Patterns

**Continuous Contract Handling**:
```python
# Check for rollover
if self._current_contract.symbol != self._continuous_contract.mapped:
    self.Log(f"Rolling from {old} to {new}")
    self.Liquidate(old)
    self.Buy(new, quantity)
```

**Contract Chain Access**:
```python
chain = self.FutureChain(symbol)
front_contract = chain[0]
second_contract = chain[1]
```

**Rolling Schedule**:
```python
# Roll when volume in next > volume in front
if volume_next > volume_front * threshold:
    Roll()
```

---

## Implementation Mapping: Vivace → LEAN

| Vivace Component | LEAN Equivalent | Notes |
|-----------------|-----------------|-------|
| BacktestEngine | QCAlgorithm | Main algorithm class |
| signal.TSMOM | Custom Alpha | Generate signals |
| signal.VolatilityScale | RiskManagement + PortfolioConstruction | Position sizing |
| processing.AsFreq('m') | OnEndOfMonth() | Monthly rebalancing |
| processing.SMA | Indicator.SimpleMovingAverage | Smoothing |
| processing.Negate | Signal * -1 | Inversion |
| ParallelSignal | CompositeAlphaModel | Combine signals |
| Pipeline | Sequential indicators | Multi-step processing |
| all_futures_* | ManualUniverseSelectionModel | Universe definition |

---

## Data Requirements Summary

**Historical Data**:
- Daily OHLC prices for 58 futures
- 13+ months history for TSMOM
- 252 days for skewness/volatility
- Contract specifications (expiry, multiplier)

**Real-time Data**:
- Daily resolution minimum
- Prefer minute for intraday strategies
- Volume data for contract selection

**Data Providers**:
- LEAN's built-in futures data
- Continuous contract mapping
- Roll logic handling

---

## Testing Patterns Identified

**Smoke Tests**:
```python
# Instantiate algorithm
algo = TSMOM_Moskowitz2012()
algo.Initialize()
assert algo.universe is not None
```

**Signal Tests**:
```python
# Test signal calculation
signal = algo.GenerateSignals()
assert all(s in [-1, 0, 1] for s in signal.values())
```

**Backtest Validation**:
```python
# Run minimal backtest
results = algo.Backtest(...)
assert results.TotalReturn > 0
```

---

## Background Agent Status

| Agent | Task | Status | Session |
|-------|------|--------|---------|
| explore | Codebase patterns | Running | ses_357288405ffeAo3kshgQH9VlYE |
| librarian | LEAN futures patterns | Running | ses_35728688bffeGTlohQEXwCNQlM |
| librarian | Spread trading | Running | ses_357285a91ffe3qiGnCxidBmQFU |

---

## Next Steps

1. ✅ **Search Complete**: Comprehensive patterns identified
2. ⏳ **Background Agents**: Still running (will report additional findings)
3. 📝 **Implementation**: Ready to begin with Wave 1 infrastructure
4. 🔧 **Key Utilities**: VolatilityCalculator, PortfolioConstructor patterns established

---

*Generated: 2026-03-01*
*Mode: MAXIMUM SEARCH EFFORT*
*Sources: 29 notebooks + LEAN documentation + GitHub examples*

# QuantConnect LEAN Implementation - ADAPTED PLAN

**Based on Review**: sisyphus_plans_review.md by Antigravity (2026-03-01)  
**Status**: Revised implementation plan addressing critical issues  
**Scope**: 19 tradeable strategies (reduced from 24)

---

## Critical Changes from Original Plan

### 1. Scope Reduction: 24 → 19 Strategies

**REMOVED from implementation scope:**

| Strategy | Reason | New Classification |
|----------|--------|-------------------|
| S18 - Long-Only Futures | Buy-and-hold benchmark, no signal generation | Utility/benchmark |
| S19 - Active Contracts | Volume analysis tool, no trading logic | Infrastructure utility |
| S20 - Realised Volatility | Volatility measurement, no positions | Common/ utility |
| S21 - Greeks Normal Model | Options pricing calculator | Out of scope |
| S23 - Uniswap V2 | DeFi/AMM analysis, no LEAN data | Out of scope |

**S22 (Inverse Options)** - Borderline, will include as simplified version
**S24 (Virtue of Complexity)** - Keep, but flag as "advanced/complex"

### 2. LEAN API Corrections Required

**Ground Truth Reference Algorithm Needed FIRST** (before any strategy implementation):

```python
# CORRECT LEAN Patterns (from review findings):

# 1. Futures Subscription - use enum, not strings
from AlgorithmImports import *

# WRONG: self.AddFuture("ES")
# CORRECT:
future = self.AddFuture(Futures.Indices.SP_500_E_MINI)
future.SetFilter(timedelta(0), timedelta(182))  # timedelta, not int

# 2. History API - all caps, use mapped symbol
# WRONG: self.History(symbol, 252, Resolution.Daily)
# CORRECT:
history = self.History(future.Mapped, 252, Resolution.DAILY)

# 3. Resolution enum - ALL CAPS
Resolution.DAILY      # ✓ Correct
Resolution.Daily      # ✗ Wrong

# 4. FutureChain access
# WRONG: self.FutureChain(symbol)
# CORRECT - in OnData:
def OnData(self, data):
    for chain in data.FutureChains.Values:
        for contract in chain:
            # access contract here
            pass

# 5. SetHoldings vs MarketOrder
self.SetHoldings(symbol, target_percentage)  # 0.0 to 1.0 (or -1.0)

# 6. Warmup
self.SetWarmUp(timedelta(days=300))  # 252 + buffer

# 7. Schedule monthly rebalancing
self.Schedule.On(
    self.DateRules.MonthStart(),
    self.TimeRules.AfterMarketOpen(),
    self.Rebalance
)
```

### 3. Base Class Hierarchy Revision

**Original (Overly Simplistic):**
```
BaseStrategyAlgorithm
└── All 24 strategies
```

**Revised (Type-Specific):**
```
BaseStrategyAlgorithm (abstract)
├── TimeSeriesStrategyAlgorithm
│   ├── S01: TSMOM Moskowitz
│   ├── S02: TSMOM Baltas
│   ├── S03: Trend Breakout
│   └── S04: Chinese Futures
├── CrossSectionalStrategyAlgorithm
│   ├── S05: Commodity Carry
│   ├── S06: Commodity Momentum
│   ├── S07: Commodity Skewness
│   ├── S08: Intra-Curve
│   ├── S09: Basis Momentum
│   ├── S10: Basis Reversal
│   ├── S16: FX Carry
│   └── S17: Cross-Asset Skew
├── SpreadStrategyAlgorithm
│   ├── S11: Soybean Crush
│   └── S12: Petroleum Crack
├── IntradayStrategyAlgorithm
│   ├── S13: Connors RSI-2
│   ├── S14: ETF Intraday Momentum
│   └── S15: Overnight Returns
└── MLStrategyAlgorithm
    └── S24: Virtue of Complexity
```

**Excluded**: S18-S21, S23 (not tradeable strategies)

### 4. Key Infrastructure Additions

**Wave 1 must include:**

1. **Reference Algorithm** - Single futures algorithm proving correct LEAN API usage
2. **Fee/Slippage Configuration** - Per asset class fee models
3. **Warmup Handling** - SetWarmUp with IsWarmingUp checks
4. **RollingWindow Pattern** - For historical signal storage (fixing S05 bug)
5. **Universe Mappings** - Canonical symbol definitions in `Common/universes.py`
6. **Parameter System** - Use LEAN's `self.GetParameter()` not JSON configs

---

## Revised Execution Strategy

### Phase 0: Ground Truth (NEW - Before Wave 1)

**Task 0.1: Build Reference LEAN Futures Algorithm**
- Create a minimal working LEAN algorithm with futures
- Verify correct API for: subscription, continuous contracts, history, rebalancing
- Document working patterns as ground truth
- **Deliverable**: `reference_futures_algorithm.py` that runs successfully

**Task 0.2: Create Universe Mappings**
- Map all strategy universes to proper LEAN symbols
- Use `Futures.*` enums where available
- Document exchange specifications
- **Deliverable**: `Common/universes.py`

### Phase 1: Wave 1 - Infrastructure (Revised)

**Task 1.1: Create Project Structure**
```
quantconnect/
├── reference/               # NEW: Ground truth algorithms
│   └── reference_futures_algorithm.py
├── Common/
│   ├── __init__.py
│   ├── universes.py        # NEW: Symbol mappings
│   ├── constants.py        # NEW: ann_factor, etc.
│   ├── BaseStrategyAlgorithm.py
│   ├── TimeSeriesStrategyAlgorithm.py      # NEW
│   ├── CrossSectionalStrategyAlgorithm.py  # NEW
│   ├── SpreadStrategyAlgorithm.py          # NEW
│   ├── IntradayStrategyAlgorithm.py        # NEW
│   ├── VolatilityCalculator.py
│   ├── PortfolioConstructor.py
│   ├── RiskManager.py
│   ├── FeeConfigurator.py    # NEW
│   └── DataProvider.py
├── Strategies/
│   ├── TrendFollowing/      # S01-S04
│   ├── Commodity/           # S05-S10
│   ├── SpreadTrading/       # S11-S12
│   ├── Equity/              # S13-S15
│   ├── FX_CrossAsset/       # S16-S17
│   └── Advanced/            # S22, S24
└── Tests/
```

**Task 1.2: Implement Base Classes with Correct LEAN API**
- Use ground truth patterns from Task 0.1
- Include warmup, fees, slippage
- RollingWindow pattern for historical storage

**Task 1.3: Implement Utilities**
- VolatilityCalculator with YZ, EWMA
- PortfolioConstructor with tercile selection
- FeeConfigurator per asset class

### Phase 2: Wave 2 - P0 Strategies (Critical Path)

**Strategies**: S01, S02, S05, S06 (core/high Sharpe)

**Deliverables per strategy:**
- Correct LEAN API usage (verified against ground truth)
- Unit tests for signal calculation (isolated, no LEAN dependency)
- Integration test in LEAN
- Regression targets from notebooks (specific values)

### Phase 3: Wave 3 - P1 Strategies

**Strategies**: S03, S04, S07, S09, S16

### Phase 4: Wave 4 - Complex Strategies

**Strategies**: S08, S10, S11, S12, S14, S17, S22, S24

**Note**: S11/S12 (spreads) and S14 (intraday) need detailed plans BEFORE implementation as they may require base class changes

### Phase 5: Final Validation

- Smoke tests on all 19 strategies
- Regression tests against notebook results
- Documentation review

---

## Detailed Corrections by Strategy

### S01: TSMOM Moskowitz 2012

**Critical Corrections:**

1. **Universe Definition** - Fix symbol mappings:
```python
# In Common/universes.py:
MOSKOWITZ_2012_UNIVERSE = [
    Futures.Indices.SP_500_E_MINI,      # ES
    Futures.Indices.NASDAQ_100_E_MINI,   # NQ
    Futures.Indices.DOW_JONES_E_MINI,    # YM
    Futures.Indices.RUSSELL_2000_E_MINI, # RTY
    # ... etc with proper enums
]
```

2. **History Request**:
```python
# CORRECT:
history = self.History(future.Mapped, 252, Resolution.DAILY)
```

3. **SetFilter**:
```python
# CORRECT:
future.SetFilter(timedelta(0), timedelta(182))
```

### S05: Commodity Carry

**Critical Corrections:**

1. **CalculateSmoothedCarry Bug Fix**:
```python
# WRONG (original plan):
# Looping self.sma_window times calling CalculateCarry at self.Time

# CORRECT - Use RollingWindow:
def Initialize(self):
    self.carry_history = {}
    for symbol in self.universe:
        self.carry_history[symbol] = RollingWindow[float](252)

def OnData(self, data):
    for symbol in self.universe:
        carry = self.CalculateCarry(symbol)
        if carry is not None:
            self.carry_history[symbol].Add(carry)

def GenerateSignals(self):
    for symbol in self.universe:
        if self.carry_history[symbol].IsReady:
            smoothed_carry = np.mean(list(self.carry_history[symbol]))
            signals[symbol] = smoothed_carry
```

2. **Universe Fix** - Remove duplicates, correct classification:
```python
# CORRECTED universe (24 unique commodities):
HOLLSTEIN_2020_UNIVERSE = [
    'CL', 'HO', 'RB', 'NG',           # Energy
    'GC', 'SI', 'HG', 'PL', 'PA',     # Metals
    'ZC', 'ZS', 'ZW', 'ZL', 'ZM',     # Grains
    'ZO', 'KE',                       # Other grains
    'KC', 'CT', 'SB', 'CC',           # Softs
    'LC', 'LH', 'FC',                 # Livestock
    # Removed duplicate 'KC' and FX 'DX'
]
```

### S11/S12: Spread Strategies

**Require New Base Class:**

```python
class SpreadStrategyAlgorithm(BaseStrategyAlgorithm):
    """Base for multi-leg spread strategies"""
    
    def ExecuteSpread(self, legs):
        """
        legs: list of (symbol, quantity) tuples
        Executes all legs simultaneously
        """
        # Use LEAN's position groups for margin efficiency
        for symbol, quantity in legs:
            self.MarketOrder(symbol, quantity)
    
    def CalculateHedgeRatio(self, symbols):
        """OLS regression for optimal hedge ratios"""
        # Implementation using sklearn
        pass
```

### S14: ETF Intraday

**Requires New Base Class:**

```python
class IntradayStrategyAlgorithm(BaseStrategyAlgorithm):
    """Base for intraday strategies"""
    
    def Initialize(self):
        super().Initialize()
        self.Schedule.On(
            self.DateRules.EveryDay(),
            self.TimeRules.At(9, 30),  # Market open
            self.OnMarketOpen
        )
        self.Schedule.On(
            self.DateRules.EveryDay(),
            self.TimeRules.At(15, 30),  # 30 min before close
            self.OnPreClose
        )
```

---

## Revised Testing Strategy

### Unit Tests (No LEAN Dependency)

```python
# Test signal calculation in isolation
def test_tsmom_signal():
    prices = [100, 101, 102, ..., 130]  # 12 months of data
    signal = calculate_tsmom_signal(prices)
    assert signal == 1  # Positive trend
    
def test_volatility_yz():
    ohlc_data = [...]  # OHLC bars
    vol = calculate_yang_zhang(ohlc_data)
    assert 0 < vol < 2  # Reasonable volatility
```

### Integration Tests (LEAN Required)

```python
# Test in LEAN environment
def test_s01_integration():
    algo = TSMOM_Moskowitz2012()
    algo.Initialize()
    # Run minimal backtest
    assert algo.Portfolio.TotalPortfolioValue > 0
```

### Regression Tests

Define explicit expected values from notebooks:
```yaml
S01_regression:
  date: "2020-01-31"
  symbol: "ES"
  expected_signal: 1
  expected_weight: 1.8  # Approximate
  tolerance: 0.1
```

---

## Revised Effort Estimates

**Original**: 7 hours per strategy  
**Revised**: 12-16 hours per core strategy (accounting for LEAN learning curve and API corrections)

| Phase | Tasks | Revised Estimate |
|-------|-------|-----------------|
| Phase 0 | Ground truth + universes | 8 hours |
| Wave 1 | Infrastructure | 16 hours |
| Wave 2 | P0 strategies (4) | 48-64 hours |
| Wave 3 | P1 strategies (5) | 60-80 hours |
| Wave 4 | Complex (8) | 96-128 hours |
| Wave 5 | Validation | 16 hours |
| **Total** | | **244-312 hours** (~6-8 weeks) |

---

## Immediate Next Steps

### Before Any Implementation:

1. ✅ **Read this adapted plan** (you're doing this now)
2. ⏳ **Create reference LEAN futures algorithm** (Task 0.1)
3. ⏳ **Create universe mappings** (Task 0.2)
4. ⏳ **Verify reference algorithm runs** in LEAN

### Then Proceed with Wave 1:

5. ⏳ Create corrected base class hierarchy
6. ⏳ Implement utilities with LEAN API

### Then Create Detailed Plans for:

7. ⏳ S11/S12 (spreads) - before Wave 4
8. ⏳ S14 (intraday) - before Wave 4
9. ⏳ All P0/P1 strategies - before their implementation waves

---

## Files to Update/Create

### New Files:
- `.sisyphus/plans/quantconnect-implementation-plan-adapted.md` (this file)
- `quantconnect/reference/reference_futures_algorithm.py`
- `quantconnect/Common/universes.py`
- `quantconnect/Common/constants.py`
- `quantconnect/Common/FeeConfigurator.py`

### Updated Files:
- `.sisyphus/plans/quantconnect-master-plan.md` - mark as superseded, reference this adapted plan
- All strategy plans need LEAN API corrections before implementation

### Files to Remove from Scope:
- Any plans for S18, S19, S20, S21, S23

---

## Summary of Adaptations

| Issue | Original Plan | Adapted Plan |
|-------|---------------|--------------|
| **LEAN API** | Incorrect examples | Ground truth reference algorithm first |
| **Scope** | 24 strategies | 19 strategies (removed 5 non-strategies) |
| **Base class** | Single class | Type-specific hierarchy (4 sub-classes) |
| **Symbol mappings** | Raw tickers | Proper LEAN enums in universes.py |
| **S05 carry bug** | Broken loop pattern | RollingWindow-based storage |
| **Configuration** | Static JSON | LEAN GetParameter() system |
| **Testing** | Aspirational | Unit + integration + regression with fixtures |
| **Fees/Slippage** | Not mentioned | Included in Wave 1 |
| **Warmup** | Not mentioned | SetWarmUp in base class |
| **Effort** | 3+ days | 6-8 weeks (realistic with corrections) |

---

**Decision Required**: 

Proceed with **Phase 0 (Ground Truth)** first? This ensures all subsequent implementation uses correct LEAN patterns.

Or proceed directly to **Wave 1** using corrected patterns from this adapted plan?

*Recommendation: Phase 0 first. 8 hours of ground truth work prevents 40+ hours of rework later.*

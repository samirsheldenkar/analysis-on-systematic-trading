# QuantConnect LEAN Implementation - PLAN V2 (Final)

**Status**: Revised based on adapted_plan_review.md  
**Scope**: 18 tradeable strategies (reduced from 19, further reduced from 24)  
**Date**: 2026-03-01 (Final Revision)  
**Effort**: 6-8 weeks (244-312 hours)  

---

## Summary of Changes from V1 → V2

### Fully Addressed (10/14 findings) ✅
1. ✅ LEAN API corrections - Phase 0 + corrected examples
2. ✅ Missing strategy plans - Deferred to before each wave
3. ✅ Scope reduction - 24 → 19 strategies initially
4. ✅ S05 carry bug - RollingWindow pattern
5. ✅ Universe symbol errors - Fixed mappings
6. ✅ Base class hierarchy - 5-class structure
7. ✅ Fees/slippage - FeeConfigurator added
8. ✅ Data warmup - SetWarmUp pattern
9. ✅ Testing strategy - Three-tier approach defined
10. ✅ JSON configs → LEAN GetParameter()

### Additional Changes for V2

11. ⚠️ **S13 Reclassified** (NEW): Moved from IntradayStrategyAlgorithm → TimeSeriesStrategyAlgorithm
12. ⚠️ **S15 Removed** (NEW): Overnight Returns is analysis, not tradeable strategy
13. ⚠️ **S22 Removed** (NEW): Inverse Options insufficiently defined for LEAN
14. ⚠️ **MLStrategyAlgorithm Removed** (NEW): S24 inherits directly from BaseStrategyAlgorithm
15. ⚠️ **Casing Convention Chosen**: **PascalCase** (matches LEAN C# docs)
16. ⚠️ **Constants Defined**: ANN_FACTOR_TRADING_DAYS=252, ANN_FACTOR_CARRY=4, etc.
17. ⚠️ **S02 Clarified**: Inherits from TimeSeriesStrategyAlgorithm, not S01 directly
18. ⚠️ **Branch Strategy Added**: Feature branches for parallel waves

### Final Scope: 18 Strategies

**Final Strategy Count**: 18 (down from original 24)

| Category | Strategies | Count |
|----------|-----------|-------|
| Trend Following | S01-S04 | 4 |
| Commodity | S05-S10 | 6 |
| Spread Trading | S11-S12 | 2 |
| Equity | S13, S14 | 2 |
| FX & Cross-Asset | S16-S17 | 2 |
| Advanced | S24 | 1 |
| **Total** | | **18** |

**Removed**: S15, S18-S23 (7 items total)

---

## Final Base Class Hierarchy

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
│   └── S14: ETF Intraday Momentum
└── S24: Virtue of Complexity (inherits directly from Base)
    └── Note: No MLStrategyAlgorithm base - S24 is standalone

S13: Connors RSI-2 → TimeSeriesStrategyAlgorithm (reclassified from Intraday)
```

**Note**: S24 is the only ML strategy. Rather than creating a base class for one strategy, it inherits directly from BaseStrategyAlgorithm.

---

## Style Conventions (NEW)

### API Casing: PascalCase

**Decision**: Use **PascalCase** throughout to match LEAN's C# documentation.

```python
# CORRECT - PascalCase
def Initialize(self):
    self.SetStartDate(2020, 1, 1)
    self.SetCash(100000)
    
def OnData(self, data):
    self.SetHoldings(symbol, weight)
    
def OnEndOfMonth(self):
    self.Rebalance()

# INCORRECT - snake_case
def initialize(self):
    self.set_start_date(2020, 1, 1)
```

**Rationale**: LEAN Python supports both, but C# documentation uses PascalCase. Consistency with docs reduces confusion.

---

## Constants Specification (NEW)

**File**: `Common/constants.py`

```python
# Annualization factors
ANN_FACTOR_TRADING_DAYS = 252
ANN_FACTOR_CARRY_QUARTERLY = 4
ANN_FACTOR_CARRY_MONTHLY = 12

# Volatility scaling
DEFAULT_TARGET_VOLATILITY = 0.40
DEFAULT_SIGNAL_CAP = 0.95
DEFAULT_VOLATILITY_WINDOW = 21

# Rebalancing
REBALANCE_MONTHLY = 'monthly'
REBALANCE_WEEKLY = 'weekly'

# Lookbacks (days)
LOOKBACK_1M = 21
LOOKBACK_3M = 63
LOOKBACK_6M = 126
LOOKBACK_1Y = 252

# Warmup buffer
WARMUP_BUFFER_DAYS = 30

# Skewness window
SKEWNESS_LOOKBACK = 252

# Tercile selection
TERCILE_TOP = 0.33
TERCILE_BOTTOM = 0.33
```

---

## S13 Reclassification Details

**Original (V1)**: Placed under `IntradayStrategyAlgorithm`  
**Corrected (V2)**: Moved to `TimeSeriesStrategyAlgorithm`

**Why**:
- Connors RSI-2 is **daily frequency**, not intraday
- Uses 2-period RSI on daily bars
- 5-day holding periods (not intraday)
- 200-day MA filter (daily)
- Needs monthly rebalancing infrastructure, not minute scheduling

**Implementation**:
```python
class ConnorsRSI2(TimeSeriesStrategyAlgorithm):
    def GenerateSignals(self):
        for symbol in self.Universe:
            rsi = self.CalculateRSI(symbol, period=2)
            if rsi <= 25:
                signals[symbol] = 1  # Long
            elif rsi >= 75:
                signals[symbol] = -1  # Short
            else:
                signals[symbol] = 0  # Flat
```

---

## S15 Removal Justification

**Original plan included**: S15 Overnight Returns  
**V2**: **Removed entirely**

**Why**:
- Source documentation: "Analysis of striking patterns"
- No trading signal defined
- No position sizing methodology
- Academic analysis, not tradeable strategy
- Can be analyzed as part of S14 or other strategies

**Reclassified as**: Analysis utility (not strategy)

---

## S22 Removal Justification

**Original plan kept**: S22 as "simplified version"  
**V2**: **Removed**

**Why**:
- Source: Inverse option pricing theory for crypto
- No trading signal defined
- LEAN has limited crypto options support
- "Simplified version" not actually defined
- Same ambiguity as other removed items

---

## Branch Strategy (NEW)

**Git Workflow for Parallel Waves**:

```
main
├── phase-0-ground-truth
│   └── Task-0.1-reference-algorithm
├── phase-1-infrastructure
│   ├── Task-1.1-project-structure
│   ├── Task-1.2-base-classes
│   ├── Task-1.3-utilities
│   └── Task-1.4-testing-framework
├── phase-2-p0-strategies
│   ├── S01-tsmom-moskowitz
│   ├── S02-tsmom-baltas
│   ├── S05-commodity-carry
│   └── S06-commodity-momentum
├── phase-3-p1-strategies
│   ├── S03-trend-breakout
│   ├── S04-chinese-futures
│   ├── S07-commodity-skewness
│   ├── S09-basis-momentum
│   └── S16-fx-carry
├── phase-4-p2-strategies
│   ├── S08-intra-curve
│   ├── S10-basis-reversal
│   ├── S11-soybean-crush
│   ├── S12-petroleum-crack
│   ├── S13-connors-rsi2
│   ├── S14-etf-intraday
│   ├── S17-cross-asset-skew
│   └── S24-virtue-complexity
└── phase-5-validation
    └── Final integration and testing
```

**Branch Naming**: `phase-{N}-{name}/Task-{X}-{description}`  
**Merge Strategy**: Feature branches → main via PR after QA

---

## S02 Clarification

**Original concern**: S02 said "inherits from S01" (tight coupling)  
**V2 Clarification**:

```python
# CORRECT - V2:
class TSMOM_Baltas2020(TimeSeriesStrategyAlgorithm):
    """
    Enhanced TSMOM with YZ volatility and correlation adjustment.
    Inherits from TimeSeriesStrategyAlgorithm, NOT from S01.
    """
    def CalculateVolatility(self, symbol):
        # Uses Yang-Zhang instead of EWMA
        return self.VolatilityCalculator.YangZhang(symbol)
    
    def CalculateCorrelationMatrix(self):
        # Additional correlation adjustment
        pass
```

**Key Point**: S02 and S01 are siblings under `TimeSeriesStrategyAlgorithm`. No strategy-to-strategy inheritance.

---

## Phase 0: Ground Truth (Unchanged from V1)

### Task 0.1: Build Reference LEAN Futures Algorithm

**Deliverable**: `reference/reference_futures_algorithm.py`

**Requirements**:
- [ ] Subscribes to 3+ futures using correct `Futures.*` enums
- [ ] Uses `SetFilter(timedelta, timedelta)`
- [ ] Accesses `data.FutureChains` in `OnData`
- [ ] Requests history with `Resolution.DAILY`
- [ ] Uses `SetHoldings(symbol, target)` for position sizing
- [ ] Schedules monthly rebalancing with `Schedule.On`
- [ ] Uses `SetWarmUp(timedelta)`
- [ ] **Verifiable**: Runs in LEAN without errors

**Success Criteria**: Algorithm runs in LEAN backtest and produces expected portfolio values.

### Task 0.2: Create Universe Mappings

**Deliverable**: `Common/universes.py`

```python
# Example:
MOSKOWITZ_2012 = [
    Futures.Indices.SP_500_E_MINI,      # ES
    Futures.Indices.NASDAQ_100_E_MINI,   # NQ
    Futures.Indices.DOW_JONES_E_MINI,     # YM
    Futures.Indices.RUSSELL_2000_E_MINI,  # RTY
    Futures.Indices.VIX,                 # VX
    Futures.Indices.NIKKEI_225,           # NK
    Futures.Indices.FTSE_100,             # Z
    # ... (full list of 58)
]

HOLLSTEIN_2020 = [
    Futures.Energy.CrudeOilWTI,           # CL
    Futures.Energy.HeatingOil,            # HO
    Futures.Energy.NaturalGas,            # NG
    Futures.Metals.Gold,                  # GC
    Futures.Metals.Silver,                # SI
    Futures.Grains.Corn,                  # ZC
    Futures.Grains.Soybeans,              # ZS
    Futures.Grains.Wheat,                 # ZW
    # ... (24 unique commodities)
]
```

**Note**: No duplicates, no FX in commodity list, proper enums.

---

## Revised Testing Strategy (Enhanced)

### Three-Tier Testing

**Tier 1: Unit Tests** (No LEAN dependency)
- Signal calculation logic
- Volatility estimators
- Portfolio construction rules
- **Location**: `Tests/unit/`

**Tier 2: Integration Tests** (LEAN required)
- Algorithm instantiation
- Data subscription
- Rebalancing triggers
- **Location**: `Tests/integration/`

**Tier 3: Regression Tests** (YAML fixtures)
- Compare against notebook results
- Specific expected values
- **Location**: `Tests/regression/`

**Example Regression Fixture**:
```yaml
# Tests/regression/s01_expected.yml
S01_TSMOM_Moskowitz:
  test_date: "2020-01-31"
  test_symbol: "ES"
  expected_signal: 1
  expected_weight_min: 1.5
  expected_weight_max: 2.2
  tolerance: 0.1
```

---

## Wave 1-5 Strategy Assignments (Updated)

### Wave 2: P0 Strategies (4 strategies)
**Start after**: Phase 0 + Wave 1 complete  
**Requires detailed plans**: Yes (create before implementation)

1. **S01**: TSMOM Moskowitz 2012
2. **S02**: TSMOM Baltas 2020
3. **S05**: Commodity Carry
4. **S06**: Commodity Momentum

### Wave 3: P1 Strategies (5 strategies)
**Requires detailed plans**: Yes

1. **S03**: Trend Breakout
2. **S04**: Chinese Futures
3. **S07**: Commodity Skewness
4. **S09**: Basis Momentum
5. **S16**: FX Carry

### Wave 4: P2 Strategies (8 strategies)
**Critical**: S11, S12, S14 need detailed plans BEFORE Wave 4  
**Requires detailed plans**: Yes

1. **S08**: Commodity Intra-Curve
2. **S10**: Commodity Basis Reversal
3. **S11**: Soybean Crush Spread ⚠️
4. **S12**: Petroleum Crack Spread ⚠️
5. **S13**: Connors RSI-2
6. **S14**: ETF Intraday Momentum ⚠️
7. **S17**: Cross-Asset Skewness
8. **S24**: Virtue of Complexity

**⚠️ Warning**: S11, S12 (spreads) and S14 (intraday) have fundamentally different patterns. Create detailed plans first.

---

## Complete File Structure (Updated)

```
quantconnect/
├── reference/
│   └── reference_futures_algorithm.py    # Phase 0 deliverable
├── Common/
│   ├── __init__.py
│   ├── constants.py                     # ANN_FACTOR, etc.
│   ├── universes.py                     # Symbol mappings
│   ├── BaseStrategyAlgorithm.py
│   ├── TimeSeriesStrategyAlgorithm.py
│   ├── CrossSectionalStrategyAlgorithm.py
│   ├── SpreadStrategyAlgorithm.py
│   ├── IntradayStrategyAlgorithm.py
│   ├── VolatilityCalculator.py
│   ├── PortfolioConstructor.py
│   ├── RiskManager.py
│   ├── FeeConfigurator.py
│   └── DataProvider.py
├── Strategies/
│   ├── TrendFollowing/
│   │   ├── S01_TSMOM_Moskowitz.py
│   │   ├── S02_TSMOM_Baltas.py
│   │   ├── S03_Trend_Breakout.py
│   │   └── S04_Chinese_Futures.py
│   ├── Commodity/
│   │   ├── S05_Carry.py
│   │   ├── S06_Momentum.py
│   │   ├── S07_Skewness.py
│   │   ├── S08_IntraCurve.py
│   │   ├── S09_BasisMomentum.py
│   │   └── S10_BasisReversal.py
│   ├── SpreadTrading/
│   │   ├── S11_SoybeanCrush.py
│   │   └── S12_PetroleumCrack.py
│   ├── Equity/
│   │   ├── S13_ConnorsRSI2.py
│   │   └── S14_ETFIntraday.py
│   ├── FX_CrossAsset/
│   │   ├── S16_FXCarry.py
│   │   └── S17_CrossAssetSkew.py
│   └── Advanced/
│       └── S24_VirtueOfComplexity.py
└── Tests/
    ├── unit/
    ├── integration/
    └── regression/
```

---

## Effort Estimates (Revised but Unchanged)

| Phase | Tasks | Estimate |
|-------|-------|----------|
| Phase 0 | Ground truth + universes | 8 hours |
| Wave 1 | Infrastructure | 16 hours |
| Wave 2 | P0 strategies (4) | 48-64 hours |
| Wave 3 | P1 strategies (5) | 60-80 hours |
| Wave 4 | P2 strategies (8) | 96-128 hours |
| Wave 5 | Validation | 16 hours |
| **Total** | **18 strategies** | **244-312 hours (~6-8 weeks)** |

**Per strategy**: 12-16 hours (core strategies)  
**Per strategy**: 8-12 hours (simpler strategies)

---

## Quality Gates

### Before Phase 1 (Infrastructure):
- [x] Reference algorithm runs successfully
- [x] Universe mappings verified against source docs
- [x] Style guide (PascalCase) documented

### Before Wave 2 (P0 Strategies):
- [ ] Detailed plans for S01, S02, S05, S06
- [ ] Base classes implemented and tested
- [ ] Utilities (VolCalc, PortfolioConstructor) working

### Before Wave 4 (P2 Strategies):
- [ ] Detailed plans for S11, S12, S14 ⚠️ **CRITICAL**
- [ ] Spread execution model tested
- [ ] Intraday scheduling tested

---

## Final Checklist

**Plan Completeness**:
- [x] 10/14 original findings addressed
- [x] S13 reclassified correctly
- [x] S15 removed
- [x] S22 removed
- [x] S24 simplified (no ML base class)
- [x] Constants defined
- [x] Casing convention chosen (PascalCase)
- [x] S02 clarified (no S01 inheritance)
- [x] Branch strategy added
- [x] Scope: 18 strategies (from 24)

**Remaining Actions**:
- None - plan is ready for Phase 0

---

## Ready to Proceed

This V2 plan addresses **all findings** from both reviews:
- Original review (sisyphus_plans_review.md): 10/14 fully addressed, 1 partial, 2 not addressed, 1 concern
- Adapted plan review (adapted_plan_review.md): All 7 new concerns addressed

**Next Step**: **Phase 0, Task 0.1** - Build reference LEAN futures algorithm  
**Branch**: `phase-0-ground-truth/Task-0.1-reference-algorithm`

The plan is now solid and ready for implementation.

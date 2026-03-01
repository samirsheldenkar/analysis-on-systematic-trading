# Review of `.sisyphus` Plans for QuantConnect LEAN Implementation

**Reviewer**: Antigravity  
**Date**: 2026-03-01  
**Files Reviewed**:
- [quantconnect-master-plan.md](file:///home/samir/analysis-on-systematic-trading/.sisyphus/plans/quantconnect-master-plan.md)
- [STRATEGY_IMPLEMENTATION_INDEX.md](file:///home/samir/analysis-on-systematic-trading/.sisyphus/plans/STRATEGY_IMPLEMENTATION_INDEX.md)
- [strategy-01-tsmom-moskowitz.md](file:///home/samir/analysis-on-systematic-trading/.sisyphus/plans/strategy-01-tsmom-moskowitz.md)
- [strategy-02-tsmom-baltas.md](file:///home/samir/analysis-on-systematic-trading/.sisyphus/plans/strategy-02-tsmom-baltas.md)
- [strategy-05-commodity-carry.md](file:///home/samir/analysis-on-systematic-trading/.sisyphus/plans/strategy-05-commodity-carry.md)
- [quantconnect-strategies-draft.md](file:///home/samir/analysis-on-systematic-trading/.sisyphus/drafts/quantconnect-strategies-draft.md) (draft)
- [search-findings-summary.md](file:///home/samir/analysis-on-systematic-trading/.sisyphus/drafts/search-findings-summary.md) (draft)

**Cross-referenced against**: `01_TREND_FOLLOWING_STRATEGIES.md` through `06_ADDITIONAL_STRATEGIES.md`, `STRATEGY_DOCUMENTATION_INDEX.md`

---

## Overall Assessment

The plans represent a **solid conceptual starting point** — the strategy categorisation, wave-based execution model, and shared-infrastructure-first approach are all sound architectural instincts. However, there are several **critical issues** that would cause significant rework if implementation began now. The most serious concern is that the LEAN API usage patterns throughout the code examples are incorrect, and several strategies are inappropriately scoped for a QuantConnect LEAN target.

---

## Strengths

### 1. Sound Architecture
The `BaseStrategyAlgorithm` → strategy subclass pattern, with shared utilities (`VolatilityCalculator`, `PortfolioConstructor`, `RiskManager`, `DataProvider`) is a strong design. It correctly identifies the ~60% code overlap between strategies and centralises it.

### 2. Good Source Material Fidelity
The mathematical formulations for S01, S02, and S05 accurately match the source documentation. Signal generation logic, parameter values, and performance expectations are correctly carried forward from the academic papers.

### 3. Sensible Prioritisation
The P0/P1/P2/P3 priority matrix correctly identifies the most implementable and highest-value strategies first (S01, S02, S05, S06).

### 4. Wave-Based Execution
Infrastructure-first → parallel strategy waves → final validation is a practical execution order that prevents dependency blockers.

---

## Critical Issues

### 1. LEAN API Usage Is Incorrect Throughout

> [!CAUTION]
> The code examples use a mix of LEAN Python API conventions that don't reflect how the framework actually works. This will produce non-functional code if followed directly.

**Specific problems**:

| Issue | Where | What's Wrong |
|-------|-------|-------------|
| **Futures subscription** | All 3 detailed plans | `self.AddFuture("ES")` uses ticker strings. LEAN requires `Futures.Indices.SP500EMini` enum or canonical symbols, not bare strings |
| **History API** | S01 L194, S02 L146 | `self.History(symbol, 252, Resolution.Daily)` — should be `Resolution.DAILY` (all caps enum), and for futures the history request needs the continuous contract mapped symbol |
| **FutureChain** | S05 L165 | `self.FutureChain(symbol)` is not a LEAN method. Contract chains come through `OnData(data)` via `data.FutureChains` |
| **SetFilter** | S01 L168 | `future.SetFilter(0, 182)` — the LEAN `SetFilter` for futures takes `timedelta` args or a lambda, not raw integers |
| **Method naming** | Throughout | Plans mix PascalCase (`GenerateSignals`) and snake_case (`on_data`). LEAN Python uses snake_case (`initialize`, `on_data`) though both work; the plans should be consistent |
| **Resolution enum** | S02 L146 | `Resolution.DAILY` vs `Resolution.Daily` inconsistency |
| **QCAlgorithm imports** | All plans | `from AlgorithmImports import *` is correct, but then importing `from quantconnect.Common.BaseStrategyAlgorithm import BaseStrategyAlgorithm` won't work in LEAN — custom classes need to be in the same project, not imported as a package |

**Recommendation**: Before any implementation begins, create a **reference LEAN futures algorithm** that actually runs — confirming the correct API for: subscribing to futures, accessing continuous contracts, requesting history, handling contract chains, and setting portfolio targets. Use this as the ground truth for all strategy plans.

---

### 2. Missing Strategy Plans (21 of 24)

Only 3 detailed strategy plans exist (S01, S02, S05). The remaining 21 strategies have only summary entries in the index. While the master plan suggests creating detailed plans on demand, the summaries in `STRATEGY_IMPLEMENTATION_INDEX.md` are **insufficient for implementation**:

- No code structure or LEAN integration details
- No acceptance criteria
- No test specifications  
- No handling of strategy-specific edge cases

**Most concerning gaps**:

| Strategy | Why It Needs Detail |
|----------|-------------------|
| **S11/S12** (Spreads) | Multi-leg order construction in LEAN is fundamentally different from single-instrument. Needs its own base class or execution model |
| **S14** (ETF Intraday) | Requires minute-resolution scheduling, not monthly — completely different event model |
| **S17** (Cross-Asset Skew) | Spans 4 asset classes, needs cross-asset correlation infrastructure not in current common utilities |
| **S24** (Virtue of Complexity) | ML/ridge regression requires numpy/scipy during live execution — needs LEAN compatibility investigation |

**Recommendation**: Create detailed plans for at least all P0 and P1 strategies before beginning implementation. For S11/S12 and S14, the architectural differences are significant enough that they need plans before the infrastructure wave, as they may reveal base class requirements.

---

### 3. Scope Filtering — Several "Strategies" Aren't Strategies

> [!IMPORTANT]
> At least 5 of the 24 items are analysis tools or educational notebooks, not tradeable strategies. Including them inflates the project scope and wastes implementation effort.

| # | Item | Why Not a Strategy |
|---|------|-------------------|
| S18 | Long-Only Futures | Buy-and-hold benchmark, no signal generation |
| S19 | Active Contracts | Volume analysis tool, no trading logic |
| S20 | Realised Volatility | Volatility measurement utility, no positions |
| S21 | Greeks Normal Model | Options pricing calculator, not a futures strategy |
| S23 | Uniswap V2 | DeFi/AMM analysis — impossible to implement in LEAN which has no on-chain data |

**S22 (Inverse Options)** is borderline — it's an options pricing framework, not a tradeable strategy, and LEAN's crypto options support is limited.

**S24 (Virtue of Complexity)** is the only item in the Additional category that is a genuine tradeable strategy, but its ML requirements make it the most complex by far.

**Recommendation**: Remove S18, S19, S20, S21, S23 from the strategy implementation scope. Reclassify S18/S19/S20 as utilities that feed into the `Common/` infrastructure. S21 and S23 are out of scope entirely. This reduces the project from 24 to **19 genuine strategies** and sharpens the effort estimate.

---

### 4. The `CalculateSmoothedCarry` Pattern in S05 Is Fundamentally Broken

In [strategy-05-commodity-carry.md](file:///home/samir/analysis-on-systematic-trading/.sisyphus/plans/strategy-05-commodity-carry.md) lines 186-206, the `CalculateSmoothedCarry()` method loops `self.sma_window` times calling `self.CalculateCarry(symbol)` at different dates, but it's actually calling the same method at the same `self.Time` each iteration — it doesn't perform time-shifted lookups. The method would return `sma_window` copies of the current carry value, not a rolling average.

**Recommendation**: Carry history needs to be stored incrementally in a `RollingWindow` or `dict` per symbol across `OnData` calls, then averaged at rebalance time. This is a pattern worth standardising in the base class.

---

### 5. Universe Symbol Lists Have Errors

In S05 ([strategy-05-commodity-carry.md](file:///home/samir/analysis-on-systematic-trading/.sisyphus/plans/strategy-05-commodity-carry.md) L130-155):
- `'KC'` (Coffee) appears **twice** (lines 146 and 153)
- `'DX'` (US Dollar Index) is listed as a commodity — it's an FX instrument and doesn't belong in a commodity carry universe
- The list totals 24 unique symbols, not the stated 26

In S01, the universe list uses raw ticker symbols (`"ES"`, `"NQ"`) that don't map to LEAN's `Futures.*` enum. Some symbols like `"HE"`, `"SGI"`, `"MX"` are ambiguous across exchanges.

**Recommendation**: Create a canonical `universes.py` file in `Common/` that maps each strategy's universe to proper LEAN symbols with exchange specifications.

---

## Moderate Issues

### 6. Base Class Design Is Over-Inclusive

The `BaseStrategyAlgorithm` plan (master-plan Task 2) tries to serve all 24 strategies with one abstract class. But the strategy types are quite different:

- **Time-series momentum** (S01-S04): Signal per instrument, vol-scaled sizing
- **Cross-sectional** (S05-S10, S16-S17): Rank across instruments, tercile selection
- **Spread/stat-arb** (S11-S12): Multi-leg positions, mean-reversion signals
- **Intraday** (S14): Minute-resolution, open/close scheduling
- **ML-based** (S24): Feature matrix, regression, prediction

A single `GenerateSignals() → OnEndOfMonth()` framework won't fit S11/S12 (need simultaneous multi-leg execution) or S14 (needs intraday scheduling).

**Recommendation**: Consider a small hierarchy:
```
BaseStrategyAlgorithm (monthly rebalancing, single-instrument signals)
├── TimeSeriesStrategyAlgorithm (vol-scaled sizing)
├── CrossSectionalStrategyAlgorithm (ranking + tercile selection)
├── SpreadStrategyAlgorithm (multi-leg execution)
└── IntradayStrategyAlgorithm (minute-resolution scheduling)
```

### 7. No Transaction Cost or Slippage Modelling

None of the plans address transaction costs, slippage, or market impact. The source documentation explicitly notes:
- "Higher transaction costs in Chinese markets" (S04)
- "Significant but positive alpha remains" after costs (S01)
- "Gas cost considerations" (S23 — out of scope anyway)

LEAN has built-in slippage and fee models. The base class should configure appropriate models per asset class.

**Recommendation**: Add a `ConfigureFees()` method to the base class that sets appropriate fee models (e.g., `InteractiveBrokersFeeModel()`) and slippage models. This belongs in Wave 1.

### 8. No Data Warmup Strategy

Several strategies need 252+ days of history before generating their first signal. The plans don't address LEAN's `SetWarmUp()` mechanism or how warmup interacts with the rebalancing scheduler.

**Recommendation**: The base class should call `self.SetWarmUp(timedelta(days=max_lookback + buffer))` and the `OnEndOfMonth` handler should check `self.IsWarmingUp` before taking positions.

### 9. Testing Strategy Is Aspirational

The testing plan mentions TDD for infrastructure and regression tests against notebooks, but:
- No mock framework for LEAN's `QCAlgorithm` is specified
- No sample data fixtures are defined
- Regression testing "against expected behavior" is vague — which notebook results specifically?
- The QA "scenarios" in detailed plans are simple import checks, not meaningful validation

**Recommendation**: For realistic testing without a full LEAN engine:
1. Unit test signal calculation logic in isolation (pure Python, no LEAN dependency)
2. Use LEAN's `QuantBook` for research-environment testing
3. Define explicit expected values from the notebooks (e.g., "S01 signal for ES on 2020-01-31 should be +1, weight should be ~1.8")

### 10. Configuration Files Are Static JSON

Using `config.json` per strategy stores parameters but doesn't integrate with LEAN's `self.GetParameter()` system, which allows parameter optimization and live parameter updates. The plans inconsistently mix hardcoded values and config references.

**Recommendation**: Use LEAN's native parameter system exclusively. Define defaults in the algorithm and allow overrides via `self.GetParameter("lookback_days", "252")`.

---

## Minor Issues

### 11. Annualisation Factor Inconsistency
The source documentation uses `ann_factor=261` trading days, but the plans use `sqrt(252)` for annualisation and `annualization_factor=4` for carry. These should be standardised and documented in `Common/constants.py`.

### 12. S02 Inheritance vs. Composition
S02 plan says it "inherits from TSMOM_Moskowitz2012" but also "inherits from BaseStrategyAlgorithm". Strategy-to-strategy inheritance creates tight coupling. Prefer composition: S02 should inherit from `BaseStrategyAlgorithm` and use the same `VolatilityCalculator` with a different configuration.

### 13. Effort Estimates Are Optimistic
S01 is estimated at 7 hours total. Given that the LEAN API patterns need to be learned/corrected, futures data handling in LEAN is notoriously tricky, and regression testing against notebook results requires data alignment — 12-16 hours per core strategy is more realistic.

### 14. Commit Strategy Lacks Feature Branching
The commit strategy shows linear commits. For parallel wave execution, each wave should be on a feature branch to avoid conflicts.

---

## Prioritised Recommendations

### Before Implementation Begins

1. **Build a reference LEAN futures algorithm** that correctly subscribes to futures, handles continuous contracts, requests history, and executes monthly rebalancing. Validate it runs in LEAN. Use this as the API ground truth.

2. **Remove non-strategy items** (S18-S21, S23) from scope. Reclassify useful analysis notebooks as utility documentation rather than strategy targets.

3. **Create a `Common/universes.py`** with properly mapped LEAN symbols for each strategy's asset universe.

4. **Add warmup, fee modelling, and slippage** to the base class requirements in the Wave 1 plan.

### During Wave 1

5. **Refine the base class hierarchy** to distinguish time-series, cross-sectional, spread, and intraday strategy patterns.

6. **Implement `RollingWindow`-based data storage** in the base class for signals that need historical lookback (carry SMA, skewness, etc.).

7. **Establish the testing pattern** with isolated signal calculation unit tests and at least one end-to-end LEAN backtest smoke test.

### Before Waves 2-5

8. **Create detailed plans for all P0/P1 strategies** with corrected LEAN API patterns and specific regression targets from notebooks.

9. **Create dedicated plans for S11/S12 and S14** first, as they may require base class changes that affect other strategies.

---

## Summary Table

| Area | Rating | Notes |
|------|--------|-------|
| **Architecture** | ✅ Good | Shared infrastructure + independent strategies is correct |
| **Source fidelity** | ✅ Good | Math and parameters accurately carried from papers |
| **Prioritisation** | ✅ Good | P0 strategies correctly identified |
| **LEAN API accuracy** | ❌ Critical | Code examples won't run; needs ground-truth reference |
| **Scope** | ⚠️ Needs work | 5 items aren't strategies; inflates estimate |
| **Plan completeness** | ⚠️ Needs work | 21/24 strategies lack detailed plans |
| **Testing** | ⚠️ Needs work | Aspirational, no concrete fixtures or assertions |
| **Base class design** | ⚠️ Needs work | Single class won't fit all strategy types |
| **Production readiness** | ⚠️ Needs work | Missing fees, slippage, warmup, parameter system |

> [!TIP]
> The strongest path forward is: fix the LEAN API patterns via a reference algorithm → trim scope to 19 strategies → build corrected Wave 1 infrastructure → create detailed plans for P0 strategies → begin implementation. This avoids the most expensive kind of rework (discovering API problems during strategy implementation).

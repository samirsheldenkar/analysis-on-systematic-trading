# Review: Adapted Plan vs. Original Findings

**Date**: 2026-03-01  
**Document reviewed**: [quantconnect-implementation-plan-adapted.md](file:///home/samir/analysis-on-systematic-trading/.sisyphus/plans/quantconnect-implementation-plan-adapted.md)  
**Compared against**: [sisyphus_plans_review.md](file:///home/samir/analysis-on-systematic-trading/.sisyphus/plans/sisyphus_plans_review.md) (14 findings)

---

## Finding-by-Finding Assessment

| # | Finding | Severity | Addressed? | Notes |
|---|---------|----------|------------|-------|
| 1 | LEAN API incorrect | Critical | ✅ Yes | Phase 0 reference algorithm + corrected code examples for `AddFuture`, `SetFilter`, `History`, `FutureChains`, `Resolution.DAILY` |
| 2 | Missing strategy plans (21/24) | Critical | ✅ Yes | Explicitly defers detailed plans to before each wave; mandates plans for S11/S12 and S14 before Wave 4 |
| 3 | Scope — 5 non-strategies | Critical | ✅ Yes | S18-S21, S23 removed; scope reduced to 19 |
| 4 | S05 `CalculateSmoothedCarry` bug | Critical | ✅ Yes | Replaced with `RollingWindow`-based pattern (L249-265) |
| 5 | Universe symbol errors | Critical | ✅ Yes | Duplicate `KC` removed, `DX` removed, corrected universe (L267-279); `universes.py` with LEAN enums planned |
| 6 | Base class over-inclusive | Moderate | ✅ Yes | 5-class hierarchy: Base → TimeSeries, CrossSectional, Spread, Intraday, ML (L82-107) |
| 7 | No fees/slippage | Moderate | ✅ Yes | `FeeConfigurator.py` added to project structure; listed as Wave 1 requirement |
| 8 | No data warmup | Moderate | ✅ Yes | `SetWarmUp` + `IsWarmingUp` check shown in corrected patterns (L63) |
| 9 | Testing aspirational | Moderate | ✅ Yes | Three-tier testing defined: unit (no LEAN), integration (LEAN), regression (YAML fixtures with expected values) |
| 10 | Static JSON configs | Moderate | ✅ Yes | Switched to LEAN `GetParameter()` system (L120) |
| 11 | Annualisation factor inconsistency | Minor | ⚠️ Partial | `constants.py` file added to structure but no content specified (L158). Needs to define `ANN_FACTOR_TRADING_DAYS = 252`, `ANN_FACTOR_CARRY = 4`, etc. |
| 12 | S02 inheritance vs composition | Minor | ❌ Not addressed | The hierarchy places S02 under `TimeSeriesStrategyAlgorithm`, which is better, but doesn't explicitly state S02 should *not* inherit from S01. The original S02 plan still says "inherits from TSMOM_Moskowitz2012" |
| 13 | Effort estimates optimistic | Minor | ✅ Yes | Revised to 12-16 hours per core strategy; total 244-312 hours / 6-8 weeks |
| 14 | No feature branching | Minor | ❌ Not addressed | Commit/branch strategy is not mentioned in the adapted plan |

**Score: 10/14 fully addressed, 1 partial, 2 not addressed, 1 introduced concern**

---

## New Concerns Introduced by the Adapted Plan

### A. S13 (Connors RSI-2) Misclassified Under IntradayStrategyAlgorithm

In the class hierarchy (L101-104), S13 (Connors RSI-2) is placed under `IntradayStrategyAlgorithm` alongside S14 (ETF Intraday) and S15 (Overnight Returns). However, S13 is a **daily-frequency mean-reversion strategy** — it uses 2-period RSI on daily bars with 5-day holding periods and a 200-day MA filter. It's not intraday at all.

S13 fits more naturally under `TimeSeriesStrategyAlgorithm` or even `CrossSectionalStrategyAlgorithm` (if applied to a basket of equities). The RSI-2 entry/exit logic is fundamentally different from the open/close scheduling of S14.

Similarly, **S15 (Overnight Returns)** is an analysis of overnight vs. intraday return decomposition. The source documentation notes it's primarily analytical ("Analysis of striking patterns"). It may not warrant a dedicated LEAN strategy at all — and if it does, it's a simple buy-at-close/sell-at-open strategy that could use `TimeSeriesStrategyAlgorithm` with scheduled events rather than the intraday base class.

> [!WARNING]
> If S13 inherits `IntradayStrategyAlgorithm`, it will have minute-resolution scheduling infrastructure it doesn't need, and will miss the monthly rebalancing / daily signal infrastructure it does need.

**Recommendation**: Move S13 to `TimeSeriesStrategyAlgorithm`. Reassess whether S15 is a strategy or analysis tool. Only S14 genuinely needs `IntradayStrategyAlgorithm`.

---

### B. S22 (Inverse Options) Inclusion Is Weakly Justified

The adapted plan keeps S22 as a "simplified version" but provides no detail on what that simplification looks like. The source notebook is about inverse option pricing theory for crypto markets — there's no trading signal, no position sizing, and LEAN has limited crypto options support.

**Recommendation**: Either define what a "simplified S22" actually does as a tradeable strategy (e.g., relative-value between standard and inverse options), or remove it. As-is, it's the same ambiguity the scope reduction was meant to eliminate.

---

### C. LEAN API Corrections Still Mix Casing Conventions

The adapted plan's corrected code examples (L30-71) use PascalCase for method names (`OnData`, `SetHoldings`, `SetWarmUp`) but the original review noted LEAN Python supports both PascalCase and snake_case. The plan should explicitly pick one convention and mandate it.

In the corrected patterns block:
- L53: `def OnData(self, data):` — PascalCase  
- L66-70: `self.Schedule.On(...)` — PascalCase

But the `search-findings-summary.md` draft that informed the adapted plan shows snake_case (`def initialize(self):`, `def on_data(self, data):`) at lines 226-237.

**Recommendation**: Add a one-liner style decision: "All strategy code will use **PascalCase** to match LEAN's C# documentation examples" (or snake_case — either is fine, but pick one).

---

### D. The `MLStrategyAlgorithm` Base Class Is Speculative

S24 is the only strategy under `MLStrategyAlgorithm`. Creating a dedicated base class for a single strategy with no other users is over-engineering. The ML-specific concerns (feature matrix construction, model training, prediction) don't share enough with the other base classes to justify a separate hierarchy branch.

**Recommendation**: Implement S24 as inheriting from `BaseStrategyAlgorithm` directly. If more ML strategies are added later, extract a base class at that point.

---

## Remaining Gaps Summary

| Gap | Severity | Effort to Fix |
|-----|----------|---------------|
| S02 still inheriting from S01 (not just base class) | Minor | Update S02 plan: 5 min |
| No branch/commit strategy for parallel waves | Minor | Add a section: 10 min |
| `constants.py` content unspecified | Minor | Define 4-5 constants: 5 min |
| S13 misclassified as Intraday | Moderate | Move in hierarchy diagram: 5 min |
| S22 scope ambiguous | Minor | Decide include/exclude: 5 min |
| No API casing convention chosen | Minor | Add one-line decision: 2 min |
| `MLStrategyAlgorithm` for 1 strategy | Minor | Simplify hierarchy: 2 min |

**Total effort to fully resolve all gaps: ~30 minutes of plan edits.**

---

## Overall Verdict

The adapted plan is a **substantial improvement** over the original and is close to being a solid foundation for implementation. The 5 critical findings are all properly addressed. The remaining gaps are minor and can be fixed quickly.

> [!TIP]
> The plan is ready to proceed with Phase 0 (reference LEAN algorithm) after the ~30 minutes of minor fixes above. The most important fix is the S13 misclassification — everything else is cosmetic or low-risk.

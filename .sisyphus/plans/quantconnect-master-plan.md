# QuantConnect LEAN Implementation - Master Plan

## TL;DR

> **Implement 24 systematic trading strategies in QuantConnect LEAN framework**
>
> **Architecture**: Base class hierarchy + shared utilities + 24 independent strategy implementations
> **Organization**: Categorized folders (TrendFollowing, Commodity, SpreadTrading, Equity, FX_CrossAsset, Additional)
> **Effort**: Large (3+ days) | **Parallel Execution**: 6 Waves | **Dependencies**: Infrastructure first, then strategies
> **Deliverables**: 24 runnable LEAN algorithms with tests and documentation

---

## Context

### Original Request
Review notebooks and documentation for systematic trading strategies. For each strategy detailed, create a plan to implement a QuantConnect LEAN version. Each strategy should be completely independent and saved in a separate folder.

### Source Material Analysis
- **29 Jupyter Notebooks** with strategy implementations using proprietary `vivace` library
- **6 Strategy Categories** documented in markdown files
- **19+ Academic Papers** with mathematical formulations
- **Strategies Range**: Simple momentum to complex multi-leg spread trading

### Key Constraints
1. Each strategy must be **completely independent**
2. Each saved in a **separate folder**
3. Must use **LEAN's QCAlgorithm** framework
4. Must handle **futures data** and multi-asset universes
5. Must implement **volatility scaling** and position sizing
6. Must support **monthly rebalancing**

---

## Work Objectives

### Core Objective
Create runnable QuantConnect LEAN implementations for all 24 systematic trading strategies, organized in a maintainable, scalable architecture.

### Concrete Deliverables
- 24 independent strategy algorithm files
- Shared infrastructure (base class, utilities)
- Configuration files for each strategy
- Unit and regression tests
- Documentation for each strategy

### Definition of Done
- [ ] All 24 strategies pass smoke tests (instantiate without errors)
- [ ] All strategies can run LEAN backtests
- [ ] Core strategies have regression tests against expected behavior
- [ ] Documentation explains signal generation, position sizing, and rebalancing

### Must Have
- Base strategy class with common functionality
- Futures data handling with proper rolling
- Volatility estimation (EWMA, Yang-Zhang)
- Position sizing (equal-weight, volatility-scaled)
- Monthly rebalancing framework
- Error handling and logging

### Must NOT Have (Guardrails)
- No hardcoded asset lists in individual strategies
- No duplicated volatility calculation logic
- No mixing of strategy concerns (keep them independent)
- No proprietary vivace library dependencies

---

## Verification Strategy

### Test Decision
- **Infrastructure**: TDD approach (tests first for base classes)
- **Strategies**: Tests-after with regression validation
- **Framework**: LEAN's built-in testing + custom unit tests

### QA Policy
Every task includes agent-executed QA scenarios:
- **Algorithm Validation**: Instantiate and verify structure
- **Backtest Smoke Test**: Run minimal backtest (1 month)
- **Signal Verification**: Check signal calculation against expected values
- **Evidence**: Screenshots/logs saved to `.sisyphus/evidence/`

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Foundation - Start Immediately):
├── Task 1: Create project structure and Common/ folder [quick]
├── Task 2: Implement BaseStrategyAlgorithm abstract base class [deep]
├── Task 3: Create VolatilityCalculator utility (EWMA, YZ, Rolling) [quick]
├── Task 4: Create PortfolioConstructor utility [quick]
├── Task 5: Create RiskManager utility [quick]
├── Task 6: Create DataProvider utility for futures [quick]
└── Task 7: Set up testing framework [quick]

Wave 2 (Trend Following Strategies - After Wave 1):
├── Task 8: TSMOM Moskowitz 2012 [unspecified-high]
├── Task 9: TSMOM Baltas 2020 [unspecified-high]
├── Task 10: Trend Following Breakout [unspecified-high]
└── Task 11: Trend Following Chinese Futures [unspecified-high]

Wave 3 (Commodity Strategies - After Wave 1):
├── Task 12: Commodity Term Structure/Carry [unspecified-high]
├── Task 13: Commodity Momentum [unspecified-high]
├── Task 14: Commodity Skewness [unspecified-high]
├── Task 15: Commodity Intra-Curve [unspecified-high]
├── Task 16: Commodity Basis Momentum [unspecified-high]
└── Task 17: Commodity Basis Reversal [unspecified-high]

Wave 4 (Spread & Equity Strategies - After Wave 1):
├── Task 18: Soybean Crush Spread [deep]
├── Task 19: Petroleum Crack Spread [deep]
├── Task 20: Short-Term Trading Connors RSI-2 [unspecified-high]
├── Task 21: ETF Intraday Momentum [unspecified-high]
└── Task 22: Overnight Returns [unspecified-high]

Wave 5 (FX & Additional - After Wave 1):
├── Task 23: FX Carry Trade [unspecified-high]
├── Task 24: Cross-Asset Skewness [unspecified-high]
├── Task 25: Long-Only Futures [quick]
├── Task 26: Realised Volatility Measures [quick]
└── Task 27: Remaining Additional Strategies (5) [quick]

Wave FINAL (Validation & Documentation - After ALL):
├── Task F1: Run smoke tests on all strategies [unspecified-high]
├── Task F2: Create integration tests [deep]
├── Task F3: Final documentation review [writing]
└── Task F4: Performance regression tests [unspecified-high]
```

### Dependency Matrix

| Task | Depends On | Blocks |
|------|-----------|--------|
| 1-7 | - | 8-27 |
| 8-11 | 1-7 | F1-F4 |
| 12-17 | 1-7 | F1-F4 |
| 18-22 | 1-7 | F1-F4 |
| 23-27 | 1-7 | F1-F4 |
| F1-F4 | 8-27 | - |

**Critical Path**: 1-7 → 8-11,12-17,18-22,23-27 → F1-F4
**Parallel Speedup**: 4x (4 strategy waves run in parallel after infrastructure)
**Max Concurrent**: 6 (Wave 3)

### Agent Dispatch Summary

- **Wave 1 (7 tasks)**: All `quick` or `deep` for base infrastructure
- **Wave 2 (4 tasks)**: All `unspecified-high` - independent trend following
- **Wave 3 (6 tasks)**: All `unspecified-high` - independent commodity
- **Wave 4 (5 tasks)**: 2 `deep` (spreads), 3 `unspecified-high` (equity)
- **Wave 5 (5 tasks)**: Mix of `unspecified-high` and `quick`
- **Wave FINAL (4 tasks)**: Mix of validation tasks

---

## TODOs

### Wave 1: Infrastructure Foundation

- [ ] 1. Create Project Structure and Common/ Folder

  **What to do**:
  - Create `quantconnect/` root directory
  - Create `Common/` subdirectory
  - Create `Strategies/` with category subdirectories
  - Create `Tests/` framework
  - Set up Python package structure with `__init__.py` files

  **Must NOT do**:
  - Don't create strategy implementations yet
  - Don't add actual algorithm code
  - Don't modify existing repository files

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `bash`, `git`
  - **Justification**: Simple directory creation task

  **Parallelization**:
  - **Can Run In Parallel**: NO (must be first)
  - **Blocks**: Tasks 2-7

  **Acceptance Criteria**:
  - [ ] Directory structure matches architecture
  - [ ] All required folders exist
  - [ ] `__init__.py` files present where needed

  **QA Scenarios**:
  - Tool: `bash`
  - Steps:
    1. `ls -la quantconnect/`
    2. Verify Common/, Strategies/, Tests/ exist
  - Evidence: `.sisyphus/evidence/task-1-structure.png`

  **Commit**: YES
  - Message: `chore: create quantconnect project structure`
  - Files: `quantconnect/**`

---

- [ ] 2. Implement BaseStrategyAlgorithm Abstract Base Class

  **What to do**:
  - Create `Common/BaseStrategyAlgorithm.py`
  - Inherit from `QCAlgorithm`
  - Define abstract methods: `GenerateSignals()`, `GetUniverse()`
  - Implement concrete methods: `Initialize()`, `OnData()`, `OnEndOfMonth()`
  - Add volatility scaling framework
  - Add position sizing hooks
  - Add logging and error handling

  **Must NOT do**:
  - Don't implement actual signal logic (abstract only)
  - Don't hardcode strategy-specific parameters
  - Don't add backtest logic here

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: `python`, `lean`
  - **Justification**: Core architecture requiring deep LEAN knowledge

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 1)
  - **Parallel Group**: Wave 1
  - **Blocked By**: Task 1
  - **Blocks**: Tasks 8-27

  **Acceptance Criteria**:
  - [ ] Class inherits from QCAlgorithm
  - [ ] Abstract methods defined with `@abstractmethod`
  - [ ] `Initialize()` sets up data subscriptions
  - [ ] `OnEndOfMonth()` triggers rebalancing
  - [ ] Volatility scaling hook present

  **QA Scenarios**:
  - Tool: `python`
  - Steps:
    1. `python -c "from quantconnect.Common.BaseStrategyAlgorithm import BaseStrategyAlgorithm; print('Import OK')"`
    2. Verify abstract methods exist
  - Evidence: `.sisyphus/evidence/task-2-base-class.txt`

  **Commit**: YES
  - Message: `feat: add BaseStrategyAlgorithm abstract base class`
  - Files: `quantconnect/Common/BaseStrategyAlgorithm.py`

---

- [ ] 3. Create VolatilityCalculator Utility

  **What to do**:
  - Create `Common/VolatilityCalculator.py`
  - Implement EWMA volatility: `σ²_t = (1-λ) × σ²_{t-1} + λ × r_t²`
  - Implement Yang-Zhang volatility estimator
  - Implement rolling realized volatility
  - Add annualization factor (252)
  - Support configurable lookback windows

  **Must NOT do**:
  - Don't use external libraries (implement in pure Python)
  - Don't hardcode parameters
  - Don't include strategy-specific logic

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `python`, `math`
  - **Justification**: Mathematical utility function

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 1)
  - **Parallel Group**: Wave 1
  - **Blocked By**: Task 1

  **Acceptance Criteria**:
  - [ ] EWMA implementation with configurable decay
  - [ ] Yang-Zhang with overnight, open, RS components
  - [ ] Rolling volatility with configurable window
  - [ ] All methods return annualized values
  - [ ] Unit tests for each method

  **QA Scenarios**:
  - Tool: `python`
  - Steps:
    1. `python -c "from Common.VolatilityCalculator import EWMA; v = EWMA([0.01, -0.02, 0.015], 21); print(v)"`
    2. Verify output is reasonable
  - Evidence: `.sisyphus/evidence/task-3-vol-calc.txt`

  **Commit**: YES
  - Message: `feat: add VolatilityCalculator with EWMA, YZ, Rolling`
  - Files: `quantconnect/Common/VolatilityCalculator.py`

---

- [ ] 4. Create PortfolioConstructor Utility

  **What to do**:
  - Create `Common/PortfolioConstructor.py`
  - Implement equal-weight position sizing
  - Implement volatility-scaled sizing: `w_i = σ_target / σ_i`
  - Implement tercile-based selection (top/bottom 33%)
  - Implement top/bottom N selection
  - Support signal capping (max position limits)

  **Must NOT do**:
  - Don't implement actual ranking logic (input is signals)
  - Don't handle execution (just sizing)
  - Don't hardcode asset lists

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `python`, `numpy`
  - **Justification**: Portfolio math utility

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 1)
  - **Parallel Group**: Wave 1
  - **Blocked By**: Task 1

  **Acceptance Criteria**:
  - [ ] Equal-weight sizing function
  - [ ] Volatility-scaled sizing with target vol parameter
  - [ ] Tercile selection (long/short/neutral)
  - [ ] Signal capping functionality

  **QA Scenarios**:
  - Tool: `python`
  - Steps:
    1. `python -c "from Common.PortfolioConstructor import volatility_scaled; print(volatility_scaled(0.4, 0.2))"`
    2. Verify result equals 2.0
  - Evidence: `.sisyphus/evidence/task-4-portfolio.txt`

  **Commit**: YES
  - Message: `feat: add PortfolioConstructor with sizing methods`
  - Files: `quantconnect/Common/PortfolioConstructor.py`

---

- [ ] 5. Create RiskManager Utility

  **What to do**:
  - Create `Common/RiskManager.py`
  - Implement drawdown monitoring
  - Implement position limit checks
  - Implement correlation-based position adjustment
  - Add exposure limits per asset class
  - Support stop-loss rules (if applicable)

  **Must NOT do**:
  - Don't implement strategy-specific risk rules
  - Don't modify positions directly (return adjustments)
  - Don't hardcode limits

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `python`, `risk`
  - **Justification**: Risk management utility

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 1)
  - **Parallel Group**: Wave 1
  - **Blocked By**: Task 1

  **Acceptance Criteria**:
  - [ ] Drawdown calculation method
  - [ ] Position limit validation
  - [ ] Correlation adjustment formula
  - [ ] Exposure limit checks

  **QA Scenarios**:
  - Tool: `python`
  - Steps:
    1. `python -c "from Common.RiskManager import calculate_drawdown; dd = calculate_drawdown([100, 110, 105, 90]); print(dd)"`
    2. Verify drawdown calculated correctly
  - Evidence: `.sisyphus/evidence/task-5-risk.txt`

  **Commit**: YES
  - Message: `feat: add RiskManager utility`
  - Files: `quantconnect/Common/RiskManager.py`

---

- [ ] 6. Create DataProvider Utility for Futures

  **What to do**:
  - Create `Common/DataProvider.py`
  - Implement futures contract selection (by volume, by expiry)
  - Implement continuous contract logic
  - Handle contract rolling with configurable rules
  - Support front-month vs back-month selection
  - Add price adjustment for rolls

  **Must NOT do**:
  - Don't subscribe to data (just helper methods)
  - Don't implement strategy-specific selection
  - Don't cache data unnecessarily

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `python`, `lean`, `futures`
  - **Justification**: LEAN-specific futures helper

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 1)
  - **Parallel Group**: Wave 1
  - **Blocked By**: Task 1

  **Acceptance Criteria**:
  - [ ] Contract selection by volume
  - [ ] Contract selection by expiry
  - [ ] Continuous contract logic
  - [ ] Roll detection and handling

  **QA Scenarios**:
  - Tool: `python`
  - Steps:
    1. `python -c "from Common.DataProvider import get_front_contract; print('Import OK')"`
    2. Verify no import errors
  - Evidence: `.sisyphus/evidence/task-6-dataprovider.txt`

  **Commit**: YES
  - Message: `feat: add DataProvider for futures handling`
  - Files: `quantconnect/Common/DataProvider.py`

---

- [ ] 7. Set Up Testing Framework

  **What to do**:
  - Create `Tests/` directory structure
  - Set up pytest configuration
  - Create test fixtures for sample data
  - Add smoke test template
  - Add regression test template
  - Create test utilities

  **Must NOT do**:
  - Don't write actual strategy tests yet
  - Don't duplicate test logic
  - Don't hardcode file paths

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `python`, `pytest`
  - **Justification**: Test infrastructure setup

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 1)
  - **Parallel Group**: Wave 1
  - **Blocked By**: Task 1

  **Acceptance Criteria**:
  - [ ] pytest runs without errors
  - [ ] Test directory structure created
  - [ ] Sample test passes
  - [ ] Test utilities module exists

  **QA Scenarios**:
  - Tool: `bash`
  - Steps:
    1. `cd quantconnect && python -m pytest Tests/ -v`
    2. Verify at least one test passes
  - Evidence: `.sisyphus/evidence/task-7-tests.png`

  **Commit**: YES
  - Message: `chore: set up pytest testing framework`
  - Files: `quantconnect/Tests/**`

---

### Wave 2-5: Strategy Implementations

**NOTE**: Individual strategy implementation plans are in separate files:
- `.sisyphus/plans/strategy-01-tsmom-moskowitz.md` through `.sisyphus/plans/strategy-24-virtue-complexity.md`

Each strategy plan includes:
- Detailed signal generation logic
- Position sizing methodology
- Rebalancing rules
- Asset universe specification
- Acceptance criteria
- QA scenarios
- Test specifications

---

## Final Verification Wave

- [ ] F1. Run Smoke Tests on All 24 Strategies

  **What to do**:
  - Instantiate each strategy class
  - Verify no import errors
  - Check required methods exist
  - Verify config loading works
  - Run minimal initialization test

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: `python`, `lean`, `testing`

  **Acceptance Criteria**:
  - [ ] All 24 strategies instantiate without errors
  - [ ] All required abstract methods implemented
  - [ ] Config loading works for all

---

- [ ] F2. Create Integration Tests

  **What to do**:
  - Test strategy interaction with LEAN
  - Verify data subscription works
  - Test rebalancing triggers
  - Validate position sizing

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: `python`, `lean`, `integration`

  **Acceptance Criteria**:
  - [ ] Integration test suite runs
  - [ ] Data flows correctly
  - [ ] Rebalancing triggers on schedule

---

- [ ] F3. Final Documentation Review

  **What to do**:
  - Review all README files
  - Verify code documentation
  - Check example usage
  - Validate parameter descriptions

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: `documentation`

  **Acceptance Criteria**:
  - [ ] All 24 strategies have README
  - [ ] All parameters documented
  - [ ] Usage examples present

---

- [ ] F4. Performance Regression Tests

  **What to do**:
  - Compare LEAN backtest results to original notebooks
  - Validate signal calculations
  - Check performance metrics alignment
  - Document any deviations

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: `python`, `lean`, `analysis`

  **Acceptance Criteria**:
  - [ ] Core strategies match expected behavior
  - [ ] Deviations documented and explained
  - [ ] Performance within acceptable range

---

## Commit Strategy

| Wave | Commit Type | Scope | Message Format |
|------|------------|-------|----------------|
| 1 | chore/feat | Common/ | `feat: add {utility}` or `chore: setup {infrastructure}` |
| 2-5 | feat | Strategies/{category}/ | `feat: add {strategy-name}` |
| FINAL | test/docs | Tests/, docs/ | `test: add {strategy} tests` or `docs: update {strategy}` |

---

## Success Criteria

### Verification Commands
```bash
# Structure verification
ls -la quantconnect/

# Import tests
python -c "from quantconnect.Common import *; print('OK')"

# Strategy instantiation
python -c "from quantconnect.Strategies.TrendFollowing.TSMOM_Moskowitz import TSMOM_Moskowitz; s = TSMOM_Moskowitz(); print('OK')"

# Test suite
python -m pytest quantconnect/Tests/ -v
```

### Final Checklist
- [ ] All 24 strategies implemented
- [ ] All strategies pass smoke tests
- [ ] Infrastructure utilities complete
- [ ] Documentation complete
- [ ] Tests passing
- [ ] Regression tests run

---

## Strategy Index

| # | ID | Strategy | Category | Complexity | Reference |
|---|----|----------|----------|------------|-----------|
| 1 | S01 | TSMOM Moskowitz 2012 | TrendFollowing | Medium | JFE 2012 |
| 2 | S02 | TSMOM Baltas 2020 | TrendFollowing | High | Wiley 2020 |
| 3 | S03 | Trend Breakout | TrendFollowing | Medium | Managerial Finance 2014 |
| 4 | S04 | Chinese Futures | TrendFollowing | Medium | JFM 2017 |
| 5 | S05 | Commodity Carry | Commodity | Medium | JFE 2018 |
| 6 | S06 | Commodity Momentum | Commodity | Medium | JF 2013 |
| 7 | S07 | Commodity Skewness | Commodity | Medium | JBF 2018 |
| 8 | S08 | Commodity Intra-Curve | Commodity | High | La Française 2015 |
| 9 | S09 | Basis Momentum | Commodity | High | JF 2019 |
| 10 | S10 | Basis Reversal | Commodity | High | SSRN 2025 |
| 11 | S11 | Soybean Crush | SpreadTrading | High | JFM 1999 |
| 12 | S12 | Petroleum Crack | SpreadTrading | High | JFM 1999 |
| 13 | S13 | Connors RSI-2 | Equity | Low | Connors 2009 |
| 14 | S14 | ETF Intraday | Equity | Medium | JFE 2018 |
| 15 | S15 | Overnight Returns | Equity | Low | arXiv 2020 |
| 16 | S16 | FX Carry | FX_CrossAsset | Medium | Deutsche Bank 2009 |
| 17 | S17 | Cross-Asset Skew | FX_CrossAsset | High | SSRN 2019 |
| 18 | S18 | Long-Only Futures | Additional | Low | - |
| 19 | S19 | Active Contracts | Additional | Low | - |
| 20 | S20 | Realized Vol | Additional | Medium | Santander 2012 |
| 21 | S21 | Greeks Normal | Additional | Medium | - |
| 22 | S22 | Inverse Options | Additional | High | arXiv 2021 |
| 23 | S23 | Uniswap V2 | Additional | High | - |
| 24 | S24 | Virtue of Complexity | Additional | Very High | SSRN 2022 |

---

*Generated: 2026-03-01*
*Planner: Prometheus*
*Project: QuantConnect LEAN Implementation*

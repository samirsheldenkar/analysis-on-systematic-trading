# Draft: QuantConnect LEAN Implementation Plans

## Analysis Summary

**Total Strategies Identified: 24**

### Category 1: Trend Following Strategies (4)

| # | Strategy | Reference | Key Components |
|---|----------|-----------|----------------|
| 1 | Time-Series Momentum (Moskowitz 2012) | JFE 2012 | 12-month lookback, volatility scaling, 58 futures |
| 2 | Time-Series Momentum Enhanced (Baltas 2020) | Wiley 2020 | YZ volatility, correlation adjustment, turnover reduction |
| 3 | Trend Following with Breakout Signal | Managerial Finance 2014 | Breakout entry, trailing exit, binary signals |
| 4 | Trend Following in Chinese Futures | JFM 2017 | 29 Chinese futures, multiple lookbacks |

### Category 2: Commodity Strategies (6)

| # | Strategy | Reference | Key Components |
|---|----------|-----------|----------------|
| 5 | Commodity Term Structure/Carry | JFE 2018 | Backwardation/contango, tercile selection |
| 6 | Commodity Momentum | JF 2013 | Cross-sectional ranking, monthly rebalancing |
| 7 | Commodity Skewness | JBF 2018 | 252-day skewness, long negative, short positive |
| 8 | Commodity Intra-Curve | La Française 2015 | F3 vs F0 spread, two-leg construction |
| 9 | Commodity Basis Momentum | JF 2019 | Front vs next month momentum, top/bottom 4 |
| 10 | Commodity Basis Reversal | SSRN 2025 | Weekly basis reversal, spread variant |

### Category 3: Spread Trading (2)

| # | Strategy | Reference | Key Components |
|---|----------|-----------|----------------|
| 11 | Soybean Crush Spread | JFM 1999 | Mean reversion, 5-day MA, seasonal patterns |
| 12 | Petroleum Crack Spread | JFM 1999 | Cointegration, 3:2:1 ratio, unit conversions |

### Category 4: Equity Strategies (3)

| # | Strategy | Reference | Key Components |
|---|----------|-----------|----------------|
| 13 | Short-Term Trading (Connors RSI-2) | Connors 2009 | RSI-2 ≤25 entry, 200-day MA filter |
| 14 | ETF Intraday Momentum | JFE 2018 | First/last 30-min predictability |
| 15 | Overnight Returns | arXiv 2020 | Overnight vs intraday decomposition |

### Category 5: FX & Cross-Asset (2)

| # | Strategy | Reference | Key Components |
|---|----------|-----------|----------------|
| 16 | FX Carry Trade | Deutsche Bank 2009 | Interest rate differentials, 6 currencies |
| 17 | Cross-Asset Skewness | SSRN 2019 | 4 asset classes, equal-risk leverage |

### Category 6: Additional Strategies (7)

| # | Strategy | Reference | Key Components |
|---|----------|-----------|----------------|
| 18 | Long-Only Futures Performance | - | Buy-and-hold, roll analysis |
| 19 | Actively Traded Contract Months | - | Volume analysis, contract selection |
| 20 | Realised Volatility Measures | Santander 2012 | Yang-Zhang, EWMA, Parkinson |
| 21 | Greeks Under Normal Model | - | Bachelier vs Black-Scholes |
| 22 | Inverse Options | arXiv 2021 | Crypto applications, inverse payoff |
| 23 | Uniswap V2 Liquidity Pool | - | AMM mechanics, impermanent loss |
| 24 | The Virtue of Complexity | SSRN 2022 | ML/ridge regression, overparameterization |

## Implementation Requirements

### Per-Strategy Folder Structure
```
quantconnect/
├── 01_tsmom_moskowitz2012/
│   ├── main.py
│   ├── config.json
│   ├── README.md
│   └── tests/
├── 02_tsmom_baltas2020/
│   ├── ...
... (24 total folders)
```

### Common Components Needed
1. **Data Handler**: Futures contract management, rolling
2. **Signal Generator**: Technical indicators, statistical measures
3. **Portfolio Constructor**: Equal-weight, volatility-scaled, tercile-based
4. **Risk Manager**: Position sizing, drawdown limits
5. **Backtest Runner**: LEAN integration

### Key Technical Requirements
- LEAN's QCAlgorithm base class
- Futures data subscription
- Contract rolling logic
- Volatility estimation (EWMA, Yang-Zhang)
- Cross-sectional ranking
- Monthly rebalancing
- Performance metrics calculation

### Data Requirements
- Futures price data (daily)
- Multiple asset classes (equity, bond, FX, commodity)
- Contract specifications
- Volume data for liquidity screening

## Next Steps
1. Wait for Oracle consultation on architecture
2. Wait for Librarian research on LEAN patterns
3. Create individual implementation plans for each strategy
4. Prioritize based on complexity and dependencies



## Architectural Recommendations (From Oracle Consultation)

### Recommended Structure
```
quantconnect/
├── Common/                           # Shared utilities
│   ├── BaseStrategyAlgorithm.py     # Abstract base class
│   ├── RiskManager.py               # Position sizing, drawdown limits
│   ├── VolatilityCalculator.py      # EWMA, Yang-Zhang, Rolling
│   ├── DataProvider.py              # Futures data handling
│   └── PortfolioConstructor.py      # Equal-weight, tercile, etc.
│
├── Strategies/                       # Categorized strategy folders
│   ├── TrendFollowing/              # 01-04
│   ├── Commodity/                   # 05-10
│   ├── SpreadTrading/               # 11-12
│   ├── Equity/                      # 13-15
│   ├── FX_CrossAsset/               # 16-17
│   └── Additional/                  # 18-24
│
└── Tests/                           # Strategy validation tests
    ├── unit/
    ├── regression/
    └── smoke/
```

### Key Architecture Decisions
1. **Base Class Pattern**: `BaseStrategyAlgorithm(QCAlgorithm)` with abstract methods
   - `GenerateSignals()` - Strategy-specific signal logic
   - `GetUniverse()` - Asset universe selection
   - Concrete implementations for common operations

2. **Shared Infrastructure**: Common utilities folder
   - Volatility calculations (EWMA, Yang-Zhang)
   - Position sizing (volatility-scaled, equal-weight)
   - Rebalancing scheduler (monthly default)
   - Futures contract rolling logic

3. **Strategy Independence**: Each strategy folder contains:
   - Strategy class inheriting from base
   - config.json with parameters
   - README.md with documentation
   - tests/ folder with validation

4. **LEAN Futures Implementation**:
   - Use `AddFuture()` with `FutureFilter`
   - Handle continuous contracts via `Mapped` property
   - Manage rollovers in base class
   - Volume-based contract selection

### Implementation Approach
- **Code Duplication Reduction**: ~60% via base class and shared utilities
- **Maintainability**: Categorized folder structure
- **Testability**: Separate test suite with regression tests
- **Scalability**: Easy to add new strategies following the pattern

### Estimated Effort
- **Total**: Large (3+ days)
- **Per Strategy**: 2-4 hours (simpler) to 6-8 hours (complex)
- **Infrastructure**: 1 day for base classes and utilities
- **Testing**: Parallel with implementation

### Risk Considerations
- Futures rollover timing varies by asset class
- Volatility lookback periods differ across strategies
- Strategy parameter conflicts in multi-strategy backtests
- Spread strategies need multi-leg position support



## Plan Files Created

### Master Plan
- `.sisyphus/plans/quantconnect-master-plan.md` - Overall project structure and workflow

### Detailed Strategy Plans
- `.sisyphus/plans/strategy-01-tsmom-moskowitz.md` - Time-Series Momentum (Moskowitz 2012)
- `.sisyphus/plans/strategy-02-tsmom-baltas.md` - Time-Series Momentum Enhanced (Baltas 2020)
- `.sisyphus/plans/strategy-05-commodity-carry.md` - Commodity Term Structure / Carry

### Strategy Index
- `.sisyphus/plans/STRATEGY_IMPLEMENTATION_INDEX.md` - Complete index of all 24 strategies

## Summary

**Total Strategies Analyzed**: 24
**Categories**: 6 (TrendFollowing, Commodity, SpreadTrading, Equity, FX_CrossAsset, Additional)
**Detailed Plans Created**: 3 (S01, S02, S05)
**Index Created**: 1 (covers all 24 with summaries)

### Implementation Priority
- **P0 (Start First)**: S01, S02, S05, S06 - Core strategies with high Sharpe ratios
- **P1 (Next)**: S03, S04, S07, S09, S16 - Important variations
- **P2 (Later)**: S08, S10, S11, S12, S14 - Specialized/higher complexity
- **P3 (Final)**: S13, S15, S17, S18-S24 - Analysis tools

### Key Technical Patterns Identified
1. **Base Class Architecture**: Inherit from QCAlgorithm, abstract methods for signals
2. **Shared Utilities**: VolatilityCalculator, PortfolioConstructor, RiskManager
3. **LEAN Integration**: Futures data, continuous contracts, monthly rebalancing
4. **Testing Framework**: Smoke tests, regression tests, unit tests

### Next Actions
1. Run `/start-work` to begin implementation
2. Start with Wave 1 (infrastructure: BaseStrategyAlgorithm, utilities)
3. Then implement P0 strategies in parallel
4. Create detailed plans for remaining strategies as needed during implementation

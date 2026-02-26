# Trend Following Strategies Documentation

## Table of Contents

1. [Time-Series Momentum (Moskowitz 2012)](#1-time-series-momentum-moskowitz-2012)
2. [Time-Series Momentum Enhanced (Baltas 2020)](#2-time-series-momentum-enhanced-baltas-2020)
3. [Trend Following with Breakout Signal](#3-trend-following-with-breakout-signal)
4. [Trend Following in Chinese Futures](#4-trend-following-in-chinese-futures)

---

## 1. Time-Series Momentum (Moskowitz 2012)

**Notebook:** `trend_following_moskowitz2012.ipynb`

**Reference:** Moskowitz, T.J., Ooi, Y.H. and Pedersen, L.H., 2012. "Time series momentum." Journal of Financial Economics, 104(2), pp.228-250.

### Strategy Overview

Time-series momentum (TSM) exploits the persistence of returns at the 1-12 month horizon. The strategy goes long assets with positive past returns and short assets with negative past returns, scaled by volatility to target constant risk exposure.

### Core Concept

- **Signal**: Past 12-month excess return predicts future return direction
- **Position Sizing**: Volatility-scaled positions targeting constant volatility
- **Portfolio**: Equal-weighted across all assets and asset classes

### Mathematical Formulation

**Signal Generation:**
```
sign(r_i,t-12m) = sign(Excess Return_i)
```

**Position Sizing:**
```
w_i,t = σ_target / σ_i,t × sign(r_i,t-12m)
```

Where:
- `w_i,t` = weight for asset i at time t
- `σ_target` = target volatility (40% annualized in implementation)
- `σ_i,t` = realized volatility of asset i (estimated via EWMA)
- `r_i,t-12m` = past 12-month return

**Scaled Returns:**
```
r_scaled_i,t = r_i,t × w_i,t
```

### Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Lookback Period | 12 months | Formation period for momentum signal |
| Holding Period | 1 month | Rebalancing frequency |
| Target Volatility | 40% | Annualized volatility target per instrument |
| Volatility Window | 21 days | Rolling volatility estimation |
| Signal Cap | 0.95 | Maximum position size limit |

### Asset Universe

- **Equity Index Futures**: 24 instruments (S&P 500, Nasdaq, Dow, Russell, etc.)
- **Currency Futures**: 9 instruments (EUR, JPY, GBP, CHF, etc.)
- **Commodity Futures**: 17 instruments (energy, metals, agriculture)
- **Bond Futures**: 8 instruments (US Treasuries, Euro Bund, etc.)
- **Total**: 58 liquid futures contracts

### Performance Characteristics

| Metric | Value |
|----------|-------|
| Sharpe Ratio | ~0.70-0.80 |
| Annualized Return | ~15-20% gross |
| Transaction Costs | Significant but positive alpha remains |
| Crisis Performance | Strongest during market crises |

### Key Findings from Paper

1. TSMOM exists across all major asset classes and is statistically significant
2. Returns show persistence for 1-12 months with partial reversal over longer horizons
3. Consistent with behavioral theories: initial under-reaction followed by delayed over-reaction
4. Diversified TSM portfolio delivers substantial abnormal returns with little exposure to standard factors
5. Performs best during extreme market conditions (crises)
6. Speculators appear to profit at the expense of hedgers

### Implementation Notes

- Uses the `vivace` proprietary library for backtesting
- Signals aggregated monthly via `post_process=AsFreq(freq='m', method='pad')`
- Volatility estimated using EWMA with 21-day window
- Equal weighting across asset classes
- Performance strongest during extreme market conditions
- Provides hedging value during crises

---

## 2. Time-Series Momentum Enhanced (Baltas 2020)

**Notebook:** `trend_following_baltas2020.ipynb`

**Reference:** Baltas, N. and Kosowski, R., 2020. "Demystifying time-series momentum strategies: Volatility estimators, trading rules and pairwise correlations." Market Momentum: Theory and Practice, Wiley.

### Strategy Overview

Baltas and Kosowski (2020) extends Moskowitz (2012) by exploring alternative volatility estimators, trading rules, and the impact of pairwise correlations on portfolio construction.

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

### Performance Characteristics

- **Turnover Reduction**: >30% reduction without performance degradation
- **Sharpe Improvement**: Enhanced Sharpe ratios through better volatility estimation
- **Post-2008 Performance**: Outperformance more pronounced in recent period
- **Correlation Impact**: Product weighting reduces correlation-induced position inflation

### Implementation Notes

- Uses `VolatilityScale` signal with multiple estimator options
- `TSMOMBaltas2020` signal for momentum component
- `post_process=AsFreq(freq='m', method='pad')` for monthly alignment
- Comparison between rolling (21-day) and Yang-Zhang estimators
- Product weighting (`'product'`) vs equal weighting analysis

---

## 3. Trend Following with Breakout Signal

**Notebook:** `trend_following_breakout.ipynb`

**Reference:** Chevallier, J. and Ielpo, F., 2014. "'Time series momentum' in commodity markets." Managerial Finance.

### Strategy Overview

Breakout-based trend signal that enters long when price breaks above local maximum over a lookback horizon, maintaining position until price breaches trailing minimum threshold.

### Core Concept

- **Entry**: Price breaks above 1-year local maximum
- **Exit**: Price breaches trailing minimum threshold
- **Signal Type**: Binary (long/short only, no neutral)
- **Comparison**: Alternative mechanism to pure TSMOM

### Mathematical Formulation

**Breakout Signal:**
```
s_t^breakout = +1 if Price_t > max(Price_{t-L}, …, Price_{t-1})
               -1 if Price_t < trailing_min_t
```

Where:
- `L` = lookback period (252 trading days ≈ 1 year)
- `trailing_min_t` = trailing minimum threshold

**Combined Position:**
```
position_i,t = s_t^breakout × scaling_i,t
```

Where `scaling_i,t` is volatility-based position sizing.

### Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Breakout Lookback | 252 days | Local maximum lookback period |
| Volatility Method | EWM or Rolling | EWMA (com=60) or rolling (21-day) |
| Target Volatility | 40% | Annualized volatility target |
| Weighting | Product | Cross-signal combination |

### Asset Universe

- 50 futures universe (same as Moskowitz 2012)
- Equities, bonds, FX, commodities

### Performance Characteristics

- Different drawdown profile vs. standard TSMOM
- Binary signal produces different risk characteristics
- Comparable Sharpe ratios with distinct timing of returns

### Implementation Notes

- `BreakoutLocalExtreme` signal class
- Combined with `VolatilityScale` for risk management
- Product weighting with TSMOM signal
- Monthly post-processing alignment
- Direct comparison with Moskowitz 2012 baseline

---

## 4. Trend Following in Chinese Futures

**Notebook:** `commodity_trend_following_chinese_futures.ipynb`

**Reference:** Li, B., Zhang, D. and Zhou, Y., 2017. "Do trend following strategies work in Chinese futures markets?" Journal of Futures Markets, 37(12), pp.1226-1254.

### Strategy Overview

Tests trend following strategies on Chinese commodity futures markets, accounting for specific market structure and regulatory environment.

### Key Findings from Paper

- Trend following **outperforms buy-and-hold** on both individual contracts and portfolios
- Outperformance is **robust** to transaction costs, data frequency, subprime crisis, shorting constraints, delayed execution, liquidity, and parameter variations
- **Data snooping warning**: Profitability may be subject to data snooping bias

### Implementation Considerations

- **Market Structure**: Trading hours, contract specifications, regulatory environment
- **Transaction Costs**: Higher costs in Chinese markets
- **Shorting Constraints**: Limited short selling capabilities
- **Out-of-Sample Testing**: Critical to avoid data snooping

### Asset Universe

- 29 Chinese futures contracts
- Commodities: metals, agriculture, energy
- Financial futures: bonds, equity indices

### Performance Characteristics

- Positive risk-adjusted returns
- Robust across multiple lookback periods
- Higher transaction costs impact net returns

### Implementation Notes

- Volatility targeting (40% annualized)
- Multiple lookback periods tested (50, 100, 200 days)
- Walk-forward validation recommended
- Account for evening trading sessions
- Consider margin requirement differences

---

## Academic Paper Summary

### Moskowitz, Ooi, Pedersen (2012) - "Time Series Momentum"

**Key Findings:**
- Significant time series momentum across 58 futures instruments
- Returns persist for 1-12 months, reverse over longer horizons
- Sharpe ratio ~0.70-0.80
- Strongest performance during market crises
- Little exposure to standard risk factors

**Methodology:**
- 12-month lookback, 1-month holding
- Volatility scaling to 40% target
- Equal-weighted across assets

**Asset Classes:**
- 24 equity indices, 9 currencies, 17 commodities, 8 bonds

---

### Baltas and Kosowski (2020) - "Demystifying Time-Series Momentum"

**Key Findings:**
- Alternative volatility estimators (YZ) reduce turnover >30%
- Pairwise correlations affect diversification
- Dynamic leverage improves performance
- Post-2008 outperformance

**Methodology:**
- Compare EWMA, YZ, rolling volatility
- Product vs equal weighting
- Correlation-adjusted position sizing

---

### Chevallier and Ielpo (2014) - "Time Series Momentum in Commodities"

**Key Methodology:**
- Markov-switching models for regime identification
- Daily frequency data covering 1995-2012
- Extended TSMOM to commodity markets

**Key Findings:**
- Commodities exhibit different characteristics than standard assets
- Distinct regime-switching properties compared to equities
- Understanding regimes crucial for effective trend-following

---

### Zhang and Zhou (2017) - "Trend Following in Chinese Futures"

**Key Findings:**
- Trend following outperforms buy-and-hold in Chinese futures markets
- Robust to transaction costs, data frequency, subprime crisis
- Robust to shorting constraints, delayed execution, liquidity
- Data snooping warning: profitability may be subject to bias

**Implementation:**
- 29 Chinese futures contracts
- Multiple lookback periods (50, 100, 200 days)
- Out-of-sample testing critical
- Account for evening sessions and margin requirements

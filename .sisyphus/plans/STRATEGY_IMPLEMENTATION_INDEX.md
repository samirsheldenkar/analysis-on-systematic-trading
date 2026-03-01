# QuantConnect LEAN Strategy Implementation Index

## Overview

This index provides a quick reference for all 24 systematic trading strategies to be implemented in QuantConnect LEAN framework.

**Status**: Planning Complete  
**Total Strategies**: 24  
**Categories**: 6  
**Estimated Total Effort**: 3+ days  

---

## Strategy Quick Reference Table

| # | ID | Strategy Name | Category | Complexity | Key Signal | Sizing | Sharpe |
|---|----|---------------|----------|------------|------------|--------|--------|
| 1 | S01 | TSMOM Moskowitz 2012 | TrendFollowing | Medium | 12m return sign | Vol-scaled (40%) | 0.75 |
| 2 | S02 | TSMOM Baltas 2020 | TrendFollowing | High | 12m return sign | YZ vol + correlation | 0.80 |
| 3 | S03 | Trend Breakout | TrendFollowing | Medium | Breakout above local max | Vol-scaled | - |
| 4 | S04 | Chinese Futures | TrendFollowing | Medium | Multiple lookbacks | Vol-scaled (40%) | - |
| 5 | S05 | Commodity Carry | Commodity | Medium | Term structure slope | Tercile (33%) | 0.495-0.640 |
| 6 | S06 | Commodity Momentum | Commodity | Medium | 12m return rank | Equal-weight | 0.611 |
| 7 | S07 | Commodity Skewness | Commodity | Medium | 252d skewness | Long negative | 0.026 |
| 8 | S08 | Intra-Curve | Commodity | High | F3-F0 spread | Equal-weight | -0.117 |
| 9 | S09 | Basis Momentum | Commodity | High | Front vs next momentum | Equal-dollar | 0.439 |
| 10 | S10 | Basis Reversal | Commodity | High | Weekly basis reversal | Equal-weight | 0.351-0.646 |
| 11 | S11 | Soybean Crush | SpreadTrading | High | Mean reversion | Z-score | - |
| 12 | S12 | Petroleum Crack | SpreadTrading | High | Cointegration | Z-score | - |
| 13 | S13 | Connors RSI-2 | Equity | Low | RSI ≤ 25 | Fixed size | - |
| 14 | S14 | ETF Intraday | Equity | Medium | First/last 30min | Equal-weight | - |
| 15 | S15 | Overnight Returns | Equity | Low | Overnight vs intraday | Analysis | - |
| 16 | S16 | FX Carry | FX_CrossAsset | Medium | Interest rate diff | Tercile (33%) | 0.304 |
| 17 | S17 | Cross-Asset Skew | FX_CrossAsset | High | 4-asset skewness | Equal-risk | 0.72 |
| 18 | S18 | Long-Only Futures | Additional | Low | Buy-and-hold | Equal-weight | - |
| 19 | S19 | Active Contracts | Additional | Low | Volume-based | - | - |
| 20 | S20 | Realized Volatility | Additional | Medium | YZ, EWMA measures | - | - |
| 21 | S21 | Greeks Normal | Additional | Medium | Bachelier model | - | - |
| 22 | S22 | Inverse Options | Additional | High | Inverse payoff | - | - |
| 23 | S23 | Uniswap V2 | Additional | High | AMM mechanics | - | - |
| 24 | S24 | Virtue of Complexity | Additional | Very High | ML/ridge regression | - | - |

---

## Detailed Strategy Specifications

### Category 1: Trend Following Strategies (S01-S04)

#### S01: Time-Series Momentum (Moskowitz 2012) ✓
**Status**: Detailed plan created → `strategy-01-tsmom-moskowitz.md`

**Core Logic**:
- Signal: sign(12-month return)
- Sizing: target_vol / instrument_vol × signal
- Universe: 58 futures (24 equity, 9 FX, 17 commodity, 8 bonds)
- Rebalancing: Monthly

**Key Parameters**:
```python
lookback_days = 252
volatility_window = 21
target_volatility = 0.40
signal_cap = 0.95
```

**LEAN Implementation**:
```python
class TSMOM_Moskowitz2012(BaseStrategyAlgorithm):
    def GenerateSignals(self):
        for symbol in self.universe:
            history = self.History(symbol, 252)
            past_return = history['close'].iloc[-1] / history['close'].iloc[0] - 1
            signals[symbol] = np.sign(past_return)
```

**Expected Performance**: Sharpe ~0.75, CAGR 15-20%

---

#### S02: Time-Series Momentum Enhanced (Baltas 2020) ✓
**Status**: Detailed plan created → `strategy-02-tsmom-baltas.md`

**Enhancements over S01**:
- Yang-Zhang volatility estimator
- Correlation-adjusted weights
- Multiple volatility methods

**Key Parameters**:
```python
volatility_type = 'YangZhang'  # or 'EWMA', 'Rolling'
volatility_window = 21
correlation_window = 63
use_correlation_adjustment = True
```

**Yang-Zhang Formula**:
```
σ_YZ = √(σ_O² + 0.34×σ_C² + 0.66×σ_RS²)
```

**Correlation Adjustment**:
```
w_i* = target_vol / (Σ_j |correlation_ij| × vol_j)
```

**Expected Performance**: Sharpe ~0.80, 30%+ turnover reduction

---

#### S03: Trend Following with Breakout Signal
**Status**: Plan summary below (detailed plan on demand)

**Core Logic**:
- Entry: Price breaks above 1-year local maximum
- Exit: Price breaches trailing minimum threshold
- Signal: Binary (long/short only, no neutral)

**Key Parameters**:
```python
breakout_lookback = 252  # days
volatility_method = 'EWM'  # or 'Rolling'
target_volatility = 0.40
weighting = 'Product'
```

**Signal Formula**:
```
s_t = +1 if Price_t > max(Price_{t-252}, ..., Price_{t-1})
      -1 if Price_t < trailing_min_t
```

**Reference**: Chevallier & Ielpo (2014), Managerial Finance

---

#### S04: Trend Following in Chinese Futures
**Status**: Plan summary below (detailed plan on demand)

**Core Logic**:
- Multiple lookback periods (50, 100, 200 days)
- Tests on 29 Chinese futures contracts
- Accounts for market-specific characteristics

**Key Parameters**:
```python
lookback_periods = [50, 100, 200]
target_volatility = 0.40
rebalancing = 'monthly'
```

**Special Considerations**:
- Higher transaction costs in Chinese markets
- Shorting constraints
- Evening trading sessions
- Margin requirement differences

**Reference**: Li, Zhang & Zhou (2017), Journal of Futures Markets

---

### Category 2: Commodity Strategies (S05-S10)

#### S05: Commodity Term Structure / Carry ✓
**Status**: Detailed plan created → `strategy-05-commodity-carry.md`

**Core Logic**:
- Signal: log(F1/F2) × annualization_factor
- Long backwardation, short contango
- Tercile-based selection

**Key Parameters**:
```python
expiry_shift = 1
sma_window = 252
annualization_factor = 4
selection = 'terciles'  # top/bottom 33%
```

**Formula**:
```
Carry = log(Front_Price / Second_Price) × 4
```

**Expected Performance**:
- With smoothing: CAGR 5.69%, Sharpe 0.495
- Without smoothing: CAGR 10.4%, Sharpe 0.640

**Reference**: Koijen et al. (2018), Journal of Financial Economics

---

#### S06: Commodity Momentum
**Status**: Plan summary below (detailed plan on demand)

**Core Logic**:
- Cross-sectional momentum ranking
- Long top performers, short bottom performers
- 1-year lookback

**Key Parameters**:
```python
lookback = 252  # days
rebalancing = 'monthly'
strategy = 'DELTA_ONE'
```

**Signal**:
```
R_i = P_t / P_{t-252} - 1
Rank across commodities
Long top, short bottom
```

**Expected Performance**: CAGR 11.1%, Sharpe 0.611, Max DD 56.2%

**Reference**: Asness, Moskowitz & Pedersen (2013), The Journal of Finance

---

#### S07: Commodity Skewness
**Status**: Plan summary below (detailed plan on demand)

**Core Logic**:
- Calculate 252-day return skewness
- Long most negative skewness, short most positive
- Negate signal for proper alignment

**Key Parameters**:
```python
lookback = 252  # days
rebalancing = 'monthly'
```

**Signal**:
```
Skew_i = skewness(R_i over 252 days)
Signal = -Skew_i
```

**Expected Performance**: CAGR 0.4%, Sharpe 0.026, Max DD 91.9%
**Note**: Weak standalone performance, stronger in combination

**Reference**: Fernandez-Perez et al. (2018), Journal of Banking & Finance

---

#### S08: Commodity Intra-Curve
**Status**: Plan summary below (detailed plan on demand)

**Core Logic**:
- Intra-curve carry strategy
- Long 3-month forward, short front contract
- Two-leg construction per commodity

**Key Parameters**:
```python
forward_leg = 'F3'  # 3-month forward
front_leg = 'F0'    # Near contract
roll_schedule = 'FIFTH_BIZ_DAY'
roll_period = 5
```

**Spread Formula**:
```
S_i,t = F3_i,t - F0_i,t
```

**Expected Performance**: CAGR -0.3%, Sharpe -0.117
**Note**: Shows weak standalone performance, requires refinement

**Reference**: La Française Group (2015)

---

#### S09: Commodity Basis Momentum
**Status**: Plan summary below (detailed plan on demand)

**Core Logic**:
- Momentum in basis (front vs next contract)
- 12-month rolling window
- Long top 4, short bottom 4

**Key Parameters**:
```python
window = 11  # months
roll_schedule = 21  # days prior to expiry
selection = 'top_bottom_4'
weighting = 'equal_dollar'
```

**Signal Formula**:
```
BM_t = ∏_{s=t-11}^{t}(1 + R1_s) - ∏_{s=t-11}^{t}(1 + R2_s)
```

**Expected Performance**:
- Spread variant: CAGR 3.14%, Sharpe 0.439
- Outright variant: Sharpe 0.065

**Reference**: Boons & Prado (2019), The Journal of Finance

---

#### S10: Commodity Basis Reversal
**Status**: Plan summary below (detailed plan on demand)

**Core Logic**:
- Short-term basis reversal
- Weekly observation schedule
- Cross-sectional and time-series variants

**Key Parameters**:
```python
roll_schedule = 21  # days
rebalancing = 'monthly'  # or 'weekly'
weighting = 'equal_weight'
```

**Variants**:
1. Cross-sectional outright
2. Time-series spread

**Expected Performance**:
- Cross-sectional: CAGR 6.7%, Sharpe 0.351
- Spread: Sharpe 0.646

**Reference**: Rossi, Zhang & Zhu (2025), SSRN 5250499

---

### Category 3: Spread Trading (S11-S12)

#### S11: Soybean Crush Spread
**Status**: Plan summary below (detailed plan on demand)

**Core Logic**:
- Mean-reversion to 5-day moving average
- Exploit processing margin deviations
- Seasonal patterns

**Key Parameters**:
```python
analysis_period = '1985-1995'
mean_reversion = '5_day_MA'
r_squared = 0.975
```

**Crush Spread Formula**:
```
Crush = (Meal_Price × 2.2) + (Oil_Price × 11) - Soybean_Price
```

**Trading Rules**:
- Enter long crush when spread < 5-day MA (cheap)
- Enter short crush when spread > 5-day MA (expensive)
- Exit when spread reverts

**Assets**: Soybeans (S), Soybean Meal (SM), Soybean Oil (BO)

**Reference**: Simon (1999), Journal of Futures Markets

---

#### S12: Petroleum Crack Spread
**Status**: Plan summary below (detailed plan on demand)

**Core Logic**:
- Cointegration-based statistical arbitrage
- 3:2:1 crack spread
- Unit conversion critical (barrels to gallons)

**Key Parameters**:
```python
unit_conversion = 42  # gallons per barrel
ratios = ['3:2:1', '1:1:0', '1:0:1']
method = 'cointegration'
```

**Crack Spread Formula (3:2:1)**:
```
CS = (2/3 × HO × 42) + (1/3 × RB × 42) - CL
```

**Trading Rules**:
- Enter long spread when residual > threshold
- Enter short spread when residual < threshold
- Exit when residual reverts

**Assets**: Crude Oil (CL), RBOB Gasoline (RB), Heating Oil (HO)

**Reference**: Girma & Paulson (1999), Journal of Futures Markets

---

### Category 4: Equity Strategies (S13-S15)

#### S13: Short-Term Trading (Connors RSI-2)
**Status**: Plan summary below (detailed plan on demand)

**Core Logic**:
- Mean-reversion using 2-period RSI
- Trend filter (200-day MA)
- Fixed 5-day holding period

**Key Parameters**:
```python
rsi_period = 2
buy_threshold = 25
sell_threshold = 75
trend_filter = '200_day_MA'
hold_period = 5
```

**Rules**:
- Buy when RSI ≤ 25 and price > 200 MA
- Sell when RSI ≥ 75
- Hold for 5 days
- Do not use stop losses

**Strategies**:
1. 3-day down + above 200 MA
2. New 10-day low + above 200 MA
3. Double 7 Connors
4. Month-end seasonal

**Reference**: Connors & Alvarez (2009)

---

#### S14: ETF Intraday Momentum
**Status**: Plan summary below (detailed plan on demand)

**Core Logic**:
- First 30-min return predicts last 30-min return
- High-frequency data required

**Key Parameters**:
```python
first_period = '9:30-10:00'
last_period = '15:30-16:00'
data_window = '9:30-16:00'
```

**Returns**:
```
r1 = Return from previous close to first 30 minutes
r12 = Return from 60min to 30min before close
r13 = Return from 30min before close to close
```

**Trading**:
- Long last half-hour if first half-hour positive
- Short last half-hour if first half-hour negative

**Assets**: SPY, ^IXIC, XIU.TO, ^FCHI, 10 ETFs

**Reference**: Gao et al. (2018), Journal of Financial Economics

---

#### S15: Overnight Returns
**Status**: Plan summary below (detailed plan on demand)

**Core Logic**:
- Decompose returns into overnight vs intraday
- Analysis of striking patterns

**Key Parameters**:
```python
markets = 21  # global indices
```

**Return Decomposition**:
```
r_overnight = (AdjClose_t / AdjClose_{t-1}) / (Close_t / Open_t) - 1
r_intraday = Close_t / Open_t - 1
```

**Key Findings**:
- Overnight returns: +1,062% (Canada TSX 60)
- Intraday returns: -67% (Canada TSX 60)
- Pattern universal except China

**Reference**: Knuteson (2020), arXiv 2010.01727

---

### Category 5: FX & Cross-Asset (S16-S17)

#### S16: FX Carry Trade
**Status**: Plan summary below (detailed plan on demand)

**Core Logic**:
- Long high interest rate currencies
- Short low interest rate currencies
- Exploit forward rate bias

**Key Parameters**:
```python
universe = ['EUR', 'JPY', 'GBP', 'CAD', 'AUD', 'NZD']
selection = 'top_bottom_33%'
rebalancing = 'monthly'
annualization = 4
```

**Carry Formula**:
```
Carry = log(F1 / F2) × 4 ≈ i_domestic - i_foreign
```

**Portfolio Construction**:
- Rank 6 currencies by carry
- Long top 33% (2 instruments)
- Short bottom 33% (2 instruments)

**Expected Performance**: CAGR 3.35%, Sharpe 0.304, Max DD 46.6%

**Reference**: Deutsche Bank (2009), Koijen et al. (2018)

---

#### S17: Cross-Asset Skewness
**Status**: Plan summary below (detailed plan on demand)

**Core Logic**:
- Long negative skewness, short positive across 4 asset classes
- Equal-risk leverage
- Global Skewness Factor

**Key Parameters**:
```python
asset_classes = ['commodity', 'equity', 'bonds', 'fx']
leverage = 'equal_risk'
combination = 'mean'
```

**Formula**:
```
GSF = mean(levered_daily_returns across four portfolios)
```

**Expected Performance**:
- Within class: Sharpe 0.35
- Cross-asset: Sharpe 0.72

**Reference**: Baltas & Salinas (2019), SSRN 3505422

---

### Category 6: Additional Strategies (S18-S24)

#### S18: Long-Only Futures Performance
**Status**: Plan summary below (detailed plan on demand)

**Core Logic**:
- Buy-and-hold futures performance
- Roll yield analysis
- Asset class comparison

**Key Parameters**:
```python
strategy = 'buy_and_hold'
roll_methodology = 'front_month'
```

**Analysis**:
- Long-only returns by asset class
- Roll cost/benefit
- Performance attribution

---

#### S19: Actively Traded Contract Months
**Status**: Plan summary below (detailed plan on demand)

**Core Logic**:
- Volume by contract month analysis
- Optimal roll schedules
- Liquidity management

**Key Parameters**:
```python
selection = 'volume_based'
roll_timing = 'optimal'
```

---

#### S20: Realized Volatility Measures
**Status**: Plan summary below (detailed plan on demand)

**Core Logic**:
- Multiple volatility calculation methods
- Yang-Zhang, EWMA, Parkinson, Garman-Klass

**Key Parameters**:
```python
methods = ['YangZhang', 'EWMA', 'Rolling', 'Parkinson', 'GarmanKlass']
window = 21
```

**Formulas**:
```
YZ = √(σ_O² + 0.34×σ_C² + 0.66×σ_RS²)
EWMA: σ²_t = (1-λ)×σ²_{t-1} + λ×r_t²
Parkinson: σ² = (ln(H/L))² / (4×ln(2))
```

**Reference**: Santander (2012)

---

#### S21: Greeks Under Normal Model
**Status**: Plan summary below (detailed plan on demand)

**Core Logic**:
- Greeks calculation under Bachelier (Normal) model
- Forward-based calculations

**Key Parameters**:
```python
model = 'Bachelier'  # vs 'BlackScholes'
```

**Formulas**:
```
Call: C = (F - K)×N(d) + σ×√T×n(d)
d = (F - K) / (σ×√T)
Delta: Δ = N(d)
Gamma: Γ = n(d) / (σ×√T)
Vega: ν = √T × n(d)
```

---

#### S22: Inverse Options
**Status**: Plan summary below (detailed plan on demand)

**Core Logic**:
- Inverse option payoff analysis
- Crypto/DeFi applications

**Key Parameters**:
```python
payoff_type = 'inverse'
underlying = 'crypto'
```

**Formulas**:
```
Inverse Call: max(1/S_T - 1/K, 0)
Inverse Put: max(1/K - 1/S_T, 0)
```

**Reference**: Alexander & Imeraj (2021), arXiv 2107.12041

---

#### S23: Uniswap V2 Liquidity Pool
**Status**: Plan summary below (detailed plan on demand)

**Core Logic**:
- AMM mechanics (constant product formula)
- LP yield analysis
- Impermanent loss calculation

**Key Parameters**:
```python
fee = 0.003  # 0.3%
tokens = 18
```

**Formulas**:
```
Constant Product: x × y = k
Swap: tokenB_out = (tokenA_in × reserve_B) / (reserve_A + tokenA_in)
Impermanent Loss: IL = 2×√(p_f/p_i)/(1+p_f/p_i) - 1
```

---

#### S24: The Virtue of Complexity
**Status**: Plan summary below (detailed plan on demand)

**Core Logic**:
- Machine learning with overparameterization
- Ridge regression
- Random features

**Key Parameters**:
```python
method = 'ridge_regression'
regularization = 'l2'
features = 'random'
```

**Formula**:
```
β̂_ridge = argmin{Σ(y_i - X_iβ̂)² + λ||β̂||²}
```

**Key Finding**: Overparameterization (N > T) can outperform simple models

**Reference**: Kelly, Malamud & Zhou (2022), SSRN 4166368

---

## Implementation Priority Matrix

| Priority | Strategies | Rationale |
|----------|-----------|-----------|
| **P0** | S01, S02, S05, S06 | Core/foundational strategies, high Sharpe |
| **P1** | S03, S04, S07, S09, S16 | Important variations, good diversification |
| **P2** | S08, S10, S11, S12, S14 | Specialized strategies, higher complexity |
| **P3** | S13, S15, S17, S18-S24 | Analysis tools, lower priority standalone |

---

## Common Implementation Patterns

### Signal Generation Pattern
```python
def GenerateSignals(self):
    signals = {}
    for symbol in self.universe:
        # Calculate signal logic
        signal = self.CalculateSignal(symbol)
        if signal is not None:
            signals[symbol] = signal
    return signals
```

### Volatility Scaling Pattern
```python
def CalculatePositionSize(self, symbol, signal):
    volatility = self.CalculateVolatility(symbol)
    if volatility > 0:
        size = self.target_volatility / volatility * signal
        return max(min(size, self.signal_cap), -self.signal_cap)
    return 0
```

### Monthly Rebalancing Pattern
```python
def OnEndOfMonth(self):
    signals = self.GenerateSignals()
    for symbol, signal in signals.items():
        size = self.CalculatePositionSize(symbol, signal)
        self.SetHoldings(symbol, size)
```

---

## Testing Strategy

### Unit Tests (per strategy)
- Signal calculation validation
- Position sizing accuracy
- Rebalancing trigger verification
- Edge case handling

### Regression Tests (core strategies)
- Compare to original notebook results
- Performance metric alignment
- Signal correlation check

### Smoke Tests (all strategies)
- Algorithm instantiation
- Config loading
- Basic backtest run
- No errors on startup

---

## Documentation Requirements

Each strategy must include:
1. **README.md**: Strategy description, parameters, usage
2. **config.json**: All configurable parameters
3. **docstrings**: Python docstrings for all methods
4. **Test comments**: What each test validates

---

## Files Generated

```
.sisyphus/plans/
├── quantconnect-master-plan.md              ← Master plan
├── strategy-01-tsmom-moskowitz.md           ← Detailed: S01
├── strategy-02-tsmom-baltas.md              ← Detailed: S02
├── strategy-05-commodity-carry.md           ← Detailed: S05
└── STRATEGY_IMPLEMENTATION_INDEX.md         ← This file
```

---

## Next Steps

1. **Review**: Validate plan completeness and accuracy
2. **Execute**: Run `/start-work` to begin implementation
3. **Prioritize**: Start with P0 strategies (S01, S02, S05, S06)
4. **Iterate**: Create detailed plans for remaining strategies as needed
5. **Test**: Validate each implementation against original notebooks

---

*Generated: 2026-03-01*
*Planner: Prometheus*
*Project: QuantConnect LEAN Implementation*
*Strategies: 24 total across 6 categories*

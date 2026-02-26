# FX and Cross-Asset Strategies

## Table of Contents

1. [FX Carry Trade](#1-fx-carry-trade)
2. [Cross-Asset Skewness](#2-cross-asset-skewness)

---

## 1. FX Carry Trade

**Notebook:** `fx_carry.ipynb`

**Reference:** Deutsche Bank, 2009. "db Currency Return"; Koijen et al. 2018 "Carry"

### Strategy Overview

FX carry trade: long high interest rate currencies, short low interest rate currencies. Exploits the forward rate bias and interest rate differentials.

### Core Concept

- **Carry**: Interest rate differential between currencies
- **Forward Rate Bias**: Forward rates not unbiased predictors of future spot rates
- **Risk Premium**: Compensation for currency risk

### Mathematical Formulation

**Carry Calculation:**
```
Carry_t = log(F1_t / F2_t) × annualisationFactor
```

Where:
- `F1_t` = front contract price
- `F2_t` = second contract price
- `annualisationFactor` = 4 (quarterly contracts)

**Interest Rate Differential (Approximation):**
```
Carry ≈ i_domestic - i_foreign
```

**Portfolio Construction:**
- Rank 6 currencies by carry
- Long top 33% (2 instruments)
- Short bottom 33% (2 instruments)
- Monthly rebalancing

### Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Universe | 6 currencies | EUR, JPY, GBP, CAD, AUD, NZD |
| Selection | Top/bottom 33% | Long 2, short 2 |
| Rebalancing | Monthly | Position adjustment |
| Annualization | 4x | Quarterly roll |

### Asset Universe

- CME FX futures
- EUR, JPY, GBP, CAD, AUD, NZD vs USD

### Performance Characteristics

| Metric | Value |
|----------|-------|
| CAGR | 3.35% |
| Volatility | 11.02% |
| Sharpe | 0.304 |
| Max DD | 46.6% |
| Calmar | 0.072 |
| Skewness | Positive modest |
| Kurtosis | 7.66 |

### Key Findings from Papers

**Deutsche Bank (2009):**
- Carry trades exploit forward rate bias
- Carry trades have been profitable over time
- Low correlation with traditional asset classes
- Currency risk bearing rewarded with positive returns

**Koijen et al. (2018):**
- Carry predicts returns across asset classes
- Rejects Uncovered Interest Parity
- Risk premium for recession, liquidity, volatility exposure
- Carry captures many known predictors in unifying framework

### Implementation Notes

- Front contract used for exposure
- Backfilled front-to-next for carry calculation
- Carry dispersion has shrunk recently
- Weaker performance in recent data
- `XSCarryFutureFuture` signal

### Trading Mechanics

**Classic Carry Trade:**
```
Carry = r_high - r_low
```

**Example:**
- Borrow in low-rate currency (JPY at 0%)
- Invest in high-rate currency (AUD at 5%)
- Profit = 5% - 0% = 5% (simplified)

**Risks:**
- Currency depreciation can wipe out interest differential
- Sudden unwinding of carry trades ("carry trade unwind")
- High volatility periods

---

## 2. Cross-Asset Skewness

**Notebook:** `cross_asset_skewness.ipynb`

**Reference:** Baltas, N. and Salinas, G., 2019. "Cross-Asset Skew." SSRN.

### Strategy Overview

Cross-asset skewness strategy: long assets with negative skewness, short assets with positive skewness across four asset classes.

### Core Concept

- **Skewness Premium**: Negative skewness commands risk premium
- **Cross-Asset Diversification**: Combine skewness strategies across asset classes
- **Global Skewness Factor**: Combined levered portfolio

### Mathematical Formulation

**Skewness Portfolios by Asset Class:**
```
Commodity Skewness Portfolio
Equity Skewness Portfolio
Fixed Income Skewness Portfolio
Currency Skewness Portfolio
```

**Leverage Normalization:**
```
get_leverage(equity_curve) = 0.1 / (volatility(equity_curve) × sqrt(252))
```

**Global Skewness Factor (GSF):**
```
GSF = mean(levered_daily_returns across four portfolios)
```

**Portfolio Construction:**
1. Calculate skewness for each asset in each class
2. Rank within asset class
3. Long negative skewness, short positive skewness
4. Apply equal-risk leverage
5. Combine across asset classes into GSF

### Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Asset Classes | 4 | Commodity, equity, bonds, FX |
| Leverage | Equal-risk | Volatility-scaled |
| Combination | Mean | Across levered portfolios |

### Asset Universe

- **Commodities**: Hollstein 2020 universe
- **Equities**: Major indices
- **Fixed Income**: Government bonds
- **Currencies**: G10 currencies

### Performance Characteristics

| Metric | Within Class | Cross-Asset |
|----------|--------------|-------------|
| Sharpe | 0.35 | 0.72 |

**Key Finding:** Cross-asset combination doubles Sharpe ratio due to diversification.

### Theoretical Foundation

**Cumulative Prospect Theory:**
```
U(x) = x^α × p^α  for x > 0, with α < 1
```

Investors prefer positive skewness (lottery-like payoffs), causing:
- Overpricing of positively skewed assets
- Underpricing of negatively skewed assets
- Higher expected returns for negative skewness (risk compensation)

### Key Findings from Paper

1. Realized skewness predicts returns across four asset classes
2. Sharpe ratio 0.35 within classes, 0.72 across classes
3. Not subsumed by value, momentum, or carry factors
4. Significant diversification benefits from cross-asset approach
5. Little evidence of common risk driver across asset classes
6. Patterns not subsumed by other factors
7. Robust across different skewness measures and sub-samples

### Implementation Notes

- Equal-risk leverage via `get_leverage`
- GSF constructed from combined portfolios
- Per-asset and cross-asset metrics reported
- Regime shift considerations (commodity financialization)
- Cross-asset diversification benefits
- Mean-variance efficient multi-factor portfolios assign positive weight to skewness

### Diversification Benefits

**Within Asset Class:**
- Single asset class skewness strategy
- Sharpe ~0.35
- Concentrated risk

**Cross-Asset:**
- Combines four asset classes
- Sharpe ~0.72
- Diversification benefit doubles risk-adjusted return

**Mechanism:**
- Different risk drivers across asset classes
- Low correlations between skewness premia
- Natural hedge across markets

---

## Academic Paper Summaries

### Deutsche Bank (2009) - "db Currency Return"

**Key Findings:**
- G10 Currency Universe
- Three core strategies: Carry, Momentum, Valuation
- Carry exploits forward rate bias
- Carry trades profitable over time (June 1989 - February 2009)
- Low correlation with traditional assets
- Academics attribute returns to currency risk bearing

**Carry Formula:**
```
Carry ≈ i_domestic - i_foreign
```

---

### Koijen et al. (2018) - "Carry"

**Key Findings:**
- Carry predicts returns across asset classes
- Rejects Uncovered Interest Parity and Expectations Hypothesis
- Risk premium for global recession, liquidity, volatility
- Carry captures many predictors in unifying framework

**Fundamental Identity:**
```
r = carry + E(Δp) + ε
```

**Carry by Asset Class:**
- **Currencies**: carry ≈ interest rate differential
- **Commodities**: carry = (F/S) - 1 (backwardation/contango)
- **Equities**: carry = dividend yield - risk-free rate
- **Bonds**: carry = yield - expected yield change

---

### Baltas and Salinas (2019) - "Cross-Asset Skew"

**Key Findings:**
- Realized skewness predicts returns across four asset classes
- Sharpe ratio 0.35 within classes, 0.72 across classes
- Not subsumed by value, momentum, or carry factors
- Significant diversification benefits
- Time period: 1990-2017

**Portfolio Construction:**
- Commodity, equity, bond, currency skewness portfolios
- Equal-risk leverage normalization
- Global Skewness Factor (GSF) from combined portfolios

**Theoretical Basis:**
- Cumulative prospect theory
- Investor preference for positive skewness
- Compensation for negative skewness risk

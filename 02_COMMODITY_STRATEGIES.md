# Commodity Strategies Documentation

## Table of Contents

1. [Commodity Term Structure / Carry](#1-commodity-term-structure--carry)
2. [Commodity Momentum](#2-commodity-momentum)
3. [Commodity Skewness](#3-commodity-skewness)
4. [Commodity Intra-Curve](#4-commodity-intra-curve)
5. [Commodity Basis Momentum](#5-commodity-basis-momentum)
6. [Commodity Basis Reversal](#6-commodity-basis-reversal)

---

## 1. Commodity Term Structure / Carry

**Notebook:** `commodity_term_structure.ipynb`

**Reference:** Koijen, R.S., Moskowitz, T.J., Pedersen, L.H. and Vrugt, E.B., 2018. "Carry." Journal of Financial Economics, 127(2), pp.197-225.

### Strategy Overview

The commodity carry strategy exploits the term structure of futures prices. Assets in backwardation (front month > back month) tend to have positive roll yields, while assets in contango tend to have negative roll yields. The strategy goes long backwardated commodities and short contango commodities.

### Core Concept

- **Carry**: Return assuming futures prices stay constant
- **Backwardation**: Futures price < Spot price (positive carry)
- **Contango**: Futures price > Spot price (negative carry)
- **Analogy**: Similar to FX carry trade

### Mathematical Formulation

**Carry Signal:**
```
Carry_t,i = log(F1_i,t / F2_i,t) × annualisationFactor
```

Where:
- `F1_i,t` = price of 1st front contract for commodity i
- `F2_i,t` = price of 2nd front contract for commodity i
- `annualisationFactor` = 4 (quarterly contracts)

**Smoothed Carry:**
```
Carry_sma_t,i = SMA(Carry_t,i, window=252)
```

**Portfolio Construction:**
- Rank commodities by Carry_sma_t,i
- Long top tercile (33%), short bottom tercile (33%)
- Equal-weight within terciles
- Monthly rebalancing

### Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Expiry Shift | 1 | Front contract selection |
| SMA Window | 252 days | Carry smoothing period |
| Rebalancing | Monthly | Position adjustment frequency |
| Selection | Terciles | Top/bottom 33% |

### Asset Universe

- 26 commodities (Hollstein 2020 universe)
- Energy, metals, agriculture, livestock

### Performance Characteristics

| Metric | With Smoothing | Without Smoothing |
|----------|---------------|-------------------|
| CAGR | 5.69% | 10.4% |
| Volatility | 11.5% | 16.3% |
| Sharpe | 0.495 | 0.640 |
| Max DD | 33.8% | 51.0% |

### Key Findings from Paper

1. Carry predicts returns across multiple asset classes
2. Carry captures risk premia for exposure to global recession, liquidity, and volatility risks
3. Commodity carry reflects convenience yield and storage cost dynamics
4. Carry smooths out noise from seasonal effects

### Implementation Notes

- `XSCarryFutureFuture` signal with `nth_expiry_shift=1`
- Post-processing: `Pipeline(SMA(252), AsFreq('m'))`
- Liquidity considerations: Some contracts less liquid
- Carry smoothing significantly changes risk/return profile
- Uses front-to-second contract relationship

---

## 2. Commodity Momentum

**Notebook:** `commodity_momentum.ipynb`

**Reference:** Asness, C.S., Moskowitz, T.J. and Pedersen, L.H., 2013. "Value and momentum everywhere." The Journal of Finance, 68(3), pp.929-985.

### Strategy Overview

Cross-sectional commodity momentum ranks commodities by their past 1-year performance and goes long the top performers while shorting the bottom performers.

### Mathematical Formulation

**Momentum Signal:**
```
R_i,t,1yr = P_i,t / P_i,t-252 - 1
MomentumSignal_i,t = rank(R_i,t,1yr) across i
```

**Portfolio Construction:**
- Rank by 1-year trailing performance
- Long top subset, short bottom subset
- Equal-weight across selected contracts
- Monthly rebalancing

### Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Lookback | 252 days | 1-year performance window |
| Rebalancing | Monthly | Position adjustment frequency |
| Strategy | DELTA_ONE | Equal-weight exposure |

### Asset Universe

- 26 futures (Hollstein 2020 universe)

### Performance Characteristics

| Metric | Value |
|----------|-------|
| CAGR | 11.1% |
| Volatility | 18.2% |
| Sharpe | 0.611 |
| Max DD | 56.2% |
| Calmar | 0.198 |

### Key Findings from Paper

1. Value and momentum premiums exist consistently across 8 diverse markets/asset classes
2. Both factors are positively correlated within markets but negatively correlated across asset classes
3. Combined value + momentum portfolios outperform either factor alone due to diversification
4. Global risk factors (funding liquidity, volatility) partially explain patterns
5. Evidence supports behavioral theories (sentiment-driven mispricing)

### Implementation Notes

- `XSMomentum` signal with `lookback=252`
- Post-processing: `AsFreq(freq='m', method='pad')`
- Momentum regime changes noted (notably stall since ~2015)
- Diversification across 26 contracts mitigates single-contract risk
- Monthly rebalancing controls turnover

---

## 3. Commodity Skewness

**Notebook:** `commodity_skewness.ipynb`

**Reference:** Fernandez-Perez, A., Frijns, B., Fuertes, A.M. and Miffre, J., 2018. "The skewness of commodity futures returns." Journal of Banking & Finance, 86, pp.143-158.

### Strategy Overview

The commodity skewness strategy exploits the relationship between return skewness and expected returns. Commodities with more negative skewness tend to have higher expected returns (compensation for crash risk).

### Core Concept

- **Negative Risk Premium**: Low skewness assets earn higher returns
- **Investor Preference**: Investors prefer positive skewness (lottery-like payoffs)
- **Compensation**: Negative skewness commands risk premium

### Mathematical Formulation

**Skewness Calculation:**
```
Skew_i,t = skewness of returns R_i,τ over lookback window L (L=252)
Signal_i,t = -Skew_i,t  (Negate to align long on most negative skewness)
```

**Portfolio Construction:**
- Compute rolling 252-day skewness for each contract
- Negate to align signal (long negative skewness)
- Rank across contracts
- Long most negative, short most positive
- Monthly rebalancing

### Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Lookback | 252 days | Skewness calculation window |
| Rebalancing | Monthly | Position adjustment frequency |

### Asset Universe

- 26 futures (Hollstein 2020 universe)

### Performance Characteristics

| Metric | Value |
|----------|-------|
| CAGR | 0.4% |
| Volatility | 15.8% |
| Sharpe | 0.026 |
| Max DD | 91.9% |

### Key Findings from Paper

1. Total skewness commands a negative risk premium
2. Low skewness assets earn higher returns (8% annual excess return)
3. Skewness explains cross-section of commodity returns better than backwardation/contango
4. Returns remain after controlling for standard risk factors
5. Explained by investor skewness preference and selective hedging

### Implementation Notes

- `XSSkewness` signal with `lookback=252`
- Post-processing: `Pipeline([Negate(), AsFreq('m')])`
- **Sample sensitivity**: Results vary significantly by period
- **Post-publication weakness**: Signal weaker in recent data
- Skewness may reflect priced risk but robustness limited

---

## 4. Commodity Intra-Curve

**Notebook:** `commodity_intra_curve.ipynb`

**Reference:** La Française Group, 2015. "Commodity premia: It's all about risk control."

### Strategy Overview

Intra-curve carry strategy: trades spread between different tenors on the same commodity curve (F3 vs F0) to capture curve premia.

### Core Concept

- **Intra-Curve Carry**: Within-curve spread trading
- **F3 vs F0**: Long 3-month forward, short front contract
- **Hedging Demand**: Exploits producer/consumer hedging differences

### Mathematical Formulation

**Spread Signal:**
```
S_i,t = F3_i,t - F0_i,t
```

**Two-Leg Construction:**
- `i_F3`: long with forwardness=3
- `i_F0`: short with forwardness=0
- Spread = F3 - F0

**Roll Rules:**
- `roll_rule = FIFTH_BIZ_DAY`
- `roll_period = 5`

### Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Forward Leg | F3 | 3-month forward contract |
| Front Leg | F0 | Near/front contract |
| Roll Schedule | 5th business day | Roll timing |
| Roll Period | 5 days | Roll execution window |

### Asset Universe

- 22 futures (La Française 2015 universe)

### Performance Characteristics

| Metric | Value |
|----------|-------|
| CAGR | -0.3% |
| Volatility | 2.97% |
| Sharpe | -0.117 |

### Implementation Notes

- Two-leg per commodity (F3 long, F0 short)
- Naive configuration shows weak performance
- Substantial winter-time volatility (natural gas driver)
- Seasonal/weather exposures significant
- Further refinements recommended

---

## 5. Commodity Basis Momentum

**Notebook:** `commodity_basis_momentum.ipynb`

**Reference:** Boons, M. and Prado, M.P., 2019. "Basis momentum." The Journal of Finance, 74(1), pp.239-279.

### Strategy Overview

Basis momentum captures momentum in the basis (front contract vs. next-month contract) with predictive content for cross-sectional commodity returns.

### Core Concept

- **Basis**: Difference between front and deferred contracts
- **Basis Momentum**: Momentum in this spread
- **Supply-Demand**: Captures market-clearing imbalances

### Mathematical Formulation

**Basis Momentum Signal:**
```
BM_t,i = ∏_{s=t-11}^{t} (1 + R1_i,s) - ∏_{s=t-11}^{t} (1 + R2_i,s)
```

Where:
- `R1_i,s` = return of T1 (first front) in month s
- `R2_i,s` = return of T2 (second front) in month s
- Product over 12-month window

**Portfolio Construction:**
- Rank commodities by BM_t,i
- Long top 4, short bottom 4
- Equal-dollar weighting
- Monthly rebalancing

### Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Window | 11 months | Basis momentum lookback |
| Roll Schedule | 21 days | Days prior to expiry |
| Selection | Top/bottom 4 | Long 4, short 4 |
| Weighting | Equal-dollar | Portfolio construction |

### Asset Universe

- 27 futures (Boons 2019 universe)

### Performance Characteristics

| Variant | CAGR | Volatility | Sharpe | Max DD | Calmar |
|---------|------|------------|--------|--------|--------|
| Outright | 1.46% | 22.5% | 0.065 | 92.6% | 0.016 |
| Spread | 3.14% | 7.15% | 0.439 | 24.6% | 0.128 |

### Key Findings from Paper

1. Basis-momentum strongly outperforms benchmark predictors
2. Captures supply-demand imbalances in futures markets
3. Performs best when speculator/intermediary market-clearing capacity is impaired
4. Inconsistent with storage theory, inventory theory, and hedging pressure
5. Returns represent compensation for priced risk related to market frictions

### Implementation Notes

- Front-vs-next-month pairing crucial
- Regime dependence evident in drawdown patterns
- Spread version has better risk-adjusted metrics
- `roll_schedule=21` for contract management
- Results depend on T1/T2 construction across data sources

---

## 6. Commodity Basis Reversal

**Notebook:** `commodity_basis_reversal.ipynb`

**Reference:** Rossi, A.G., Zhang, Y. and Zhu, Y., 2025. "Short-Term Basis Reversal." SSRN 5250499.

### Strategy Overview

Short-term basis reversal: the basis tends to revert; Rossi explores cross-sectional outright reversal and time-series/spread reversal.

### Core Concept

- **Basis Reversion**: Tendency of basis to mean-revert
- **Cross-Sectional**: Rank commodities by reversal signal
- **Time-Series**: Pairwise spread reversal
- **Short-Term**: Weekly/monthly horizon

### Mathematical Formulation

**Cross-Sectional Outright:**
- `nth_expiry_shift_front=-1`
- `nth_expiry_shift_back=0`
- Rank across commodities by reversal statistic
- Long strongest reversal, short weakest

**Time-Series Spread:**
- `BasisReversalSpread` for spreads across i1/i2 pairs
- Front/back alignment
- Weekly/monthly observation schedule

### Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Roll Schedule | 21 days | Contract roll timing |
| Rebalancing | Monthly/Weekly | Depends on variant |
| Weighting | Equal-weight | Portfolio construction |

### Asset Universe

- 22 futures (Rossi 2025 universe)
- Two legs per commodity (front/back)

### Performance Characteristics

| Variant | CAGR | Volatility | Sharpe | Max DD | Calmar |
|---------|------|------------|--------|--------|--------|
| Cross-Sectional | 6.7% | 19.1% | 0.351 | 53.7% | 0.125 |
| Spread | 4.4% | - | 0.646 | 16.6% | - |

### Key Findings

1. Spread exhibits negative autocorrelation
2. Edge is statistically robust and economically significant
3. Arises from relative mispricing across the curve, not individual contract reversals
4. Time-series spread variant shows stronger risk-adjusted metrics

### Implementation Notes

- Both cross-sectional and time-series interpretations
- Results depend on contract universe and roll conventions
- Careful data alignment to avoid look-ahead
- `XSBasisReversal` and `BasisReversalSpread` signals
- Spread variant shows stronger risk-adjusted metrics

---

## Academic Paper Summaries

### Koijen et al. (2018) - "Carry"

**Key Findings:**
- Carry predicts returns across asset classes
- Rejects Uncovered Interest Parity
- Risk premium for recession, liquidity, volatility exposure
- Unifying framework for multiple predictors

**Carry Formula:**
```
r = carry + E(Δp) + ε
```

**Carry by Asset Class:**
- Currencies: carry ≈ i_domestic - i_foreign
- Commodities: carry = (F_T / S_T) - 1
- Equities: carry = (D / P) - (r_f / y)

---

### Asness, Moskowitz, Pedersen (2013) - "Value and Momentum Everywhere"

**Key Findings:**
- Value and momentum exist across 8 markets
- Negatively correlated across asset classes (-0.35)
- Combined portfolios outperform (Sharpe ~1.1-1.4)
- Asset classes: equities, bonds, currencies, commodities

---

### Fernandez-Perez et al. (2018) - "Skewness of Commodity Futures"

**Key Findings:**
- Low skewness earns higher returns (8% excess return)
- Explained by cumulative prospect theory
- Long negative skew, short positive skew

---

### Boons and Prado (2019) - "Basis Momentum"

**Key Findings:**
- Basis momentum outperforms benchmark predictors
- Captures supply-demand imbalances
- 12-month rolling window
- Long top 4, short bottom 4

---

### Rossi, Zhang, Zhu (2025) - "Short-Term Basis Reversal"

**Key Findings:**
- Weekly spread between contracts 1 and 2
- Negative autocorrelation
- Front reacts faster to news
- Sharpe 0.646 for spread variant

---

### La Française Group (2015) - "Commodity Premia"

**Key Findings:**
- Intra-curve trading focus
- Risk control critical
- ARP strategies: +20% to -20%
- UCITS implementation

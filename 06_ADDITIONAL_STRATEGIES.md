# Additional Strategies and Analysis

## Table of Contents

1. [Long-Only Futures Performance](#1-long-only-futures-performance)
2. [Actively Traded Contract Months](#2-actively-traded-contract-months)
3. [Realised Volatility Measures](#3-realised-volatility-measures)
4. [Greeks Under Normal Model](#4-greeks-under-normal-model)
5. [Inverse Options](#5-inverse-options)
6. [Uniswap V2 Liquidity Pool](#6-uniswap-v2-liquidity-pool)
7. [The Virtue of Complexity](#7-the-virtue-of-complexity)

---

## 1. Long-Only Futures Performance

**Notebook:** `futures_long_only.ipynb`

### Strategy Overview

Analysis of long-only performance on futures contracts across asset classes.

### Core Concept

- **Buy-and-Hold**: Passive long exposure to futures
- **Roll Strategy**: Front-month roll methodology
- **Asset Class Comparison**: Performance across equities, bonds, commodities, FX

### Key Analysis

**Front-Month Roll:**
```
Roll yield = (Front_price - Next_price) / Next_price
```

**Long-Only Returns:**
```
Total_return = Price_change + Roll_yield
```

### Performance Characteristics

**By Asset Class:**
- **Equities**: Positive drift, momentum
- **Bonds**: Interest rate exposure, carry
- **Commodities**: Spot price change + roll yield
- **FX**: Currency appreciation/depreciation

### Implementation Notes

- Front-month roll formula
- Active contract management
- Performance attribution by asset class
- Roll cost/benefit analysis

---

## 2. Actively Traded Contract Months

**Notebook:** `futures_active_contracts.ipynb`

### Strategy Overview

Analysis of volume by contract month and active contract management.

### Core Concept

- **Volume Analysis**: Which contract months are most liquid
- **Roll Timing**: Optimal roll schedules
- **Liquidity Management**: Trade most active contracts

### Key Analysis

**Volume by Contract Month:**
```
Volume_rank = rank(Volume_by_month)
Active_contract = argmax(Volume_by_month)
```

**Roll Decision:**
```
Roll_when: Volume_next > Volume_front × threshold
```

### Implementation Notes

- Volume by contract month analysis
- Active contract selection rules
- Liquidity-based roll decisions
- Avoid illiquid distant months

---

## 3. Realised Volatility Measures

**Notebook:** `realised_volatility.ipynb`

**Reference:** Santander, 2012. "Measuring Historical Volatility."

### Strategy Overview

Various realized volatility calculation methods and their applications.

### Mathematical Formulation

**Standard Realized Volatility:**
```
σ = √(Σ(r_i - r̄)² / (n-1))
```

**Yang-Zhang Volatility:**
```
σ_YZ = √(σ_O² + k×σ_C² + (1-k)×σ_RS²)
```

Where:
- `σ_O` = open volatility
- `σ_C` = close-to-close volatility
- `σ_RS` = Rogers-Satchell volatility
- `k` = weighting parameter (~0.34)

**Rogers-Satchell Volatility:**
```
σ_RS² = ln(H/C) × ln(H/O) + ln(L/C) × ln(L/O)
```

Where:
- H = high price
- L = low price
- O = open price
- C = close price

**EWMA Volatility:**
```
σ²_EWMA,t = (1-λ) × σ²_EWMA,t-1 + λ × r_t²
```

Where λ = 2/(n+1) for n-day window.

### Volatility Estimators

1. **Close-to-Close**: Simple standard deviation of returns
2. **Yang-Zhang**: Most efficient, uses OHLC
3. **EWMA**: Exponentially weighted
4. **Parkinson**: Uses high-low range
5. **Garman-Klass**: Uses OHLC

### Implementation Notes

- Multiple volatility estimators
- Rolling window calculations
- Annualization factors
- Comparison of methods
- Applications to position sizing

---

## 4. Greeks Under Normal Model

**Notebook:** `Greeks_under_normal_model.ipynb`

### Strategy Overview

Greeks calculation under the Normal (Bachelier) model as opposed to log-normal Black-Scholes.

### Core Concept

- **Normal Model**: Arithmetic Brownian motion
- **Forward-Based Greeks**: Greeks calculated on forward prices
- **Alternative to Black-Scholes**: Different distributional assumptions

### Mathematical Formulation

**Normal Model (Bachelier):**
```
dF = σ dW
```

**Black-Scholes Model (Log-Normal):**
```
dF/F = σ dW
```

**Greeks:**
- **Delta**: ∂V/∂F
- **Gamma**: ∂²V/∂F²
- **Vega**: ∂V/∂σ
- **Theta**: ∂V/∂t
- **Rho**: ∂V/∂r

### Normal Model Greeks

**Call Option:**
```
C = (F - K) × N(d) + σ × √T × n(d)
```

Where:
```
d = (F - K) / (σ × √T)
N() = cumulative normal distribution
n() = normal density function
```

**Delta:**
```
Δ = N(d)
```

**Gamma:**
```
Γ = n(d) / (σ × √T)
```

**Vega:**
```
ν = √T × n(d)
```

### Applications

- Short-term options
- When volatility is low
- Interest rate options (Bachelier model)
- When log-normal assumption breaks down

### Implementation Notes

- Forward-based calculations
- Normal distribution assumptions
- Comparison with log-normal model
- Applications to specific markets
- Short-dated options

---

## 5. Inverse Options

**Notebook:** `inverse_option.ipynb`

**Reference:** Alexander, C. and Imeraj, A., 2021. "Inverse Options in a Black-Scholes World." arXiv:2107.12041.

### Strategy Overview

Analysis of inverse options with applications to cryptocurrency markets.

### Core Concept

- **Inverse Payoff**: Options with inverted payoff structure
- **Crypto Applications**: DeFi inverse perpetuals
- **Black-Scholes Framework**: Pricing under normal model

### Mathematical Formulation

**Standard Option Payoff:**
```
Payoff = max(S_T - K, 0)  [Call]
Payoff = max(K - S_T, 0)  [Put]
```

**Inverse Option Payoff:**
```
Payoff = max(1/S_T - 1/K, 0)  [Inverse Call]
Payoff = max(1/K - 1/S_T, 0)  [Inverse Put]
```

**Present Value Calculations:**
- PV in USD vs BTC (for crypto)
- d1, d2 calculations
- Greeks analysis

### Crypto Applications

**DeFi Inverse Perpetuals:**
- Common in cryptocurrency derivatives
- Payoff denominated in quote currency (e.g., USD)
- Payout in base currency (e.g., BTC)
- Creates convexity vs linear payoff

**Example:**
```
Standard: Profit/Loss in USD
Inverse: Profit/Loss in BTC
```

### Implementation Notes

- Present value calculations in USD vs BTC
- Greeks analysis
- d1, d2 calculations
- Crypto-specific considerations
- DeFi applications

---

## 6. Uniswap V2 Liquidity Pool

**Notebook:** `crypto_uniswap_graph.ipynb`

### Strategy Overview

Analysis of Uniswap V2 liquidity pool yields using The Graph data.

### Core Concept

- **AMM Mechanics**: Constant product formula (x × y = k)
- **LP Yield**: Fee earnings from trading
- **Impermanent Loss**: Loss from price divergence

### Mathematical Formulation

**Constant Product:**
```
x × y = k
```

Where:
- x = token A reserves
- y = token B reserves
- k = constant (invariant)

**Swap Calculation:**
```
tokenB_out = (tokenA_in × reserve_B) / (reserve_A + tokenA_in)
```

**New Reserves:**
```
reserve_A_new = reserve_A + tokenA_in
reserve_B_new = reserve_B - tokenB_out
```

**Invariant Check:**
```
reserve_A_new × reserve_B_new = k (approximately, minus fees)
```

### Fee Structure

**0.3% Trading Fee:**
```
fee = 0.003 × tokenA_in
fee_added_to_reserves = fee
new_k = (reserve_A + tokenA_in) × (reserve_B - tokenB_out + fee)
```

**LP Earnings:**
- Fees accumulate to reserves
- LPs earn proportionate to their share
- Fees increase k over time

### Impermanent Loss

**Definition:**
Loss when price diverges from entry vs holding tokens.

**Formula:**
```
IL = 2 × √(p_final/p_initial) / (1 + p_final/p_initial) - 1
```

**Worst Case:**
- 50% loss at extreme price ratios (100x move)
- Becomes permanent if liquidity removed at different price

**Example:**
```
If price doubles:
IL = 2 × √2 / (1 + 2) - 1 ≈ -5.7%

If price halves:
IL = 2 × √(0.5) / (1 + 0.5) - 1 ≈ -5.7%
```

### Trading Applications

**Arbitrage:**
- Prices diverge from CEXs/other DEXs
- Arbitrageurs restore equilibrium
- Profits from price discrepancies

**Liquidity Provision:**
- Earn fees vs. impermanent loss risk
- Trade-off: fees vs. divergence
- Range orders (V3 more efficient)

**Gas Costs:**
- LP management involves transaction expenses
- Must account for gas costs
- Batch operations to save gas

### Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Fee | 0.3% | Trading fee to LPs |
| Tokens | 18 | Pool coverage in analysis |
| APY | Variable | Depends on volume and TVL |

### Implementation Notes

- The Graph subgraph data
- 18 tokens analyzed
- APY calculations
- Impermanent loss analysis
- Gas cost considerations

---

## 7. The Virtue of Complexity

**Notebook:** `the_virtue_of_complexity_everywhere.ipynb`

**Reference:** Kelly, B.T., Malamud, S. and Zhou, K., 2022. "The virtue of complexity everywhere." SSRN 4166368.

### Strategy Overview

Machine learning approach demonstrating that complex models with more parameters than observations can outperform simple models.

### Core Concept

- **Overparameterization**: More parameters than data points
- **Ridge Regression**: Regularization for complexity control
- **Out-of-Sample Prediction**: Focus on forecasting accuracy

### Mathematical Formulation

**Ridge Regression:**
```
β̂_ridge = argmin{Σ(y_i - X_iβ̂)² + λ||β̂||²}
```

Where:
- λ = regularization parameter
- ||β̂||² = L2 penalty (sum of squared coefficients)

**Overparameterization Bound (Main Result):**
```
R*(T) = E[min{R²(N), R²(N*)}] - penalty(N)
```

Where:
- `R*(T)` = optimal out-of-sample R-squared
- `R²(N)` = sample R-squared using N parameters
- `N` = number of parameters
- `penalty(N)` = complexity penalty

**Key Finding:**
When `N > T` (parameters > observations), the penalty is small relative to potential R² improvement, making overparameterization beneficial.

**Signal-to-Noise Ratio:**
```
SNR² = σ²_signal / σ²_noise
```

**Bias-Variance Tradeoff:**
```
MSE = Bias² + Variance + Noise
```

For `n < T`, optimal: `n = T` (overfit).  
For `n > T`, optimal: `n >> T` (rich signal modeling).

### Key Findings from Paper

1. Simple models (few parameters) severely understate return predictability
2. Complex models with parameters > observations outperform
3. "Overparameterization is optimal" for prediction under regularity conditions
4. Machine learning justification: complexity virtue provides theoretical foundation for ML in finance
5. High-dimensional models capture complex return patterns missed by simple factor models

### Performance Results

- **Predictive R²**: Complex models achieve significantly higher out-of-sample R²
- **Sharpe ratio improvement**: Complexity-adjusted portfolios outperform simple benchmark models
- **Factor model comparison**: ML models capture nonlinear patterns missed by CAPM/Fama-French
- **Economic significance**: Alphas remain significant after transaction costs

### Implementation Notes

- Ridge regression for regularization
- Random features for complexity
- Memory/computation trade-offs
- Feature space expansion
- Out-of-sample testing critical
- K-fold cross-validation

### Applications to Finance

**Traditional Approach:**
```
r = α + β_1 × F1 + β_2 × F2 + ε
```

**Complexity Approach:**
```
r = f(F1, F2, F3, ..., F_N) where N >> T
```

**Benefits:**
- Captures nonlinear interactions
- Models complex relationships
- Better prediction accuracy
- Robust to model misspecification

---

## Implementation Framework Summary

All strategies in this repository use the `vivace` proprietary library for:

### Data Management
- Contract handling
- Roll schedules
- Price adjustments
- Multi-asset universes

### Signal Generation
- Technical indicators
- Statistical measures
- Cross-sectional rankings
- Time-series momentum

### Backtesting
- `BacktestEngine` with various strategy types
- `DELTA_ONE` for equal-risk weighting
- `VolatilityScale` for volatility targeting
- `TSMOM` for momentum signals

### Performance Analysis
- `Performance` class with standard metrics
- CAGR, Sharpe, Max DD, Calmar
- Skewness, Kurtosis
- Worst returns

### Portfolio Construction
- Equal-weight
- Volatility-scaled
- Product weighting
- Tercile-based selection

### Common Parameters

| Parameter | Typical Value | Description |
|-----------|--------------|-------------|
| Target Volatility | 40% | Annualized volatility target |
| Rebalancing | Monthly | Standard rebalancing frequency |
| Signal Cap | 0.95 | Maximum position size |
| Volatility Window | 21 days | EWMA lookback |
| Ann Factor | 261 | Trading days per year |

---

## Additional Papers

### Santander (2012) - "Measuring Historical Volatility"

**Status**: Not located in searches
- May be an unpublished working paper
- Alternative: Review Google TF Quant Finance for realized volatility implementations

---

### Alexander and Imeraj (2021) - "Inverse Options"

**Key Findings:**
- Inverse options with inverted payoff
- Crypto applications (DeFi inverse perpetuals)
- Black-Scholes framework
- Present value calculations in USD vs BTC

---

### Kelly, Malamud, Zhou (2022) - "The Virtue of Complexity Everywhere"

**Key Findings:**
- Overparameterized models outperform
- Ridge regression with random features
- Theoretical justification for ML in finance
- Higher out-of-sample R²
- Sharpe ratio improvement
- Alphas significant after costs

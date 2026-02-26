# Academic Papers Summary - Systematic Trading Strategies

This document provides detailed summaries of all academic papers referenced in the repository.

---

## Core Papers (Major Strategies)

### 1. Moskowitz, Ooi, Pedersen (2012) - "Time Series Momentum"
**Journal:** Journal of Financial Economics, 104(2), pp.228-250

**Key Findings:**
- Documented significant "time series momentum" across 58 liquid futures instruments
- Returns show persistence for 1-12 months, with partial reversal over longer horizons
- Consistent with sentiment theories: initial under-reaction followed by delayed over-reaction
- Diversified TSM portfolio delivers Sharpe ratio ~0.70-0.80
- Little exposure to standard asset pricing factors
- Performs best during extreme markets and crises
- Speculators profit at the expense of hedgers

**Methodology:**
- **Core Signal:** Past 12-month excess return of each instrument predicts its future return
- **Position Sizing:** Volatility-scaled positions, typically targeting 40% annualized volatility
- **Portfolio Construction:** Equal-weighted across all assets and asset classes

**Key Equation:**
```
w_i,t = σ_target / σ_i,t × sign(r_i,t-12m)
```

**Asset Classes Tested:**
- Equity index futures (24 instruments)
- Currency futures (9 instruments)
- Commodity futures (17 instruments)
- Bond futures (8 instruments)
- Total: 58 liquid futures contracts

**Performance Results:**
- Sharpe Ratio: ~0.70-0.80
- Annualized Return: ~15-20% gross
- Alpha after transaction costs remains positive
- Strongest performance during market crises

---

### 2. Baltas and Kosowski (2020) - "Demystifying Time-Series Momentum"
**Book:** Market Momentum: Theory and Practice, Wiley

**Key Findings:**
- More efficient volatility estimation (Yang-Zhang) can reduce portfolio turnover by >30%
- Price trend detection improvements reduce unnecessary trades
- Incorporating pairwise signed correlations via dynamic leverage improves performance
- Outperformance more pronounced in post-2008 period
- Transaction costs significantly impact profitability

**Volatility Estimators Compared:**
1. Standard EWMA (Equally Weighted Moving Average)
2. EWMA with daily decay
3. Realized volatility (historical)
4. Yang-Zhang realized volatility (most efficient)

**Key Equations:**

**Correlation-Adjusted Weight:**
```
w_i,t* = σ_target / (Σ_j |c_ij| × σ_j,t)
```

**EWMA Volatility:**
```
σ²_EWMA,t = (1-λ) × σ²_EWMA,t-1 + λ × (r_i,t)²
```

---

### 3. Asness, Moskowitz, Pedersen (2013) - "Value and Momentum Everywhere"
**Journal:** The Journal of Finance, 68(3), pp.929-985

**Key Findings:**
- Value and momentum premiums exist consistently across 8 diverse markets
- Both factors are positively correlated within markets but negatively correlated across asset classes (-0.35)
- Combined value + momentum portfolios outperform either factor alone (Sharpe ~1.1-1.4)
- Value and momentum together explain cross-sectional returns better than standard models
- Global risk factors (funding liquidity, volatility) partially explain patterns
- Evidence supports behavioral theories (sentiment-driven mispricing)

**Correlation Structure:**
```
ρ(Value, Momentum) < 0 (within markets)
ρ(Value_i, Momentum_j) ≈ -0.35 (across asset classes)
```

**Asset Classes Tested:**
- Equity Indices: US, UK, Europe, Japan
- Country Equity: Japan, UK, Continental Europe
- Global Government Bonds: US, UK, Japan, Germany
- Currencies: G10 developed markets
- Commodities: Energy, metals, agricultural, livestock

---

### 4. Koijen, Moskowitz, Pedersen, Vrugt (2018) - "Carry"
**Journal:** Journal of Financial Economics, 127(2), pp.197-225

**Key Findings:**
- Carry predicts returns cross-sectionally and in time series across multiple asset classes
- Carry is not explained by known predictors
- Carry strategies earn risk premiums for exposure to global recession, liquidity, and volatility risks
- Reject generalized Uncovered Interest Parity and Expectations Hypothesis
- Carry captures many known predictors in a unifying framework

**Fundamental Identity:**
```
r = carry + E(Δp) + ε
```

**Carry by Asset Class:**
- **Currencies:** carry_currency ≈ i_domestic - i_foreign
- **Commodities:** carry_commodity = (F_T / S_T) - 1
- **Equities:** carry_equity = (D / P) - (r_f / y)

**Risk Compensation:**
1. Global recession risk
2. Liquidity risk
3. Volatility risk

---

### 5. Fernandez-Perez, Frijns, Fuertes, Miffre (2018) - "Skewness of Commodity Futures"
**Journal:** Journal of Banking & Finance, 86, pp.143-158

**Key Findings:**
- Total skewness commands a negative risk premium
- Low skewness assets earn higher returns (8% annual excess return)
- Skewness explains cross-section of commodity returns better than backwardation/contango
- Returns remain after controlling for standard risk factors
- Explained by investor skewness preference (cumulative prospect theory) and selective hedging

**Theoretical Foundation (Cumulative Prospect Theory):**
```
U(x) = x^α × p^α for x > 0, with α < 1
```

**Skewness Calculation:**
```
γ_i = (1/T) × Σ(r_j - μ)³ / σ³
```

**Trading Rule:**
- Long assets with most negative skewness
- Short assets with most positive skewness

---

### 6. Boons and Prado (2019) - "Basis Momentum"
**Journal:** The Journal of Finance, 74(1), pp.239-279

**Key Findings:**
- Basis-momentum strongly outperforms benchmark predictors
- Captures supply-demand imbalances in futures markets
- Performs best when speculator/intermediary market-clearing capacity is impaired
- Inconsistent with storage theory, inventory theory, and hedging pressure
- Returns represent compensation for priced risk related to market frictions

**Signal Formula:**
```
BM_t,i = ∏_{s=t-11}^{t} (1 + R1_i,s) - ∏_{s=t-11}^{t} (1 + R2_i,s)
```

**Where:**
- R1 = return of front contract
- R2 = return of second contract
- Product over 12-month window

---

### 7. Kelly, Malamud, Zhou (2022) - "The Virtue of Complexity Everywhere"
**Working Paper:** SSRN 4166368

**Key Findings:**
- Simple models (few parameters) severely understate return predictability
- Complex models with parameters > observations outperform
- Overparameterization is optimal for prediction under regularity conditions
- Provides theoretical foundation for ML approaches in finance

**Theoretical Result:**
```
R*(T) = E[min{R²(N), R²(N*)}] - penalty(N)
```

**Ridge Regression:**
```
β̂_ridge = argmin{Σ(y_i - X_iβ̂)² + λ||β̂||²}
```

---

## Supporting Papers

### 8. Chevallier and Ielpo (2014) - "Time Series Momentum in Commodities"
**Journal:** Managerial Finance

**Key Methodology:**
- Markov-switching models for regime identification
- Daily frequency data covering 1995-2012
- Extended TSMOM to commodity markets

**Key Findings:**
- Commodities exhibit different characteristics than standard assets
- Distinct regime-switching properties compared to equities
- Understanding regimes crucial for effective trend-following

---

### 9. Simon (1999) - "The Soybean Crush Spread"
**Journal:** Journal of Futures Markets, 19(3), pp.271-289

**Key Findings:**
- Deviations from long-run equilibrium were transitory
- Strong seasonality in crush spread
- Persistent uptrend in soymeal/soyoil relative to soybeans
- Tendency to revert toward 5-day average
- Trading rules based on these results would be profitable

**Crush Spread Formula:**
```
Crush = (Meal_price × 2.2) + (Oil_price × 11) - Soybean_price
```

---

### 10. Girma and Paulson (1999) - "Risk Arbitrage in Petroleum Futures Spreads"
**Journal:** Journal of Futures Markets, 19(8), pp.931-955

**Key Findings:**
- Crack spreads exhibit mean-reverting behavior
- Statistical arbitrage opportunities exist in petroleum futures
- Cointegration framework validates stationary relationships
- Multiple spread configurations tested

**Crack Spread Formulas:**
```
CS = (2/3 × HO × 42) + (1/3 × RB × 42) - CL
GCS = RB × 42 - CL
HOCS = HO × 42 - CL
```

---

### 11. Baltas and Salinas (2019) - "Cross-Asset Skew"
**Working Paper:** SSRN 3505422

**Key Findings:**
- Realized skewness predicts returns across four asset classes
- Sharpe ratio 0.35 within classes, 0.72 across classes
- Not subsumed by value, momentum, or carry factors
- Significant diversification benefits from cross-asset approach

**Portfolio Construction:**
- Commodity, equity, fixed income, currency skewness portfolios
- Equal-risk leverage normalization
- Global Skewness Factor (GSF) from combined portfolios

---

### 12. Knuteson (2020) - "Strikingly Suspicious Overnight and Intraday Returns"
**arXiv:** 2010.01727

**Key Findings:**
- Overnight returns wildly positive, intraday returns disturbingly negative
- Canada TSX 60: Overnight +1,062%, Intraday -67%
- Pattern consistent across 21 global indices (except China)
- Pattern robust across markets and time periods
- No consensus on cause

**Return Decomposition:**
```
r_overnight = (AdjClose_t / AdjClose_{t-1}) / (Close_t / Open_t) - 1
r_intraday = Close_t / Open_t - 1
```

---

### 13. Gao et al. (2018) - "Market Intraday Momentum"
**Journal:** Journal of Financial Economics, 129(2), pp.394-414

**Key Findings:**
- First half-hour return predicts last half-hour return
- Statistically and economically significant predictability
- Stronger on volatile days, high volume days, recession days
- Consistent with infrequent portfolio rebalancing model

**Returns:**
```
r1 = Return from previous close to first 30 minutes
r12 = Return from 60 min before close to 30 min before close
r13 = Return from 30 min before close to close
```

**Asset Universe:** SPY and 10 actively traded ETFs

---

### 14. Connors and Alvarez (2009) - "Short Term Trading Strategies That Work"
**Book:** TradingMarkets Publishing Group

**Key Findings:**
- RSI-2 strategy: Buy when RSI ≤ 25, sell when RSI ≥ 75
- Trend filter: Only trade above 200-day MA
- Key principles: buy pullbacks not breakouts, buy fear not greed
- Do not use stops (statistical backtesting showed stops reduce returns)
- Hold overnight and near month-end

**Strategy Rules:**
1. Enter long 5 days when market down 3 days and price > 200 MA
2. Enter long on new 10-day lows if price > 200 MA
3. RSI-2 based entries and exits

---

### 15. Rossi, Zhang, Zhu (2025) - "Short-Term Basis Reversal"
**Working Paper:** SSRN 5250499

**Key Findings:**
- Weekly spread between first and second nearby futures contracts
- Negative autocorrelation in spreads
- Front-month contracts react faster to news than deferred contracts
- Both cross-sectional outright and time-series spread variants
- Edge is statistically robust and economically significant

**Signal:**
```
Spread_t = Return(Contract_1)_t - Return(Contract_2)_t
```

---

### 16. La Française Group (2015) - "Commodity Premia"

**Key Findings:**
- ARP strategies: +20% to -20% performance range
- LFIS premia strategy: +3% over period
- Intra-curve trading requires sophisticated risk control
- Diversification benefit more important than independent return
- Capacity constraints significant for exotic premia

---

### 17. Zhang and Zhou (2017) - "Trend Following in Chinese Futures"
**Journal:** Journal of Futures Markets, 37(12), pp.1226-1254

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

---

### 18. Bakshi, Gao, Rossi (2019) - "Understanding Sources of Commodity Risk"
**Journal:** Management Science, 65(2), pp.619-641

**Key Findings:**
- Three-factor model: Average + Carry + Momentum
- One- and two-factor models are rejected
- Global equity volatility prices carry portfolios
- Speculative activity prices momentum portfolios

**Factor Model:**
```
r = β_avg × Average + β_carry × Carry + β_mom × Momentum + ε
```

---

### 19. Hollstein, Prokopczuk, Tharann (2020) - "Anomalies in Commodity Futures"
**Journal:** Quantitative Finance, 11(4)

**Priced Anomalies:**
- Jump risk
- Momentum
- Skewness
- Volatility-of-volatility

**Not Priced:**
- Downside beta
- Idiosyncratic volatility
- MAX effect

**Key Recommendation:**
- Monthly rebalancing superior to annual
- Annual holding periods substantially weaker

---

## Trading Mechanics Reference

### Crack Spread (3:2:1)

**Refinery Yield:** 3 barrels crude → 2 barrels gasoline + 1 barrel diesel

**Formula:**
```
CS = (2/3 × Gasoline × 42) + (1/3 × Heating_Oil × 42) - Crude
```

**Example:**
- Gasoline: $2.57/gal
- Heating Oil: $2.79/gal
- Crude: $84.54/bbl

```
Revenue = (2 × 42 × $2.57) + (1 × 42 × $2.79) = $333.06
Cost = 3 × $84.54 = $253.62
Spread = ($333.06 - $253.62) / 3 = $26.48/barrel
```

**Note:** True margin ~$20/barrel lower due to variable costs (labor, utilities, catalysts)

---

### Crush Spread (Soybean Complex)

**Physical Process:**
- 1 bushel soybeans (60 lbs) → ~44-48 lbs meal + ~11 lbs oil

**Formula:**
```
Crush = (Meal_price × 2.2) + (Oil_price × 11) - Soybean_price
```

**Trading:**
- Long crush: Long soybeans / Short meal + oil (bet on higher margins)
- Short crush: Short soybeans / Long meal + oil (bet on lower margins)

---

### Uniswap V2 AMM Mechanics

**Constant Product Formula:**
```
x × y = k
```

**Swap Calculation:**
```
tokenB_out = (tokenA_in × reserve_B) / (reserve_A + tokenA_in)
```

**Impermanent Loss:**
```
IL = 2 × √(p_final/p_initial) / (1 + p_final/p_initial) - 1
```

**Fee Structure:** 0.3% of trade value to LPs

---

*Last Updated: February 2026*

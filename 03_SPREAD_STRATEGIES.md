# Statistical Arbitrage - Spread Trading Strategies

## Table of Contents

1. [Soybean Crush Spread](#1-soybean-crush-spread)
2. [Petroleum Crack Spread](#2-petroleum-crack-spread)

---

## 1. Soybean Crush Spread

**Notebook:** `commodity_crush_spread_stat_arb.ipynb`

**Reference:** Simon, D.P., 1999. "The soybean crush spread: Empirical evidence and trading strategies." Journal of Futures Markets, 19(3), pp.271-289.

### Strategy Overview

The crush spread represents the gross processing margin for converting soybeans into soybean meal and soybean oil. Statistical arbitrage exploits deviations from the long-run equilibrium relationship between these three related commodities.

### Core Concept

- **Crush Spread**: Gross processing margin for soybeans
- **Mean Reversion**: Deviations from equilibrium are transitory
- **Seasonality**: Strong seasonal patterns in crush margins

### Physical Process

- 1 bushel soybeans (60 lbs) → ~44-48 lbs soybean meal + ~11 lbs soybean oil

### Mathematical Formulation

**Crush Spread (Standard):**
```
Crush_spread = 100 × Price_meal + 600 × Price_oil - 50 × Price_soybean
```

**Crush Spread (CME-Aligned):**
```
Crush_spread_cme = (Meal_price × 2.2) + (Oil_price × 11) - Soybean_price
```

**Long-Run Equilibrium (OLS Regression):**
```
Soybean_t = β_0 + β_1 × Soymeal_t + β_2 × Soyoil_t + β_3 × Trend_t + Σ(γ_m × MonthDummy_m) + ε_t
```

### Unit Conversions

| Component | Units | Conversion |
|-----------|-------|------------|
| Soybeans | per 100 bushels | Base unit (60 lbs/bushel) |
| Soybean Meal | per ton | 2,200 lbs = 100 lbs equivalent × 100 |
| Soybean Oil | per unit | 600 lbs equivalent |

### Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Analysis Period | Jan 1985 - Feb 1995 | Simon (1999) study period |
| Mean Reversion | 5-day MA | Deviation from 5-day moving average |
| R-squared | ~0.975-0.978 | OLS regression fit |

### Trading Rules

**Entry/Exit:**
- Enter long crush when spread < 5-day MA (cheap crush)
- Enter short crush when spread > 5-day MA (expensive crush)
- Exit when spread reverts toward equilibrium

**Mean-Reversion Characteristics:**
- Deviations from long-run equilibrium are transitory
- Strong tendency to revert toward 5-day average
- Strong seasonality in spreads

### Seasonal Patterns

- **February-June**: Lower crush margins
- **September-November**: Higher crush margins
- Monthly dummy variables capture seasonality

### Asset Universe

- Soybeans (S)
- Soybean Meal (SM)
- Soybean Oil (BO)

### Performance Characteristics

**OLS Results:**
- R-squared: 0.975-0.978 (high explanatory power)
- Strong F-statistics
- Significant coefficients for SM (~0.0217) and BO (~0.1046)
- Significant trend and month effects

**Mean-Reversion Properties:**
- Strong mean-reversion toward 5-day average
- Seasonal patterns documented

### Implementation Notes

- USDA 1988 definitions for gross crush margin
- CME contract specifications
- Unit conversion complexity
- Walk-forward validation recommended
- Seasonal hedging patterns affect equilibrium
- **Look-ahead bias warning**: Backtests may have in-sample bias

### Key Findings from Paper

1. Deviations from long-run equilibrium were transitory
2. Strong seasonality in crush spread
3. Persistent uptrend in soymeal/soyoil relative to soybeans
4. Tendency to revert toward 5-day average
5. Trading rules based on these results would be profitable

---

## 2. Petroleum Crack Spread

**Notebook:** `commodity_crack_spread_stat_arb.ipynb`

**Reference:** Girma, P.B. and Paulson, A.S., 1999. "Risk arbitrage opportunities in petroleum futures spreads." Journal of Futures Markets, 19(8), pp.931-955.

### Strategy Overview

The crack spread represents the theoretical refining margin from converting crude oil into refined products (gasoline and heating oil). Statistical arbitrage exploits deviations from the equilibrium relationship between crude oil and product futures.

### Core Concept

- **Crack Spread**: Refining margin from crude to products
- **Cointegration**: Long-run equilibrium relationship
- **Statistical Arbitrage**: Trade deviations from equilibrium

### Mathematical Formulation

**3:2:1 Crack Spread (CS):**
```
CS = (2/3 × Heating_oil_price × 42) + (1/3 × Gasoline_price × 42) - Crude_oil_price
```

**1:1:0 Gasoline Crack Spread (GCS):**
```
GCS = Gasoline_price × 42 - Crude_oil_price
```

**1:0:1 Heating Oil Crack Spread (HOCS):**
```
HOCS = Heating_oil_price × 42 - Crude_oil_price
```

### Unit Conversions

**Critical:** 1 barrel = 42 gallons

| Product | Unit | Conversion |
|---------|------|------------|
| Crude Oil | per barrel | Base unit |
| Gasoline | per gallon | × 42 |
| Heating Oil | per gallon | × 42 |

### Cointegration Methodology

**Step 1: Unit Root Tests**
- ADF test on individual price series (CL, HO, XB)
- Confirm non-stationarity of prices

**Step 2: Cointegration Tests**
- Engle-Granger cointegration test
- Test residuals for stationarity
- Use Schwarz's BIC to select optimal lag

**Step 3: OLS Estimation**
```
Product_t = α + β × Crude_t + ε_t
```

**Step 4: Trading Signal**
```
Signal_t = Residual_t / σ_residual
```

### Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Unit Conversion | 42 gal/bbl | Critical for consistency |
| Ratios | 3:2:1, 1:1:0, 1:0:1 | Various crack configurations |
| Method | Cointegration | GP1999 approach |
| Test | ADF, BIC | Stationarity and lag selection |

### Asset Universe

- Crude Oil (CL)
- RBOB Gasoline (XB)
- Heating Oil (HO)

### Trading Rules

**Entry/Exit:**
- Enter long spread when residual > threshold (expensive products vs. crude)
- Enter short spread when residual < threshold (cheap products vs. crude)
- Exit when residual reverts toward zero

**Mean-Reversion Characteristics:**
- Cointegration validates long-run equilibrium
- Residuals are stationary
- Strong mean-reversion properties

### Risk Management

**Unit Conversions:**
- Carefully convert barrels to gallons (×42)
- Ensure consistent units across contracts

**Cointegration Controls:**
- ADF tests validate stationarity
- BIC selects optimal lag
- Residuals serve as trading signal

### Performance Characteristics

**Cointegration Results:**
- Cointegration confirmed for CS, GCS, HOCS
- Stationarity of spreads validated
- Strong evidence of long-run equilibrium

**OLS Results:**
- Coefficients and t-stats for cointegration relationship
- Regression diagnostics provided

### Implementation Notes

- GP1999 approach with ADF/BIC-selected lags
- OLS regressions for cointegration vector
- Multiple spread configurations tested
- Data-snooping warnings noted
- Unit conversion complexity
- Walk-forward validation recommended

### Key Findings from Paper

1. Crack spreads exhibit mean-reverting behavior
2. Statistical arbitrage opportunities exist in petroleum futures
3. Cointegration framework validates stationary relationships
4. Multiple spread configurations (CS, GCS, HOCS) tested
5. Spread relationships deviate from fundamental refining economics

---

## Trading Mechanics Reference

### Crush Spread

**Physical Process:**
```
1 bushel soybeans (60 lbs) → ~44-48 lbs meal + ~11 lbs oil
```

**Trading:**
- **Long crush**: Long soybeans / Short meal + oil (bet on higher margins)
- **Short crush**: Short soybeans / Long meal + oil (bet on lower margins)

**Key Factors:**
- Chinese demand for meal (largest importer)
- Biodiesel demand for oil
- Crushing capacity utilization
- Freight and transportation costs

### Crack Spread

**Refinery Yield:**
```
3 barrels crude → 2 barrels gasoline + 1 barrel diesel
```

**Example Calculation:**
```
Gasoline: $2.57/gal
Heating Oil: $2.79/gal
Crude: $84.54/bbl

Revenue = (2 × 42 × $2.57) + (1 × 42 × $2.79) = $333.06
Cost = 3 × $84.54 = $253.62
Spread = ($333.06 - $253.62) / 3 = $26.48/barrel
```

**True Margin:**
- Variable costs: ~$20/barrel lower
- Actual margin: $26.48 - $20.00 = ~$6.58/barrel
- Includes labor, utilities, catalysts

**Trading Applications:**
- **Long spread**: Long 2 RBOB + 1 HO / Short 3 CL (betting on higher margins)
- **Short spread**: Short 2 RBOB + 1 HO / Long 3 CL (betting on lower margins)
- Refiners use to hedge processing economics
- Sensitive to: product slate, crude selection, regional demand

---

## Academic Paper Summaries

### Simon (1999) - "The Soybean Crush Spread"

**Key Findings:**
- 1-1-1 crush spread analysis
- Mean-reversion to 5-day average
- Strong seasonality
- Profitable trading rules
- OLS R²: 0.975-0.978

**Crush Formula:**
```
Crush = (Meal_price × 2.2) + (Oil_price × 11) - Soybean_price
```

---

### Girma and Paulson (1999) - "Petroleum Crack Spreads"

**Key Findings:**
- 3:2:1, 1:1:0, 1:0:1 crack spreads
- Cointegration framework
- Statistical arbitrage opportunities
- Mean-reverting residuals

**Crack Spread Formulas:**
```
CS = (2/3 × HO × 42) + (1/3 × RB × 42) - CL
GCS = RB × 42 - CL
HOCS = HO × 42 - CL
```

**Where:**
- CL = Crude Oil
- RB = RBOB Gasoline
- HO = Heating Oil
- 42 = gallons per barrel

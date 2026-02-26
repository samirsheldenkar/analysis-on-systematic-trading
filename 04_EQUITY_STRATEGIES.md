# Equity Strategies Documentation

## Table of Contents

1. [Short-Term Trading (Connors RSI-2)](#1-short-term-trading-connors-rsi-2)
2. [ETF Intraday Momentum](#2-etf-intraday-momentum)
3. [Overnight Returns](#3-overnight-returns)

---

## 1. Short-Term Trading (Connors RSI-2)

**Notebook:** `equity_short_term_trading_connors.ipynb`

**Reference:** Connors, L.A. and Alvarez, C., 2009. "Short Term Trading Strategies that Work: A Quantified Guide to Trading Stocks and ETFs." TradingMarkets Publishing Group.

### Strategy Overview

Short-term mean-reversion strategies based on Connors RSI-2 indicator. Buy pullbacks in uptrends using rapid mean-reversion signals.

### Core Concept

- **Mean Reversion**: Something stretched too far snaps back
- **RSI-2**: 2-period Relative Strength Index for rapid signals
- **Trend Filter**: Only trade above 200-day moving average

### Mathematical Formulation

**RSI-2 Calculation:**
```
RSI-2 = 100 × (Average of up changes over 2 days) / (Average of total changes over 2 days)
```

**Strategy 1 Rules:**
```
LONG if:
  - Market down 3 days in a row AND
  - Price above 200-day MA
HOLD for 5 days
```

**Strategy 2 Rules:**
```
LONG if:
  - Market makes new 10-day low AND
  - Price above 200-day MA
HOLD for 5 days
```

**Strategy 3 (Double7Connors):**
- Uses `signal.Double7Connors()` from vivace
- Connors RSI-2 based signal
- Pipeline processing

**Strategy 4 (Month-End):**
- Long-only variant near month-end
- Seasonal effects exploitation

### Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| RSI Period | 2 | Connors RSI-2 |
| Buy Threshold | ≤25 | Oversold entry |
| Sell Threshold | ≥75 | Overbought exit |
| Trend Filter | 200-day MA | Long-term trend direction |
| Hold Period | 5 days | Fixed holding period |

### Asset Universe

- US equities (multiple stocks)
- S&P 500 index

### Key Principles

1. **Buy pullbacks, not breakouts**
2. **Buy above 200-day MA** (trend filter)
3. **Buy fear, not greed**
4. **Do not use stop losses** (reduces returns)
5. **Hold overnight**
6. **Hold near end of month**
7. **Use RSI-2 for rapid mean reversion**

### Performance Characteristics

**Strategy Performance:**
- RSI-2 ≤ 25: Oversold entry
- RSI-2 ≥ 75: Overbought exit
- Fixed 5-day holding period
- 200-day MA trend filter

**Risk Management:**
- No stop losses (backtesting showed stops reduce returns)
- Trend filter (200-day MA) avoids counter-trend trades
- Fixed holding period reduces discretion

### Implementation Notes

- `Double7Connors` signal from vivace library
- `DELTA_ONE` strategy implementation
- Performance metrics via `Performance` class
- Potential look-ahead bias warnings
- Mean reversion sensitive to lookback windows
- Regime shifts may affect performance

---

## 2. ETF Intraday Momentum

**Notebook:** `equity_etf_intraday_momentum.ipynb`

**Reference:** Gao, L., Han, Y., Li, S.Z. and Zhou, G., 2018. "Market intraday momentum." Journal of Financial Economics, 129(2), pp.394-414.

### Strategy Overview

Intraday momentum in equity ETFs: first half-hour return predicts last half-hour return.

### Core Concept

- **Intraday Predictability**: First 30 minutes predicts last 30 minutes
- **Continuation**: Early momentum continues to close
- **Information Processing**: Slow diffusion of information

### Mathematical Formulation

**Intraday Returns:**
```
r1 = Return from previous day's close to first 30 minutes
r12 = Return from 60 min before close to 30 min before close
r13 = Return from 30 min before close to close
```

**Predictive Relationship:**
```
r13 = α + β × r1 + ε
```

Where β > 0 and statistically significant.

**Key Finding:**
- First half-hour return predicts last half-hour return
- Coefficient β is positive and significant

### Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| First Period | 9:30-10:00 | First half-hour |
| Last Period | 15:30-16:00 | Last half-hour |
| Data Window | 9:30-16:00 | Avoid after-hours |

### Asset Universe

- SPY (primary)
- ^IXIC (Nasdaq)
- XIU.TO (Canada)
- ^FCHI (France)
- 10 actively traded ETFs

### Trading Strategy

- Long last half-hour if first half-hour positive
- Short last half-hour if first half-hour negative
- ETF-focused implementation

### Performance Characteristics

**Predictability Stronger On:**
- More volatile days
- Higher volume days
- Recession days
- Major macroeconomic news days

**Statistical Significance:**
- β coefficient positive and significant
- Economically meaningful
- Consistent across ETFs

### Implementation Notes

- High-frequency data required (30-minute bars)
- Filter to 9:30-16:00 to avoid after-hours
- `BacktestEngine` with `DELTA_ONE`
- Pipeline for signal processing
- Consistent with infrequent portfolio rebalancing model
- Late-informed trading near close

### Key Findings from Paper

1. First half-hour return predicts last half-hour return
2. Statistically and economically significant predictability
3. Stronger on volatile, high volume, recession days
4. Theoretically consistent with infrequent rebalancing model
5. Late-informed trading near market close

---

## 3. Overnight Returns

**Notebook:** `overnight_returns.ipynb`

**Reference:** Knuteson, B., 2020. "Strikingly Suspicious Overnight and Intraday Returns." arXiv:2010.01727.

### Strategy Overview

Analysis of overnight vs intraday return decomposition across global equity markets.

### Core Concept

- **Overnight Premium**: Overnight returns wildly positive
- **Intraday Drag**: Intraday returns disturbingly negative
- **Pattern**: Consistent across markets except China

### Mathematical Formulation

**Return Decomposition:**
```
Total Return = Overnight Return + Intraday Return

r_overnight,t = (AdjClose_t / AdjClose_{t-1}) / (Close_t / Open_t) - 1
r_intraday,t = Close_t / Open_t - 1
```

### Key Findings

| Market | Overnight | Intraday | Pattern |
|--------|-----------|----------|---------|
| Canada TSX 60 | +1,062% | -67% | Extreme divergence |
| US Markets | Positive | Negative | Consistent |
| Global (21 indices) | Positive | Negative | Universal except China |

### Asset Universe

- 21 major global stock market indices
- US, Europe, Asia, Canada

### Performance Characteristics

**Stunning Pattern:**
- Overnight returns have been wildly positive
- Intraday returns have been disturbingly negative
- Same general pattern across all 21 indices
- Exception: China shows different pattern

**Robustness:**
- Pattern robust across markets and time
- Multi-decade analysis
- Consistent across different regions

### Mechanism

- Author argues pattern indicates serious market microstructure issues
- Magnitude and consistency cannot be explained by traditional risk theories
- Potential liquidity provision problems
- No consensus on cause in academic literature

### Implementation Notes

- Yahoo Finance data
- Different inception dates per market
- Data limitations for some markets (UK/China gaps)
- Pattern noted for over a decade
- Potential market structure anomaly
- Requires further investigation

### Key Findings from Paper

1. Overnight returns wildly positive across 21 global indices
2. Intraday returns disturbingly negative
3. Canada TSX 60: Overnight +1,062%, Intraday -67%
4. Pattern consistent except for China
5. Pattern very robust across markets and time
6. No consensus on cause
7. Indicates potential serious market microstructure issues

---

## Academic Paper Summaries

### Connors and Alvarez (2009) - "Short Term Trading Strategies That Work"

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

### Gao et al. (2018) - "Market Intraday Momentum"

**Key Findings:**
- First half-hour return predicts last half-hour return
- Statistically and economically significant
- Stronger on volatile, high volume days
- Stronger on recession days
- Theoretically consistent with infrequent rebalancing

**Returns:**
```
r1 = Previous close to first 30 minutes
r12 = 60 min before close to 30 min before close
r13 = 30 min before close to close
```

**Asset Universe:** SPY and 10 actively traded ETFs

---

### Knuteson (2020) - "Strikingly Suspicious Overnight Returns"

**Key Findings:**
- Overnight returns wildly positive
- Intraday returns disturbingly negative
- Canada TSX 60: Overnight +1,062%, Intraday -67%
- Pattern consistent across 21 global indices (except China)
- Pattern robust across markets and time
- No consensus on cause
- Potential market microstructure issues

**Return Decomposition:**
```
r_overnight = (AdjClose_t / AdjClose_{t-1}) / (Close_t / Open_t) - 1
r_intraday = Close_t / Open_t - 1
```

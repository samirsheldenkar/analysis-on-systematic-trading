# Systematic Trading Strategies - Documentation Index

This repository contains comprehensive documentation for all systematic trading strategies implemented in the Jupyter notebooks. Each strategy is derived from academic research with detailed mathematical formulations, implementation notes, and performance characteristics.

---

## Documentation Structure

### Core Documentation Files

1. **[01_TREND_FOLLOWING_STRATEGIES.md](01_TREND_FOLLOWING_STRATEGIES.md)**
   - Time-Series Momentum (Moskowitz 2012)
   - Time-Series Momentum Enhanced (Baltas 2020)
   - Trend Following with Breakout Signal
   - Trend Following in Chinese Futures

2. **[02_COMMODITY_STRATEGIES.md](02_COMMODITY_STRATEGIES.md)**
   - Commodity Term Structure / Carry
   - Commodity Momentum
   - Commodity Skewness
   - Commodity Intra-Curve
   - Commodity Basis Momentum
   - Commodity Basis Reversal

3. **[03_SPREAD_STRATEGIES.md](03_SPREAD_STRATEGIES.md)**
   - Soybean Crush Spread
   - Petroleum Crack Spread

4. **[04_EQUITY_STRATEGIES.md](04_EQUITY_STRATEGIES.md)**
   - Short-Term Trading (Connors RSI-2)
   - ETF Intraday Momentum
   - Overnight Returns

5. **[05_FX_CROSS_ASSET.md](05_FX_CROSS_ASSET.md)**
   - FX Carry Trade
   - Cross-Asset Skewness

6. **[06_ADDITIONAL_STRATEGIES.md](06_ADDITIONAL_STRATEGIES.md)**
   - Long-Only Futures Performance
   - Actively Traded Contract Months
   - Realised Volatility Measures
   - Greeks Under Normal Model
   - Inverse Options
   - Uniswap V2 Liquidity Pool
   - The Virtue of Complexity

7. **[ACADEMIC_PAPERS_SUMMARY.md](ACADEMIC_PAPERS_SUMMARY.md)**
   - Comprehensive summaries of all 19+ academic papers
   - Key findings, methodologies, and equations
   - Trading mechanics reference

---

## Quick Reference Guide

### By Strategy Type

#### Trend Following
| Strategy | Notebook | Reference | Sharpe |
|----------|----------|-----------|--------|
| TSMOM (Moskowitz 2012) | `trend_following_moskowitz2012.ipynb` | JFE 2012 | ~0.75 |
| TSMOM Enhanced (Baltas 2020) | `trend_following_baltas2020.ipynb` | Wiley 2020 | ~0.80 |
| Breakout Signal | `trend_following_breakout.ipynb` | Managerial Finance 2014 | - |
| Chinese Futures | `commodity_trend_following_chinese_futures.ipynb` | JFM 2017 | - |

#### Commodity Strategies
| Strategy | Notebook | Reference | Sharpe |
|----------|----------|-----------|--------|
| Term Structure/Carry | `commodity_term_structure.ipynb` | JFE 2018 | 0.495 |
| Momentum | `commodity_momentum.ipynb` | JF 2013 | 0.611 |
| Skewness | `commodity_skewness.ipynb` | JBF 2018 | 0.026 |
| Basis Momentum | `commodity_basis_momentum.ipynb` | JF 2019 | 0.439 |
| Basis Reversal | `commodity_basis_reversal.ipynb` | SSRN 2025 | 0.646 |
| Intra-Curve | `commodity_intra_curve.ipynb` | La Française 2015 | -0.117 |

#### Spread Trading
| Strategy | Notebook | Reference | Method |
|----------|----------|-----------|--------|
| Soybean Crush | `commodity_crush_spread_stat_arb.ipynb` | JFM 1999 | Mean Reversion |
| Petroleum Crack | `commodity_crack_spread_stat_arb.ipynb` | JFM 1999 | Cointegration |

#### Equity Strategies
| Strategy | Notebook | Reference | Sharpe |
|----------|----------|-----------|--------|
| Connors RSI-2 | `equity_short_term_trading_connors.ipynb` | Connors 2009 | - |
| Intraday Momentum | `equity_etf_intraday_momentum.ipynb` | JFE 2018 | - |
| Overnight Returns | `overnight_returns.ipynb` | arXiv 2020 | - |

#### FX & Cross-Asset
| Strategy | Notebook | Reference | Sharpe |
|----------|----------|-----------|--------|
| FX Carry | `fx_carry.ipynb` | Deutsche Bank 2009 | 0.304 |
| Cross-Asset Skew | `cross_asset_skewness.ipynb` | SSRN 2019 | 0.72 |

---

## Academic Papers Covered

### Core Papers

1. **Moskowitz, Ooi, Pedersen (2012)** - "Time Series Momentum" - JFE
2. **Baltas and Kosowski (2020)** - "Demystifying Time-Series Momentum" - Wiley
3. **Asness, Moskowitz, Pedersen (2013)** - "Value and Momentum Everywhere" - JF
4. **Koijen et al. (2018)** - "Carry" - JFE
5. **Fernandez-Perez et al. (2018)** - "Skewness of Commodity Futures" - JBF
6. **Boons and Prado (2019)** - "Basis Momentum" - JF
7. **Kelly, Malamud, Zhou (2022)** - "The Virtue of Complexity" - SSRN

### Supporting Papers

8. **Chevallier and Ielpo (2014)** - "Time Series Momentum in Commodities"
9. **Simon (1999)** - "Soybean Crush Spread" - JFM
10. **Girma and Paulson (1999)** - "Petroleum Crack Spreads" - JFM
11. **Baltas and Salinas (2019)** - "Cross-Asset Skew" - SSRN
12. **Knuteson (2020)** - "Overnight Returns" - arXiv
13. **Gao et al. (2018)** - "Market Intraday Momentum" - JFE
14. **Connors and Alvarez (2009)** - "Short Term Trading Strategies"
15. **Rossi, Zhang, Zhu (2025)** - "Short-Term Basis Reversal" - SSRN
16. **La Française Group (2015)** - "Commodity Premia"
17. **Zhang and Zhou (2017)** - "Trend Following in Chinese Futures" - JFM
18. **Bakshi, Gao, Rossi (2019)** - "Commodity Risk Sources" - Management Science
19. **Hollstein et al. (2020)** - "Anomalies in Commodity Futures"

---

## Implementation Framework

### Common Parameters

| Parameter | Typical Value | Description |
|-----------|--------------|-------------|
| Target Volatility | 40% | Annualized volatility target |
| Rebalancing | Monthly | Standard rebalancing frequency |
| Signal Cap | 0.95 | Maximum position size |
| Volatility Window | 21 days | EWMA lookback |
| Ann Factor | 261 | Trading days per year |

### Performance Metrics

All notebooks report:
- **CAGR** - Compound Annual Growth Rate
- **Volatility** - Annualized standard deviation
- **Sharpe** - Sharpe ratio (return/volatility)
- **Max DD** - Maximum Drawdown
- **Calmar** - CAGR / Max DD
- **Skewness** - Return distribution skewness
- **Kurtosis** - Return distribution kurtosis

### Vivace Library

All strategies use the proprietary `vivace` library for:
- **Data Management**: Contract handling, roll schedules
- **Signal Generation**: Technical indicators, statistical measures
- **Backtesting**: `BacktestEngine` with strategy types
- **Performance Analysis**: `Performance` class
- **Portfolio Construction**: Equal-weight, volatility-scaled

---

## How to Use This Documentation

1. **Start with the Index**: This file provides an overview of all strategies
2. **Read Strategy Documentation**: Each strategy file contains detailed formulations
3. **Check Academic Papers**: Reference summaries provide theoretical foundations
4. **Review Notebooks**: Original notebooks contain actual implementations
5. **Compare Performance**: Tables provide quick performance comparisons

---

## File Organization

```
analysis-on-systematic-trading/
├── 01_TREND_FOLLOWING_STRATEGIES.md
├── 02_COMMODITY_STRATEGIES.md
├── 03_SPREAD_STRATEGIES.md
├── 04_EQUITY_STRATEGIES.md
├── 05_FX_CROSS_ASSET.md
├── 06_ADDITIONAL_STRATEGIES.md
├── ACADEMIC_PAPERS_SUMMARY.md
├── STRATEGY_DOCUMENTATION_INDEX.md (this file)
├── README.md (original)
├── *.ipynb (29 notebooks)
└── sandbox/
```

---

## Key Concepts Summary

### Trend Following
- **Signal**: Past 12-month return direction
- **Sizing**: Volatility-scaled to 40% target
- **Universe**: 58 futures across 4 asset classes
- **Performance**: Sharpe ~0.75-0.80

### Carry
- **Signal**: Term structure slope (backwardation/contango)
- **Sizing**: Tercile-based selection
- **Universe**: Commodities, FX, bonds, equities
- **Performance**: Sharpe ~0.30-0.65

### Momentum
- **Signal**: Past 12-month performance ranking
- **Sizing**: Cross-sectional long/short
- **Universe**: Commodities, equities globally
- **Performance**: Sharpe ~0.60

### Skewness
- **Signal**: Rolling 252-day skewness
- **Sizing**: Long negative, short positive
- **Universe**: Commodities, cross-asset
- **Performance**: Sharpe 0.03-0.72 (cross-asset higher)

### Basis
- **Signal**: Front vs back contract momentum/reversal
- **Sizing**: Equal-dollar or equal-risk
- **Universe**: Commodity futures
- **Performance**: Sharpe 0.06-0.65

### Spread Trading
- **Signal**: Mean-reversion to equilibrium
- **Sizing**: Z-score based entry/exit
- **Universe**: Crush, crack spreads
- **Performance**: Cointegration-based

---

## Citation

If using this documentation or the strategies herein, please cite the original academic papers:

- Moskowitz et al. (2012) for time-series momentum
- Koijen et al. (2018) for carry strategies
- Asness et al. (2013) for value and momentum
- Boons and Prado (2019) for basis momentum
- And others as referenced

---

## Last Updated

February 2026

## Total Coverage

- **29 Jupyter Notebooks** documented
- **19+ Academic Papers** summarized
- **7 Documentation Files** created
- **60+ Trading Strategies** described

---

*For detailed mathematical formulations, implementation notes, and performance characteristics, refer to the specific strategy documentation files.*

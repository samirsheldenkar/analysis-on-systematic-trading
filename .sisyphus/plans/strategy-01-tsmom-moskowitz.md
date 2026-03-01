# Strategy Implementation Plan: S01 - Time-Series Momentum (Moskowitz 2012)

## TL;DR

> **Moskowitz et al. (2012) Time-Series Momentum Strategy**
>
> **Signal**: 12-month past return sign (long positive, short negative)
> **Sizing**: Volatility-scaled to 40% annualized target
> **Universe**: 58 liquid futures (24 equity, 9 FX, 17 commodity, 8 bonds)
> **Rebalancing**: Monthly
> **Expected Sharpe**: ~0.75

---

## Context

### Original Reference
Moskowitz, T.J., Ooi, Y.H. and Pedersen, L.H., 2012. "Time series momentum." Journal of Financial Economics, 104(2), pp.228-250.

### Core Concept
Time-series momentum exploits the persistence of returns at the 1-12 month horizon. The strategy goes long assets with positive past returns and short assets with negative past returns, scaled by volatility to target constant risk exposure.

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
- `σ_target` = target volatility (40% annualized)
- `σ_i,t` = realized volatility (EWMA, 21-day)
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

---

## Implementation Requirements

### Input Data
- Daily futures price data for 58 instruments
- History requirement: 13 months minimum (12-month signal + 1-month buffer)
- Data source: LEAN futures data

### Output Signals
- Signal per instrument: -1 (short), 0 (flat), +1 (long)
- Position weight per instrument: float (can be >1 due to leverage)
- Rebalancing triggers: Monthly at end of month

### LEAN Components

**Algorithm Class:**
```python
class TSMOM_Moskowitz2012(BaseStrategyAlgorithm):
    def __init__(self):
        self.lookback_days = 252  # 12 months
        self.volatility_window = 21
        self.target_volatility = 0.40
        self.signal_cap = 0.95
        self.rebalancing_freq = 'monthly'
```

**Required Methods:**
1. `GetUniverse()` - Returns list of 58 futures symbols
2. `GenerateSignals()` - Calculates 12-month return sign
3. `CalculateVolatility()` - EWMA volatility for each instrument
4. `CalculatePositionSizes()` - Volatility-scaled weights
5. `OnEndOfMonth()` - Rebalancing logic

---

## Work Objectives

### Concrete Deliverables
1. `Strategies/TrendFollowing/TSMOM_Moskowitz2012.py` - Main algorithm
2. `Strategies/TrendFollowing/TSMOM_Moskowitz2012_config.json` - Parameters
3. `Strategies/TrendFollowing/TSMOM_Moskowitz2012_README.md` - Documentation
4. `Tests/test_TSMOM_Moskowitz2012.py` - Unit tests

### Definition of Done
- [ ] Algorithm inherits from BaseStrategyAlgorithm
- [ ] Implements all required abstract methods
- [ ] Config file loads successfully
- [ ] Generates correct signals for sample data
- [ ] Position sizing matches volatility target
- [ ] Monthly rebalancing triggers correctly

### Must Have
- Exact 252-day (12-month) lookback
- EWMA volatility with 21-day window
- 40% volatility target per instrument
- Equal-weight across instruments (after vol scaling)
- Signal capping at 0.95

### Must NOT Have
- No cross-sectional ranking (this is time-series)
- No stop-loss logic
- No regime filtering
- No transaction cost adjustments

---

## Implementation Details

### Directory Structure
```
quantconnect/Strategies/TrendFollowing/
├── TSMOM_Moskowitz2012.py
├── TSMOM_Moskowitz2012_config.json
├── TSMOM_Moskowitz2012_README.md
└── tests/
    └── test_TSMOM_Moskowitz2012.py
```

### Code Structure

```python
from AlgorithmImports import *
from quantconnect.Common.BaseStrategyAlgorithm import BaseStrategyAlgorithm
from quantconnect.Common.VolatilityCalculator import EWMA
from quantconnect.Common.PortfolioConstructor import volatility_scaled

class TSMOM_Moskowitz2012(BaseStrategyAlgorithm):
    def Initialize(self):
        # Load configuration
        self.SetStartDate(2000, 1, 1)
        self.SetEndDate(2024, 12, 31)
        self.SetCash(100000)
        
        # Parameters
        self.lookback_days = 252
        self.volatility_window = 21
        self.target_volatility = 0.40
        self.signal_cap = 0.95
        
        # Universe
        self.universe = self.GetUniverse()
        for symbol in self.universe:
            future = self.AddFuture(symbol)
            future.SetFilter(0, 182)  # Front month
    
    def GetUniverse(self):
        """Returns list of 58 futures symbols"""
        return [
            # Equity indices (24)
            "ES", "NQ", "YM", "RTY", "VX",  # US
            "VG", "DJ", "GX", "Z",  # Europe
            "NK", "TP", "TW", "SG",  # Asia
            "HI", "XU", "AE", "MX",  # Emerging
            "IB", "OM", "HE", "BTP", "SGI",  # Other
            # Currencies (9)
            "DX", "EC", "JY", "BP", "CD", "AD", "NE", "SF", "MP",
            # Commodities (17)
            "CL", "HO", "RB", "NG",  # Energy
            "GC", "SI", "HG", "PL", "PA",  # Metals
            "ZC", "ZS", "ZW", "ZL", "ZM", "ZO", "KC",  # Agriculture
            # Bonds (8)
            "ZB", "ZN", "ZF", "ZT", "UB", "GE", "DU", "OAT"
        ]
    
    def GenerateSignals(self):
        """Calculate 12-month return sign for each instrument"""
        signals = {}
        
        for symbol in self.universe:
            history = self.History(symbol, self.lookback_days + 1, Resolution.Daily)
            if len(history) < self.lookback_days:
                continue
            
            # Calculate 12-month return
            past_return = (history['close'].iloc[-1] / history['close'].iloc[0]) - 1
            
            # Signal is sign of past return
            signals[symbol] = np.sign(past_return)
        
        return signals
    
    def CalculateVolatility(self, symbol):
        """Calculate EWMA volatility"""
        history = self.History(symbol, self.volatility_window * 2, Resolution.Daily)
        returns = history['close'].pct_change().dropna()
        
        # EWMA volatility (annualized)
        vol = EWMA(returns.values, self.volatility_window)
        return vol * np.sqrt(252)  # Annualize
    
    def OnEndOfMonth(self):
        """Monthly rebalancing"""
        signals = self.GenerateSignals()
        
        for symbol, signal in signals.items():
            volatility = self.CalculateVolatility(symbol)
            
            if volatility > 0:
                # Volatility-scaled position
                target_weight = self.target_volatility / volatility * signal
                
                # Apply signal cap
                target_weight = max(min(target_weight, self.signal_cap), -self.signal_cap)
                
                # Set target portfolio percentage
                self.SetHoldings(symbol, target_weight)
```

### Configuration File

```json
{
  "strategy_name": "TSMOM_Moskowitz2012",
  "description": "Time-Series Momentum strategy from Moskowitz et al. (2012)",
  "parameters": {
    "lookback_days": 252,
    "volatility_window": 21,
    "target_volatility": 0.40,
    "signal_cap": 0.95,
    "rebalancing_freq": "monthly"
  },
  "universe": {
    "equity_indices": 24,
    "currencies": 9,
    "commodities": 17,
    "bonds": 8,
    "total": 58
  },
  "expected_performance": {
    "sharpe_ratio": 0.75,
    "annualized_return": "15-20% gross"
  },
  "reference": "Moskowitz, T.J., Ooi, Y.H. and Pedersen, L.H., 2012. 'Time series momentum.' Journal of Financial Economics, 104(2), pp.228-250."
}
```

---

## Acceptance Criteria

### Signal Calculation Tests
- [ ] Given 12 months of positive returns, signal = +1
- [ ] Given 12 months of negative returns, signal = -1
- [ ] Given flat returns, signal = 0 (or prior signal)
- [ ] Signals generated for all 58 instruments

### Volatility Calculation Tests
- [ ] EWMA volatility calculated with 21-day window
- [ ] Volatility annualized by sqrt(252)
- [ ] Volatility > 0 for all active instruments
- [ ] Reasonable volatility range (5% - 100%)

### Position Sizing Tests
- [ ] Position size = target_vol / instrument_vol × signal
- [ ] Position capped at ±0.95
- [ ] Long positions for positive signals
- [ ] Short positions for negative signals
- [ ] Total gross exposure reasonable (not excessive)

### Rebalancing Tests
- [ ] Rebalancing triggers monthly
- [ ] All positions updated on rebalance date
- [ ] No intra-month rebalancing

### Integration Tests
- [ ] Algorithm runs without errors
- [ ] Data subscriptions work
- [ ] Orders generated correctly
- [ ] Portfolio targets set

---

## QA Scenarios

### Scenario 1: Signal Generation Validation
**Tool**: Python unit test
**Preconditions**: Sample 13-month price data
**Steps**:
1. Load sample data with known 12-month return
2. Call GenerateSignals()
3. Verify signal matches expected sign
**Expected Result**: Signal equals sign of 12-month return
**Evidence**: Test output log

### Scenario 2: Volatility Calculation
**Tool**: Python unit test
**Preconditions**: Sample 21+ days of price data
**Steps**:
1. Load sample data
2. Calculate EWMA volatility
3. Compare to manual calculation
**Expected Result**: Within 0.1% of manual calc
**Evidence**: Test comparison output

### Scenario 3: Position Sizing
**Tool**: Python unit test
**Preconditions**: Known volatility and signal
**Steps**:
1. Set target_vol = 0.40, instrument_vol = 0.20, signal = +1
2. Calculate position size
3. Verify equals 2.0 (40%/20%)
**Expected Result**: Position size = 2.0
**Evidence**: Test assertion output

### Scenario 4: Monthly Rebalancing
**Tool**: LEAN backtest
**Preconditions**: Algorithm initialized
**Steps**:
1. Run backtest for 3 months
2. Log rebalancing dates
3. Verify trades only on month-end
**Expected Result**: Rebalancing occurs on last day of each month
**Evidence**: Trade log

---

## Dependencies

### Prerequisites
- Task 1-7 complete (infrastructure)
- BaseStrategyAlgorithm implemented
- VolatilityCalculator working
- PortfolioConstructor available

### Shared Components Used
- `BaseStrategyAlgorithm`
- `VolatilityCalculator.EWMA`
- `PortfolioConstructor.volatility_scaled`

---

## Estimated Effort

- **Development**: 4 hours
- **Testing**: 2 hours
- **Documentation**: 1 hour
- **Total**: 7 hours

---

## Notes

### Implementation Notes
- This is the foundational time-series momentum strategy
- Later strategies (Baltas 2020) build on this base
- 58 instruments require significant data
- Monthly rebalancing is critical for performance

### Potential Challenges
- LEAN futures data format vs. vivace library
- Contract rolling logic
- Performance with 58 instruments
- Memory management for 12-month history

### References
- Original Paper: https://doi.org/10.1016/j.jfineco.2011.11.003
- QuantConnect LEAN Docs: https://www.quantconnect.com/docs/v2/

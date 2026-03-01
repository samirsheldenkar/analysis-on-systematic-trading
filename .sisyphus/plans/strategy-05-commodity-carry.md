# Strategy Implementation Plan: S05 - Commodity Term Structure / Carry

## TL;DR

> **Koijen et al. (2018) Commodity Carry Strategy**
>
> **Signal**: Term structure slope (backwardation = positive carry)
> **Logic**: Long backwardated, short contango commodities
> **Sizing**: Tercile-based (top/bottom 33%)
> **Universe**: 26 commodities (Hollstein 2020)
> **Rebalancing**: Monthly
> **Expected Sharpe**: 0.495 (with smoothing), 0.640 (without)

---

## Context

### Original Reference
Koijen, R.S., Moskowitz, T.J., Pedersen, L.H. and Vrugt, E.B., 2018. "Carry." Journal of Financial Economics, 127(2), pp.197-225.

### Core Concept
The commodity carry strategy exploits the term structure of futures prices. Assets in backwardation (front month > back month) tend to have positive roll yields, while assets in contango tend to have negative roll yields. The strategy goes long backwardated commodities and short contango commodities.

**Carry**: Return assuming futures prices stay constant
**Backwardation**: Futures price < Spot price (positive carry)
**Contango**: Futures price > Spot price (negative carry)

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

**Key Finding**: Carry smoothing significantly changes risk/return profile.

---

## Implementation Requirements

### Input Data
- Daily futures price data for 26 commodities
- Front and second contracts for each
- Contract specifications for expiry

### Output Signals
- Carry signal per commodity (continuous value)
- Ranked positions
- Long/short/flat signals

### LEAN Components

**Algorithm Class:**
```python
class CommodityCarry(BaseStrategyAlgorithm):
    def __init__(self):
        self.expiry_shift = 1
        self.sma_window = 252
        self.rebalancing_freq = 'monthly'
        self.selection_method = 'terciles'
```

**Special Requirements:**
- Access to multiple contract months
- Calculate carry from front vs. second contract
- Rank across commodities
- Tercile selection

---

## Implementation Details

### Code Structure

```python
from AlgorithmImports import *
from quantconnect.Common.BaseStrategyAlgorithm import BaseStrategyAlgorithm

class CommodityCarry(BaseStrategyAlgorithm):
    def Initialize(self):
        self.SetStartDate(2000, 1, 1)
        self.SetCash(100000)
        
        # Parameters
        self.expiry_shift = 1
        self.sma_window = 252
        self.use_smoothing = True
        self.annualization_factor = 4  # Quarterly contracts
        
        # Universe: 26 commodities
        self.universe = [
            'CL',  # Crude Oil
            'HO',  # Heating Oil
            'RB',  # RBOB Gasoline
            'NG',  # Natural Gas
            'GC',  # Gold
            'SI',  # Silver
            'HG',  # Copper
            'PL',  # Platinum
            'PA',  # Palladium
            'ZC',  # Corn
            'ZS',  # Soybeans
            'ZW',  # Wheat
            'ZL',  # Soybean Oil
            'ZM',  # Soybean Meal
            'ZO',  # Oats
            'KC',  # Coffee
            'CT',  # Cotton
            'SB',  # Sugar
            'CC',  # Cocoa
            'LC',  # Live Cattle
            'LN',  # Lean Hogs
            'GF',  # Feeder Cattle
            'KC',  # Coffee
            'DX',  # Not commodity, but included
        ]
        
        for symbol in self.universe:
            future = self.AddFuture(symbol)
            # Allow selection of front and second contracts
            future.SetFilter(0, 90)
    
    def CalculateCarry(self, symbol):
        """Calculate carry signal for a commodity"""
        # Get chain for this future
        chain = self.FutureChain(symbol)
        
        if len(chain) < 2:
            return None
        
        # Get front and second contracts
        front_contract = chain[0]
        second_contract = chain[1]
        
        # Get prices
        front_price = self.Securities[front_contract.Symbol].Price
        second_price = self.Securities[second_contract.Symbol].Price
        
        if front_price <= 0 or second_price <= 0:
            return None
        
        # Calculate carry
        carry = np.log(front_price / second_price) * self.annualization_factor
        
        return carry
    
    def CalculateSmoothedCarry(self, symbol):
        """Calculate 252-day SMA of carry"""
        if not self.use_smoothing:
            return self.CalculateCarry(symbol)
        
        # Get historical carry values
        carry_history = []
        
        for day in range(self.sma_window):
            date = self.Time - timedelta(days=day)
            # Note: In practice, need to handle historical data properly
            # This is simplified
            carry = self.CalculateCarry(symbol)
            if carry is not None:
                carry_history.append(carry)
        
        if len(carry_history) < self.sma_window / 2:
            return None
        
        smoothed_carry = np.mean(carry_history[-self.sma_window:])
        return smoothed_carry
    
    def GenerateSignals(self):
        """Generate carry signals for all commodities"""
        carry_signals = {}
        
        for symbol in self.universe:
            carry = self.CalculateSmoothedCarry(symbol)
            if carry is not None:
                carry_signals[symbol] = carry
        
        return carry_signals
    
    def ConstructPortfolio(self, carry_signals):
        """Construct portfolio using tercile selection"""
        if len(carry_signals) < 6:  # Need at least 6 for terciles
            return {}
        
        # Rank by carry
        ranked = sorted(carry_signals.items(), key=lambda x: x[1])
        n = len(ranked)
        
        # Tercile boundaries
        tercile_size = n // 3
        
        long_symbols = [s for s, _ in ranked[-tercile_size:]]  # Top tercile
        short_symbols = [s for s, _ in ranked[:tercile_size]]  # Bottom tercile
        
        # Equal weight within terciles
        long_weight = 1.0 / len(long_symbols) if long_symbols else 0
        short_weight = -1.0 / len(short_symbols) if short_symbols else 0
        
        targets = {}
        for symbol in long_symbols:
            targets[symbol] = long_weight
        for symbol in short_symbols:
            targets[symbol] = short_weight
        
        return targets
    
    def OnEndOfMonth(self):
        """Monthly rebalancing"""
        carry_signals = self.GenerateSignals()
        targets = self.ConstructPortfolio(carry_signals)
        
        for symbol, target in targets.items():
            self.SetHoldings(symbol, target)
```

### Configuration File

```json
{
  "strategy_name": "CommodityCarry",
  "description": "Commodity carry strategy from Koijen et al. (2018)",
  "parameters": {
    "expiry_shift": 1,
    "sma_window": 252,
    "use_smoothing": true,
    "annualization_factor": 4,
    "rebalancing_freq": "monthly",
    "selection_method": "terciles"
  },
  "universe": {
    "count": 26,
    "categories": ["energy", "metals", "agriculture", "livestock"]
  },
  "performance": {
    "cagr_smoothed": "5.69%",
    "cagr_unsmoothed": "10.4%",
    "sharpe_smoothed": 0.495,
    "sharpe_unsmoothed": 0.640,
    "max_dd_smoothed": "33.8%",
    "max_dd_unsmoothed": "51.0%"
  },
  "reference": "Koijen, R.S., Moskowitz, T.J., Pedersen, L.H. and Vrugt, E.B., 2018. 'Carry.' Journal of Financial Economics, 127(2), pp.197-225."
}
```

---

## Acceptance Criteria

### Carry Calculation Tests
- [ ] Carry calculated as log(F1/F2) × 4
- [ ] Handles missing contract data
- [ ] Returns None for insufficient data
- [ ] Values reasonable (typical range: -50% to +50%)

### Smoothing Tests
- [ ] 252-day SMA calculated correctly
- [ ] Can be disabled via config
- [ ] Handles missing historical data

### Portfolio Construction Tests
- [ ] Top tercile selected for long
- [ ] Bottom tercile selected for short
- [ ] Equal weights within terciles
- [ ] Handles small universe sizes

### Rebalancing Tests
- [ ] Monthly rebalancing triggers
- [ ] All positions updated
- [ ] Smooth transitions

---

## Dependencies

### Prerequisites
- Task 1-7 (infrastructure)
- Access to futures chain data
- Multiple contract month support

### Unique Requirements
- Contract expiry handling
- Front/second contract selection
- Cross-sectional ranking

---

## Estimated Effort

- **Development**: 5 hours
- **Testing**: 3 hours
- **Documentation**: 1 hour
- **Total**: 9 hours

---

## Notes

### Implementation Notes
- Requires access to futures chain (multiple contracts)
- Carry smoothing significantly affects results
- Contract rolling must be handled
- Tercile selection requires sufficient universe size

### Key Insights from Paper
1. Carry predicts returns across asset classes
2. Carry captures risk premia for recession, liquidity, volatility
3. Commodity carry reflects convenience yield and storage costs
4. Smoothing reduces noise from seasonal effects

### References
- Koijen et al. (2018) - Main paper
- Hollstein et al. (2020) - Universe specification

# QuantConnect Implementation Plan V2 - Notepad

## Inherited Wisdom

### Plan Status
- **Progress**: 10/27 tasks completed
- **Current Work**: Phase 0, Task 0.1 - Build Reference LEAN Futures Algorithm
- **Worktree**: `/home/samir/analysis-on-systematic-trading-worktree`

### Key Decisions from Plan
1. **Casing**: PascalCase (matching LEAN C# docs)
2. **Scope**: 18 strategies (reduced from 24)
3. **Base Class Hierarchy**: 5-class structure
4. **Constants**: ANN_FACTOR_TRADING_DAYS=252, etc.

### Branch Strategy
- Current branch: `phase-0-ground-truth`
- All work happens in worktree at `/home/samir/analysis-on-systematic-trading-worktree`

---

## Task 0.1: Reference LEAN Futures Algorithm

### Requirements
- [ ] Subscribes to 3+ futures using correct `Futures.*` enums
- [ ] Uses `SetFilter(timedelta, timedelta)`
- [ ] Accesses `data.FutureChains` in `OnData`
- [ ] Requests history with `Resolution.DAILY`
- [ ] Uses `SetHoldings(symbol, target)` for position sizing
- [ ] Schedules monthly rebalancing with `Schedule.On`
- [ ] Uses `SetWarmUp(timedelta)`
- [ ] **Verifiable**: Runs in LEAN without errors

### API Patterns from Research
```python
# Futures setup
self.future = self.add_future(
    Futures.Indices.SP_500_E_MINI,
    extended_market_hours=True,
    data_normalization_mode=DataNormalizationMode.BACKWARDS_RATIO,
    data_mapping_mode=DataMappingMode.OPEN_INTEREST
)

# Filter for front month
self.future.set_filter(lambda u: u.front_month())

# Access chain
chain = slice.future_chains.get(self.future.symbol)

# Schedule monthly
self.schedule.on(self.date_rules.month_start(), self.time_rules.at(9, 31), self.rebalance)

# Warmup
self.set_warm_up(timedelta(7))

# Set holdings
self.set_holdings(symbol, weight)
```

---

## Task 0.2: Universe Mappings
- Create `Common/universes.py`
- MOSKOWITZ_2012: 58 futures
- HOLLSTEIN_2020: 24 commodities

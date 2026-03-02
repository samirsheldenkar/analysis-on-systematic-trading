"""
Reference LEAN Futures Algorithm

This is a reference implementation demonstrating proper LEAN v2 Python API patterns
for futures trading algorithms. It serves as a template and ground truth for all
subsequent strategy implementations in the QuantConnect LEAN framework.

Key Patterns Demonstrated:
- Multiple futures subscriptions using Futures.* enums
- SetFilter with timedelta for universe selection
- Accessing futures chains via slice.futures_chains
- History requests with Resolution.DAILY
- SetHoldings for position sizing
- Scheduled monthly rebalancing
- Warmup period configuration

Usage:
    This algorithm can be run directly in QuantConnect LEAN backtester.
    It demonstrates the core patterns used by all strategies in this project.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

from AlgorithmImports import *


class ReferenceFuturesAlgorithm(QCAlgorithm):
    """
    Reference algorithm demonstrating LEAN v2 Python API patterns for futures trading.

    This algorithm subscribes to multiple futures, uses monthly rebalancing,
    and demonstrates proper patterns for position sizing and warmup.
    """

    def initialize(self) -> None:
        """
        Initialize the algorithm configuration.

        Sets up:
        - Start and end dates for backtesting
        - Cash account balance
        - Multiple futures subscriptions
        - Contract filters
        - Warmup period
        - Scheduled monthly rebalancing
        """
        # Set backtest date range
        self.set_start_date(2020, 1, 1)
        self.set_end_date(2024, 12, 31)

        # Set initial cash
        self.set_cash(1_000_000)

        # Set warmup period to ensure indicators have sufficient history
        # Using 30 days to cover most lookback periods
        self.set_warm_up(timedelta(days=30))

        # Subscribe to multiple futures using Futures.* enums
        # Using 4 futures across different asset classes for diversification
        self.future_es = self.add_future(Futures.Indices.SP_500_E_MINI)
        self.future_nq = self.add_future(Futures.Indices.NASDAQ_100_E_MINI)
        self.future_gc = self.add_future(Futures.Metals.GOLD)
        self.future_cl = self.add_future(Futures.Energy.CRUDE_OIL_WTI)

        # Set filter for each future using SetFilter with timedelta
        # This selects contracts within 0-62 days to expiration (front month)
        # First timedelta: minimum days to expiration
        # Second timedelta: maximum days to expiration
        self.future_es.set_filter(timedelta(0), timedelta(62))
        self.future_nq.set_filter(timedelta(0), timedelta(62))
        self.future_gc.set_filter(timedelta(0), timedelta(62))
        self.future_cl.set_filter(timedelta(0), timedelta(62))

        # Store futures symbols for easy access
        self.future_symbols = [
            self.future_es.symbol,
            self.future_nq.symbol,
            self.future_gc.symbol,
            self.future_cl.symbol,
        ]

        # Target allocation per future (equal weight)
        self.target_weight = 0.20  # 20% per future = 80% total, 20% cash

        # Schedule monthly rebalancing
        # Fires on first trading day of each month at 9:31 AM market open
        self.schedule.on(
            self.date_rules.month_start(), self.time_rules.at(9, 31), self.rebalance
        )

        # Track rebalance count for logging
        self.rebalance_count = 0

    def on_data(self, data: Slice) -> None:
        """
        Called on each new data point.

        Accesses futures chains to get contract information.
        This demonstrates the proper pattern for accessing future chains.

        Args:
            data: Slice object containing current market data
        """
        # Skip during warmup period
        if self.is_warming_up:
            return

        # Access futures chains via slice.futures_chains
        # This provides dictionary of continuous_symbol -> futures chain
        for continuous_symbol in self.future_symbols:
            chain = data.futures_chains.get(continuous_symbol)

            if chain is None:
                continue

            # Iterate through contracts in the chain
            for contract in chain:
                # Access contract properties:
                # - contract.symbol: the specific contract symbol
                # - contract.expiry: contract expiration date
                # - contract.open_interest: open interest
                # - contract.last_price: last traded price
                # - contract.bid_price, contract.ask_price: quote prices
                pass  # Placeholder for strategy-specific logic

    def rebalance(self) -> None:
        """
        Monthly rebalancing function called by schedule.

        Uses SetHoldings for position sizing which handles:
        - Portfolio weight allocation
        - Order sizing based on current portfolio value
        - Automatic risk management via leverage limits
        """
        self.rebalance_count += 1
        self.log(f"Rebalancing #{self.rebalance_count} at {self.time}")

        # Get current portfolio value
        portfolio_value = self.portfolio.total_value

        # Prepare list of holdings targets
        targets = []

        for symbol in self.future_symbols:
            # Get the mapped contract (continuous future contract)
            # The mapped contract handles rollover automatically
            future_obj = None

            if symbol == self.future_es.symbol:
                future_obj = self.future_es
            elif symbol == self.future_nq.symbol:
                future_obj = self.future_nq
            elif symbol == self.future_gc.symbol:
                future_obj = self.future_gc
            elif symbol == self.future_cl.symbol:
                future_obj = self.future_cl

            if future_obj and future_obj.mapped:
                targets.append(PortfolioTarget(future_obj.mapped, self.target_weight))

        # Execute SetHoldings with multiple targets
        # liquidateExistingHoldings=False to keep positions from previous month
        if targets:
            self.set_holdings(targets, liquidate_existing_holdings=False)

    def request_history_example(self) -> None:
        """
        Example of requesting historical futures data.

        Demonstrates the history request pattern for futures:
        - Use FutureUniverse type for chain data
        - Specify Resolution.DAILY for daily bars
        - Use flatten=True for DataFrame format
        """
        # Request 21 days of history for ES futures
        # Returns FutureUniverse objects containing all contracts for each day
        history = self.history[FutureUniverse](
            self.future_es.symbol, 21, Resolution.DAILY
        )

        # Process history
        for future_universe in history:
            for contract in future_universe:
                # Access historical contract data
                close_price = contract.close
                open_interest = contract.open_interest
                timestamp = future_universe.end_time

    def on_end_of_algorithm(self) -> None:
        """
        Called at the end of the algorithm run.

        Logs final statistics for analysis.
        """
        self.log(f"Algorithm completed. Total rebalances: {self.rebalance_count}")
        self.log(f"Final portfolio value: ${self.portfolio.total_value:,.2f}")


# Alternative implementation using data.FutureChains (older pattern)
class ReferenceFuturesAlgorithmAlt(QCAlgorithm):
    """
    Alternative reference using older data.FutureChains pattern.

    This demonstrates an alternative pattern for accessing futures data
    that some algorithms may still use.
    """

    def initialize(self) -> None:
        """Initialize the alternative algorithm."""
        self.set_start_date(2020, 1, 1)
        self.set_end_date(2024, 12, 31)
        self.set_cash(1_000_000)
        self.set_warm_up(timedelta(days=30))

        # Add futures
        self.future_es = self.add_future(Futures.Indices.SP_500_E_MINI)
        self.future_nq = self.add_future(Futures.Indices.NASDAQ_100_E_MINI)
        self.future_gc = self.add_future(Futures.Metals.GOLD)

        # Set filter using lambda (alternative pattern)
        self.future_es.set_filter(lambda u: u.front_month())
        self.future_nq.set_filter(lambda u: u.front_month())
        self.future_gc.set_filter(lambda u: u.front_month())

        # Schedule rebalancing
        self.schedule.on(
            self.date_rules.month_start(), self.time_rules.at(9, 31), self.rebalance
        )

    def on_data(self, data: Slice) -> None:
        """
        Alternative pattern using data.future_chains.

        Note: slice.futures_chains and data.future_chains are equivalent
        in the current LEAN API.
        """
        if self.is_warming_up:
            return

        # Using data.future_chains instead of slice.futures_chains
        for symbol, chain in data.future_chains.items():
            for contract in chain:
                # Process contract data
                pass

    def rebalance(self) -> None:
        """Execute rebalancing using SetHoldings."""
        # Use single-symbol SetHoldings pattern
        if self.future_es.mapped:
            self.set_holdings(self.future_es.mapped, 0.33)
        if self.future_nq.mapped:
            self.set_holdings(self.future_nq.mapped, 0.33)
        if self.future_gc.mapped:
            self.set_holdings(self.future_gc.mapped, 0.33)

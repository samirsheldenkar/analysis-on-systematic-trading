# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean Algorithmic Trading Engine v2.0.
# Copyright 2014 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from AlgorithmImports import *
from datetime import time
from BaseStrategyAlgorithm import BaseStrategyAlgorithm


class IntradayStrategyAlgorithm(BaseStrategyAlgorithm):
    """
    Base class for intraday trading strategies.

    Strategies that trade within a single trading day, using minute or
    second resolution data and scheduled rebalancing events.

    Suitable for:
    - S14: ETF Intraday Momentum
    """

    def Initialize(self):
        """
        Initialize the intraday strategy.

        Call super().Initialize() and add strategy-specific setup.
        """
        super().Initialize()

    def IntradaySignal(self, symbol: Symbol, data: Slice) -> int:
        """
        Generate intraday trading signal for a security.

        Args:
            symbol: The security to generate signal for
            data: Current minute/bar data

        Returns:
            int: Signal value (-1, 0, 1)
        """
        return 0

    def ScheduleIntradayRebalance(self, rebalanceTime: time):
        """
        Schedule intraday rebalancing event.

        Args:
            rebalanceTime: Time of day to rebalance (e.g., time(9, 45))
        """
        self.Schedule.On(
            self.DateRules.EveryDay(),
            self.TimeRules.At(rebalanceTime.hour, rebalanceTime.minute),
            self.Rebalance,
        )

    def ScheduleMarketCloseExit(self, exitTime: time):
        """
        Schedule position exit before market close.

        Args:
            exitTime: Time to exit positions (e.g., time(15, 45))
        """
        self.Schedule.On(
            self.DateRules.EveryDay(),
            self.TimeRules.At(exitTime.hour, exitTime.minute),
            self.ClosePositions,
        )

    def ClosePositions(self):
        """
        Close all positions at end of trading day.

        Override in subclasses to implement specific exit logic.
        """
        pass

    def CalculateIntradayReturns(
        self, symbol: Symbol, lookbackMinutes: int = 60
    ) -> float:
        """
        Calculate intraday return for a security.

        Args:
            symbol: The security to calculate return for
            lookbackMinutes: Number of minutes to look back

        Returns:
            float: Intraday return
        """
        return 0.0

    def ApplyIntradayVolatilityFilter(self, signal: int, intradayVol: float) -> int:
        """
        Apply volatility filter to intraday signal.

        Args:
            signal: Raw signal value
            intradayVol: Intraday volatility measure

        Returns:
            int: Filtered signal value
        """
        return signal

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
from datetime import timedelta


class BaseStrategyAlgorithm(QCAlgorithm):
    """
    Abstract base class for all QuantConnect strategy algorithms.

    Provides common initialization patterns, warmup handling, and rebalancing
    infrastructure that all strategy types inherit from.

    Inherit from this class to implement specific strategy types:
    - TimeSeriesStrategyAlgorithm: For time-series momentum strategies
    - CrossSectionalStrategyAlgorithm: For cross-sectional ranking strategies
    - SpreadStrategyAlgorithm: For spread trading strategies
    - IntradayStrategyAlgorithm: For intraday trading strategies
    """

    def Initialize(self):
        """
        Initialize the algorithm. Must be implemented by subclasses.

        Sets up:
        - Start and end dates
        - Cash amount
        - Security subscriptions
        - Universe selection
        - Brokerage model
        - Fee model
        - Warmup period
        """
        raise NotImplementedError("Subclasses must implement Initialize()")

    def SetWarmUp(self, lookbackPeriod: int = 252):
        """
        Configure warmup period for historical data.

        Args:
            lookbackPeriod: Number of trading days to warmup (default: 252 = 1 year)
        """
        warmupPeriod = timedelta(days=lookbackPeriod + 30)
        self.SetWarmUp(warmupPeriod)

    def Rebalance(self):
        """
        Stub method for portfolio rebalancing.

        Override in subclasses to implement specific rebalancing logic.
        Called by scheduled events or signal triggers.
        """
        pass

    def OnData(self, data: Slice):
        """
        Event handler for new data.

        Args:
            data: Current slice of market data
        """
        pass

    def OnEndOfDay(self, symbol: Symbol = None):
        """
        Event handler for end of trading day.

        Args:
            symbol: Optional symbol to filter by
        """
        pass

    def OnEndOfMonth(self):
        """
        Event handler for end of month.

        Override in subclasses to implement month-end rebalancing.
        """
        pass

    def OnEndOfAlgorithm(self):
        """
        Event handler called when algorithm ends.

        Use for cleanup and final reporting.
        """
        pass

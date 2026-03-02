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
from typing import List, Optional


class DataProvider:
    """
    Utility class for data access in QuantConnect strategies.

    Provides methods for fetching historical data and retrieving
    current prices for securities.
    """

    def __init__(self, algorithm: QCAlgorithm):
        """
        Initialize the DataProvider.

        Args:
            algorithm: The QCAlgorithm instance for data access
        """
        self.Algorithm = algorithm

    def GetHistory(
        self,
        symbol: Symbol,
        lookbackPeriod: int = 252,
        resolution: Resolution = Resolution.Daily,
    ) -> pd.DataFrame:
        """
        Get historical price data for a symbol.

        Args:
            symbol: The security symbol
            lookbackPeriod: Number of periods to look back
            resolution: Data resolution (default: Daily)

        Returns:
            DataFrame with historical price data
        """
        raise NotImplementedError("GetHistory is not yet implemented")

    def GetCurrentPrice(self, symbol: Symbol) -> float:
        """
        Get the current price for a symbol.

        Args:
            symbol: The security symbol

        Returns:
            Current price or None if not available
        """
        raise NotImplementedError("GetCurrentPrice is not yet implemented")

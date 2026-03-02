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
from BaseStrategyAlgorithm import BaseStrategyAlgorithm


class SpreadStrategyAlgorithm(BaseStrategyAlgorithm):
    """
    Base class for spread trading strategies.

    Strategies that trade the spread between two related securities,
    typically relying on mean reversion or cointegration.

    Suitable for:
    - S11: Soybean Crush Spread
    - S12: Petroleum Crack Spread
    """

    def Initialize(self):
        """
        Initialize the spread trading strategy.

        Call super().Initialize() and add strategy-specific setup.
        """
        super().Initialize()

    def CalculateSpread(
        self, leg1Symbol: Symbol, leg2Symbol: Symbol, data: Slice
    ) -> float:
        """
        Calculate the spread between two securities.

        Args:
            leg1Symbol: First leg of the spread
            leg2Symbol: Second leg of the spread
            data: Current market data

        Returns:
            float: Spread value
        """
        return 0.0

    def CheckForMeanReversion(
        self, spreadHistory: list, zScoreThreshold: float = 2.0
    ) -> str:
        """
        Check if spread is in mean reversion territory.

        Args:
            spreadHistory: Historical spread values
            zScoreThreshold: Z-score threshold for signals

        Returns:
            str: "long", "short", or "neutral"
        """
        return "neutral"

    def CalculateZScore(self, spreadHistory: list) -> float:
        """
        Calculate z-score of current spread relative to history.

        Args:
            spreadHistory: Historical spread values

        Returns:
            float: Z-score
        """
        return 0.0

    def CalculateHedgeRatio(self, leg1Prices: list, leg2Prices: list) -> float:
        """
        Calculate optimal hedge ratio for spread.

        Args:
            leg1Prices: Historical prices for leg 1
            leg2Prices: Historical prices for leg 2

        Returns:
            float: Hedge ratio
        """
        return 1.0

    def ExecuteSpreadTrade(
        self, leg1Symbol: Symbol, leg2Symbol: Symbol, hedgeRatio: float, direction: str
    ):
        """
        Execute spread trade with legs.

        Args:
            leg1Symbol: First leg symbol
            leg2Symbol: Second leg symbol
            hedgeRatio: Hedge ratio between legs
            direction: "long" or "short" the spread
        """
        pass

    def CloseSpreadPositions(self, leg1Symbol: Symbol, leg2Symbol: Symbol):
        """
        Close all spread positions.

        Args:
            leg1Symbol: First leg symbol
            leg2Symbol: Second leg symbol
        """
        pass

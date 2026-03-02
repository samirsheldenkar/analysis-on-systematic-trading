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


class CrossSectionalStrategyAlgorithm(BaseStrategyAlgorithm):
    """
    Base class for cross-sectional ranking strategies.

    Strategies that rank, compare, or weight securities relative to each
    other, rather than on an absolute basis.

    Suitable for:
    - S05: Commodity Carry
    - S06: Commodity Momentum
    - S07: Commodity Skewness
    - S08: Intra-Curve
    - S09: Basis Momentum
    - S10: Basis Reversal
    - S16: FX Carry
    - S17: Cross-Asset Skew
    """

    def Initialize(self):
        """
        Initialize the cross-sectional strategy.

        Call super().Initialize() and add strategy-specific setup.
        """
        super().Initialize()

    def RankAssets(self, metrics: dict) -> list:
        """
        Rank assets based on cross-sectional metrics.

        Args:
            metrics: Dictionary mapping Symbol to metric value

        Returns:
            list: List of Symbols sorted by metric (highest to lowest)
        """
        sortedAssets = sorted(metrics.items(), key=lambda x: x[1], reverse=True)
        return [symbol for symbol, _ in sortedAssets]

    def CalculateCrossSectionalWeights(self, rankedAssets: list) -> dict:
        """
        Calculate portfolio weights based on cross-sectional ranking.

        Args:
            rankedAssets: List of Symbols sorted by signal strength

        Returns:
            dict: Dictionary mapping Symbol to weight
        """
        weights = {}
        return weights

    def SelectTopN(self, rankedAssets: list, n: int) -> list:
        """
        Select top N assets from ranked list.

        Args:
            rankedAssets: List of ranked Symbols
            n: Number of assets to select

        Returns:
            list: Top N Symbols
        """
        return rankedAssets[:n]

    def SelectBottomN(self, rankedAssets: list, n: int) -> list:
        """
        Select bottom N assets from ranked list.

        Args:
            rankedAssets: List of ranked Symbols
            n: Number of assets to select

        Returns:
            list: Bottom N Symbols
        """
        return rankedAssets[-n:]

    def CalculateLongShortWeights(self, longAssets: list, shortAssets: list) -> dict:
        """
        Calculate equal-weight long/short positions.

        Args:
            longAssets: List of Symbols to go long
            shortAssets: List of Symbols to go short

        Returns:
            dict: Dictionary mapping Symbol to weight
        """
        weights = {}
        return weights

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


class FeeConfigurator:
    """
    Utility class for configuring brokerage models and fees in QuantConnect strategies.

    Provides methods for setting up brokerage models and customizing
    fee structures for different security types.
    """

    def __init__(self, algorithm: QCAlgorithm):
        """
        Initialize the FeeConfigurator.

        Args:
            algorithm: The QCAlgorithm instance to configure
        """
        self.Algorithm = algorithm

    def ConfigureBrokerageModel(
        self, brokerage: str = "Default", accountType: str = "Margin"
    ):
        """
        Configure the brokerage model for the algorithm.

        Args:
            brokerage: Brokerage name (default: "Default")
            accountType: Account type - "Cash" or "Margin" (default: "Margin")
        """
        raise NotImplementedError("ConfigureBrokerageModel is not yet implemented")

    def SetFees(
        self,
        securityType: SecurityType,
        feePerContract: float = None,
        percentage: float = None,
    ):
        """
        Set custom fees for a specific security type.

        Per plan requirements, allows customization of fees including
        per-contract fees for futures and percentage-based fees.

        Args:
            securityType: Type of security to configure
            feePerContract: Fee per contract (for futures/options)
            percentage: Percentage fee (for equities)
        """
        raise NotImplementedError("SetFees is not yet implemented")

from typing import List

# Note: Import Futures from AlgorithmImports in your LEAN algorithm:
#   from AlgorithmImports import Futures
#
# Usage:
#   for future in MOSKOWITZ_2012:
#       self.AddFuture(future)

# =============================================================================
# MOSKOWITZ 2012 - 58 Liquid Futures
# Reference: "Time Series Momentum" (Moskowitz, Ooi, Pedersen, 2012)
# Breakdown: 24 equity indices, 9 currencies, 17 commodities, 8 bonds
# =============================================================================

MOSKOWITZ_2012: List[str] = [
    # -------------------------------------------------------------------------
    # Equity Index Futures (24)
    # -------------------------------------------------------------------------
    # US Indices
    "SP_500_E_MINI",  # ES - E-mini S&P 500
    "NASDAQ_100_E_MINI",  # NQ - E-mini NASDAQ 100
    "DOW_30_E_MINI",  # YM - E-mini Dow Jones 30
    "RUSSELL_2000_E_MINI",  # RTY - E-mini Russell 2000
    "VIX",  # VX - CBOE Volatility Index
    "SP_400_MID_CAP_E_MINI",  # EMD - E-mini S&P MidCap 400
    # European Indices
    "EURO_STOXX_50",  # FESX - Euro Stoxx 50
    "FTSE_100_E_MINI",  # FT1 - E-mini FTSE 100 (GBP)
    # Asian Indices
    "NIKKEI_225_DOLLAR",  # NKD - Nikkei-225 Dollar
    "NIKKEI_225_YEN_CME",  # NIY - Nikkei-225 Yen (CME)
    "HANG_SENG",  # HSI - Hang Seng Index
    "TOPIX_USD",  # TPD - USD Denominated Topix
    # Emerging Market Indices
    "MSCI_TAIWAN_INDEX",  # TW - MSCI Taiwan
    "MSCI_EMERGING_MARKETS_INDEX",  # MXEF - MSCI Emerging Markets
    "MSCI_ASIA_PACIFIC_EX_JAPAN_NTR",  # MXAJ - MSCI Asia Pacific ex Japan
    "FTSE_CHINA_50_E_MINI",  # FT5 - E-mini FTSE China 50
    # Sector/Specialty Indices
    "DOW_JONES_REAL_ESTATE",  # RX - Dow Jones Real Estate
    "SP_500_ANNUAL_DIVIDEND_INDEX",  # SDA - S&P 500 Annual Dividend
    "BLOOMBERG_COMMODITY_INDEX",  # AW - Bloomberg Commodity Index
    "SP_GSCI_COMMODITY",  # GD - S&P-GSCI Commodity Index
    # Indian Indices
    "NIFTY_50",  # NIFTY - NSE Nifty 50
    "BANK_NIFTY",  # BANKNIFTY - NSE BankNifty
    "BSE_SENSEX",  # SENSEX - S&P BSE Sensex
    # Additional Index
    "MICRO_RUSSELL_2000_E_MINI",  # M2K - Micro E-mini Russell 2000
    # -------------------------------------------------------------------------
    # Currency Futures (9)
    # -------------------------------------------------------------------------
    "EUR",  # 6E - Euro FX
    "GBP",  # 6B - British Pound
    "JPY",  # 6J - Japanese Yen
    "CHF",  # 6S - Swiss Franc
    "AUD",  # 6A - Australian Dollar
    "CAD",  # 6C - Canadian Dollar
    "NZD",  # 6N - New Zealand Dollar
    "USD",  # DX - U.S. Dollar Index
    "MXN",  # 6M - Mexican Peso
    # -------------------------------------------------------------------------
    # Commodity Futures (17)
    # -------------------------------------------------------------------------
    # Energy (5)
    "CRUDE_OIL_WTI",  # CL - WTI Crude Oil
    "BRENT_CRUDE",  # B - Brent Crude
    "NATURAL_GAS",  # NG - Natural Gas
    "HEATING_OIL",  # HO - Heating Oil
    "GASOLINE",  # RB - RBOB Gasoline
    # Metals (5)
    "GOLD",  # GC - Gold
    "SILVER",  # SI - Silver
    "COPPER",  # HG - Copper
    "PLATINUM",  # PL - Platinum
    "PALLADIUM",  # PA - Palladium
    # Grains (4)
    "CORN",  # ZC - Corn
    "SOYBEANS",  # ZS - Soybeans
    "WHEAT",  # ZW - SRW Wheat
    "OATS",  # ZO - Oats
    # Meats (3)
    "LIVE_CATTLE",  # LE - Live Cattle
    "FEEDER_CATTLE",  # GF - Feeder Cattle
    "LEAN_HOGS",  # HE - Lean Hogs
    # -------------------------------------------------------------------------
    # Bond Futures (8)
    # -------------------------------------------------------------------------
    "Y_30_TREASURY_BOND",  # ZB - 30Y US Treasury Bond
    "Y_10_TREASURY_NOTE",  # ZN - 10Y US Treasury Note
    "Y_5_TREASURY_NOTE",  # ZF - 5Y US Treasury Note
    "Y_2_TREASURY_NOTE",  # ZT - 2Y US Treasury Note
    "EURO_DOLLAR",  # GE - Eurodollar
    "ULTRA_US_TREASURY_BOND",  # UB - Ultra 30Y US Treasury Bond
    "ULTRA_10_YEAR_US_TREASURY_NOTE",  # TN - Ultra 10Y US Treasury Note
    "FIVE_YEAR_USD_MAC_SWAP",  # F1U - 5Y USD MAC Swap
]


# =============================================================================
# HOLLSTEIN 2020 - 24 Commodity Futures
# Reference: "Anomalies in commodity futures markets: Risk or mispricing?"
# (Hollstein, Prokopczuk, Tharann, 2020)
# Note: Excludes FX futures - commodities only
# =============================================================================

HOLLSTEIN_2020: List[str] = [
    # -------------------------------------------------------------------------
    # Energy (5)
    # -------------------------------------------------------------------------
    "CRUDE_OIL_WTI",  # CL - WTI Crude Oil
    "BRENT_CRUDE",  # B - Brent Crude
    "NATURAL_GAS",  # NG - Natural Gas
    "HEATING_OIL",  # HO - Heating Oil
    "GASOLINE",  # RB - RBOB Gasoline
    # -------------------------------------------------------------------------
    # Metals (6)
    # -------------------------------------------------------------------------
    "GOLD",  # GC - Gold
    "SILVER",  # SI - Silver
    "COPPER",  # HG - Copper
    "PLATINUM",  # PL - Platinum
    "PALLADIUM",  # PA - Palladium
    "ALUMINUM_M_WUS_TRANSACTION_PREMIUM_PLATTS_25_MT",  # AUP - Aluminum
    # -------------------------------------------------------------------------
    # Grains (6)
    # -------------------------------------------------------------------------
    "CORN",  # ZC - Corn
    "SOYBEANS",  # ZS - Soybeans
    "WHEAT",  # ZW - SRW Wheat
    "HRW_WHEAT",  # KE - KC HRW Wheat
    "OATS",  # ZO - Oats
    "SOYBEAN_MEAL",  # ZM - Soybean Meal
    # -------------------------------------------------------------------------
    # Meats (3)
    # -------------------------------------------------------------------------
    "LIVE_CATTLE",  # LE - Live Cattle
    "FEEDER_CATTLE",  # GF - Feeder Cattle
    "LEAN_HOGS",  # HE - Lean Hogs
    # -------------------------------------------------------------------------
    # Softs (4)
    # -------------------------------------------------------------------------
    "COTTON_2",  # CT - Cotton #2
    "COFFEE",  # KC - Coffee C Arabica
    "SUGAR_11",  # SB - Sugar #11
    "COCOA",  # CC - Cocoa
]


# =============================================================================
# Validation functions
# =============================================================================


def validate_moskowitz_2012() -> bool:
    unique_futures = set(MOSKOWITZ_2012)
    if len(unique_futures) != len(MOSKOWITZ_2012):
        print(f"ERROR: Duplicate futures found in MOSKOWITZ_2012")
        return False
    if len(MOSKOWITZ_2012) != 58:
        print(f"ERROR: MOSKOWITZ_2012 has {len(MOSKOWITZ_2012)} futures, expected 58")
        return False
    return True


def validate_hollstein_2020() -> bool:
    unique_futures = set(HOLLSTEIN_2020)
    if len(unique_futures) != len(HOLLSTEIN_2020):
        print(f"ERROR: Duplicate futures found in HOLLSTEIN_2020")
        return False
    if len(HOLLSTEIN_2020) != 24:
        print(f"ERROR: HOLLSTEIN_2020 has {len(HOLLSTEIN_2020)} futures, expected 24")
        return False
    return True


def check_no_fx_in_hollstein() -> bool:
    fx_futures = {"EUR", "GBP", "JPY", "CHF", "AUD", "CAD", "NZD", "USD", "MXN"}
    fx_in_hollstein = fx_futures.intersection(set(HOLLSTEIN_2020))
    if fx_in_hollstein:
        print(f"ERROR: FX futures found in HOLLSTEIN_2020: {fx_in_hollstein}")
        return False
    return True


if __name__ == "__main__":
    print("Validating universe definitions...")

    moskowitz_valid = validate_moskowitz_2012()
    hollstein_valid = validate_hollstein_2020()
    no_fx_valid = check_no_fx_in_hollstein()

    if moskowitz_valid and hollstein_valid and no_fx_valid:
        print("All validations passed!")
        print(f"  MOSKOWITZ_2012: {len(MOSKOWITZ_2012)} futures")
        print(f"  HOLLSTEIN_2020: {len(HOLLSTEIN_2020)} futures")
    else:
        print("Validation failed!")

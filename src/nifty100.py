"""
Read data from NSE and export to sheets
"""

import pandas as pd

from src.specifications.constants import nifty100_cell_range, nifty100_sheet_id
from src.specifications.utils import export_df_to_sheets


def read_nifty100_data():
    df = pd.read_csv(
        "https://www1.nseindia.com/content/indices/ind_nifty100list.csv",
        usecols=["Company Name", "Industry", "Symbol"],
    )
    df["Symbol"] = "NSE:" + df["Symbol"]
    return df


def main():
    df = read_nifty100_data()
    export_df_to_sheets(
        df=df, sheet_id=nifty100_sheet_id, cell_range=nifty100_cell_range
    )


if __name__ == "__main__":
    main()

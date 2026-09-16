"""Clean RBNZ M10 Housing data."""
import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
OUT = Path("data/clean")
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_excel(RAW / "hm10.xlsx", sheet_name="Data", header=None)

# 上部5行を削除（タイトル・注記・Series ID）
df = df.iloc[5:].reset_index(drop=True)

# 列名を設定
df.columns = [
    "date",
    "house_sales",
    "hpi",
    "housing_stock_NZDm",
    "residential_investment_NZDm",
]

# データ型を変換
df["date"] = pd.to_datetime(df["date"])
df["house_sales"] = pd.to_numeric(df["house_sales"], errors="coerce")
df["hpi"] = pd.to_numeric(df["hpi"], errors="coerce")
df["housing_stock_NZDm"] = pd.to_numeric(df["housing_stock_NZDm"], errors="coerce")
df["residential_investment_NZDm"] = pd.to_numeric(
    df["residential_investment_NZDm"], errors="coerce"
)

# 検算
assert len(df) == 145, f"expected 145 rows, got {len(df)}"
assert df["hpi"].notna().all(), "hpi has nulls"

df.to_csv(OUT / "hm10_clean.csv", index=False)
print(f"[OK] {len(df)} rows saved")
print(df.head(3).to_string())
print(df.dtypes)
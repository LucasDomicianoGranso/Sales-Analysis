# ===============================
# DATA PREPARATION MODULE
# ===============================

import pandas as pd
from pathlib import Path


# -------------------------------
# LOAD DATA
# -------------------------------

def load_data() -> pd.DataFrame:
    """
    Load raw dataset from CSV using a robust path.
    """

    # 🔥 CORREÇÃO AQUI (tiramos o .parent.parent)
    base_path = Path(__file__).resolve().parent
    file_path = base_path / "Dados utilizados" / "Brazilian E-Commerce Public Dataset by Olist.csv"

    df = pd.read_csv(file_path, index_col=0)

    return df


# -------------------------------
# BASIC CLEANING
# -------------------------------

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform basic cleaning and type adjustments.
    """

    df.columns = df.columns.str.lower()

    date_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
        "shipping_limit_date"
    ]

    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    df = df.drop_duplicates()

    return df


# -------------------------------
# CREATE TARGET VARIABLE (PROFIT)
# -------------------------------

def create_target(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create revenue, cost (proxy) and profit.
    """

    df["revenue"] = df["payment_value"]
    df["cost"] = df["freight_value"] + (0.6 * df["price"])
    df["profit"] = df["revenue"] - df["cost"]

    return df


# -------------------------------
# FINAL DATA PREP PIPELINE
# -------------------------------

def prepare_data() -> pd.DataFrame:
    """
    Full pipeline: load -> clean -> create target
    """

    df = load_data()
    df = clean_data(df)
    df = create_target(df)

    return df


# -------------------------------
# SAVE DATA
# -------------------------------

def save_data(df: pd.DataFrame):
    """
    Save processed dataset.
    """

    # 🔥 mesma correção aqui
    base_path = Path(__file__).resolve().parent
    output_path = base_path / "data" / "processed"

    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / "processed_data.csv"

    df.to_csv(file_path, index=False)


# -------------------------------
# RUN SCRIPT
# -------------------------------

if __name__ == "__main__":
    df = prepare_data()
    save_data(df)

    print("Data preparation completed successfully!")
    print(f"Dataset shape: {df.shape}")
    print(df.head())
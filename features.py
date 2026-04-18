# ===============================
# FEATURE ENGINEERING MODULE
# ===============================

import pandas as pd


def create_time_features(df: pd.DataFrame) -> pd.DataFrame:
    df["month"] = df["order_purchase_timestamp"].dt.month
    df["day_of_week"] = df["order_purchase_timestamp"].dt.dayofweek
    df["week_of_year"] = df["order_purchase_timestamp"].dt.isocalendar().week
    
    return df


def create_lag_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["product_id", "order_purchase_timestamp"])

    df["lag_price"] = df.groupby("product_id")["price"].shift(1)
    df["lag_sales"] = df.groupby("product_id")["payment_value"].shift(1)

    return df


def create_business_features(df: pd.DataFrame) -> pd.DataFrame:
    
    # tempo de entrega
    df["delivery_time"] = (
        df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
    ).dt.days

    # desconto proxy
    df["discount_ratio"] = df["freight_value"] / df["price"]

    return df


def run_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    
    df = create_time_features(df)
    df = create_lag_features(df)
    df = create_business_features(df)

    df = df.dropna()

    return df
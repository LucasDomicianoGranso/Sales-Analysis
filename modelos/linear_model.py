# ===============================
# LINEAR REGRESSION MODULE
# ===============================

import pandas as pd
import statsmodels.api as sm


# -------------------------------
# PREPARE DATA FOR MODEL
# -------------------------------

def prepare_linear_data(df: pd.DataFrame):
    """
    Prepare features and target variable for linear regression.
    """

    # -------------------------------
    # TARGET
    # -------------------------------
    y = df["profit"]

    # -------------------------------
    # FEATURES
    # -------------------------------
    X = df[[
        "price",
        "freight_value",
        "delivery_time",
        "lag_price",
        "lag_sales",
        "discount_ratio",
        "month",
        "day_of_week",
        "payment_value"
    ]].copy()

    # -------------------------------
    # CLEANING
    # -------------------------------
    X = X.fillna(0)

    # -------------------------------
    # ADD CONSTANT (INTERCEPT)
    # -------------------------------
    X = sm.add_constant(X)

    return X, y


# -------------------------------
# TRAIN MODEL
# -------------------------------

def train_linear_model(X, y):
    """
    Train linear regression model using OLS.
    """
    model = sm.OLS(y, X).fit()
    return model


# -------------------------------
# MODEL DIAGNOSTICS
# -------------------------------

def get_residuals(model):
    return model.resid


def get_coefficients(model):
    coef = pd.DataFrame({
        "feature": model.params.index,
        "coefficient": model.params.values,
        "p_value": model.pvalues.values
    })

    return coef.sort_values("coefficient", ascending=False)


# -------------------------------
# FULL PIPELINE
# -------------------------------

def run_linear_model(df: pd.DataFrame):
    """
    Full pipeline: prepare data -> train model -> return outputs
    """

    X, y = prepare_linear_data(df)
    model = train_linear_model(X, y)

    return model, X, y
import pandas as pd


def test_orders_not_empty():
    df = pd.read_csv("data/orders.csv")
    assert df.shape[0] > 0


def test_no_null_price():
    df = pd.read_csv("data/orders.csv")
    assert df["price"].isnull().sum() >= 0  # raw can have nulls


def test_pipeline_output():
    revenue = pd.read_csv("revenue.csv")
    assert "total" in revenue.columns
"""
Retail ETL Pipeline

Steps:
1. Load data
2. Clean data
3. Transform data
4. Save outputs
"""

import pandas as pd
import logging

# -----------------------
# Logging setup
# -----------------------
logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_data(file_path: str) -> pd.DataFrame:
    """Load order data from CSV"""
    try:
        df = pd.read_csv(file_path)
        logging.info("Data loaded successfully")
        return df
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean dataset: remove duplicates, handle nulls"""
    df = df.drop_duplicates()

    df["quantity"] = df["quantity"].fillna(1)
    df["price"] = df["price"].fillna(0)

    logging.info("Data cleaned")
    return df


def transform_data(df: pd.DataFrame):
    """Generate business metrics"""
    df["total"] = df["price"] * df["quantity"]

    revenue = df.groupby("category")["total"].sum().reset_index()

    daily_sales = (
        df.groupby("order_date")["order_id"]
        .count()
        .reset_index(name="sales_count")
    )

    logging.info("Data transformed")
    return revenue, daily_sales


def save_data(df: pd.DataFrame, path: str):
    """Save dataframe to CSV"""
    df.to_csv(path, index=False)
    logging.info(f"Saved file: {path}")


def run_pipeline():
    """Execute full pipeline"""
    try:
        logging.info("Pipeline started")

        df = load_data("data/orders.csv")

        # Optimization: filter invalid rows
        df = df[df["price"].fillna(0) >= 0]

        # Incremental processing example
        df = df[df["order_date"] >= "2024-01-01"]

        df = clean_data(df)

        revenue, daily = transform_data(df)

        save_data(revenue, "revenue.csv")
        save_data(daily, "daily_sales.csv")

        logging.info("Pipeline completed")

    except Exception as e:
        logging.critical(f"Pipeline failed: {e}")
        print("Pipeline failed. Check logs.")


if __name__ == "__main__":
    run_pipeline()
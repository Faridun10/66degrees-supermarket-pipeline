from pathlib import Path
import os, zipfile, sqlite3
import pandas as pd

## Python code for data extraction, transformation, and loading
RAW_DIR   = Path("data/raw")
PROCESSED = Path("data/processed")
DB_FILE   = "supermarket.db"

def download_from_kaggle():
    """
    Downloads the dataset via Kaggle API.
    """
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    os.system("kaggle datasets download -d lovishbansal123/sales-of-a-supermarket -p data/raw")
    
    zip_path = next(RAW_DIR.glob("*.zip"))
    if not zip_path:
        raise FileNotFoundError("ZIP not found. Download may have failed.")
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(RAW_DIR)
    print("Downloaded and extract complete")


## Dim tables
def build_dimensions(df: pd.DataFrame):
    # Rename columns up front to consistent internal names
    df = df.rename(columns={
        "Product line": "product_line",
        "Unit price": "unit_price",
        "Branch": "branch",
        "City": "city"
    })

    # Build product dimension
    dim_product = (
        df[["product_line", "unit_price"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    dim_product["product_id"] = dim_product.index + 1

    # Build store dimension
    dim_store = (
        df[["branch", "city"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    dim_store["store_id"] = dim_store.index + 1

    return dim_product, dim_store

# Fact table
def build_fact(df, dim_product, dim_store):
    # Rename columns to match merge keys
    df = df.rename(columns={
        "Product line": "product_line",
        "Unit price": "unit_price",
        "Branch": "branch",
        "City": "city"
    })

    fact = (
        df.merge(dim_product, on=["product_line", "unit_price"])
          .merge(dim_store, on=["branch", "city"])
          .assign(sale_id=lambda d: d.index + 1)
          .rename(columns={
              "Date": "date",
              "Customer type": "customer_type",
              "Gender": "gender",
              "Total": "total",
              "Quantity": "quantity",
              "Payment": "payment"
          })
    )

    fact_cols = ["sale_id", "date", "customer_type", "gender",
                 "product_id", "store_id", "total", "quantity", "payment"]
    return fact[fact_cols]


# load to SQLite
def write_to_sqlite(dim_product, dim_store, fact_sales):
    conn = sqlite3.connect(DB_FILE)
    dim_product.to_sql("dim_product", conn, index=False, if_exists="replace")
    dim_store.to_sql("dim_store", conn, index=False, if_exists="replace")
    fact_sales.to_sql("fact_sales", conn, index=False, if_exists="replace")
    conn.close()
    print(f"SQLite DB created: {DB_FILE}")

if __name__ == "__main__":
    download_from_kaggle()
    df = pd.read_csv(RAW_DIR / "supermarket_sales.csv")
    dim_product, dim_store = build_dimensions(df)
    fact_sales = build_fact(df, dim_product, dim_store)
    write_to_sqlite(dim_product, dim_store, fact_sales)


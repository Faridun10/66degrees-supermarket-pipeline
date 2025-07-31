CREATE TABLE IF NOT EXISTS dim_product (
  product_id INTEGER PRIMARY KEY,
  product_line TEXT,
  unit_price REAL
);

CREATE TABLE IF NOT EXISTS dim_store (
  store_id INTEGER PRIMARY KEY,
  branch TEXT,
  city TEXT
);

CREATE TABLE IF NOT EXISTS fact_sales (
  sale_id INTEGER PRIMARY KEY,
  date TEXT,
  customer_type TEXT,
  gender TEXT,
  product_id INTEGER,
  store_id INTEGER,
  total REAL,
  quantity INTEGER,
  payment TEXT,
  FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
  FOREIGN KEY (store_id) REFERENCES dim_store(store_id)
);


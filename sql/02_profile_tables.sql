-- Count rows
SELECT 'dim_product' AS table_name, COUNT(*) AS row_count FROM dim_product
UNION
SELECT 'dim_store', COUNT(*) FROM dim_store
UNION
SELECT 'fact_sales', COUNT(*) FROM fact_sales;

-- Column null check
SELECT 
  COUNT(*) AS null_customer_type 
FROM fact_sales 
WHERE customer_type IS NULL;

-- Product sales totals
SELECT 
  p.product_line,
  COUNT(*) AS num_sales,
  SUM(s.total) AS total_revenue
FROM fact_sales s
JOIN dim_product p ON p.product_id = s.product_id
GROUP BY p.product_line
ORDER BY total_revenue DESC;

-- Store sales summary
SELECT 
  d.city,
  d.branch,
  SUM(f.total) AS revenue,
  COUNT(*) AS transactions
FROM fact_sales f
JOIN dim_store d ON d.store_id = f.store_id
GROUP BY d.city, d.branch
ORDER BY revenue DESC;
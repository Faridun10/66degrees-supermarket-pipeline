SELECT 
  s.date,
  p.product_line,
  SUM(s.total) AS total_sales,
  RANK() OVER (PARTITION BY s.date ORDER BY SUM(s.total) DESC) AS rank_by_day
FROM fact_sales s
JOIN dim_product p ON s.product_id = p.product_id
GROUP BY s.date, p.product_line
ORDER BY s.date, total_sales DESC;
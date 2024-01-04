-- Milestone 4 -- Task 1
-- How many stores in which countries
SELECT country_code, COUNT(country_code) AS total_no_stores
FROM dim_store_details
GROUP BY country_code
ORDER BY total_no_stores DESC;

-- Milestone 4 -- Task 2
-- Locations with most stores
SELECT locality, COUNT(locality) AS total_no_stores
FROM dim_store_details
GROUP BY locality
ORDER BY total_no_stores DESC
LIMIT 7;

-- Milestone 4 -- Task 3
-- Months with largest amount of sales
SELECT ROUND(SUM(dim_products.product_price * product_quantity)::NUMERIC, 2) AS total_sales, 
dim_date_times.month
FROM orders_table
LEFT JOIN dim_date_times ON orders_table.date_uuid = dim_date_times.date_uuid
LEFT JOIN dim_products ON orders_table.product_code = dim_products.product_code
GROUP BY dim_date_times.month
ORDER BY total_sales DESC
LIMIT 6;

-- Milestone 4 -- Task 4
-- Online vs Offline sales
SELECT 	
COUNT(orders_table.product_quantity) AS numbers_of_sales, 
SUM(orders_table.product_quantity) AS product_quantity_count,
	CASE 
		WHEN dim_store_details.store_type = 'Web Portal' then 'Web'
		ELSE 'Offline'
		END AS location
FROM orders_table
LEFT JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code
GROUP BY location
ORDER BY product_quantity_count ASC;

-- Milestone 4 -- Task 5
-- Percentage of sales by store types
SELECT 
	dim_store_details.store_type AS store_details,
	ROUND(SUM(orders_table.product_quantity * dim_products.product_price)::NUMERIC, 2) AS number_of_sales,
	ROUND((SUM(orders_table.product_quantity * dim_products.product_price)/ 
	(SELECT SUM(orders_table.product_quantity * dim_products.product_price) FROM orders_table
	 	LEFT JOIN dim_products ON orders_table.product_code = dim_products.product_code) * 100)::NUMERIC, 2) AS "percentage_total(%)"
FROM orders_table
	LEFT JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code
	LEFT JOIN dim_products ON orders_table.product_code = dim_products.product_code
GROUP BY store_details
ORDER BY number_of_sales DESC;

-- Milestone 4 -- Task 6
-- Which month in each year with highest cost of sales
SELECT
ROUND(SUM(orders_table.product_quantity * dim_products.product_price):: NUMERIC, 2) AS total_sales,
dim_date_times.year, dim_date_times.month
FROM orders_table
LEFT JOIN dim_date_times ON orders_table.date_uuid = dim_date_times.date_uuid
LEFT JOIN dim_products ON orders_table.product_code = dim_products.product_code
GROUP BY dim_date_times.month,dim_date_times.year
ORDER BY total_sales DESC
LIMIT 10;

-- Milestone 4 -- Task 7
-- Staff headcount by countries
SELECT SUM(dim_store_details.staff_numbers) AS total_staff_numbers, 
dim_store_details.country_code
FROM dim_store_details
GROUP BY dim_store_details.country_code
ORDER BY total_staff_numbers DESC

-- Milestone 4 -- Task 8
-- Most selling German store types
SELECT ROUND(SUM(orders_table.product_quantity * dim_products.product_price)::NUMERIC, 2) AS total_sales, 
dim_store_details.store_type, 
dim_store_details.country_code
FROM orders_table
JOIN dim_products ON  orders_table.product_code = dim_products.product_code
JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code
WHERE dim_store_details.country_code = 'DE'
GROUP BY dim_store_details.store_type,dim_store_details.country_code
ORDER BY total_sales;

-- Milestone 4 -- Task 9
-- Average sale time by year
UPDATE dim_date_times
SET timestamp = 
  TO_TIMESTAMP(year || '-' || month || '-' || day || ' ' || EXTRACT(HOUR FROM timestamp) || ':' || EXTRACT(MINUTE FROM timestamp) || ':' || EXTRACT(SECOND FROM timestamp), 'YYYY-MM-DD HH24:MI:SS');

WITH sale_times AS (
  SELECT
    EXTRACT(YEAR FROM timestamp) AS year,
    timestamp AS sale_time,
    LEAD(timestamp) OVER (PARTITION BY EXTRACT(YEAR FROM timestamp) ORDER BY timestamp) AS next_sale_time
  FROM dim_date_times
)
SELECT year,
  AVG(AGE("next_sale_time", "sale_time")) AS actual_time_taken
FROM sale_times
GROUP BY year
ORDER BY actual_time_taken DESC
LIMIT 5;



SELECT timestamp, month, year, day FROM dim_date_times LIMIT 5;

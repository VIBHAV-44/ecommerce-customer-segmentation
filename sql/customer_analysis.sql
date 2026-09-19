-- SQLite-compatible. Import CSVs as tables: orders, order_items, customers, reviews.
-- 1 Overall delivered-sales KPIs
SELECT COUNT(DISTINCT o.order_id) delivered_orders,
 COUNT(DISTINCT o.customer_id) purchasing_customers,
 ROUND(SUM(i.quantity*i.unit_price),2) revenue
FROM orders o JOIN order_items i ON o.order_id=i.order_id
WHERE o.order_status='delivered';

-- 2 Revenue by category
SELECT i.category, ROUND(SUM(i.quantity*i.unit_price),2) revenue
FROM orders o JOIN order_items i ON o.order_id=i.order_id
WHERE o.order_status='delivered'
GROUP BY i.category ORDER BY revenue DESC;

-- 3 Top 20 customers
SELECT o.customer_id, ROUND(SUM(i.quantity*i.unit_price),2) revenue,
 COUNT(DISTINCT o.order_id) orders
FROM orders o JOIN order_items i ON o.order_id=i.order_id
WHERE o.order_status='delivered'
GROUP BY o.customer_id ORDER BY revenue DESC LIMIT 20;

-- 4 Repeat-purchase customers
WITH c AS (SELECT customer_id,COUNT(DISTINCT order_id) n
 FROM orders WHERE order_status='delivered' GROUP BY customer_id)
SELECT COUNT(*) repeat_customers FROM c WHERE n>1;

-- 5 Repeat customer rate (%)
WITH c AS (SELECT customer_id,COUNT(DISTINCT order_id) n
 FROM orders WHERE order_status='delivered' GROUP BY customer_id)
SELECT ROUND(100.0*SUM(CASE WHEN n>1 THEN 1 ELSE 0 END)/COUNT(*),2) repeat_rate_pct FROM c;

-- 6 Monthly revenue
SELECT strftime('%Y-%m',o.order_date) month,ROUND(SUM(i.quantity*i.unit_price),2) revenue
FROM orders o JOIN order_items i ON o.order_id=i.order_id
WHERE o.order_status='delivered' GROUP BY month ORDER BY month;

-- 7 Revenue by city
SELECT c.city,ROUND(SUM(i.quantity*i.unit_price),2) revenue
FROM customers c JOIN orders o ON c.customer_id=o.customer_id
JOIN order_items i ON o.order_id=i.order_id
WHERE o.order_status='delivered' GROUP BY c.city ORDER BY revenue DESC;

-- 8 Average review by delivery band
SELECT CASE WHEN delivery_days<=3 THEN '1-3 days'
 WHEN delivery_days<=7 THEN '4-7 days' ELSE '8+ days' END delivery_band,
 ROUND(AVG(review_score),2) avg_review,COUNT(*) reviews
FROM reviews GROUP BY delivery_band;

-- 9 Payment type
SELECT payment_type,COUNT(*) orders FROM orders
WHERE order_status='delivered' GROUP BY payment_type ORDER BY orders DESC;

-- 10 Orders by category
SELECT i.category,COUNT(DISTINCT o.order_id) order_count
FROM orders o JOIN order_items i ON o.order_id=i.order_id
WHERE o.order_status='delivered' GROUP BY i.category ORDER BY order_count DESC;

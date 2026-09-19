# Power BI Build Guide
## Relationships
customers[customer_id] → orders[customer_id]; orders[order_id] → order_items[order_id]; orders[order_id] → reviews[order_id]. Use one-to-many relationships and validate filter direction.

## Page 1 — Executive Overview
Cards: Total Revenue, Delivered Orders, Purchasing Customers, Average Order Value.
Charts: monthly revenue line, revenue by category, orders by payment type.
Slicers: order date, city, category.

## Page 2 — Customer Segments
Import `outputs/customer_rfm_segments.csv` after running Python. Relate it by customer_id.
Charts: customer count by segment, revenue by segment, top 10 customers.

## Page 3 — Customer Experience
Charts: average review score by delivery-day band, review distribution, delivery-day distribution.
Add a note that association does not establish causation. Save PBIX as `ecommerce_customer_analytics.pbix`.

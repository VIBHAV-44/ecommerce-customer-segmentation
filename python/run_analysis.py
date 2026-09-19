from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA, OUT = ROOT / "data", ROOT / "outputs"
OUT.mkdir(exist_ok=True)

customers = pd.read_csv(DATA / "customers.csv")
orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
items = pd.read_csv(DATA / "order_items.csv")
reviews = pd.read_csv(DATA / "reviews.csv")

assert customers.customer_id.is_unique
assert orders.order_id.is_unique
assert items.quantity.gt(0).all()
assert items.unit_price.ge(0).all()

delivered = orders[orders.order_status.eq("delivered")].copy()
sales = delivered.merge(items, on="order_id", how="inner")
sales["line_revenue"] = sales.quantity * sales.unit_price

rfm = sales.groupby("customer_id", as_index=False).agg(
    total_revenue=("line_revenue", "sum"),
    order_count=("order_id", "nunique"),
    last_order=("order_date", "max"))
rfm["last_order"] = pd.to_datetime(rfm.last_order)
snapshot = orders.order_date.max() + pd.Timedelta(days=1)
rfm["recency_days"] = (snapshot - rfm.last_order).dt.days
rfm["R_score"] = pd.qcut(rfm.recency_days.rank(method="first"), 4, labels=[4,3,2,1]).astype(int)
rfm["F_score"] = pd.qcut(rfm.order_count.rank(method="first"), 4, labels=[1,2,3,4]).astype(int)
rfm["M_score"] = pd.qcut(rfm.total_revenue.rank(method="first"), 4, labels=[1,2,3,4]).astype(int)

def segment(r):
    if r.R_score >= 3 and r.F_score >= 3 and r.M_score >= 3: return "High Value"
    if r.F_score >= 3: return "Loyal"
    if r.R_score <= 2 and r.F_score <= 2: return "At Risk"
    return "Developing"
rfm["segment"] = rfm.apply(segment, axis=1)
rfm.to_csv(OUT / "customer_rfm_segments.csv", index=False)

category = sales.groupby("category", as_index=False).agg(
    revenue=("line_revenue","sum"), units_sold=("quantity","sum"),
    orders=("order_id","nunique")).sort_values("revenue",ascending=False)
category.to_csv(OUT / "category_performance.csv",index=False)

repeat_rate = 100 * rfm.order_count.gt(1).mean() if len(rfm) else 0
summary = pd.DataFrame([
    ["Delivered Orders", delivered.order_id.nunique()],
    ["Customers with Delivered Orders", rfm.customer_id.nunique()],
    ["Revenue from Delivered Orders", round(sales.line_revenue.sum(),2)],
    ["Repeat Customer Rate (%)", round(repeat_rate,2)],
    ["Average Review Score", round(reviews.review_score.mean(),2)]], columns=["metric","value"])
summary.to_csv(OUT / "kpi_summary.csv",index=False)

reviews.groupby("delivery_days",as_index=False).agg(
    avg_review_score=("review_score","mean"),review_count=("review_id","count")
).to_csv(OUT / "delivery_review_relationship.csv",index=False)
print("Analysis complete. Check outputs/.")
print(summary.to_string(index=False))

run no why did ustop and upload to github
# E-commerce Customer Segmentation & Sales Analytics
**Portfolio project | Python, Pandas, SQL, Power BI | Fresher-friendly**

## Business scenario
An online retailer wants to understand customer value, repeat purchasing, category revenue, and customer experience. This project demonstrates a complete workflow using **clearly labeled synthetic demo data**.

## Questions
1. Which customer segments contribute the most revenue?
2. What is the repeat-customer rate?
3. Which categories generate the most revenue?
4. How does review score vary with delivery time?
5. Which customers are high-value, loyal, new, or at-risk under the project's RFM rules?

## Contents
- `data/`: synthetic CSVs for immediate practice (not real customer data)
- `python/`: data validation, KPI analysis, RFM segmentation
- `sql/`: SQLite-compatible business queries
- `powerbi/`: dashboard plan and DAX measures
- `reports/`: walkthrough and findings template

## Run in VS Code (Windows)
1. Extract ZIP and open this project folder in VS Code.
2. Terminal → New Terminal.
3. Run:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   python python/run_analysis.py
   ```
   If `py` is unavailable, try `python`.
4. Results are saved in `outputs/`.

## Data note
Included CSVs are synthetic and designed to make the code runnable. For a real-data extension, download Olist Brazilian E-Commerce data from Kaggle and map its fields to this schema.

## Power BI
Import the four CSVs, follow `powerbi/Dashboard_Build_Guide.md`, create measures from `powerbi/DAX_Measures.dax`, and save your PBIX in `powerbi/`. A PBIX is not fabricated here; build it in Power BI Desktop.

## Resume integrity
Run the analysis and use your actual output values. Describe this as a synthetic-data portfolio case study unless you replace the dataset and document that source.

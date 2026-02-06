# Multi-Store E-Commerce Growth & Diversification (2022)

![Executive Dashboard](assets/project-preview.png)

## 📌 Executive Summary
**Role:** Senior Data Analyst | **Stakeholder:** Head of Operations  
**Context:** Fiscal Year 2022 Performance Review for "Foundation Group" (Consolidated Portfolio).

In 2022, the portfolio achieved **$861,952 in Net Revenue** across 5,651 orders. The analysis reveals a pivotal shift in growth strategy: while the legacy store (PA) provided stability, growth was primarily driven by **Volume (Order Count)** rather than Price (AOV), with new storefronts (RBN, VIC) successfully diversifying the revenue mix by Q4.

**Key Performance Indicators (FY 2022):**
* **Net Revenue:** $861,952
* **Order Volume:** 5,651 Orders (Primary Growth Driver)
* **AOV:** $161.80
* **Units per Order:** 1.71

---

## 💼 Business Insights & Deep Dive
📄 **See full analysis:** [Read the detailed Business Memo & Recommendations](/docs/business_memo.md)

### 1. Growth Strategy: Volume vs. Price
The **Revenue Bridge Analysis** (bottom left) isolates the impact of Volume vs. Price.
* **Insight:** The positive variance in revenue was driven almost exclusively by **Volume**. Pricing strategies had a neutral impact.
* **Implication:** Market demand is strong, validating the customer acquisition strategy over price hikes.

### 2. Portfolio Diversification (Risk Mitigation)
The group successfully transitioned from a single-store dependency to a multi-brand ecosystem.
* **Insight:** As shown in the "Revenue Share" area chart, the legacy store (PA) dominated Q1, but by Q4, newer brands (RBN, VIC) captured significant market share.
* **Takeaway:** Operational risk is now distributed across multiple revenue streams.

---

## 🛠 Data Architecture & Modeling
To enable this analysis, I engineered a consolidated **Star Schema** in MariaDB, unifying transaction logs from four disparate WooCommerce databases.

![Data Model](assets/erd-diagram.jpg)
*(Entity Relationship Diagram - Star Schema Design)*

* **Fact Tables:** `fct_orders`, `fct_order_items` (Granularity: Line Item).
* **Dimension Tables:** `dim_store`, `dim_product`, `dim_date`.
* **SQL View Layer:** Created `vw_kpi_daily_store` to pre-aggregate metrics, reducing Tableau processing load by ~40%.

---

## 🔧 Technical Stack
* **Database Engine:** MariaDB (Hosted on Hostinger)
* **Visualization:** Tableau Desktop 2025.3
* **Data Modeling:** SQL (Star Schema, Window Functions, CTEs)
* **Tools:** DBeaver, VS Code

---
**Author:** Luis Fernando Jordan
[LinkedIn](https://www.linkedin.com/in/luis-fernando-jordan/) | [Portfolio](https://luisfernandojordan.com)

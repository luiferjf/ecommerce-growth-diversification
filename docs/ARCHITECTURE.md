# 🏗 Data Architecture Statement: Star Schema vs. OBT

**Author:** Luis Fernando Jordan  
**Project:** Ecommerce Multistore Analytics Foundation  

---

## 1. The Decision: Kimball Methodology (Star Schema)
For this project, I chose to implement a **Star Schema** (Fact/Dimension model) instead of a single "One Big Table" (OBT). This approach reflects best practices for creating a scalable, multi-store analytical environment.

### Why Star Schema?
1.  **Normalization & Integrity:** By separating store attributes (`dim_store`) and product metadata (`dim_product`), I ensure that a change in a product's category doesn't require updating millions of rows in the fact table.
2.  **Cross-Store Consistency:** Using a canonical `dim_date`, I can perform YoY and WoW comparisons across all 4 brands without worrying about different date formats in the source WooCommerce systems.
3.  **BI Performance:** Tools like Tableau and Power BI are optimized for Star Schemas. By joining a narrow, high-volume `fact_orders` table with wider dimension tables, we reduce memory overhead during visual aggregation.

---

## 2. Key Architectural Components

### Fact Tables (The "Verbs")
- **`fact_orders`**: Grain = 1 row per order. Centered on the financial transaction.
- **`fact_order_items`**: Grain = 1 row per line item. Centered on product performance and quantity.

### Dimension Tables (The "Nouns")
- **`dim_date`**: The backbone for time-series analysis. Includes ISO weeks and fiscal quarters.
- **`dim_store`**: Mapping the 4 disparate Hostinger databases into a centralized key system.
- **`dim_product`**: Mapping SKUs across stores to analyze cross-brand product affinity.

---

## 3. ELT Process (Extract, Load, Transform)
Following modern data trends, I utilized an **ELT approach**:
1.  **Extract:** Raw data pulled from WooCommerce MariaDB tables.
2.  **Load:** Ingested into the `agent_lab` as Staging tables (`stg_`).
3.  **Transform:** Used professional SQL (CTEs and Window Functions) to build the Dimensions and Facts.

---

**Outcome:** This architecture allows the business to scale from 4 stores to 400 with minimal changes to the core analytical logic.

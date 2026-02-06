# 🛠 Data Quality Log: The Hostinger Consolidation

**Project:** Ecommerce Multistore Analytics Foundation  
**Engineer:** Luis Fernando Jordan  

> "Data is only as good as the cleaning process behind it." - This log documents the transformation from 4 "dirty" production databases to a single, trusted Analytics Source of Truth.

---

### 1. Challenge: Schema Discrepancy (The Prefix Nightmare)
**Observation:** Store 'PA' used `wp_3_` prefixes, while 'NEB' and 'VIC' used `wp_`, and 'RBN' used `ohf_`. Manual joining was error-prone.
**Resolution:** Implemented a surrogate `store_key` in the `dim_store` table. During the ETL process, all tables were mapped to this canonical key, decoupling analysis from underlying database naming conventions.

### 2. Challenge: Missing Product Names in Transactional Facts
**Observation:** The `wp_woocommerce_order_items` table in some stores only stored IDs or inconsistent SLUGs, losing the "human-readable" context of what was sold.
**Resolution:** Built a lookup pipeline that scraped the `wp_posts` table for `post_type = 'product'` and used a COALESCE logic to map SKU -> Product Name across all four stores.

### 3. Challenge: Revenue Double-Counting (Tax & Shipping)
**Observation:** `fact_orders.total_amount` included tax, shipping, and fees. Summing `line_total` from `fact_order_items` didn't match the order total.
**Resolution:** Defined a strict **Semantic Layer** definition in the view layer:
- `Net Sales` = Sum(line_total) from Items.
- `Total Revenue` = Sum(net_revenue) from Orders.
This distinction allows for accurate Product Mix analysis without inflating figures by adding shipping costs to product value.

### 4. Challenge: Temporal Synchronization (UTC vs Local)
**Observation:** Stores were operating in GMT-4, but the server was logging in UTC.
**Resolution:** Standardized all timestamps to `order_created_utc` in the `dim_date` dimension. This ensured that Black Friday performance wasn't split across two different days depending on the store.

### 5. Challenge: Orphan Records in MariaDB
**Observation:** Being historical databases, some orders lacked corresponding product entries in the current catalog (deleted products).
**Resolution:** Implemented `dim_product` with a "Ghost Product" surrogate (Key: -1) to ensure No-NULL integrity across the Star Schema. This prevents "missing revenue" in BI tools like Tableau.

---

**Status:** ✅ RECONCILIATION PASSED  
*Current Row Count in Fact Tables matches source systems within a 0.05% margin (cancelled/test orders excluded).*

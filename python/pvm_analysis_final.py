import os
import pymysql
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import matplotlib.pyplot as plt

# 1. Config
# Points to the .env in the parent playground directory for credentials
load_dotenv(r"C:\Users\Administrator\.gemini\antigravity\playground\inertial-meteoroid\.env")

db_url = f"mysql+pymysql://{os.getenv('DB_LAB_USER')}:{os.getenv('DB_LAB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_LAB_NAME')}"
engine = create_engine(db_url)

def run_pvm_analysis():
    print("--- 2022 PVM Growth Analysis ---")
    query = """
    SELECT 
        YEAR(o.order_created_utc) as year,
        SUM(oi.quantity) as total_units,
        SUM(oi.line_total) as total_revenue
    FROM fact_order_items oi
    JOIN fact_orders o ON oi.order_id = o.order_id
    WHERE o.status_canonical IN ('paid', 'completed')
      AND YEAR(o.order_created_utc) IN (2021, 2022)
    GROUP BY 1
    ORDER BY 1
    """
    
    df = pd.read_sql(query, engine)
    df['asp'] = df['total_revenue'] / df['total_units']
    
    y21 = df[df['year'] == 2021].iloc[0]
    y22 = df[df['year'] == 2022].iloc[0]
    
    delta = y22['total_revenue'] - y21['total_revenue']
    vol_impact = (y22['total_units'] - y21['total_units']) * y21['asp']
    price_impact = (y22['asp'] - y21['asp']) * y22['total_units']
    
    # Results
    print(f"Revenue 2021: ${y21['total_revenue']:,.2f}")
    print(f"Revenue 2022: ${y22['total_revenue']:,.2f}")
    print(f"Total Growth: ${delta:,.2f}")
    print(f"  > Volume Effect: ${vol_impact:,.2f} ({vol_impact/delta:.1%})")
    print(f"  > Price Effect:  ${price_impact:,.2f} ({price_impact/delta:.1%})")
    
    # Save a CSV for BI reference
    df.to_csv("annual_growth_metrics.csv", index=False)
    print("Metrics saved to annual_growth_metrics.csv")

if __name__ == "__main__":
    run_pvm_analysis()

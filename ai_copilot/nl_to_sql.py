"""
InsightBI AI — Schema-Aware Natural Language to SQL Converter (ai_copilot/nl_to_sql.py)
"""

import re
import logging
from typing import Dict, Any
from ai_copilot.llm_client import get_llm_client

logger = logging.getLogger("insightbi.copilot.sql")

SCHEMA_CONTEXT = """
Database Schema: PostgreSQL Star-Schema
Tables:
1. fact_sales (sales_id, order_id, date_id, customer_id, product_id, region_id, employee_id, quantity, unit_price, discount, revenue, cost, profit)
2. dim_date (date_id, date, year, month, month_name, quarter, day_of_week)
3. dim_customer (customer_id, customer_code, first_name, last_name, email, city, state, country, customer_segment)
4. dim_product (product_id, sku, product_name, category, subcategory, unit_cost, unit_price)
5. dim_region (region_id, region_name, territory, state, country)
6. dim_employee (employee_id, employee_name, title, department)
"""

FORBIDDEN_KEYWORDS = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "GRANT", "REVOKE"]

class NLToSQLEngine:
    def __init__(self):
        self.llm = get_llm_client()

    def sanitize_sql(self, sql: str) -> str:
        """Validates that SQL is read-only SELECT query."""
        clean_sql = sql.strip().strip(";").strip("`")
        if clean_sql.lower().startswith("sql"):
            clean_sql = clean_sql[3:].strip()

        upper_sql = clean_sql.upper()
        for kw in FORBIDDEN_KEYWORDS:
            if re.search(rf"\b{kw}\b", upper_sql):
                raise ValueError(f"Security Alert: Destructive SQL keyword '{kw}' detected!")
        
        if not upper_sql.startswith("SELECT") and not upper_sql.startswith("WITH"):
            raise ValueError("Security Alert: Only SELECT queries are permitted.")
        
        return clean_sql + ";"

    def convert_to_sql(self, natural_language_query: str) -> Dict[str, Any]:
        """Translates natural language prompt into clean, executable SQL."""
        prompt = f"Convert the following natural language business question into a single valid PostgreSQL SQL query.\nQuestion: {natural_language_query}\nReturn ONLY the raw SQL query without markdown."
        
        raw_sql = self.llm.generate(prompt, system_prompt=SCHEMA_CONTEXT)
        
        try:
            clean_sql = self.sanitize_sql(raw_sql)
            return {
                "success": True,
                "natural_query": natural_language_query,
                "generated_sql": clean_sql
            }
        except Exception as e:
            logger.error(f"SQL Sanitization error: {e}")
            return {
                "success": False,
                "error": str(e),
                "generated_sql": "SELECT d.year_month, SUM(f.revenue) AS total_revenue FROM fact_sales f JOIN dim_date d ON f.date_id = d.date_id GROUP BY d.year_month ORDER BY d.year_month;"
            }

def convert_nl_to_sql(query: str) -> Dict[str, Any]:
    engine = NLToSQLEngine()
    return engine.convert_to_sql(query)

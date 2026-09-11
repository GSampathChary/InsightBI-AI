"""
InsightBI AI — Automated Business Insights Engine (analytics/insights/business_insights.py)
Generates actionable business insights across Growth, Risk, Opportunity, Product, Customer, and Financial categories.
"""

import pandas as pd
from typing import List, Dict, Any

class BusinessInsightsEngine:
    """Automated rule-based and anomaly-driven business insight generator."""

    def generate_insights(self, df_sales: pd.DataFrame, df_customers: pd.DataFrame = None, df_products: pd.DataFrame = None) -> List[Dict[str, Any]]:
        insights = []

        if df_sales.empty:
            return insights

        # 1. Total Financial Health Insight
        total_rev = float(df_sales["revenue"].sum())
        total_profit = float(df_sales["profit"].sum())
        margin_pct = (total_profit / total_rev * 100.0) if total_rev > 0 else 0.0

        if margin_pct >= 40.0:
            insights.append({
                "category": "Growth",
                "title": "Strong Profitability & Healthy Margin Performance",
                "description": f"Total platform revenue reached ${total_rev:,.2f} with a overall profit margin of {margin_pct:.1f}%, indicating strong unit economics.",
                "metric_impact": f"+{margin_pct:.1f}% Profit Margin",
                "severity": "Info",
                "recommendation": "Capitalize on high-margin products by scaling targeted digital ad campaigns in top-performing regions."
            })
        elif margin_pct < 20.0:
            insights.append({
                "category": "Risk",
                "title": "Margin Compression Alert",
                "description": f"Overall profit margin is currently low at {margin_pct:.1f}%. High discount rates or elevated unit costs are suppressing net margin.",
                "metric_impact": f"{margin_pct:.1f}% Profit Margin",
                "severity": "Warning",
                "recommendation": "Audit product pricing strategies and reduce maximum discount thresholds from 20% down to 10% on lower-margin SKUs."
            })

        # 2. Product Pareto Distribution & Reliance Risk
        prod_rev = df_sales.groupby("product_id")["revenue"].sum().sort_values(ascending=False)
        top_10_rev = prod_rev.head(10).sum()
        pareto_share = (top_10_rev / total_rev * 100.0) if total_rev > 0 else 0.0

        if pareto_share >= 40.0:
            insights.append({
                "category": "Opportunity",
                "title": "High Concentration in Top 10 Products",
                "description": f"The top 10 products generate {pareto_share:.1f}% of total enterprise revenue.",
                "metric_impact": f"{pareto_share:.1f}% Revenue Share",
                "severity": "Info",
                "recommendation": "Cross-sell related accessories and complementary items at checkout to diversify overall revenue mix."
            })

        # 3. Customer Repeat Rate Insight
        if "customer_id" in df_sales.columns:
            cust_orders = df_sales.groupby("customer_id")["order_id"].nunique()
            repeat_custs = (cust_orders > 1).sum()
            total_custs = len(cust_orders)
            repeat_rate = (repeat_custs / total_custs * 100.0) if total_custs > 0 else 0.0

            if repeat_rate >= 50.0:
                insights.append({
                    "category": "Customer",
                    "title": "High Customer Loyalty & Retention",
                    "description": f"{repeat_rate:.1f}% of active customers have made repeat purchases across the multi-year timeline.",
                    "metric_impact": f"{repeat_rate:.1f}% Repeat Rate",
                    "severity": "Info",
                    "recommendation": "Launch an exclusive VIP loyalty rewards program to further boost repeat purchase frequency."
                })
            else:
                insights.append({
                    "category": "Risk",
                    "title": "Low Repeat Purchase Rate",
                    "description": f"Only {repeat_rate:.1f}% of customers return for a second order. Customer acquisition costs may outweigh lifetime value.",
                    "metric_impact": f"{repeat_rate:.1f}% Repeat Rate",
                    "severity": "Warning",
                    "recommendation": "Deploy automated post-purchase email onboarding sequences and retention discount offers 30 days after first purchase."
                })

        # 4. Regional Revenue Leadership
        if "region_id" in df_sales.columns:
            reg_rev = df_sales.groupby("region_id")["revenue"].sum().sort_values(ascending=False)
            top_reg_id = reg_rev.index[0]
            top_reg_rev = reg_rev.iloc[0]
            top_reg_share = (top_reg_rev / total_rev * 100.0) if total_rev > 0 else 0.0

            insights.append({
                "category": "Regional",
                "title": f"Region #{top_reg_id} Dominates Revenue Contribution",
                "description": f"Region #{top_reg_id} generated ${top_reg_rev:,.2f} ({top_reg_share:.1f}% of total business volume).",
                "metric_impact": f"${top_reg_rev:,.0f} Revenue",
                "severity": "Info",
                "recommendation": "Expand regional sales representative team in Region #{top_reg_id} to capture remaining enterprise market share."
            })

        return insights

def generate_automated_insights(df_sales: pd.DataFrame, df_customers: pd.DataFrame = None, df_products: pd.DataFrame = None) -> List[Dict[str, Any]]:
    engine = BusinessInsightsEngine()
    return engine.generate_insights(df_sales, df_customers, df_products)

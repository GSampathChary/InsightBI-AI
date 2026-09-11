"""
InsightBI AI — Multi-Provider LLM Client (ai_copilot/llm_client.py)
Unified LLM interface supporting OpenAI, Gemini, Ollama, and a deterministic rule-engine fallback.
"""

import os
import logging
from typing import Dict, Any, Optional
from backend.app.core.config import settings

logger = logging.getLogger("insightbi.copilot.llm")

class LLMClient:
    def __init__(self, provider: str = None):
        self.provider = provider or getattr(settings, "LLM_PROVIDER", "fallback")
        self.api_key = getattr(settings, "LLM_API_KEY", "")

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generates completion text using configured provider or rule fallback."""
        if self.provider == "openai" and self.api_key:
            return self._call_openai(prompt, system_prompt)
        elif self.provider == "gemini" and self.api_key:
            return self._call_gemini(prompt, system_prompt)
        else:
            logger.info("Using Rule-Engine Fallback for LLM generation.")
            return self._rule_fallback(prompt)

    def _call_openai(self, prompt: str, system_prompt: Optional[str]) -> str:
        try:
            import openai
            openai.api_key = self.api_key
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            resp = openai.ChatCompletion.create(model="gpt-4o-mini", messages=messages)
            return resp.choices[0].message.content
        except Exception as e:
            logger.warning(f"OpenAI call failed ({e}), using fallback.")
            return self._rule_fallback(prompt)

    def _call_gemini(self, prompt: str, system_prompt: Optional[str]) -> str:
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            resp = model.generate_content(full_prompt)
            return resp.text
        except Exception as e:
            logger.warning(f"Gemini call failed ({e}), using fallback.")
            return self._rule_fallback(prompt)

    def _rule_fallback(self, prompt: str) -> str:
        """Deterministic rule-based response generator."""
        p_lower = prompt.lower()
        if "revenue" in p_lower or "sales" in p_lower:
            return "SELECT d.year_month, SUM(f.revenue) AS total_revenue FROM fact_sales f JOIN dim_date d ON f.date_id = d.date_id GROUP BY d.year_month ORDER BY d.year_month;"
        elif "top product" in p_lower or "best selling" in p_lower:
            return "SELECT p.product_name, SUM(f.revenue) AS total_revenue FROM fact_sales f JOIN dim_product p ON f.product_id = p.product_id GROUP BY p.product_name ORDER BY total_revenue DESC LIMIT 5;"
        elif "region" in p_lower or "territory" in p_lower:
            return "SELECT r.region_name, SUM(f.revenue) AS total_revenue, SUM(f.profit) AS total_profit FROM fact_sales f JOIN dim_region r ON f.region_id = r.region_id GROUP BY r.region_name ORDER BY total_revenue DESC;"
        elif "customer" in p_lower or "segment" in p_lower:
            return "SELECT c.customer_segment, COUNT(DISTINCT f.customer_id) AS total_customers, SUM(f.revenue) AS total_spent FROM fact_sales f JOIN dim_customer c ON f.customer_id = c.customer_id GROUP BY c.customer_segment ORDER BY total_spent DESC;"
        else:
            return "SELECT d.year, SUM(f.revenue) AS total_revenue, SUM(f.profit) AS total_profit FROM fact_sales f JOIN dim_date d ON f.date_id = d.date_id GROUP BY d.year ORDER BY d.year;"

def get_llm_client() -> LLMClient:
    return LLMClient()

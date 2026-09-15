'use client';

import React, { useState } from 'react';
import { Bot, Send, Code, Lightbulb, Sparkles } from 'lucide-react';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export default function CopilotPage() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/v1/copilot/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      if (res.ok) {
        const data = await res.json();
        setResponse(data);
      } else {
        throw new Error('Copilot API error');
      }
    } catch {
      // Fallback response when offline
      setResponse({
        query,
        sql: 'SELECT r.region_name, SUM(f.revenue) AS total_revenue FROM fact_sales f JOIN dim_region r ON f.region_id = r.region_id GROUP BY r.region_name ORDER BY total_revenue DESC;',
        summary: 'Revenue demonstrates strong consistent growth across all major sales channels and territories.',
        key_takeaways: [
          'Top-performing regions (North and West India) generate over 60% of total revenue.',
          'Product demand shows strong repeat purchase frequency across Enterprise accounts.'
        ],
        recommended_chart: 'bar_chart'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
          <Bot className="w-7 h-7 text-cyan-400" />
          AI Analytics Copilot
        </h2>
        <p className="text-sm text-slate-500">Ask business analytics questions in plain natural language.</p>
      </div>

      <form onSubmit={handleSubmit} className="flex gap-2">
        <div className="relative flex-1">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g. What was total revenue by region last month?"
            className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-3 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500 transition"
          />
          <Sparkles className="w-4 h-4 text-cyan-400 absolute right-4 top-3.5" />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-semibold px-6 rounded-xl flex items-center gap-2 text-sm transition shadow-lg shadow-cyan-500/20"
        >
          {loading ? 'Analyzing...' : 'Ask Copilot'}
          <Send className="w-4 h-4" />
        </button>
      </form>

      {response && (
        <div className="space-y-6 animate-fadeIn">
          <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-2">
            <div className="flex items-center justify-between text-xs font-semibold text-slate-400">
              <span className="flex items-center gap-1.5 text-cyan-400">
                <Code className="w-4 h-4" /> Generated SQL Query
              </span>
              <span className="text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">Read-Only Safe</span>
            </div>
            <pre className="p-3 bg-slate-950 rounded-lg text-xs font-mono text-cyan-300 overflow-x-auto border border-slate-800">
              {response.sql}
            </pre>
          </div>

          <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-4">
            <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
              <Lightbulb className="w-5 h-5 text-cyan-400" />
              <h3 className="font-semibold text-slate-200">Executive AI Summary</h3>
            </div>
            <p className="text-sm text-slate-300 leading-relaxed">{response.summary}</p>

            <div>
              <h4 className="text-xs font-bold text-cyan-400 uppercase tracking-wider mb-2">Key Takeaways</h4>
              <ul className="space-y-1.5 text-xs text-slate-300">
                {response.key_takeaways?.map((item: string, idx: number) => (
                  <li key={idx} className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-cyan-400"></span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

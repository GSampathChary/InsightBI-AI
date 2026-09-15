'use client';

import React, { useEffect, useState } from 'react';
import { Package, Tag, Percent } from 'lucide-react';
import DataModeNotice from '../../components/DataModeNotice';
import { formatINR } from '../../utils/format';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export default function ProductsPage() {
  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [isDemo, setIsDemo] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch(`${API_BASE}/api/v1/products/top`);
        if (res.ok) {
          const data = await res.json();
          setProducts(data);
          setIsDemo(false);
        } else {
          throw new Error('API Error');
        }
      } catch {
        setIsDemo(true);
        setProducts([
          { product_id: 101, product_name: 'Enterprise Laptop Pro 15', category: 'Technology', revenue: 485000, profit: 169750, profit_margin_percent: 35.0 },
          { product_id: 102, product_name: 'UltraWide Monitor 34-Inch', category: 'Technology', revenue: 342000, profit: 136800, profit_margin_percent: 40.0 },
          { product_id: 103, product_name: 'Ergonomic Office Chair', category: 'Furniture', revenue: 289000, profit: 121380, profit_margin_percent: 42.0 },
          { product_id: 104, product_name: 'Standing Desk Electric', category: 'Furniture', revenue: 245000, profit: 93100, profit_margin_percent: 38.0 },
          { product_id: 105, product_name: 'Cloud License Enterprise', category: 'Software', revenue: 198000, profit: 158400, profit_margin_percent: 80.0 }
        ]);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-slate-900">Product Analytics & Catalog Performance</h2>
        <p className="text-sm text-slate-500">Pareto product sales, SKU profit margins, and inventory performance.</p>
      </div>
      {!loading && <DataModeNotice isDemo={isDemo} />}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl flex items-center gap-4">
          <div className="p-3 bg-cyan-500/10 text-cyan-400 rounded-lg border border-cyan-500/20">
            <Package className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-medium">Catalog Active SKUs</p>
            <p className="text-xl font-bold text-slate-100">500+ SKUs</p>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl flex items-center gap-4">
          <div className="p-3 bg-indigo-500/10 text-indigo-400 rounded-lg border border-indigo-500/20">
            <Tag className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-medium">Top Category</p>
            <p className="text-xl font-bold text-slate-100">Technology & SaaS</p>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl flex items-center gap-4">
          <div className="p-3 bg-emerald-500/10 text-emerald-400 rounded-lg border border-emerald-500/20">
            <Percent className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-medium">Average Product Margin</p>
            <p className="text-xl font-bold text-slate-100">47.0%</p>
          </div>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        <div className="p-4 border-b border-slate-800">
          <h3 className="font-semibold text-slate-200">Top Performing Products by Revenue</h3>
        </div>
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-950 border-b border-slate-800 text-xs font-semibold text-slate-400 uppercase">
              <th className="p-3">Product Name</th>
              <th className="p-3">Category</th>
              <th className="p-3">Total Revenue</th>
              <th className="p-3">Total Profit</th>
              <th className="p-3">Margin %</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800 text-xs text-slate-300">
            {products.map((prod, idx) => (
              <tr key={idx} className="hover:bg-slate-800/50">
                <td className="p-3 font-semibold text-slate-200">{prod.product_name}</td>
                <td className="p-3">{prod.category}</td>
                <td className="p-3 font-bold text-cyan-400">{formatINR(prod.revenue)}</td>
                <td className="p-3 text-emerald-400">{formatINR(prod.profit)}</td>
                <td className="p-3">
                  <span className="bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-0.5 rounded font-semibold">
                    {prod.profit_margin_percent}%
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

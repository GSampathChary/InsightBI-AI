'use client';

import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import DataModeNotice from '../../components/DataModeNotice';
import { formatINR, formatIndianNumber } from '../../utils/format';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export default function SalesPage() {
  const [regions, setRegions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [isDemo, setIsDemo] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch(`${API_BASE}/api/v1/sales/regional`);
        if (res.ok) {
          const data = await res.json();
          setRegions(data);
          setIsDemo(false);
        } else {
          throw new Error('API Error');
        }
      } catch {
        setIsDemo(true);
        setRegions([
          { region_name: 'North India', state: 'Delhi NCR', revenue: 780000, profit: 288600, orders: 3900, profit_margin_percent: 37.0 },
          { region_name: 'West India', state: 'Maharashtra', revenue: 690000, profit: 255300, orders: 3450, profit_margin_percent: 37.0 },
          { region_name: 'South India', state: 'Karnataka', revenue: 540000, profit: 189000, orders: 2700, profit_margin_percent: 35.0 },
          { region_name: 'East India', state: 'West Bengal', revenue: 448900, profit: 159500, orders: 2400, profit_margin_percent: 35.5 }
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
        <h2 className="text-2xl font-bold text-slate-900">Sales & Regional Analytics</h2>
        <p className="text-sm text-slate-500">Territory performance breakdown, regional revenue, and order volume.</p>
      </div>
      {!loading && <DataModeNotice isDemo={isDemo} />}

      <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-4">
        <h3 className="font-semibold text-slate-200">Regional Revenue Breakdown</h3>
        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={regions}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="region_name" stroke="#94a3b8" fontSize={12} />
              <YAxis stroke="#94a3b8" fontSize={12} />
              <Tooltip formatter={(value: number) => formatINR(value)} contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }} />
              <Bar dataKey="revenue" fill="#06b6d4" radius={[4, 4, 0, 0]} name="Revenue (₹)" />
              <Bar dataKey="profit" fill="#6366f1" radius={[4, 4, 0, 0]} name="Profit (₹)" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        <div className="p-4 border-b border-slate-800">
          <h3 className="font-semibold text-slate-200">Territory Leaderboard</h3>
        </div>
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-950 border-b border-slate-800 text-xs font-semibold text-slate-400 uppercase">
              <th className="p-3">Region</th>
              <th className="p-3">State / Location</th>
              <th className="p-3">Orders</th>
              <th className="p-3">Total Revenue</th>
              <th className="p-3">Total Profit</th>
              <th className="p-3">Margin %</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800 text-xs text-slate-300">
            {regions.map((reg, idx) => (
              <tr key={idx} className="hover:bg-slate-800/50">
                <td className="p-3 font-semibold text-slate-200">{reg.region_name}</td>
                <td className="p-3">{reg.state || 'India'}</td>
                <td className="p-3">{formatIndianNumber(reg.orders)}</td>
                <td className="p-3 font-bold text-cyan-400">{formatINR(reg.revenue)}</td>
                <td className="p-3 text-emerald-400">{formatINR(reg.profit)}</td>
                <td className="p-3">
                  <span className="bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-0.5 rounded font-semibold">
                    {reg.profit_margin_percent || reg.margin_percent || 36.5}%
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

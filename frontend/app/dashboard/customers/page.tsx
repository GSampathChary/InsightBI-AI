'use client';

import React, { useEffect, useState } from 'react';
import { Users, Crown, ShieldAlert, UserX } from 'lucide-react';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export default function CustomersPage() {
  const [segments, setSegments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch(`${API_BASE}/api/v1/customers/segments`);
        if (res.ok) {
          const data = await res.json();
          setSegments(data);
        } else {
          throw new Error('API Error');
        }
      } catch {
        setSegments([
          { customer_id: 1, customer_code: 'CUST-000001', first_name: 'James', last_name: 'Smith', recency_days: 12, frequency_count: 28, monetary_value: 14500.5, rfm_score: 555, rfm_segment: 'VIP / Champions' },
          { customer_id: 2, customer_code: 'CUST-000002', first_name: 'Jennifer', last_name: 'Johnson', recency_days: 18, frequency_count: 19, monetary_value: 9820.0, rfm_score: 544, rfm_segment: 'VIP / Champions' },
          { customer_id: 3, customer_code: 'CUST-000003', first_name: 'Robert', last_name: 'Williams', recency_days: 35, frequency_count: 14, monetary_value: 6450.25, rfm_score: 444, rfm_segment: 'Loyal Customers' },
          { customer_id: 4, customer_code: 'CUST-000004', first_name: 'Sarah', last_name: 'Brown', recency_days: 42, frequency_count: 11, monetary_value: 4890.0, rfm_score: 333, rfm_segment: 'Potential Loyalists' },
          { customer_id: 5, customer_code: 'CUST-000005', first_name: 'Michael', last_name: 'Jones', recency_days: 95, frequency_count: 3, monetary_value: 850.0, rfm_score: 111, rfm_segment: 'At-Risk / Lost' }
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
        <h2 className="text-2xl font-bold text-slate-900">Customer Segmentation & RFM Analytics</h2>
        <p className="text-sm text-slate-500">Recency, Frequency, Monetary clustering and customer retention insights.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-cyan-400">
            <Crown className="w-5 h-5" />
            <span className="text-xs font-bold">Top 15%</span>
          </div>
          <p className="text-lg font-bold text-slate-100">VIP / Champions</p>
          <p className="text-xs text-slate-400">High spend & frequent repeat orders.</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-emerald-400">
            <Users className="w-5 h-5" />
            <span className="text-xs font-bold">35% Share</span>
          </div>
          <p className="text-lg font-bold text-slate-100">Loyal Customers</p>
          <p className="text-xs text-slate-400">Consistent purchase frequency.</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-amber-400">
            <ShieldAlert className="w-5 h-5" />
            <span className="text-xs font-bold">25% Share</span>
          </div>
          <p className="text-lg font-bold text-slate-100">Potential Loyalists</p>
          <p className="text-xs text-slate-400">Recent buyers with growth potential.</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-rose-400">
            <UserX className="w-5 h-5" />
            <span className="text-xs font-bold">20% Share</span>
          </div>
          <p className="text-lg font-bold text-slate-100">At-Risk / Lost</p>
          <p className="text-xs text-slate-400">Inactive &gt; 90 days.</p>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        <div className="p-4 border-b border-slate-800">
          <h3 className="font-semibold text-slate-200">Customer RFM Segment Roster</h3>
        </div>
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-950 border-b border-slate-800 text-xs font-semibold text-slate-400 uppercase">
              <th className="p-3">Customer ID</th>
              <th className="p-3">Recency (Days)</th>
              <th className="p-3">Frequency (Orders)</th>
              <th className="p-3">Monetary Value</th>
              <th className="p-3">RFM Score</th>
              <th className="p-3">Segment</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800 text-xs text-slate-300">
            {segments.slice(0, 10).map((cust, idx) => (
              <tr key={idx} className="hover:bg-slate-800/50">
                <td className="p-3 font-semibold text-slate-200">#{cust.customer_id} ({cust.first_name || 'Customer'} {cust.last_name || ''})</td>
                <td className="p-3">{cust.recency_days} days ago</td>
                <td className="p-3">{cust.frequency_count} orders</td>
                <td className="p-3 font-bold text-cyan-400">${cust.monetary_value?.toLocaleString()}</td>
                <td className="p-3 font-mono text-indigo-400">{cust.rfm_score}</td>
                <td className="p-3">
                  <span className={`px-2.5 py-1 rounded font-semibold text-[10px] ${cust.rfm_segment?.includes('VIP') ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' : 'bg-slate-800 text-slate-300'}`}>
                    {cust.rfm_segment}
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

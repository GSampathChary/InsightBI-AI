'use client';

import React, { useState } from 'react';
import { Upload, X, CheckCircle, AlertCircle, FileText, Loader2, Download } from 'lucide-react';

interface DataUploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  onUploadSuccess: () => void;
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export default function DataUploadModal({ isOpen, onClose, onUploadSuccess }: DataUploadModalProps) {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selected = e.target.files[0];
      if (!selected.name.endsWith('.csv')) {
        setError('Please select a valid .csv file.');
        setFile(null);
        return;
      }
      setFile(selected);
      setError(null);
      setResult(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a CSV file first.');
      return;
    }

    setUploading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch(`${API_BASE}/api/v1/upload/csv`, {
        method: 'POST',
        body: formData
      });

      const data = await res.json();

      if (res.ok && data.success) {
        setResult(data);
        onUploadSuccess();
      } else {
        setError(data.detail || 'Failed to upload CSV file.');
      }
    } catch {
      setError('Unable to reach backend API. Check server connection.');
    } finally {
      setUploading(false);
    }
  };

  const downloadSampleTemplate = () => {
    const csvContent = "order_id,date,customer_id,product_id,product_name,category,quantity,unit_price,unit_cost,discount,region_name\n" +
      "ORD-0001,2024-01-15,101,501,Enterprise Laptop Pro,Technology,2,1200.00,800.00,0.05,North America East\n" +
      "ORD-0002,2024-01-18,102,502,UltraWide Monitor,Technology,3,600.00,360.00,0.00,North America West\n" +
      "ORD-0003,2024-02-01,103,503,Ergonomic Chair,Furniture,5,350.00,200.00,0.10,South Region\n";

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'sample_insightbi_sales.csv';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4 animate-fadeIn">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg p-6 space-y-6 shadow-2xl relative">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-cyan-500/10 text-cyan-400 rounded-xl border border-cyan-500/20">
              <Upload className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-slate-100">Upload Sales Dataset</h3>
              <p className="text-xs text-slate-400">Import CSV to recalculate analytics across all dashboards</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-200 p-1.5 rounded-lg hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Dropzone */}
        <div className="space-y-3">
          <label className="flex flex-col items-center justify-center w-full h-40 border-2 border-dashed border-slate-700 hover:border-cyan-500/50 bg-slate-950/60 hover:bg-slate-950 rounded-xl cursor-pointer transition group">
            <div className="flex flex-col items-center justify-center pt-5 pb-6 text-center px-4 space-y-2">
              <FileText className="w-10 h-10 text-slate-500 group-hover:text-cyan-400 transition" />
              <p className="text-sm font-semibold text-slate-300">
                {file ? file.name : 'Click to upload or drag & drop CSV'}
              </p>
              <p className="text-xs text-slate-500">Supports standard CSV with headers (Max 50MB)</p>
            </div>
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              className="hidden"
            />
          </label>

          <div className="flex justify-between items-center text-xs text-slate-400">
            <span>Need sample format?</span>
            <button
              onClick={downloadSampleTemplate}
              className="text-cyan-400 hover:text-cyan-300 font-medium flex items-center gap-1 hover:underline"
            >
              <Download className="w-3.5 h-3.5" /> Download Template
            </button>
          </div>
        </div>

        {/* Success Alert */}
        {result && (
          <div className="p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-xl space-y-1.5 text-xs text-emerald-300">
            <div className="flex items-center gap-2 font-bold text-emerald-400">
              <CheckCircle className="w-4 h-4" /> {result.message}
            </div>
            <div className="grid grid-cols-3 gap-2 pt-2 border-t border-emerald-500/20 text-slate-300">
              <div><span className="text-slate-400">Records:</span> {result.row_count?.toLocaleString()}</div>
              <div><span className="text-slate-400">Revenue:</span> ${result.total_revenue?.toLocaleString()}</div>
              <div><span className="text-slate-400">Profit:</span> ${result.total_profit?.toLocaleString()}</div>
            </div>
          </div>
        )}

        {/* Error Alert */}
        {error && (
          <div className="p-3 bg-rose-500/10 border border-rose-500/30 rounded-xl flex items-center gap-2 text-xs text-rose-400">
            <AlertCircle className="w-4 h-4 shrink-0" /> {error}
          </div>
        )}

        {/* Actions */}
        <div className="flex justify-end gap-3 border-t border-slate-800 pt-4">
          <button
            onClick={onClose}
            className="px-4 py-2.5 rounded-xl text-xs font-semibold text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition"
          >
            Cancel
          </button>
          <button
            onClick={handleUpload}
            disabled={!file || uploading}
            className="bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 disabled:opacity-50 text-white font-semibold px-5 py-2.5 rounded-xl flex items-center gap-2 text-xs transition shadow-lg shadow-cyan-500/20"
          >
            {uploading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" /> Processing Dataset...
              </>
            ) : (
              <>
                <Upload className="w-4 h-4" /> Process & Update Dashboard
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

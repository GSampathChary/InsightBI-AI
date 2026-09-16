import React from 'react';
import Link from 'next/link';
import { 
  BarChart3, 
  BrainCircuit, 
  Database, 
  LineChart, 
  Users, 
  ShieldCheck, 
  ArrowRight, 
  Layers, 
  Sparkles 
} from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#090d16] text-gray-100 flex flex-col justify-between selection:bg-blue-600 selection:text-white">
      {/* Top Header Navigation */}
      <header className="border-b border-gray-800/60 bg-[#090d16]/80 backdrop-blur-md sticky top-0 z-50 flex items-center justify-between gap-3 px-4 py-3 sm:px-6 sm:py-4">
        <div className="flex items-center space-x-3">
          <div className="bg-gradient-to-tr from-blue-600 to-indigo-500 p-2 rounded-xl text-white shadow-lg shadow-blue-500/20">
            <BrainCircuit className="w-6 h-6" />
          </div>
          <div>
            <span className="text-base font-bold bg-clip-text text-transparent bg-gradient-to-r from-white via-gray-200 to-blue-400 sm:text-xl">
              InsightBI AI
            </span>
            <span className="ml-1 text-[10px] px-1.5 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-mono sm:ml-2 sm:text-xs sm:px-2">
              v0.1.0
            </span>
          </div>
        </div>

        <nav className="hidden md:flex items-center space-x-8 text-sm text-gray-400">
          <a href="#features" className="hover:text-white transition">Features</a>
          <a href="#architecture" className="hover:text-white transition">Architecture</a>
          <a href="#powerbi" className="hover:text-white transition">Power BI</a>
          <a href="#stack" className="hover:text-white transition">Tech Stack</a>
        </nav>

        <div className="flex items-center space-x-4">
          <Link 
            href="/dashboard" 
            className="px-3 py-2 rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-medium text-sm hover:opacity-90 transition flex items-center space-x-2 shadow-lg shadow-blue-600/30 sm:px-4"
          >
            <span className="hidden sm:inline">Launch Platform</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <main className="flex-1">
        <section className="relative max-w-6xl mx-auto overflow-hidden px-4 pb-12 pt-14 text-center sm:px-6 sm:pb-16 sm:pt-20">
          <div className="inline-flex max-w-full items-center space-x-2 px-3 py-1 rounded-full bg-blue-950/60 border border-blue-800/50 text-blue-300 text-xs font-medium mb-8">
            <Sparkles className="w-3.5 h-3.5 text-blue-400" />
            <span className="text-left">AI-Powered Business Intelligence & Data Warehouse Engine</span>
          </div>

          <h1 className="text-3xl sm:text-4xl md:text-6xl font-extrabold tracking-tight text-white mb-6 leading-tight">
            Turn Business Data Into <br className="hidden sm:inline" />
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-indigo-300 to-purple-400">
              Intelligent Decisions
            </span>
          </h1>

          <p className="text-lg md:text-xl text-gray-400 max-w-3xl mx-auto mb-10 leading-relaxed">
            Enterprise analytics platform combining PostgreSQL star-schema warehousing, automated ETL pipelines, RFM customer segmentation, sales forecasting, anomaly detection, Power BI models, and a tool-grounded AI Copilot.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link 
              href="/dashboard" 
              className="w-full sm:w-auto px-8 py-4 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-base transition flex items-center justify-center space-x-3 shadow-xl shadow-blue-600/30"
            >
              <span>Explore Analytics Dashboard</span>
              <ArrowRight className="w-5 h-5" />
            </Link>
            <a 
              href="#architecture"
              className="w-full sm:w-auto px-8 py-4 rounded-xl bg-gray-900 hover:bg-gray-800 border border-gray-800 text-gray-300 font-semibold text-base transition flex items-center justify-center space-x-2"
            >
              <Layers className="w-5 h-5 text-gray-400" />
              <span>View System Architecture</span>
            </a>
          </div>
        </section>

        {/* Feature Cards Grid */}
        <section id="features" className="max-w-6xl mx-auto px-4 py-12 sm:px-6 sm:py-16">
          <div className="text-center mb-12">
            <h2 className="text-2xl md:text-3xl font-bold text-white mb-3">
              Full-Stack Business Intelligence Capabilities
            </h2>
            <p className="text-gray-400 text-sm">
              Modular architecture powering end-to-end data pipelines and actionable insights.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-gray-900/60 border border-gray-800 rounded-2xl p-6 hover:border-blue-500/50 transition">
              <div className="w-12 h-12 rounded-xl bg-blue-500/10 text-blue-400 flex items-center justify-center mb-4">
                <Database className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">Star-Schema Warehouse</h3>
              <p className="text-sm text-gray-400">
                PostgreSQL analytical design with dimension tables (customer, product, region, date) and fact tables for fast OLAP aggregations.
              </p>
            </div>

            <div className="bg-gray-900/60 border border-gray-800 rounded-2xl p-6 hover:border-indigo-500/50 transition">
              <div className="w-12 h-12 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center mb-4">
                <LineChart className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">ML Forecasting & RFM</h3>
              <p className="text-sm text-gray-400">
                Time-series forecasting, K-Means customer RFM segmentation, and Isolation Forest sales anomaly detection.
              </p>
            </div>

            <div className="bg-gray-900/60 border border-gray-800 rounded-2xl p-6 hover:border-purple-500/50 transition">
              <div className="w-12 h-12 rounded-xl bg-purple-500/10 text-purple-400 flex items-center justify-center mb-4">
                <BrainCircuit className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">AI Analytics Copilot</h3>
              <p className="text-sm text-gray-400">
                Natural-language Q&A powered by tool calling that translates questions into read-only SQL queries with zero hallucination.
              </p>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-800/60 py-8 px-6 text-center text-xs text-gray-500">
        <p>© 2026 InsightBI AI Platform. Built with Python, FastAPI, PostgreSQL, Power BI, Next.js & Docker.</p>
      </footer>
    </div>
  );
}

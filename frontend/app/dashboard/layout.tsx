'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, TrendingUp, Users, Package, Bot, Bell, User, Upload, RefreshCw, HelpCircle, ChevronDown } from 'lucide-react';
import DataUploadModal from '../components/DataUploadModal';

const NAV_ITEMS = [
  { name: 'Overview', hint: 'Executive summary', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Sales', hint: 'Revenue & regions', href: '/dashboard/sales', icon: TrendingUp },
  { name: 'Customers', hint: 'Segments & retention', href: '/dashboard/customers', icon: Users },
  { name: 'Products', hint: 'Catalog performance', href: '/dashboard/products', icon: Package },
  { name: 'Ask AI', hint: 'Natural language analysis', href: '/dashboard/copilot', icon: Bot },
];

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [isUploadOpen, setIsUploadOpen] = useState(false);
  const currentPage = NAV_ITEMS.find((item) => item.href === pathname) || NAV_ITEMS[0];

  return (
    <div className="flex min-h-screen bg-[#f5f6f8] text-slate-900">
      <aside className="hidden w-[250px] shrink-0 flex-col border-r border-slate-200 bg-white lg:flex">
        <div className="flex items-center gap-3 border-b border-slate-100 px-5 py-5">
          <div className="grid h-9 w-9 place-items-center rounded-lg bg-[#f2c811] text-sm font-black text-slate-900 shadow-sm">BI</div>
          <div><h1 className="text-base font-bold tracking-tight text-slate-900">InsightBI</h1><p className="text-[11px] font-medium text-slate-500">Business intelligence</p></div>
        </div>
        <div className="px-3 pt-6">
          <p className="px-3 pb-2 text-[10px] font-bold uppercase tracking-[0.12em] text-slate-400">My workspace</p>
          <nav className="space-y-1">
            {NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;
              return <Link key={item.href} href={item.href} className={`group flex items-center gap-3 rounded-md px-3 py-2.5 text-sm transition ${isActive ? 'bg-[#fff8d6] font-semibold text-slate-950' : 'font-medium text-slate-600 hover:bg-slate-100 hover:text-slate-950'}`}>
                <Icon className={`h-4 w-4 ${isActive ? 'text-[#8a6500]' : 'text-slate-400 group-hover:text-slate-700'}`} /><span>{item.name}</span>{isActive && <span className="ml-auto h-1.5 w-1.5 rounded-full bg-[#f2c811]" />}
              </Link>;
            })}
          </nav>
        </div>
        <div className="mx-3 mt-6 rounded-lg border border-[#f6df7c] bg-[#fff9dc] p-3.5"><p className="text-xs font-bold text-slate-800">New data to explore?</p><p className="mt-1 text-[11px] leading-relaxed text-slate-600">Upload a sales CSV and every report refreshes automatically.</p><button onClick={() => setIsUploadOpen(true)} className="mt-3 text-xs font-bold text-[#745700] hover:underline">Import data →</button></div>
        <div className="mt-auto border-t border-slate-100 p-3"><button className="flex w-full items-center gap-3 rounded-md p-2 text-left hover:bg-slate-50"><div className="grid h-8 w-8 place-items-center rounded-full bg-slate-100"><User className="h-4 w-4 text-slate-500" /></div><div><p className="text-xs font-semibold text-slate-700">Executive User</p><p className="text-[10px] text-slate-500">Workspace owner</p></div><ChevronDown className="ml-auto h-3.5 w-3.5 text-slate-400" /></button></div>
      </aside>
      <div className="min-w-0 flex-1">
        <header className="sticky top-0 z-20 flex h-16 items-center justify-between border-b border-slate-200 bg-white/95 px-4 backdrop-blur lg:px-7">
          <div className="min-w-0"><p className="text-[11px] font-medium text-slate-500">My workspace / {currentPage.name}</p><h2 className="truncate text-sm font-bold text-slate-800">{currentPage.hint}</h2></div>
          <div className="flex items-center gap-2"><button title="Refresh reports" onClick={() => window.location.reload()} className="hidden items-center gap-1.5 rounded-md border border-slate-200 px-3 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-50 sm:flex"><RefreshCw className="h-3.5 w-3.5" /> Refresh</button><button onClick={() => setIsUploadOpen(true)} className="flex items-center gap-2 rounded-md bg-[#f2c811] px-3.5 py-2 text-xs font-bold text-slate-900 shadow-sm transition hover:bg-[#e3b900]"><Upload className="h-3.5 w-3.5" /> Get data</button><button title="Help" className="grid h-8 w-8 place-items-center rounded-md text-slate-500 hover:bg-slate-100"><HelpCircle className="h-4 w-4" /></button><button title="Notifications" className="relative grid h-8 w-8 place-items-center rounded-md text-slate-500 hover:bg-slate-100"><Bell className="h-4 w-4" /><span className="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-[#f2c811]" /></button></div>
        </header>
        <main className="mx-auto max-w-[1600px] p-4 pb-24 sm:p-5 sm:pb-24 lg:p-7">{children}</main>
      </div>
      <nav aria-label="Dashboard navigation" className="fixed inset-x-0 bottom-0 z-30 flex border-t border-slate-200 bg-white/95 px-1 pb-[env(safe-area-inset-bottom)] backdrop-blur lg:hidden">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;
          return <Link key={item.href} href={item.href} className={`flex min-w-0 flex-1 flex-col items-center gap-1 px-1 py-2 text-[10px] font-semibold ${isActive ? 'text-[#765900]' : 'text-slate-500'}`}>
            <Icon className={`h-4 w-4 ${isActive ? 'text-[#8a6500]' : ''}`} />
            <span className="truncate">{item.name}</span>
          </Link>;
        })}
      </nav>
      <DataUploadModal isOpen={isUploadOpen} onClose={() => setIsUploadOpen(false)} onUploadSuccess={() => setTimeout(() => window.location.reload(), 1200)} />
    </div>
  );
}

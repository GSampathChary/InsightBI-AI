import { CheckCircle2, Info } from 'lucide-react';

export default function DataModeNotice({ isDemo }: { isDemo: boolean }) {
  return (
    <div
      role="status"
      className={`flex items-start gap-2 rounded-md border px-3 py-2 text-xs ${isDemo ? 'border-amber-200 bg-amber-50 text-amber-900' : 'border-emerald-200 bg-emerald-50 text-emerald-800'}`}
    >
      {isDemo ? <Info className="mt-0.5 h-4 w-4 shrink-0 text-amber-700" /> : <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-emerald-700" />}
      <p>{isDemo ? 'Demo data is displayed because the API is unavailable. Set NEXT_PUBLIC_API_URL and allow this Vercel domain in the backend CORS settings to show live data.' : 'Live API data connected.'}</p>
    </div>
  );
}

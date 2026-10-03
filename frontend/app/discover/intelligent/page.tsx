"use client";

import { useState } from "react";
import { discoverIntelligent } from "@/lib/api";
import AppCard from "@/components/apps/AppCard";
import { Search, Loader2 } from "lucide-react";

export default function IntelligentSearchPage() {
  const [keyword, setKeyword] = useState("");
  const [limit, setLimit] = useState(20);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!keyword.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const data = await discoverIntelligent({ keyword, limit });
      setResults(data.relevant_apps || data.apps || (Array.isArray(data) ? data : []));
    } catch (err: any) {
      setError(err.message || "Failed to search");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-6xl mx-auto w-full">
      <header className="mb-8">
        <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">Intelligent Search</h1>
        <p className="text-gray-500 mt-2">Discover apps using advanced filtering parameters.</p>
      </header>

      <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 mb-8">
        <form onSubmit={handleSearch} className="flex gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="e.g. AI Planner, Meditation..."
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              className="w-full pl-12 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white transition-all text-gray-900"
            />
          </div>
          <input
            type="number"
            value={limit}
            onChange={(e) => setLimit(Number(e.target.value))}
            className="w-24 px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
            placeholder="Limit"
            min={1}
            max={100}
          />
          <button
            type="submit"
            disabled={loading || !keyword.trim()}
            className="px-8 py-3 bg-indigo-600 text-white font-medium rounded-xl hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? <Loader2 className="w-5 h-5 animate-spin mx-auto" /> : "Search"}
          </button>
        </form>
      </div>

      {error && (
        <div className="p-4 bg-red-50 text-red-700 rounded-xl border border-red-100 mb-8">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {Array.isArray(results) && results.map((app: any, idx: number) => (
          <AppCard key={app.appId || idx} app={app} />
        ))}
      </div>

      {!loading && !error && results.length === 0 && keyword && (
        <div className="text-center py-20 text-gray-500 bg-white rounded-2xl border border-gray-100 border-dashed">
          No apps found matching your criteria.
        </div>
      )}
    </div>
  );
}
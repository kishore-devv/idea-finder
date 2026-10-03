"use client";

import { useState } from "react";
import { discoverBatch } from "@/lib/api";
import AppCard from "@/components/apps/AppCard";
import { List, Loader2, Plus, X } from "lucide-react";

export default function BatchSearchPage() {
  const [keywordInput, setKeywordInput] = useState("");
  const [keywords, setKeywords] = useState<string[]>([]);
  const [limit, setLimit] = useState(20);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<Record<string, any[]>>({});
  const [error, setError] = useState<string | null>(null);

  const addKeyword = () => {
    if (keywordInput.trim() && !keywords.includes(keywordInput.trim())) {
      setKeywords([...keywords, keywordInput.trim()]);
      setKeywordInput("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      addKeyword();
    }
  };

  const removeKeyword = (kw: string) => {
    setKeywords(keywords.filter(k => k !== kw));
  };

  const handleSearch = async () => {
    if (keywords.length === 0) return;

    setLoading(true);
    setError(null);
    try {
      const data = await discoverBatch({ keywords, limit });
      const batchData = data.results || data;
      const parsedResults: Record<string, any[]> = {};
      if (batchData.keyword_results) {
        batchData.keyword_results.forEach((item: any) => {
          parsedResults[item.keyword] = item.apps || [];
        });
      }
      setResults(parsedResults);
    } catch (err: any) {
      setError(err.message || "Failed to search");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-6xl mx-auto w-full">
      <header className="mb-8">
        <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">Batch Search</h1>
        <p className="text-gray-500 mt-2">Search multiple keywords simultaneously.</p>
      </header>

      <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 mb-8">
        <div className="mb-4 flex flex-wrap gap-2">
          {keywords.map(kw => (
            <span key={kw} className="inline-flex items-center gap-1 px-3 py-1 bg-indigo-50 text-indigo-700 rounded-full text-sm font-medium border border-indigo-100">
              {kw}
              <button onClick={() => removeKeyword(kw)} className="text-indigo-400 hover:text-indigo-600 focus:outline-none">
                <X className="w-4 h-4" />
              </button>
            </span>
          ))}
        </div>

        <div className="flex gap-4">
          <div className="flex-1 relative">
            <List className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Add keyword and press enter..."
              value={keywordInput}
              onChange={(e) => setKeywordInput(e.target.value)}
              onKeyDown={handleKeyDown}
              className="w-full pl-12 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white transition-all text-gray-900"
            />
          </div>
          <button
            type="button"
            onClick={addKeyword}
            disabled={!keywordInput.trim()}
            className="px-4 py-3 bg-gray-100 text-gray-700 font-medium rounded-xl hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-300 disabled:opacity-50 transition-colors"
          >
            <Plus className="w-5 h-5" />
          </button>

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
            onClick={handleSearch}
            disabled={loading || keywords.length === 0}
            className="px-8 py-3 bg-indigo-600 text-white font-medium rounded-xl hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? <Loader2 className="w-5 h-5 animate-spin mx-auto" /> : "Search All"}
          </button>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-50 text-red-700 rounded-xl border border-red-100 mb-8">
          {error}
        </div>
      )}

      <div className="space-y-12">
        {Object.entries(results).map(([kw, apps]) => (
          <div key={kw}>
            <h2 className="text-2xl font-bold text-gray-800 mb-6 border-b pb-2">Results for: "{kw}"</h2>
            {apps.length === 0 ? (
              <p className="text-gray-500">No results found.</p>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {apps.map((app: any, idx: number) => (
                  <AppCard key={app.appId || idx} app={app} />
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

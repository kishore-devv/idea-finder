"use client";

import { useState } from "react";
import { discoverHiddenGems } from "@/lib/api";
import AppCard from "@/components/apps/AppCard";
import { Sparkles, Loader2 } from "lucide-react";

export default function HiddenGemsPage() {
    const [minInstalls, setMinInstalls] = useState(10000);
    const [maxInstalls, setMaxInstalls] = useState(1000000);
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState<any[]>([]);
    const [error, setError] = useState<string | null>(null);

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();

        setLoading(true);
        setError(null);
        try {
            const data = await discoverHiddenGems(minInstalls, maxInstalls);
            setResults(data.hidden_gems || data || []);
        } catch (err: any) {
            setError(err.message || "Failed to find hidden gems");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-8 max-w-6xl mx-auto w-full">
            <header className="mb-8 flex items-center gap-3">
                <Sparkles className="w-10 h-10 text-pink-600" />
                <div>
                    <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">Hidden Gems</h1>
                    <p className="text-gray-500 mt-2">Find highly-rated apps with lower install numbers that deserve attention.</p>
                </div>
            </header>

            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 mb-8">
                <form onSubmit={handleSearch} className="flex gap-4 items-end">
                    <div className="flex-1">
                        <label className="block text-sm font-medium text-gray-700 mb-2">Min Installs</label>
                        <input
                            type="number"
                            value={minInstalls}
                            onChange={(e) => setMinInstalls(Number(e.target.value))}
                            className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-pink-500 text-gray-900"
                        />
                    </div>
                    <div className="flex-1">
                        <label className="block text-sm font-medium text-gray-700 mb-2">Max Installs</label>
                        <input
                            type="number"
                            value={maxInstalls}
                            onChange={(e) => setMaxInstalls(Number(e.target.value))}
                            className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-pink-500 text-gray-900"
                        />
                    </div>
                    <button
                        type="submit"
                        disabled={loading}
                        className="px-8 py-3 h-[52px] bg-pink-600 text-white font-medium rounded-xl hover:bg-pink-700 focus:outline-none focus:ring-2 focus:ring-pink-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        {loading ? <Loader2 className="w-5 h-5 animate-spin mx-auto" /> : "Find Gems"}
                    </button>
                </form>
            </div>

            {error && (
                <div className="p-4 bg-red-50 text-red-700 rounded-xl border border-red-100 mb-8">
                    {error}
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {results.map((app: any, idx: number) => (
                    <AppCard key={app.appId || idx} app={app} />
                ))}
            </div>

            {!loading && !error && results.length === 0 && <div className="text-center py-20 text-gray-500 bg-white rounded-2xl border border-gray-100 border-dashed">Adjust thresholds and search to uncover Hidden Gems.</div>}
        </div>
    );
}

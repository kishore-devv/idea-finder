"use client";

import { useState } from "react";
import { exploreCategory } from "@/lib/api";
import AppCard from "@/components/apps/AppCard";
import { LayoutDashboard, Loader2 } from "lucide-react";

export default function CategoriesPage() {
    const [category, setCategory] = useState("PRODUCTIVITY");
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState<any[]>([]);
    const [error, setError] = useState<string | null>(null);

    const GOOGLE_PLAY_CATEGORIES = [
        "ART_AND_DESIGN", "AUTO_AND_VEHICLES", "BEAUTY", "BOOKS_AND_REFERENCE", "BUSINESS",
        "COMICS", "COMMUNICATION", "DATING", "EDUCATION", "ENTERTAINMENT", "EVENTS",
        "FINANCE", "FOOD_AND_DRINK", "HEALTH_AND_FITNESS", "HOUSE_AND_HOME",
        "LIBRARIES_AND_DEMO", "LIFESTYLE", "MAPS_AND_NAVIGATION", "MEDICAL",
        "MUSIC_AND_AUDIO", "NEWS_AND_MAGAZINES", "PARENTING", "PERSONALIZATION",
        "PHOTOGRAPHY", "PRODUCTIVITY", "SHOPPING", "SOCIAL", "SPORTS", "TOOLS",
        "TRAVEL_AND_LOCAL", "VIDEO_PLAYERS", "WEATHER"
    ];

    const handleExplore = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!category) return;

        setLoading(true);
        setError(null);
        try {
            const data = await exploreCategory({ category });
            setResults(data.apps || data || []);
        } catch (err: any) {
            setError(err.message || "Failed to explore category");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-8 max-w-6xl mx-auto w-full">
            <header className="mb-8">
                <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">Category Explorer</h1>
                <p className="text-gray-500 mt-2">Deep dive into specific Google Play categories.</p>
            </header>

            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 mb-8">
                <form onSubmit={handleExplore} className="flex gap-4">
                    <div className="flex-1 relative">
                        <LayoutDashboard className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5" />
                        <select
                            value={category}
                            onChange={(e) => setCategory(e.target.value)}
                            className="w-full pl-12 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white transition-all text-gray-900 appearance-none"
                        >
                            <option value="" disabled>Select a category...</option>
                            {GOOGLE_PLAY_CATEGORIES.map(cat => (
                                <option key={cat} value={cat}>{cat.replace(/_/g, ' ')}</option>
                            ))}
                        </select>
                    </div>
                    <button
                        type="submit"
                        disabled={loading || !category}
                        className="px-8 py-3 bg-emerald-600 text-white font-medium rounded-xl hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        {loading ? <Loader2 className="w-5 h-5 animate-spin mx-auto" /> : "Explore"}
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

            {!loading && !error && results.length === 0 && <div className="text-center py-20 text-gray-500 bg-white rounded-2xl border border-gray-100 border-dashed">Select a category and hit Explore to see apps.</div>}
        </div>
    );
}

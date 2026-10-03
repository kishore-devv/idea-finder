"use client";

import { useEffect, useState } from "react";
import { getMarketPainPoints } from "@/lib/api";
import { Activity, Loader2, AlertCircle } from "lucide-react";

export default function MarketAnalysisPage() {
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function loadData() {
            try {
                const result = await getMarketPainPoints();
                setData(result);
            } catch (err: any) {
                setError(err.message || "Failed to load market pain points");
            } finally {
                setLoading(false);
            }
        }
        loadData();
    }, []);

    return (
        <div className="p-8 max-w-6xl mx-auto w-full">
            <header className="mb-8">
                <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">Market Pain Points</h1>
                <p className="text-gray-500 mt-2">Identify opportunities by finding gaps and poor user experiences.</p>
            </header>

            {error && (
                <div className="p-4 bg-red-50 text-red-700 rounded-xl border border-red-100 mb-8 flex items-center gap-3">
                    <AlertCircle className="w-5 h-5" />
                    {error}
                </div>
            )}

            {loading ? (
                <div className="flex justify-center items-center py-32">
                    <Loader2 className="w-10 h-10 animate-spin text-amber-500" />
                </div>
            ) : data ? (
                <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 mb-8 max-w-4xl">
                    <pre className="whitespace-pre-wrap font-mono text-sm text-gray-700 bg-gray-50 p-6 rounded-xl border border-gray-200">
                        {JSON.stringify(data, null, 2)}
                    </pre>
                </div>
            ) : (
                <div className="text-center py-20 text-gray-500 bg-white rounded-2xl border border-gray-100 border-dashed">
                    No data available.
                </div>
            )}
        </div>
    );
}

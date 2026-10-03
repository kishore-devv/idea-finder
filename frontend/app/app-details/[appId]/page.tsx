"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { analyzeApp, getAppReviews } from "@/lib/api";
import { Loader2, Star, Search, AlertCircle, ThumbsUp, ChevronLeft, ChevronRight } from "lucide-react";

export default function AppDetailsPage() {
    const { appId } = useParams() as { appId: string };

    const [loading, setLoading] = useState(true);
    const [analysis, setAnalysis] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);

    // Pagination & Reviews state
    const [reviews, setReviews] = useState<any[]>([]);
    const [totalReviews, setTotalReviews] = useState(0);
    const [limit] = useState(20);
    const [offset, setOffset] = useState(0);
    const [filterRating, setFilterRating] = useState<number | null>(null);
    const [searchQuery, setSearchQuery] = useState("");
    const [isFetchingReviews, setIsFetchingReviews] = useState(false);

    useEffect(() => {
        async function fetchBasicData() {
            try {
                const analysisData = await analyzeApp(appId).catch(() => null);
                setAnalysis(analysisData);
            } catch (err: any) {
                setError(err.message || "Failed to load app basic details");
            }
        }
        if (appId) {
            fetchBasicData();
        }
    }, [appId]);

    useEffect(() => {
        async function loadReviews() {
            setIsFetchingReviews(true);
            try {
                const reviewsData = await getAppReviews(appId, limit, offset, filterRating, searchQuery);
                setReviews(reviewsData.reviews || []);
                setTotalReviews(reviewsData.total || 0);
            } catch (err: any) {
                console.error("Failed to load reviews:", err);
            } finally {
                setIsFetchingReviews(false);
                setLoading(false);
            }
        }

        // Debounce the review loading slightly so typing in search doesn't spam backend
        const timeout = setTimeout(() => {
            if (appId) loadReviews();
        }, 400);

        return () => clearTimeout(timeout);
    }, [appId, limit, offset, filterRating, searchQuery]);

    const handleNextPage = () => {
        if (offset + limit < totalReviews) {
            setOffset(offset + limit);
        }
    };

    const handlePrevPage = () => {
        if (offset - limit >= 0) {
            setOffset(offset - limit);
        }
    };

    if (loading) {
        return (
            <div className="flex h-screen items-center justify-center">
                <Loader2 className="w-10 h-10 animate-spin text-indigo-500" />
            </div>
        );
    }

    return (
        <div className="p-8 max-w-6xl mx-auto w-full space-y-8">
            <header>
                <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">App Details & Reviews</h1>
                <p className="text-gray-500 mt-2">App ID: {appId}</p>
            </header>

            {error && (
                <div className="p-4 bg-red-50 text-red-700 rounded-xl border border-red-100 flex items-center gap-3">
                    <AlertCircle className="w-5 h-5" />
                    {error}
                </div>
            )}

            {analysis && !analysis.error && (
                <section className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="col-span-1 border-r border-gray-100 pr-6">
                        <h2 className="text-xl font-bold">{analysis.app?.title || "Unknown App"}</h2>
                        <p className="text-gray-500 mb-4">{analysis.app?.developer}</p>
                        <div className="flex items-center gap-2 font-semibold">
                            <Star className="w-5 h-5 text-yellow-400 fill-yellow-400" />
                            {analysis.app?.score?.toFixed(1)} / 5.0
                        </div>
                        <p className="text-sm text-gray-500 mt-2">{analysis.app?.reviews} Total Reviews on Store</p>
                    </div>
                    <div className="col-span-2">
                        <h3 className="font-semibold text-gray-800 mb-4">Sentiment Breakdown (Analyzed: {analysis.review_analysis?.total_reviews})</h3>
                        <div className="flex gap-4">
                            <div className="bg-emerald-50 text-emerald-700 px-4 py-2 rounded-lg flex-1 text-center font-medium border border-emerald-100">
                                Positive: {analysis.review_analysis?.positive}
                            </div>
                            <div className="bg-gray-50 text-gray-700 px-4 py-2 rounded-lg flex-1 text-center font-medium border border-gray-200">
                                Neutral: {analysis.review_analysis?.neutral}
                            </div>
                            <div className="bg-red-50 text-red-700 px-4 py-2 rounded-lg flex-1 text-center font-medium border border-red-100">
                                Negative: {analysis.review_analysis?.negative}
                            </div>
                        </div>
                    </div>
                </section>
            )}

            <section className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 relative">
                <h2 className="text-2xl font-bold mb-6">Reviews Explorer</h2>
                <div className="flex flex-wrap md:flex-nowrap gap-4 mb-8">
                    <div className="relative flex-1">
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5" />
                        <input
                            type="text"
                            placeholder="Search specific keywords across ALL reviews from DB..."
                            value={searchQuery}
                            onChange={(e) => {
                                setSearchQuery(e.target.value);
                                setOffset(0); // Reset pagination on search
                            }}
                            className="w-full pl-12 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
                        />
                    </div>
                    <select
                        value={filterRating || ""}
                        onChange={(e) => {
                            setFilterRating(e.target.value ? Number(e.target.value) : null);
                            setOffset(0); // Reset pagination on filter
                        }}
                        className="w-full md:w-48 px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
                    >
                        <option value="">All Ratings</option>
                        {[5, 4, 3, 2, 1].map(r => (
                            <option key={r} value={r}>{r} Stars</option>
                        ))}
                    </select>
                </div>

                <div className="space-y-4 min-h-[300px]">
                    <div className="flex justify-between items-center text-sm text-gray-500 font-medium">
                        <span>Showing {offset + 1}-{Math.min(offset + limit, totalReviews)} of {totalReviews} reviews.</span>
                        {isFetchingReviews && <span className="flex items-center gap-2"><Loader2 className="w-4 h-4 animate-spin" /> Fetching...</span>}
                    </div>

                    {reviews.length === 0 && !isFetchingReviews ? (
                        <div className="py-20 text-center text-gray-500 border border-dashed rounded-xl border-gray-200">
                            No reviews match your filters.
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {reviews.map((r, idx) => (
                                <div key={r.review_id || idx} className="p-5 border border-gray-100 rounded-xl bg-gray-50 hover:bg-gray-100 transition-colors">
                                    <div className="flex justify-between items-start mb-3">
                                        <div className="flex text-yellow-400">
                                            {Array.from({ length: 5 }).map((_, i) => (
                                                <Star key={i} className={`w-4 h-4 ${i < r.score ? "fill-yellow-400" : "text-gray-300"}`} />
                                            ))}
                                        </div>
                                        {r.thumbs_up > 0 && (
                                            <span className="flex items-center gap-1 text-xs font-medium text-gray-500 bg-white px-2 py-1 rounded-full border border-gray-200">
                                                <ThumbsUp className="w-3 h-3" />
                                                {r.thumbs_up}
                                            </span>
                                        )}
                                    </div>
                                    <p className="text-gray-700 text-sm whitespace-pre-wrap leading-relaxed">{r.text}</p>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {/* Pagination Controls */}
                <div className="flex justify-center items-center gap-4 mt-8 pt-6 border-t border-gray-100">
                    <button
                        onClick={handlePrevPage}
                        disabled={offset === 0 || isFetchingReviews}
                        className="flex items-center gap-1 px-4 py-2 border border-gray-200 rounded-lg bg-white text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        <ChevronLeft className="w-4 h-4" /> Prev
                    </button>
                    <span className="text-sm font-medium text-gray-500">
                        Page {Math.floor(offset / limit) + 1} of {Math.max(1, Math.ceil(totalReviews / limit))}
                    </span>
                    <button
                        onClick={handleNextPage}
                        disabled={offset + limit >= totalReviews || isFetchingReviews}
                        className="flex items-center gap-1 px-4 py-2 border border-gray-200 rounded-lg bg-white text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        Next <ChevronRight className="w-4 h-4" />
                    </button>
                </div>
            </section>
        </div>
    );
}

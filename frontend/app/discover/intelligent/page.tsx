"use client";

import { FormEvent, useState } from "react";
import { discoverIntelligent } from "@/lib/api";

type AppResult = {
  appId?: string | null;
  icon?: string | null;
  screenshots?: string[];
  title?: string | null;
  score?: number | null;
  genre?: string | null;
  price?: number | null;
  free?: boolean | null;
  description?: string | null;
  developer?: string | null;
  installs?: string | null;
  relevance_score?: number | null;
};

type DiscoveryResponse = {
  keyword: string;
  total_candidates_found: number;
  filtered_apps_found: number;
  relevant_apps_found: number;
  relevant_apps: AppResult[];
};

const installBuckets = [
  "0-1k",
  "1k-5k",
  "5k-10k",
  "10k-20k",
  "20k-50k",
  "50k-100k",
  "100k-200k",
  "200k-300k",
  "300k-500k",
  "500k-1m",
  "1m-2m",
  "2m-5m",
  "5m-10m",
  "10m-20m",
  "20m-50m",
  "50m-100m",
  "100m+",
];

export default function IntelligentDiscoveryPage() {
  const [keyword, setKeyword] = useState("");
  const [limit, setLimit] = useState(20);

  const [category, setCategory] = useState("");

  const [minRating, setMinRating] = useState("");
  const [maxRating, setMaxRating] = useState("");

  const [minRatings, setMinRatings] = useState("");
  const [maxRatings, setMaxRatings] = useState("");

  const [minReviews, setMinReviews] = useState("");
  const [maxReviews, setMaxReviews] = useState("");

  const [minInstalls, setMinInstalls] = useState("");
  const [maxInstalls, setMaxInstalls] = useState("");

  const [installBucket, setInstallBucket] = useState("");

  const [free, setFree] = useState("");
  const [containsAds, setContainsAds] = useState("");
  const [offersIap, setOffersIap] = useState("");

  const [developer, setDeveloper] = useState("");

  const [recentlyUpdatedDays, setRecentlyUpdatedDays] = useState("");
  const [oldNotUpdatedDays, setOldNotUpdatedDays] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [results, setResults] = useState<DiscoveryResponse | null>(null);

  function numberOrNull(value: string) {
    return value === "" ? null : Number(value);
  }

  function booleanOrNull(value: string) {
    if (value === "") return null;
    return value === "yes";
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();

    if (!keyword.trim()) {
      setError("Please enter a keyword.");
      return;
    }

    setLoading(true);
    setError("");
    setResults(null);

    try {
      const response = await discoverIntelligent({
        keyword: keyword.trim(),
        limit,

        category: category || null,

        min_rating: numberOrNull(minRating),
        max_rating: numberOrNull(maxRating),

        min_ratings: numberOrNull(minRatings),
        max_ratings: numberOrNull(maxRatings),

        min_reviews: numberOrNull(minReviews),
        max_reviews: numberOrNull(maxReviews),

        min_installs: numberOrNull(minInstalls),
        max_installs: numberOrNull(maxInstalls),

        install_bucket: installBucket || null,

        free: booleanOrNull(free),
        contains_ads: booleanOrNull(containsAds),
        offers_iap: booleanOrNull(offersIap),

        developer: developer || null,

        recently_updated_days: numberOrNull(recentlyUpdatedDays),
        old_not_updated_days: numberOrNull(oldNotUpdatedDays),
      });

      setResults(response);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong while discovering apps."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-7xl px-6 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Intelligent Discovery</h1>
        <p className="mt-2 text-gray-500">
          Discover relevant Google Play apps using search and data filters.
        </p>
      </div>

      <form
        onSubmit={handleSubmit}
        className="space-y-8 rounded-xl border bg-white p-6 shadow-sm"
      >
        <section>
          <h2 className="mb-4 text-xl font-semibold">Search</h2>

          <div className="grid gap-4 md:grid-cols-[1fr_140px_auto]">
            <input
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              placeholder="Example: travel buddy"
              className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            />

            <input
              type="number"
              min={1}
              max={100}
              value={limit}
              onChange={(e) => setLimit(Number(e.target.value))}
              className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            />

            <button
              type="submit"
              disabled={loading}
              className="rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:hover:bg-blue-600"
            >
              {loading ? "Discovering..." : "Discover Apps"}
            </button>
          </div>
        </section>

        <section>
          <h2 className="mb-4 text-xl font-semibold">Filters</h2>

          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            <input
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              placeholder="Category"
              className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 placeholder-gray-400 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            />

            <input
              value={developer}
              onChange={(e) => setDeveloper(e.target.value)}
              placeholder="Developer"
              className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 placeholder-gray-400 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            />

            <select
              value={installBucket}
              onChange={(e) => setInstallBucket(e.target.value)}
              className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            >
              <option value="">Install bucket</option>
              {installBuckets.map((bucket) => (
                <option key={bucket} value={bucket}>
                  {bucket}
                </option>
              ))}
            </select>

            <input
              type="number"
              step="0.1"
              value={minRating}
              onChange={(e) => setMinRating(e.target.value)}
              placeholder="Minimum rating"
              className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 placeholder-gray-400 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            />

            <input
              type="number"
              step="0.1"
              value={maxRating}
              onChange={(e) => setMaxRating(e.target.value)}
              placeholder="Maximum rating"
              className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 placeholder-gray-400 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            />

            <input
              type="number"
              value={minRatings}
              onChange={(e) => setMinRatings(e.target.value)}
              placeholder="Minimum ratings"
              className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 placeholder-gray-400 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            />

            <input
              type="number"
              value={maxRatings}
              onChange={(e) => setMaxRatings(e.target.value)}
              placeholder="Maximum ratings"
              className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 placeholder-gray-400 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            />

            <input
              type="number"
              value={minReviews}
              onChange={(e) => setMinReviews(e.target.value)}
              placeholder="Minimum reviews"
              className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 placeholder-gray-400 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            />

            <input
              type="number"
              value={maxReviews}
              onChange={(e) => setMaxReviews(e.target.value)}
              placeholder="Maximum reviews"
              className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 placeholder-gray-400 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            />

            <input
              type="number"
              value={minInstalls}
              onChange={(e) => setMinInstalls(e.target.value)}
              placeholder="Minimum installs"
              className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 placeholder-gray-400 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            />

            <input
              type="number"
              value={maxInstalls}
              onChange={(e) => setMaxInstalls(e.target.value)}
              placeholder="Maximum installs"
              className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 placeholder-gray-400 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            />

            <select
              value={free}
              onChange={(e) => setFree(e.target.value)}
              className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            >
              <option value="">Free / Paid: Any</option>
              <option value="yes">Free</option>
              <option value="no">Paid</option>
            </select>

            <select
              value={containsAds}
              onChange={(e) => setContainsAds(e.target.value)}
              className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            >
              <option value="">Ads: Any</option>
              <option value="yes">Has ads</option>
              <option value="no">No ads</option>
            </select>

            <select
              value={offersIap}
              onChange={(e) => setOffersIap(e.target.value)}
              className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            >
              <option value="">IAP: Any</option>
              <option value="yes">Has IAP</option>
              <option value="no">No IAP</option>
            </select>

            <input
              type="number"
              value={recentlyUpdatedDays}
              onChange={(e) => setRecentlyUpdatedDays(e.target.value)}
              placeholder="Updated within days"
              className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 placeholder-gray-400 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            />

            <input
              type="number"
              value={oldNotUpdatedDays}
              onChange={(e) => setOldNotUpdatedDays(e.target.value)}
              placeholder="Not updated for days"
              className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 placeholder-gray-400 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            />
          </div>
        </section>
      </form>

      {error && (
        <div className="mt-6 rounded-lg border border-red-200 bg-red-50 p-4 text-red-700">
          {error}
        </div>
      )}

      {results && (
        <section className="mt-8">
          <div className="grid gap-4 md:grid-cols-3">
            <div className="rounded-xl border bg-white p-5 shadow-sm">
              <p className="text-sm text-gray-500">Candidates</p>
              <p className="mt-2 text-3xl font-bold">
                {results.total_candidates_found}
              </p>
            </div>

            <div className="rounded-xl border bg-white p-5 shadow-sm">
              <p className="text-sm text-gray-500">Filtered</p>
              <p className="mt-2 text-3xl font-bold">
                {results.filtered_apps_found}
              </p>
            </div>

            <div className="rounded-xl border bg-white p-5 shadow-sm">
              <p className="text-sm text-gray-500">Relevant</p>
              <p className="mt-2 text-3xl font-bold">
                {results.relevant_apps_found}
              </p>
            </div>
          </div>

          {results.relevant_apps.length === 0 ? (
            <div className="mt-8 rounded-xl border bg-white p-8 text-center">
              No relevant apps found.
            </div>
          ) : (
            <div className="mt-8 grid gap-5 md:grid-cols-2">
              {results.relevant_apps.map((app, index) => (
                <article
                  key={`${app.appId ?? app.title ?? "app"}-${index}`}
                  className="rounded-xl border bg-white p-5 shadow-sm"
                >
                  <div className="flex gap-4">
                    {app.icon ? (
                      // eslint-disable-next-line @next/next/no-img-element
                      <img
                        src={app.icon}
                        alt={app.title ?? "App icon"}
                        className="h-16 w-16 rounded-xl object-cover"
                      />
                    ) : (
                      <div className="h-16 w-16 rounded-xl border" />
                    )}

                    <div className="min-w-0 flex-1">
                      <h3 className="text-lg font-semibold">
                        {app.title || "Untitled app"}
                      </h3>

                      <p className="text-sm text-gray-500">
                        {app.developer || "Unknown developer"}
                      </p>

                      <div className="mt-2 flex flex-wrap gap-2 text-sm">
                        <span>⭐ {app.score ?? "N/A"}</span>
                        <span>{app.genre || "Unknown category"}</span>
                        <span>{app.installs || "Unknown installs"}</span>
                      </div>
                    </div>
                  </div>

                  <div className="mt-4 flex flex-wrap gap-2 text-sm">
                    <span className="rounded-full border px-3 py-1">
                      {app.free ? "Free" : "Paid"}
                    </span>

                    <span className="rounded-full border px-3 py-1">
                      Relevance: {app.relevance_score ?? "N/A"}
                    </span>
                  </div>

                  <p className="mt-4 line-clamp-3 text-sm text-gray-600">
                    {app.description || "No description available."}
                  </p>
                </article>
              ))}
            </div>
          )}
        </section>
      )}
    </main>
  );
}
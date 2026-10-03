
"use client";

import { FormEvent, useState } from "react";
import { discoverBatch } from "@/lib/api";

type BatchApp = {
  app_id?: string | null;
  title?: string | null;
  score?: number | null;
  installs?: string | null;
  reviews_scraped?: number | null;
};

type BatchResult = {
  keyword: string;
  discovered?: number;
  duplicates?: number;
  skipped?: number;
  apps?: BatchApp[];
};

type BatchResponse = {
  total_keywords: number;
  results: BatchResult[];
};

export default function BatchDiscoveryPage() {
  const [keywords, setKeywords] = useState("");
  const [limit, setLimit] = useState(20);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [results, setResults] = useState<BatchResponse | null>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();

    const keywordList = keywords
      .split("\n")
      .map((keyword) => keyword.trim())
      .filter(Boolean);

    if (keywordList.length === 0) {
      setError("Enter at least one keyword.");
      return;
    }

    setLoading(true);
    setError("");
    setResults(null);

    try {
      const response = await discoverBatch({
        keywords: keywordList,
        limit,
      });

      setResults(response);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong while running batch discovery."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-7xl px-6 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Batch Discovery</h1>

        <p className="mt-2 text-gray-500">
          Search multiple keywords in one discovery operation.
        </p>
      </div>

      <form
        onSubmit={handleSubmit}
        className="rounded-xl border bg-white p-6 shadow-sm"
      >
        <div className="grid gap-5 md:grid-cols-[1fr_140px]">
          <div>
            <label className="mb-2 block text-sm font-medium">
              Keywords
            </label>

            <textarea
              value={keywords}
              onChange={(e) => setKeywords(e.target.value)}
              placeholder={`travel buddy
budget planner
habit tracker
meal planner`}
              rows={8}
              className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2"
            />

            <p className="mt-2 text-sm text-gray-500">
              Enter one keyword or search phrase per line.
            </p>
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium">
              Results per keyword
            </label>

            <input
              type="number"
              min={1}
              max={100}
              value={limit}
              onChange={(e) => setLimit(Number(e.target.value))}
              className="w-full rounded-lg border px-4 py-3"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="mt-6 rounded-lg px-6 py-3 font-semibold text-white disabled:opacity-50"
        >
          {loading ? "Discovering..." : "Run Batch Discovery"}
        </button>
      </form>

      {error && (
        <div className="mt-6 rounded-lg border border-red-200 bg-red-50 p-4 text-red-700">
          {error}
        </div>
      )}

      {results && (
        <section className="mt-8">
          <div className="mb-6 rounded-xl border bg-white p-5 shadow-sm">
            <p className="text-sm text-gray-500">Keywords processed</p>

            <p className="mt-1 text-3xl font-bold">
              {results.total_keywords}
            </p>
          </div>

          <div className="space-y-6">
            {results.results.map((result, index) => (
              <article
                key={`${result.keyword}-${index}`}
                className="rounded-xl border bg-white p-6 shadow-sm"
              >
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <h2 className="text-xl font-semibold">
                    {result.keyword}
                  </h2>

                  <div className="flex gap-3 text-sm">
                    <span>
                      Discovered: {result.discovered ?? 0}
                    </span>

                    <span>
                      Duplicates: {result.duplicates ?? 0}
                    </span>

                    <span>
                      Skipped: {result.skipped ?? 0}
                    </span>
                  </div>
                </div>

                {!result.apps || result.apps.length === 0 ? (
                  <p className="mt-5 text-sm text-gray-500">
                    No apps returned for this keyword.
                  </p>
                ) : (
                  <div className="mt-5 grid gap-4 md:grid-cols-2">
                    {result.apps.map((app, appIndex) => (
                      <div
                        key={`${app.app_id ?? app.title ?? "app"}-${appIndex}`}
                        className="rounded-lg border p-4"
                      >
                        <h3 className="font-semibold">
                          {app.title || "Untitled app"}
                        </h3>

                        <div className="mt-2 flex flex-wrap gap-3 text-sm text-gray-600">
                          <span>
                            ⭐ {app.score ?? "N/A"}
                          </span>

                          <span>
                            {app.installs ?? "Unknown installs"}
                          </span>

                          <span>
                            Reviews scraped:{" "}
                            {app.reviews_scraped ?? 0}
                          </span>
                        </div>

                        {app.app_id && (
                          <a
                            href={`https://play.google.com/store/apps/details?id=${app.app_id}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="mt-3 inline-block text-sm font-medium underline"
                          >
                            View on Google Play →
                          </a>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </article>
            ))}
          </div>
        </section>
      )}
    </main>
  );
}


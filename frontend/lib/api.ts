const API_URL = 'http://127.0.0.1:8000';

if (!API_URL) {
  throw new Error("NEXT_PUBLIC_API_URL is not configured");
}

export async function discoverIntelligent(payload: {
  keyword: string;
  limit: number;
  category?: string | null;
  min_rating?: number | null;
  max_rating?: number | null;
  min_ratings?: number | null;
  max_ratings?: number | null;
  min_reviews?: number | null;
  max_reviews?: number | null;
  min_installs?: number | null;
  max_installs?: number | null;
  install_bucket?: string | null;
  free?: boolean | null;
  contains_ads?: boolean | null;
  offers_iap?: boolean | null;
  developer?: string | null;
  recently_updated_days?: number | null;
  old_not_updated_days?: number | null;
}) {
  const response = await fetch(`${API_URL}/discover/intelligent`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) throw new Error(`API request failed: ${response.status}`);
  return response.json();
}

export async function discoverBatch(payload: { keywords: string[]; limit: number }) {
  const response = await fetch(`${API_URL}/discover/batch`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error(`API request failed: ${response.status}`);
  return response.json();
}

export async function discoverHiddenGems(min_installs: number = 10000, max_installs: number = 1000000) {
  const response = await fetch(`${API_URL}/discover/hidden-gems?min_installs=${min_installs}&max_installs=${max_installs}`);
  if (!response.ok) throw new Error(`API request failed: ${response.status}`);
  return response.json();
}

export async function getMarketPainPoints() {
  const response = await fetch(`${API_URL}/market/pain-points`);
  if (!response.ok) throw new Error(`API request failed: ${response.status}`);
  return response.json();
}

export async function exploreCategory(params: Record<string, any>) {
  const query = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== null && value !== '') {
      query.append(key, String(value));
    }
  }
  const response = await fetch(`${API_URL}/category/apps?${query.toString()}`);
  if (!response.ok) throw new Error(`API request failed: ${response.status}`);
  return response.json();
}

export async function analyzeApp(appId: string) {
  const response = await fetch(`${API_URL}/analysis/${appId}`);
  if (!response.ok) throw new Error(`API request failed: ${response.status}`);
  return response.json();
}

export async function getAppReviews(
  appId: string,
  limit: number = 50,
  offset: number = 0,
  rating?: number | null,
  search?: string
) {
  const query = new URLSearchParams({
    limit: String(limit),
    offset: String(offset)
  });
  if (rating) query.append("rating", String(rating));
  if (search) query.append("search", search);

  const response = await fetch(`${API_URL}/analysis/${appId}/reviews?${query.toString()}`);
  if (!response.ok) throw new Error(`API request failed: ${response.status}`);
  return response.json();
}

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
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json();
}
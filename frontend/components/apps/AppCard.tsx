
import Link from "next/link";

type AppCardProps = {
  app: {
    appId?: string | null;
    app_id?: string | null;
    icon?: string | null;
    title?: string | null;
    score?: number | null;
    genre?: string | null;
    category?: string | null;
    free?: boolean | null;
    description?: string | null;
    developer?: string | null;
    installs?: string | null;
    relevance_score?: number | null;
  };
};

export default function AppCard({ app }: AppCardProps) {
  const targetId = app.appId || app.app_id;

  return (
    <article className="rounded-xl border border-gray-200 bg-white p-6 shadow-md transition-shadow hover:shadow-lg">
      <div className="flex gap-4">
        {app.icon ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={app.icon}
            alt={app.title ?? "App icon"}
            className="h-16 w-16 rounded-xl object-cover"
          />
        ) : (
          <div className="h-16 w-16 rounded-xl border border-gray-300 bg-gray-100" />
        )}

        <div className="min-w-0 flex-1">
          <h3 className="text-xl font-semibold text-gray-900">
            {app.title || "Untitled app"}
          </h3>

          <p className="text-sm text-gray-600">
            {app.developer || "Unknown developer"}
          </p>

          <div className="mt-2 flex flex-wrap gap-3 text-sm text-gray-700">
            <span>⭐ {app.score ?? "N/A"}</span>
            <span>{app.genre || app.category || "Unknown category"}</span>
            <span>{app.installs || "Unknown installs"}</span>
          </div>
        </div>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-2 text-sm sm:grid-cols-4">
        <div className="rounded-lg border border-gray-200 bg-gray-50 p-2">
          <p className="text-xs text-gray-600">Rating</p>
          <p className="font-semibold text-gray-900">
            ⭐ {app.score ?? "N/A"}
          </p>
        </div>

        <div className="rounded-lg border border-gray-200 bg-gray-50 p-2">
          <p className="text-xs text-gray-600">Installs</p>
          <p className="font-semibold text-gray-900">
            {app.installs ?? "N/A"}
          </p>
        </div>

        <div className="rounded-lg border border-gray-200 bg-gray-50 p-2">
          <p className="text-xs text-gray-600">Type</p>
          <p className="font-semibold text-gray-900">
            {app.free ? "Free" : "Paid"}
          </p>
        </div>

        <div className="rounded-lg border border-gray-200 bg-gray-50 p-2">
          <p className="text-xs text-gray-600">Relevance</p>
          <p className="font-semibold text-gray-900">
            {app.relevance_score ?? "N/A"}
          </p>
        </div>
      </div>

      <p className="mt-4 line-clamp-3 text-sm text-gray-700">
        {app.description || "No description available."}
      </p>

      {targetId && (
        <Link
          href={`/app-details/${targetId}`}
          className="mt-4 inline-block font-medium text-indigo-600 underline transition-colors hover:text-indigo-800"
        >
          View Reviews & Analysis →
        </Link>
      )}
    </article>
  );
}


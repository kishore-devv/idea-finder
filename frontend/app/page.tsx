import Link from "next/link";
import { Search, Sparkles, Activity, LayoutDashboard, Brain } from "lucide-react";

export default function Home() {
  return (
    <div className="p-8 max-w-6xl mx-auto w-full">
      <header className="mb-10">
        <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight flex items-center gap-3">
          <Brain className="w-10 h-10 text-indigo-600" />
          Dashboard
        </h1>
        <p className="text-lg text-gray-500 mt-2">
          Discover app opportunities, analyze markets, and find hidden gems.
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Link href="/discover/intelligent" className="group">
          <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-xl transition-all duration-300 transform group-hover:-translate-y-1">
            <div className="bg-indigo-100 w-12 h-12 rounded-xl flex items-center justify-center mb-4 text-indigo-600 transition-colors group-hover:bg-indigo-600 group-hover:text-white">
              <Search className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Intelligent Search</h3>
            <p className="text-sm text-gray-500 line-clamp-2">
              Find apps using complex criteria and AI-driven parameters to surface the best options.
            </p>
          </div>
        </Link>

        <Link href="/categories" className="group">
          <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-xl transition-all duration-300 transform group-hover:-translate-y-1">
            <div className="bg-emerald-100 w-12 h-12 rounded-xl flex items-center justify-center mb-4 text-emerald-600 transition-colors group-hover:bg-emerald-600 group-hover:text-white">
              <LayoutDashboard className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Categories</h3>
            <p className="text-sm text-gray-500 line-clamp-2">
              Explore app categories deeply and discover what apps are leading in each segment.
            </p>
          </div>
        </Link>

        <Link href="/market-analysis" className="group">
          <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-xl transition-all duration-300 transform group-hover:-translate-y-1">
            <div className="bg-amber-100 w-12 h-12 rounded-xl flex items-center justify-center mb-4 text-amber-600 transition-colors group-hover:bg-amber-600 group-hover:text-white">
              <Activity className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Market Pain Points</h3>
            <p className="text-sm text-gray-500 line-clamp-2">
              Identify key problems users are facing by analyzing poor reviews and missing features.
            </p>
          </div>
        </Link>

        <Link href="/hidden-gems" className="group">
          <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-xl transition-all duration-300 transform group-hover:-translate-y-1">
            <div className="bg-pink-100 w-12 h-12 rounded-xl flex items-center justify-center mb-4 text-pink-600 transition-colors group-hover:bg-pink-600 group-hover:text-white">
              <Sparkles className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Hidden Gems</h3>
            <p className="text-sm text-gray-500 line-clamp-2">
              Unearth unappreciated high-quality apps with lower install bases but great potential.
            </p>
          </div>
        </Link>
      </div>
    </div>
  );
}

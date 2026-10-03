import Link from "next/link";
import { Search, List, Activity, Sparkles, LayoutDashboard } from "lucide-react";

const links = [
    { name: "Dashboard", href: "/", icon: LayoutDashboard },
    { name: "Intelligent Search", href: "/discover/intelligent", icon: Search },
    { name: "Batch Search", href: "/discover/batch", icon: List },
    { name: "Categories", href: "/categories", icon: LayoutDashboard },
    { name: "Market Pain Points", href: "/market-analysis", icon: Activity },
    { name: "Hidden Gems", href: "/hidden-gems", icon: Sparkles },
];

export default function Sidebar() {
    return (
        <aside className="w-64 bg-gray-900 text-white min-h-screen p-5 flex flex-col hidden md:flex">
            <div className="flex items-center gap-3 mb-10 text-xl font-bold tracking-tight text-white">
                <Sparkles className="text-yellow-400 w-6 h-6" />
                Idea Finder
            </div>
            <nav className="flex-1 space-y-2">
                {links.map((link) => {
                    const Icon = link.icon;
                    return (
                        <Link
                            key={link.name}
                            href={link.href}
                            className="flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 hover:bg-gray-800 hover:text-white text-gray-300 font-medium"
                        >
                            <Icon className="w-5 h-5 opacity-70" />
                            {link.name}
                        </Link>
                    );
                })}
            </nav>
            <div className="p-4 mt-auto rounded-xl bg-gray-800 text-sm text-gray-400">
                Idea Finder Pro <br />
                <span className="text-xs text-gray-500">v1.0.0</span>
            </div>
        </aside>
    );
}

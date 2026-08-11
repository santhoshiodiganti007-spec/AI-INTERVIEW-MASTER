import React from "react";
import { useAuth } from "../context/AuthContext";
import { LogOut, Flame, Zap, ShieldAlert } from "lucide-react";

export default function Navbar({ dashboardData }) {
  const { user, logout } = useAuth();

  return (
    <header className="h-16 border-b border-gray-800 bg-gray-900/60 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-20">
      {/* Search / Context Status */}
      <div className="flex items-center gap-3">
        <span className="text-xs px-2.5 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-medium">
          MNC Interview Readiness Platform
        </span>
      </div>

      {/* Stats & User Info */}
      <div className="flex items-center gap-5">
        {dashboardData && (
          <>
            {/* Streak */}
            <div className="flex items-center gap-1.5 bg-orange-500/10 border border-orange-500/20 px-3 py-1 rounded-full text-xs font-bold text-orange-400">
              <Flame className="w-4 h-4 text-orange-500 fill-orange-500" />
              <span>{dashboardData.streak || 1} Day Streak</span>
            </div>

            {/* XP & Level */}
            <div className="flex items-center gap-1.5 bg-purple-500/10 border border-purple-500/20 px-3 py-1 rounded-full text-xs font-bold text-purple-300">
              <Zap className="w-4 h-4 text-purple-400" />
              <span>Lvl {dashboardData.level || 1} ({dashboardData.xp || 0} XP)</span>
            </div>
          </>
        )}

        {/* User Dropdown / Logout */}
        <div className="flex items-center gap-3 pl-3 border-l border-gray-800">
          <div className="text-right">
            <p className="text-xs font-semibold text-white">{user?.full_name || "Candidate"}</p>
            <p className="text-[10px] text-gray-400">{user?.email || "user@example.com"}</p>
          </div>
          <button
            onClick={logout}
            title="Logout"
            className="p-2 text-gray-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
}

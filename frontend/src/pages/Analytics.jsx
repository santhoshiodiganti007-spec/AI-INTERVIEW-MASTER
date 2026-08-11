import React, { useEffect, useState } from "react";
import { fetchApi } from "../utils/api";
import { BarChart3, AlertTriangle, TrendingUp, ShieldCheck } from "lucide-react";

export default function Analytics() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadAnalytics() {
      try {
        const res = await fetchApi("/dashboard");
        setData(res);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadAnalytics();
  }, []);

  if (loading) return <div className="p-8 text-center text-gray-400">Loading diagnostic analytics...</div>;

  const scores = data?.category_scores || {};
  const weakAreas = Object.entries(scores).filter(([_, s]) => s < 65);

  return (
    <div className="space-y-6">
      <div className="glass-card p-6 rounded-2xl border border-gray-800">
        <div className="flex items-center gap-2 text-xs font-semibold text-blue-400 mb-1">
          <BarChart3 className="w-4 h-4" />
          <span>Performance Analytics & Weakness Engine</span>
        </div>
        <h1 className="text-2xl font-bold text-white">Candidate Weakness Detection & Progress</h1>
        <p className="text-sm text-gray-400 mt-1">Automatic identification of critical preparation gaps with recommended focus areas.</p>
      </div>

      {/* Weak Areas Alert Box */}
      <div className="glass-card p-6 rounded-2xl border border-amber-500/30 bg-amber-500/5 space-y-3">
        <h2 className="text-base font-bold text-amber-400 flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-amber-400" />
          <span>Detected Weak Skill Areas ({weakAreas.length})</span>
        </h2>
        {weakAreas.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {weakAreas.map(([cat, score]) => (
              <div key={cat} className="p-3 rounded-xl bg-gray-900 border border-gray-800 flex items-center justify-between">
                <span className="text-xs font-semibold text-gray-200">{cat}</span>
                <span className="text-xs font-bold text-amber-400">{score}% Score</span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-gray-300">Great progress! No critical weakness below 65% detected.</p>
        )}
      </div>

      {/* Detailed Skill Scores Grid */}
      <div className="glass-card p-6 rounded-2xl border border-gray-800 space-y-4">
        <h2 className="text-base font-bold text-white">Full Skill Dimension Breakdown</h2>
        <div className="space-y-4">
          {Object.entries(scores).map(([cat, score]) => (
            <div key={cat} className="space-y-1">
              <div className="flex justify-between text-xs font-semibold">
                <span className="text-gray-300">{cat}</span>
                <span className="text-blue-400">{score}%</span>
              </div>
              <div className="w-full bg-gray-800 rounded-full h-2.5 overflow-hidden">
                <div
                  className="gradient-bg h-full rounded-full"
                  style={{ width: `${Math.min(score, 100)}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

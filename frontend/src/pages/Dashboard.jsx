import React, { useEffect, useState } from "react";
import { fetchApi } from "../utils/api";
import { 
  Trophy, 
  TrendingUp, 
  CheckCircle2, 
  AlertCircle, 
  Sparkles, 
  Target, 
  BookOpen, 
  Code, 
  Brain, 
  ShieldAlert,
  ArrowUpRight
} from "lucide-react";

export default function Dashboard({ setCurrentPage, onDataLoaded }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const res = await fetchApi("/dashboard");
        setData(res);
        if (onDataLoaded) onDataLoaded(res);
      } catch (err) {
        console.error("Error loading dashboard:", err);
      } finally {
        setLoading(false);
      }
    }
    loadDashboard();
  }, []);

  if (loading) {
    return <div className="p-8 text-center text-gray-400">Loading candidate readiness engine...</div>;
  }

  const scores = data?.category_scores || {};

  return (
    <div className="space-y-8">
      {/* Header Banner */}
      <div className="glass-card p-6 rounded-2xl border border-gray-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-blue-400 mb-1">
            <Sparkles className="w-4 h-4" />
            <span>Target MNC: Google / Meta</span>
          </div>
          <h1 className="text-2xl font-bold text-white">Interview Readiness Control Center</h1>
          <p className="text-sm text-gray-400 mt-0.5">Track your diagnostic metrics and daily preparation checklist</p>
        </div>

        <button
          onClick={() => setCurrentPage("mock-interview")}
          className="gradient-bg px-5 py-2.5 rounded-xl text-white font-semibold text-sm shadow-lg shadow-blue-500/20 hover:opacity-95 transition-all flex items-center gap-2"
        >
          <span>Launch AI Mock Interview</span>
          <ArrowUpRight className="w-4 h-4" />
        </button>
      </div>

      {/* Readiness Gauge & Core Score */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-card p-6 rounded-2xl border border-gray-800 flex flex-col items-center justify-center text-center relative overflow-hidden">
          <div className="w-32 h-32 rounded-full border-4 border-blue-500/30 flex items-center justify-center relative mb-3 bg-blue-500/5">
            <div className="text-center">
              <span className="text-3xl font-extrabold text-white">{data?.readiness_score}%</span>
              <span className="block text-[10px] text-gray-400 font-semibold uppercase">Readiness</span>
            </div>
          </div>
          <span className="px-3 py-1 rounded-full bg-blue-500/20 text-blue-400 text-xs font-bold border border-blue-500/30">
            {data?.readiness_label}
          </span>
          <p className="text-[11px] text-gray-500 mt-3 max-w-xs leading-relaxed">
            * {data?.disclaimer}
          </p>
        </div>

        {/* Today's Preparation Checklist */}
        <div className="md:col-span-2 glass-card p-6 rounded-2xl border border-gray-800">
          <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <Target className="w-5 h-5 text-blue-400" />
            <span>Today's Preparation Checklist</span>
          </h2>
          <div className="space-y-3">
            {data?.todays_preparation?.map((item, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between p-3 rounded-xl bg-gray-900/60 border border-gray-800/80 hover:border-gray-700 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div className={`w-5 h-5 rounded-md flex items-center justify-center ${item.done ? "bg-emerald-500/20 text-emerald-400" : "bg-gray-800 text-gray-500"}`}>
                    <CheckCircle2 className="w-3.5 h-3.5" />
                  </div>
                  <span className={`text-sm ${item.done ? "line-through text-gray-500" : "text-gray-200"}`}>
                    {item.task}
                  </span>
                </div>
                <span className="text-xs px-2 py-0.5 rounded bg-gray-800 text-gray-400">High Yield</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 10 Skill Dimension Breakdown Cards */}
      <div>
        <h2 className="text-lg font-bold text-white mb-4">Diagnostic Sub-Scores</h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
          {Object.entries(scores).map(([cat, score]) => (
            <div key={cat} className="glass-card glass-card-hover p-4 rounded-xl border border-gray-800/80">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-semibold text-gray-400">{cat}</span>
                <span className="text-xs font-bold text-blue-400">{score}%</span>
              </div>
              <div className="w-full bg-gray-800 rounded-full h-2 overflow-hidden">
                <div
                  className="gradient-bg h-full rounded-full"
                  style={{ width: `${Math.min(score, 100)}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Access Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div 
          onClick={() => setCurrentPage("questions")}
          className="glass-card glass-card-hover p-5 rounded-2xl border border-gray-800 cursor-pointer group"
        >
          <div className="w-10 h-10 rounded-xl bg-blue-500/10 text-blue-400 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
            <BookOpen className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-white text-base">Question Engine</h3>
          <p className="text-xs text-gray-400 mt-1">Practice Python, OOP 14 pillars, and conceptual questions.</p>
        </div>

        <div 
          onClick={() => setCurrentPage("dsa")}
          className="glass-card glass-card-hover p-5 rounded-2xl border border-gray-800 cursor-pointer group"
        >
          <div className="w-10 h-10 rounded-xl bg-purple-500/10 text-purple-400 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
            <Code className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-white text-base">DSA Pattern Lab</h3>
          <p className="text-xs text-gray-400 mt-1">Master problem-solving patterns, complexities & Python code.</p>
        </div>

        <div 
          onClick={() => setCurrentPage("genai")}
          className="glass-card glass-card-hover p-5 rounded-2xl border border-gray-800 cursor-pointer group"
        >
          <div className="w-10 h-10 rounded-xl bg-pink-500/10 text-pink-400 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
            <Brain className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-white text-base">GenAI & RAG Architecture</h3>
          <p className="text-xs text-gray-400 mt-1">Transformers, QLoRA, self-attention & production system design.</p>
        </div>
      </div>
    </div>
  );
}

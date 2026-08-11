import React, { useEffect, useState } from "react";
import { fetchApi } from "../utils/api";
import { Compass, CheckCircle2, Clock, Calendar, RefreshCw } from "lucide-react";

export default function RoadmapView() {
  const [roadmap, setRoadmap] = useState(null);
  const [days, setDays] = useState(30);
  const [hours, setHours] = useState(2.0);
  const [generating, setGenerating] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadRoadmap() {
      try {
        const res = await fetchApi("/roadmap");
        setRoadmap(res);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadRoadmap();
  }, []);

  const handleGenerate = async () => {
    setGenerating(true);
    try {
      const res = await fetchApi("/roadmap/generate", {
        method: "POST",
        body: JSON.stringify({ duration_days: parseInt(days), available_hours: parseFloat(hours) }),
      });
      setRoadmap(res);
    } catch (err) {
      console.error(err);
    } finally {
      setGenerating(false);
    }
  };

  const handleToggleTask = async (taskId) => {
    try {
      const res = await fetchApi(`/roadmap/task/${taskId}/toggle`, { method: "POST" });
      setRoadmap((prev) => ({
        ...prev,
        tasks: prev.tasks.map((t) => (t.id === taskId ? { ...t, completed: res.completed } : t)),
      }));
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <div className="p-8 text-center text-gray-400">Loading personalized preparation plan...</div>;

  return (
    <div className="space-y-6">
      {/* Header & Controls */}
      <div className="glass-card p-6 rounded-2xl border border-gray-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-blue-400 mb-1">
            <Compass className="w-4 h-4" />
            <span>Adaptive Study Plan</span>
          </div>
          <h1 className="text-2xl font-bold text-white">{roadmap?.title || "Personalized Preparation Roadmap"}</h1>
          <p className="text-sm text-gray-400 mt-1">Structured day-by-day objectives based on your target role and available study hours.</p>
        </div>

        {/* Generator Controls */}
        <div className="flex items-center gap-3">
          <select
            value={days}
            onChange={(e) => setDays(e.target.value)}
            className="bg-gray-900 border border-gray-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none"
          >
            <option value={7}>7 Days Sprint</option>
            <option value={14}>14 Days Acceleration</option>
            <option value={30}>30 Days Mastery</option>
            <option value={60}>60 Days Deep Prep</option>
            <option value={90}>90 Days Full Track</option>
          </select>

          <button
            onClick={handleGenerate}
            disabled={generating}
            className="gradient-bg px-4 py-2 rounded-xl text-white font-semibold text-xs shadow-lg shadow-blue-500/20 flex items-center gap-2"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${generating ? "animate-spin" : ""}`} />
            <span>Regenerate Roadmap</span>
          </button>
        </div>
      </div>

      {/* Task List */}
      <div className="space-y-3">
        {roadmap?.tasks?.map((task) => (
          <div
            key={task.id}
            className={`glass-card p-4 rounded-xl border transition-all flex items-start justify-between gap-4 ${
              task.completed ? "border-emerald-500/30 bg-emerald-500/5" : "border-gray-800"
            }`}
          >
            <div className="flex items-start gap-3">
              <button
                onClick={() => handleToggleTask(task.id)}
                className={`mt-0.5 w-5 h-5 rounded-md flex items-center justify-center transition-colors ${
                  task.completed ? "bg-emerald-500 text-white" : "bg-gray-800 text-gray-500 hover:border-gray-600"
                }`}
              >
                <CheckCircle2 className="w-3.5 h-3.5" />
              </button>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-blue-400">Day {task.day_number}</span>
                  <span className="text-xs text-gray-500">•</span>
                  <span className="text-xs font-semibold text-gray-300 flex items-center gap-1">
                    <Clock className="w-3 h-3 text-gray-400" />
                    {task.estimated_minutes} mins
                  </span>
                </div>
                <h3 className={`text-sm font-bold mt-1 ${task.completed ? "line-through text-gray-400" : "text-white"}`}>
                  {task.topic}
                </h3>
                <p className="text-xs text-gray-400 mt-1">{task.learning_objective}</p>

                {task.questions && task.questions.length > 0 && (
                  <div className="mt-2 text-xs text-gray-300">
                    <span className="font-semibold text-purple-400">Questions: </span>
                    {task.questions.join(", ")}
                  </div>
                )}
              </div>
            </div>

            <span className={`text-[10px] uppercase font-bold px-2 py-1 rounded ${task.completed ? "bg-emerald-500/20 text-emerald-400" : "bg-gray-800 text-gray-400"}`}>
              {task.completed ? "Done" : "Pending"}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

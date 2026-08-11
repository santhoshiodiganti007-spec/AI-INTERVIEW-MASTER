import React, { useEffect, useState } from "react";
import { fetchApi } from "../utils/api";
import { Code2, Play, Lightbulb, CheckCircle, AlertTriangle, Cpu } from "lucide-react";

export default function DSALab() {
  const [problems, setProblems] = useState([]);
  const [selectedProb, setSelectedProb] = useState(null);
  const [userCode, setUserCode] = useState("");
  const [showHint, setShowHint] = useState(false);
  const [showSolution, setShowSolution] = useState(false);
  const [result, setResult] = useState(null);
  const [executing, setExecuting] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadProblems() {
      try {
        const res = await fetchApi("/coding-problems");
        setProblems(res);
        if (res.length > 0) {
          setSelectedProb(res[0]);
          setUserCode(res[0].python_solution || "");
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadProblems();
  }, []);

  const [errorMsg, setErrorMsg] = useState(null);

  const handleSelect = (prob) => {
    setSelectedProb(prob);
    setUserCode(prob.python_solution || "");
    setShowHint(false);
    setShowSolution(false);
    setResult(null);
    setErrorMsg(null);
  };

  const handleRun = async () => {
    if (!selectedProb) return;
    setExecuting(true);
    setErrorMsg(null);
    try {
      const res = await fetchApi(`/coding-problems/${selectedProb.id}/attempt`, {
        method: "POST",
        body: JSON.stringify({ user_code: userCode }),
      });
      setResult(res);
    } catch (err) {
      console.error("Code execution error:", err);
      setErrorMsg(err.message || "Failed to execute Python solution. Please check server connection.");
    } finally {
      setExecuting(false);
    }
  };

  if (loading) return <div className="p-8 text-center text-gray-400">Loading DSA coding challenges...</div>;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-7rem)]">
      {/* Problems Sidebar */}
      <div className="glass-card rounded-2xl border border-gray-800 p-4 flex flex-col h-full overflow-hidden">
        <h2 className="text-base font-bold text-white mb-3 flex items-center gap-2">
          <Code2 className="w-4 h-4 text-purple-400" />
          <span>DSA Pattern Problems</span>
        </h2>
        <div className="flex-1 space-y-2 overflow-y-auto custom-scrollbar pr-1">
          {problems.map((p) => (
            <div
              key={p.id}
              onClick={() => handleSelect(p)}
              className={`p-3 rounded-xl cursor-pointer border transition-all ${
                selectedProb?.id === p.id
                  ? "bg-purple-600/20 border-purple-500/40 text-white"
                  : "bg-gray-900/40 border-gray-800/80 text-gray-400 hover:border-gray-700 hover:text-gray-200"
              }`}
            >
              <div className="flex items-center justify-between text-[11px] font-semibold mb-1">
                <span className="text-purple-400">{p.topic}</span>
                <span className="px-1.5 py-0.5 rounded bg-gray-800 text-gray-300 text-[10px]">
                  {p.difficulty}
                </span>
              </div>
              <p className="text-xs font-bold">{p.title}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Workspace */}
      <div className="lg:col-span-2 glass-card rounded-2xl border border-gray-800 p-6 flex flex-col h-full overflow-y-auto custom-scrollbar space-y-6">
        {selectedProb ? (
          <>
            <div>
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-purple-400">{selectedProb.topic}</span>
                <div className="flex items-center gap-2 text-xs font-bold text-gray-400">
                  <span>Time: {selectedProb.time_complexity}</span>
                  <span>•</span>
                  <span>Space: {selectedProb.space_complexity}</span>
                </div>
              </div>
              <h1 className="text-xl font-bold text-white mt-1">{selectedProb.title}</h1>
              <p className="text-sm text-gray-300 mt-2 leading-relaxed">{selectedProb.problem_statement}</p>
            </div>

            {/* Hint & Solution Toggles */}
            <div className="flex items-center gap-3">
              <button
                onClick={() => setShowHint(!showHint)}
                className="px-3 py-1.5 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs font-semibold flex items-center gap-1.5"
              >
                <Lightbulb className="w-3.5 h-3.5" />
                <span>{showHint ? "Hide Hint" : "Show Pattern Hint"}</span>
              </button>
              <button
                onClick={() => setShowSolution(!showSolution)}
                className="px-3 py-1.5 rounded-lg bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-semibold flex items-center gap-1.5"
              >
                <Cpu className="w-3.5 h-3.5" />
                <span>{showSolution ? "Hide Solution" : "View Optimized Approach"}</span>
              </button>
            </div>

            {showHint && (
              <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 text-xs text-amber-300">
                <b>Hint:</b> {selectedProb.hint}
              </div>
            )}

            {showSolution && (
              <div className="p-4 rounded-xl bg-gray-900 border border-gray-800 space-y-2">
                <p className="text-xs text-gray-300"><b>Optimized Strategy:</b> {selectedProb.optimized_approach}</p>
                <pre className="text-xs font-mono text-emerald-400 bg-black/50 p-3 rounded-lg overflow-x-auto">
                  {selectedProb.python_solution}
                </pre>
              </div>
            )}

            {/* Python Code Workspace */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs font-semibold text-gray-300">
                <span>Python Solution Workspace</span>
                <span>Python 3.12</span>
              </div>
              <textarea
                rows={10}
                value={userCode}
                onChange={(e) => setUserCode(e.target.value)}
                className="w-full font-mono text-xs bg-gray-950 border border-gray-800 rounded-xl p-4 text-emerald-400 focus:outline-none focus:border-purple-500"
              />
              <button
                onClick={handleRun}
                disabled={executing}
                className="gradient-bg px-5 py-2.5 rounded-xl text-white font-semibold text-sm shadow-lg shadow-purple-500/20 flex items-center gap-2"
              >
                <Play className="w-4 h-4 fill-white" />
                <span>{executing ? "Executing Test Cases..." : "Run & Submit Python Code"}</span>
              </button>
            </div>

            {/* Error Message */}
            {errorMsg && (
              <div className="p-4 rounded-xl border bg-red-500/10 border-red-500/30 text-red-400 text-xs space-y-1">
                <div className="font-bold flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4" />
                  <span>Execution Request Error</span>
                </div>
                <p>{errorMsg}</p>
              </div>
            )}

            {/* Test Results */}
            {result && (
              <div className={`p-4 rounded-xl border ${result.passed ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-400" : "bg-red-500/10 border-red-500/30 text-red-400"} text-xs space-y-1`}>
                <div className="font-bold flex items-center gap-2">
                  {result.passed ? <CheckCircle className="w-4 h-4" /> : <AlertTriangle className="w-4 h-4" />}
                  <span>{result.passed ? "All Test Cases Passed!" : "Submission Failed"}</span>
                </div>
                <p>{result.feedback}</p>
              </div>
            )}
          </>
        ) : (
          <div className="text-center text-gray-400 my-auto">Select a coding problem.</div>
        )}
      </div>
    </div>
  );
}

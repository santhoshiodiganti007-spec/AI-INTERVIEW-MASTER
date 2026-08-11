import React, { useEffect, useState } from "react";
import { fetchApi } from "../utils/api";
import { BookOpen, CheckCircle2, ChevronRight, Sparkles, Send } from "lucide-react";

export default function QuestionBank() {
  const [questions, setQuestions] = useState([]);
  const [selectedQ, setSelectedQ] = useState(null);
  const [userAnswer, setUserAnswer] = useState("");
  const [evaluation, setEvaluation] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadQuestions() {
      try {
        const res = await fetchApi("/questions");
        setQuestions(res);
        if (res.length > 0) setSelectedQ(res[0]);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadQuestions();
  }, []);

  const handleSelect = (q) => {
    setSelectedQ(q);
    setUserAnswer("");
    setEvaluation(null);
  };

  const handleSubmit = async () => {
    if (!selectedQ || !userAnswer.trim()) return;
    setSubmitting(true);
    try {
      const res = await fetchApi(`/questions/${selectedQ.id}/attempt`, {
        method: "POST",
        body: JSON.stringify({ user_answer: userAnswer }),
      });
      setEvaluation(res.evaluation);
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div className="p-8 text-center text-gray-400">Loading structured question database...</div>;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-7rem)]">
      {/* Sidebar List */}
      <div className="glass-card rounded-2xl border border-gray-800 p-4 flex flex-col h-full overflow-hidden">
        <h2 className="text-base font-bold text-white mb-3 flex items-center gap-2">
          <BookOpen className="w-4 h-4 text-blue-400" />
          <span>Question Directory ({questions.length})</span>
        </h2>
        <div className="flex-1 space-y-2 overflow-y-auto custom-scrollbar pr-1">
          {questions.map((q) => (
            <div
              key={q.id}
              onClick={() => handleSelect(q)}
              className={`p-3 rounded-xl cursor-pointer border transition-all ${
                selectedQ?.id === q.id
                  ? "bg-blue-600/20 border-blue-500/40 text-white"
                  : "bg-gray-900/40 border-gray-800/80 text-gray-400 hover:border-gray-700 hover:text-gray-200"
              }`}
            >
              <div className="flex items-center justify-between text-[11px] font-semibold mb-1">
                <span className="text-blue-400">{q.category}</span>
                <span className="px-1.5 py-0.5 rounded bg-gray-800 text-gray-300 text-[10px] uppercase">
                  {q.difficulty}
                </span>
              </div>
              <p className="text-xs font-medium line-clamp-2">{q.question}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Question Details & Answer Workspace */}
      <div className="lg:col-span-2 glass-card rounded-2xl border border-gray-800 p-6 flex flex-col h-full overflow-y-auto custom-scrollbar">
        {selectedQ ? (
          <div className="space-y-6">
            <div>
              <div className="flex items-center gap-2 text-xs font-semibold text-blue-400 mb-1">
                <span>{selectedQ.category}</span>
                <span>•</span>
                <span>{selectedQ.topic}</span>
              </div>
              <h1 className="text-xl font-bold text-white">{selectedQ.question}</h1>
            </div>

            {/* Answer Input */}
            <div className="space-y-2">
              <label className="block text-xs font-semibold text-gray-300">Your Technical Response</label>
              <textarea
                rows={5}
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                placeholder="Write your explanation here..."
                className="w-full bg-gray-900 border border-gray-700 rounded-xl p-4 text-sm text-white focus:outline-none focus:border-blue-500"
              />
              <button
                onClick={handleSubmit}
                disabled={submitting || !userAnswer.trim()}
                className="gradient-bg px-5 py-2.5 rounded-xl text-white font-semibold text-sm shadow-lg shadow-blue-500/20 flex items-center gap-2 disabled:opacity-50"
              >
                <span>{submitting ? "Evaluating..." : "Submit Answer for AI Evaluation"}</span>
                <Send className="w-4 h-4" />
              </button>
            </div>

            {/* AI Evaluation Output */}
            {evaluation && (
              <div className="glass-card p-5 rounded-xl border border-blue-500/30 space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-base font-bold text-white">AI Evaluation Score</h3>
                  <span className="text-xl font-extrabold text-blue-400">{evaluation.overall_score}/10</span>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
                  <div className="p-2 bg-gray-900 rounded-lg">
                    <span className="text-gray-400">Accuracy:</span> <span className="text-white font-bold">{evaluation.technical_accuracy}</span>
                  </div>
                  <div className="p-2 bg-gray-900 rounded-lg">
                    <span className="text-gray-400">Depth:</span> <span className="text-white font-bold">{evaluation.depth}</span>
                  </div>
                  <div className="p-2 bg-gray-900 rounded-lg">
                    <span className="text-gray-400">Clarity:</span> <span className="text-white font-bold">{evaluation.clarity}</span>
                  </div>
                  <div className="p-2 bg-gray-900 rounded-lg">
                    <span className="text-gray-400">Comm:</span> <span className="text-white font-bold">{evaluation.communication}</span>
                  </div>
                </div>
                <div>
                  <h4 className="text-xs font-bold text-emerald-400 uppercase mb-1">What Was Good</h4>
                  <ul className="list-disc list-inside text-xs text-gray-300 space-y-1">
                    {evaluation.what_was_good?.map((g, idx) => <li key={idx}>{g}</li>)}
                  </ul>
                </div>
                <div>
                  <h4 className="text-xs font-bold text-amber-400 uppercase mb-1">What Was Missing</h4>
                  <ul className="list-disc list-inside text-xs text-gray-300 space-y-1">
                    {evaluation.what_was_missing?.map((m, idx) => <li key={idx}>{m}</li>)}
                  </ul>
                </div>
              </div>
            )}

            {/* Expected Solution & Key Points */}
            <div className="p-5 rounded-xl bg-gray-900/60 border border-gray-800 space-y-3">
              <h3 className="text-sm font-bold text-white">Expected Solution Reference</h3>
              <p className="text-xs text-gray-300 leading-relaxed">{selectedQ.expected_answer}</p>
              <div>
                <h4 className="text-xs font-semibold text-blue-400 uppercase mb-1">Key Points</h4>
                <ul className="list-disc list-inside text-xs text-gray-400 space-y-1">
                  {selectedQ.key_points?.map((kp, idx) => <li key={idx}>{kp}</li>)}
                </ul>
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center text-gray-400 my-auto">Select a question from the directory.</div>
        )}
      </div>
    </div>
  );
}

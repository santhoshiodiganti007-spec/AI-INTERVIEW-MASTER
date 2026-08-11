import React, { useState } from "react";
import { fetchApi } from "../utils/api";
import { Sparkles, CheckCircle2, ArrowRight } from "lucide-react";

const ASSESSMENT_QUESTIONS = [
  {
    id: 1,
    category: "Python & Concurrency",
    question: "Explain Python's GIL (Global Interpreter Lock). Why does multithreading not scale CPU-bound tasks in CPython?",
    defaultAnswer: "CPython's GIL is a mutex preventing multiple native threads from executing Python bytecodes simultaneously to ensure memory thread-safety in reference counting. CPU-bound tasks require multiprocessing."
  },
  {
    id: 2,
    category: "OOP Pillars",
    question: "What is Method Overriding vs Method Overloading in Python? How is overloading pythonically achieved?",
    defaultAnswer: "Method Overriding is replacing a parent class implementation in a subclass. Python does not support classical compile-time method overloading natively; it uses default arguments, *args/**kwargs, or @singledispatch."
  },
  {
    id: 3,
    category: "Generative AI / RAG",
    question: "In Transformer self-attention, why are dot-products scaled by sqrt(d_k)? What is Hybrid Search in RAG?",
    defaultAnswer: "Scaling by sqrt(d_k) prevents large dot-product magnitudes from driving softmax into regions with extremely small gradients. Hybrid Search combines dense vector search and sparse BM25 keyword search via RRF."
  }
];

export default function InitialAssessment({ setCurrentPage }) {
  const [answers, setAnswers] = useState({
    1: ASSESSMENT_QUESTIONS[0].defaultAnswer,
    2: ASSESSMENT_QUESTIONS[1].defaultAnswer,
    3: ASSESSMENT_QUESTIONS[2].defaultAnswer,
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleTextChange = (id, val) => {
    setAnswers((prev) => ({ ...prev, [id]: val }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetchApi("/assessment/submit", {
        method: "POST",
        body: JSON.stringify({ answers }),
      });
      setResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="glass-card p-6 rounded-2xl border border-gray-800">
        <div className="flex items-center gap-2 text-xs font-semibold text-blue-400 mb-1">
          <Sparkles className="w-4 h-4" />
          <span>Diagnostic Baseline Engine</span>
        </div>
        <h1 className="text-2xl font-bold text-white">Initial Interview Assessment</h1>
        <p className="text-sm text-gray-400 mt-1">Answer these core technical prompts to generate your benchmark AI Readiness Score.</p>
      </div>

      {result ? (
        <div className="glass-card p-8 rounded-2xl border border-blue-500/30 text-center space-y-4">
          <div className="w-20 h-20 mx-auto rounded-full bg-blue-500/20 text-blue-400 border border-blue-500/40 flex items-center justify-center text-2xl font-extrabold">
            {result.readiness_score}%
          </div>
          <h2 className="text-xl font-bold text-white">Assessment Complete!</h2>
          <p className="text-sm text-blue-400 font-semibold">Diagnostic Rating: {result.readiness_label}</p>
          <p className="text-xs text-gray-400 max-w-md mx-auto">Your preparation metrics and daily study tasks have been dynamically updated.</p>
          <button
            onClick={() => setCurrentPage("dashboard")}
            className="gradient-bg px-6 py-2.5 rounded-xl text-white font-semibold text-sm shadow-lg shadow-blue-500/20"
          >
            Go to Control Dashboard
          </button>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-6">
          {ASSESSMENT_QUESTIONS.map((q, idx) => (
            <div key={q.id} className="glass-card p-6 rounded-2xl border border-gray-800 space-y-3">
              <div className="flex items-center justify-between text-xs font-semibold">
                <span className="text-blue-400">Prompt #{idx + 1} • {q.category}</span>
                <span className="text-gray-500">MNC Level</span>
              </div>
              <p className="text-sm font-semibold text-white">{q.question}</p>
              <textarea
                rows={4}
                value={answers[q.id] || ""}
                onChange={(e) => handleTextChange(q.id, e.target.value)}
                className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-blue-500"
              />
            </div>
          ))}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl gradient-bg text-white font-semibold text-sm shadow-lg shadow-blue-500/20 flex items-center justify-center gap-2"
          >
            <span>{loading ? "Evaluating..." : "Submit Diagnostic Assessment"}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>
      )}
    </div>
  );
}

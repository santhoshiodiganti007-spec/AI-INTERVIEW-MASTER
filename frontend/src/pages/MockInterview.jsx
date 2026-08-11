import React, { useState } from "react";
import { fetchApi } from "../utils/api";
import { Mic, Send, Sparkles, CheckCircle2, Award, Play, Bot } from "lucide-react";

export default function MockInterview() {
  const [interviewType, setInterviewType] = useState("Full MNC Interview");
  const [session, setSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [userAnswer, setUserAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [evalReport, setEvalReport] = useState(null);

  const startInterview = async () => {
    setLoading(true);
    setEvalReport(null);
    try {
      const res = await fetchApi("/mock-interview/start", {
        method: "POST",
        body: JSON.stringify({ interview_type: interviewType }),
      });
      setSession(res);
      setMessages([
        { sender: "ai", text: res.question_text, number: res.question_number }
      ]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSendAnswer = async () => {
    if (!session || !userAnswer.trim()) return;
    const currentText = userAnswer;
    setUserAnswer("");
    
    setMessages((prev) => [...prev, { sender: "user", text: currentText }]);
    setLoading(true);

    try {
      const res = await fetchApi(`/mock-interview/${session.mock_interview_id}/answer`, {
        method: "POST",
        body: JSON.stringify({ answer_text: currentText }),
      });

      if (res.previous_answer_evaluation) {
        setMessages((prev) => [
          ...prev,
          { sender: "eval", evaluation: res.previous_answer_evaluation }
        ]);
      }

      if (res.status === "COMPLETED") {
        setMessages((prev) => [
          ...prev,
          { sender: "ai", text: "Thank you! That completes our dynamic mock interview session. Generating your full evaluation report..." }
        ]);
        setEvalReport(res);
      } else {
        setMessages((prev) => [
          ...prev,
          { sender: "ai", text: res.question_text, number: res.question_number }
        ]);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="glass-card p-6 rounded-2xl border border-gray-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-purple-400 mb-1">
            <Bot className="w-4 h-4" />
            <span>Interactive Dynamic AI Interviewer</span>
          </div>
          <h1 className="text-2xl font-bold text-white">AI Mock Interview Room</h1>
          <p className="text-sm text-gray-400 mt-1">Multi-turn adaptive questions with real-time feedback & follow-ups.</p>
        </div>

        {!session && (
          <div className="flex items-center gap-3">
            <select
              value={interviewType}
              onChange={(e) => setInterviewType(e.target.value)}
              className="bg-gray-900 border border-gray-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none"
            >
              <option value="Python Interview">Python Interview</option>
              <option value="DSA Interview">DSA Interview</option>
              <option value="AIML Interview">AIML Interview</option>
              <option value="GenAI Interview">GenAI Interview</option>
              <option value="Full MNC Interview">Full MNC Interview</option>
            </select>
            <button
              onClick={startInterview}
              disabled={loading}
              className="gradient-bg px-5 py-2 rounded-xl text-white font-semibold text-xs shadow-lg shadow-purple-500/20 flex items-center gap-2"
            >
              <Play className="w-3.5 h-3.5 fill-white" />
              <span>Start Session</span>
            </button>
          </div>
        )}
      </div>

      {/* Chat Messages */}
      {session && (
        <div className="glass-card p-6 rounded-2xl border border-gray-800 flex flex-col h-[500px]">
          <div className="flex-1 overflow-y-auto custom-scrollbar space-y-4 pr-2">
            {messages.map((msg, idx) => {
              if (msg.sender === "ai") {
                return (
                  <div key={idx} className="flex gap-3">
                    <div className="w-8 h-8 rounded-full gradient-bg flex items-center justify-center text-white shrink-0">
                      <Bot className="w-4 h-4" />
                    </div>
                    <div className="bg-gray-900 border border-gray-800 p-4 rounded-2xl max-w-2xl text-xs text-gray-200 leading-relaxed">
                      <span className="text-[10px] font-bold text-purple-400 block mb-1 uppercase">
                        AI Technical Interviewer {msg.number ? `(Question #${msg.number})` : ""}
                      </span>
                      {msg.text}
                    </div>
                  </div>
                );
              } else if (msg.sender === "user") {
                return (
                  <div key={idx} className="flex justify-end gap-3">
                    <div className="bg-blue-600/20 border border-blue-500/30 p-4 rounded-2xl max-w-2xl text-xs text-white leading-relaxed">
                      <span className="text-[10px] font-bold text-blue-400 block mb-1 uppercase">Your Answer</span>
                      {msg.text}
                    </div>
                  </div>
                );
              } else if (msg.sender === "eval") {
                const ev = msg.evaluation;
                return (
                  <div key={idx} className="p-3 rounded-xl bg-purple-950/40 border border-purple-500/30 text-xs space-y-1">
                    <span className="font-bold text-purple-300">Turn Score: {ev.overall_score}/10</span>
                    <p className="text-gray-300"><b>Better Answer Tip:</b> {ev.better_answer}</p>
                  </div>
                );
              }
              return null;
            })}
          </div>

          {/* Input Box */}
          {!evalReport && (
            <div className="flex gap-3 pt-4 border-t border-gray-800 mt-4">
              <input
                type="text"
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSendAnswer()}
                placeholder="Type your verbal/technical response..."
                className="flex-1 bg-gray-900 border border-gray-700 rounded-xl px-4 py-2.5 text-xs text-white focus:outline-none focus:border-purple-500"
              />
              <button
                onClick={handleSendAnswer}
                disabled={loading || !userAnswer.trim()}
                className="gradient-bg px-5 py-2 rounded-xl text-white font-semibold text-xs shadow-lg shadow-purple-500/20 flex items-center gap-2"
              >
                <Send className="w-3.5 h-3.5" />
                <span>Submit</span>
              </button>
            </div>
          )}
        </div>
      )}

      {/* Final Evaluation Report Modal/Section */}
      {evalReport && (
        <div className="glass-card p-6 rounded-2xl border border-purple-500/40 space-y-4">
          <div className="flex items-center gap-3">
            <Award className="w-8 h-8 text-purple-400" />
            <div>
              <h2 className="text-xl font-bold text-white">Full Interview Performance Report</h2>
              <p className="text-xs text-purple-300 font-semibold">
                Overall AI Preparation Score: {evalReport.overall_score}%
              </p>
            </div>
          </div>
          <p className="text-xs text-gray-300">{evalReport.summary_evaluation?.overall_performance}</p>
          <p className="text-[11px] text-gray-500 italic">* {evalReport.summary_evaluation?.disclaimer}</p>
        </div>
      )}
    </div>
  );
}

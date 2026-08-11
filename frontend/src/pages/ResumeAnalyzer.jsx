import React, { useEffect, useState } from "react";
import { fetchApi } from "../utils/api";
import { FileCheck, Upload, Sparkles, CheckCircle2 } from "lucide-react";

export default function ResumeAnalyzer() {
  const [data, setData] = useState(null);
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadResumeData() {
      try {
        const res = await fetchApi("/resume/questions");
        setData(res);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadResumeData();
  }, []);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    setUploading(true);
    try {
      const formData = new FormData();
      formData.append("file", file);
      const token = localStorage.getItem("token");
      const res = await fetch("/api/v1/resume/upload", {
        method: "POST",
        headers: token ? { Authorization: `Bearer ${token}` } : {},
        body: formData,
      });
      const resData = await res.json();
      setData({
        has_resume: true,
        filename: resData.filename,
        parsed_skills: resData.parsed_skills,
        generated_questions: resData.generated_questions,
      });
    } catch (err) {
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  if (loading) return <div className="p-8 text-center text-gray-400">Loading resume intelligence...</div>;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="glass-card p-6 rounded-2xl border border-gray-800">
        <div className="flex items-center gap-2 text-xs font-semibold text-blue-400 mb-1">
          <FileCheck className="w-4 h-4" />
          <span>Project Deep-Dive & Question Extractor</span>
        </div>
        <h1 className="text-2xl font-bold text-white">PDF Resume Intelligence</h1>
        <p className="text-sm text-gray-400 mt-1">Upload your PDF resume to extract skills and generate project deep-dive interview questions.</p>
      </div>

      {/* File Upload Box */}
      <div className="glass-card p-6 rounded-2xl border border-gray-800 space-y-4">
        <form onSubmit={handleUpload} className="flex flex-col md:flex-row items-center gap-4">
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files[0])}
            className="block w-full text-xs text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-blue-600/20 file:text-blue-400 hover:file:bg-blue-600/30 cursor-pointer"
          />
          <button
            type="submit"
            disabled={uploading || !file}
            className="gradient-bg px-6 py-2.5 rounded-xl text-white font-semibold text-xs shadow-lg shadow-blue-500/20 flex items-center gap-2 whitespace-nowrap disabled:opacity-50"
          >
            <Upload className="w-4 h-4" />
            <span>{uploading ? "Parsing PDF..." : "Upload & Analyze Resume"}</span>
          </button>
        </form>

        {data?.filename && (
          <p className="text-xs text-emerald-400 font-semibold flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4" />
            <span>Active Resume: {data.filename}</span>
          </p>
        )}
      </div>

      {/* Extracted Skills & Deep-Dive Questions */}
      {data && (
        <div className="space-y-6">
          {data.parsed_skills && (
            <div className="glass-card p-5 rounded-2xl border border-gray-800">
              <h3 className="text-xs font-bold text-gray-400 uppercase mb-3">Extracted Core Technologies</h3>
              <div className="flex flex-wrap gap-2">
                {data.parsed_skills.map((skill, idx) => (
                  <span key={idx} className="px-3 py-1 rounded-lg bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-semibold">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          )}

          <div className="glass-card p-6 rounded-2xl border border-gray-800 space-y-4">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-blue-400" />
              <span>Project Architecture & Technical Questions</span>
            </h3>
            <div className="space-y-3">
              {data.generated_questions?.map((q, idx) => (
                <div key={idx} className="p-4 rounded-xl bg-gray-900 border border-gray-800 text-xs text-gray-200 leading-relaxed font-medium">
                  <span className="text-blue-400 font-bold mr-2">Q{idx + 1}:</span>
                  {q}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

import React, { useState } from "react";
import { Award, Download, CheckCircle2, FileText, Sparkles } from "lucide-react";

export default function PDFExport() {
  const [downloading, setDownloading] = useState(false);

  const handleDownloadPDF = async () => {
    setDownloading(true);
    try {
      const token = localStorage.getItem("token");
      const res = await fetch("/api/v1/pdf/generate", {
        method: "POST",
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });

      if (!res.ok) throw new Error("PDF Generation failed");

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "AI_Interview_Master_Workbook.pdf";
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="glass-card p-6 rounded-2xl border border-gray-800 text-center space-y-4">
        <div className="w-16 h-16 mx-auto rounded-2xl gradient-bg flex items-center justify-center shadow-lg shadow-blue-500/20">
          <Award className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-2xl font-bold text-white">Generate Interview Workbook PDF</h1>
        <p className="text-sm text-gray-400 max-w-lg mx-auto leading-relaxed">
          Compile your customized preparation plan into a clean, printable PDF containing candidate profile, readiness score, high-yield track questions, weakness diagnosis, and final interview checklist.
        </p>

        <div className="p-4 rounded-xl bg-gray-900 border border-gray-800 text-left space-y-2 text-xs text-gray-300 max-w-md mx-auto">
          <div className="font-bold text-blue-400 uppercase">PDF Sections Included:</div>
          <ul className="list-disc list-inside space-y-1">
            <li>Candidate Profile & Target Role Overview</li>
            <li>10-Dimension Skill Readiness Score Breakdown</li>
            <li>Customized Day-by-Day Preparation Plan</li>
            <li>High-Yield Python, DSA, AIML & GenAI Questions</li>
            <li>Final MNC Interview Day Checklist</li>
          </ul>
        </div>

        <button
          onClick={handleDownloadPDF}
          disabled={downloading}
          className="gradient-bg px-8 py-3 rounded-xl text-white font-semibold text-sm shadow-lg shadow-blue-500/20 inline-flex items-center gap-2"
        >
          <Download className="w-4 h-4" />
          <span>{downloading ? "Compiling PDF..." : "Download Printable PDF Workbook"}</span>
        </button>
      </div>
    </div>
  );
}

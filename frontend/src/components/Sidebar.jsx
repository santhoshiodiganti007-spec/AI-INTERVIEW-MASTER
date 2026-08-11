import React from "react";
import { 
  LayoutDashboard, 
  FileText, 
  HelpCircle, 
  Code2, 
  Brain, 
  Cpu, 
  Mic, 
  Compass, 
  BarChart3, 
  FileCheck, 
  User, 
  Award,
  Sparkles
} from "lucide-react";

export default function Sidebar({ currentPage, setCurrentPage }) {
  const menuItems = [
    { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
    { id: "assessment", label: "Initial Assessment", icon: FileText },
    { id: "questions", label: "Question Bank", icon: HelpCircle },
    { id: "dsa", label: "DSA Pattern Lab", icon: Code2 },
    { id: "aiml", label: "AIML Track", icon: Brain },
    { id: "genai", label: "GenAI & LLM Track", icon: Cpu },
    { id: "mock-interview", label: "AI Mock Interview", icon: Mic, highlight: true },
    { id: "resume", label: "Resume Analyzer", icon: FileCheck },
    { id: "roadmap", label: "Personalized Roadmap", icon: Compass },
    { id: "analytics", label: "Analytics & Weakness", icon: BarChart3 },
    { id: "pdf", label: "PDF Workbook", icon: Award },
    { id: "profile", label: "Profile & Settings", icon: User },
  ];

  return (
    <aside className="w-64 bg-gray-900/90 border-r border-gray-800 flex flex-col h-screen sticky top-0 z-30">
      {/* Brand Header */}
      <div className="p-5 border-b border-gray-800 flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl gradient-bg flex items-center justify-center shadow-lg shadow-blue-500/20">
          <Sparkles className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="font-bold text-lg text-white leading-tight">AI INTERVIEW</h1>
          <p className="text-xs font-semibold gradient-text tracking-wider">MASTER</p>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto custom-scrollbar">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentPage === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setCurrentPage(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                isActive
                  ? "bg-blue-600/20 text-blue-400 border border-blue-500/30 shadow-md shadow-blue-500/10"
                  : item.highlight
                  ? "bg-purple-600/10 text-purple-300 hover:bg-purple-600/20 border border-purple-500/20"
                  : "text-gray-400 hover:text-white hover:bg-gray-800/60"
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? "text-blue-400" : item.highlight ? "text-purple-400" : "text-gray-400"}`} />
              <span>{item.label}</span>
              {item.highlight && (
                <span className="ml-auto text-[10px] bg-purple-500/20 text-purple-300 px-1.5 py-0.5 rounded font-bold uppercase">
                  Live
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Footer Track Badge */}
      <div className="p-4 border-t border-gray-800">
        <div className="glass-card p-3 rounded-xl text-xs text-gray-400 flex items-center justify-between">
          <span>Target MNC Track:</span>
          <span className="font-bold text-blue-400">Google / Meta</span>
        </div>
      </div>
    </aside>
  );
}

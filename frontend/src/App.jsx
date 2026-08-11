import React, { useState } from "react";
import { AuthProvider, useAuth } from "./context/AuthContext";
import Sidebar from "./components/Sidebar";
import Navbar from "./components/Navbar";

import Auth from "./pages/Auth";
import Dashboard from "./pages/Dashboard";
import InitialAssessment from "./pages/InitialAssessment";
import QuestionBank from "./pages/QuestionBank";
import DSALab from "./pages/DSALab";
import AIMLTrack from "./pages/AIMLTrack";
import GenAITrack from "./pages/GenAITrack";
import MockInterview from "./pages/MockInterview";
import ResumeAnalyzer from "./pages/ResumeAnalyzer";
import RoadmapView from "./pages/RoadmapView";
import Analytics from "./pages/Analytics";
import PDFExport from "./pages/PDFExport";
import Profile from "./pages/Profile";

function MainApp() {
  const { user, loading } = useAuth();
  const [currentPage, setCurrentPage] = useState("dashboard");
  const [dashboardData, setDashboardData] = useState(null);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0b0f19] flex items-center justify-center text-gray-400 font-medium">
        Initializing AI INTERVIEW MASTER platform...
      </div>
    );
  }

  if (!user) {
    return <Auth />;
  }

  const renderPage = () => {
    switch (currentPage) {
      case "dashboard":
        return <Dashboard setCurrentPage={setCurrentPage} onDataLoaded={setDashboardData} />;
      case "assessment":
        return <InitialAssessment setCurrentPage={setCurrentPage} />;
      case "questions":
        return <QuestionBank />;
      case "dsa":
        return <DSALab />;
      case "aiml":
        return <AIMLTrack />;
      case "genai":
        return <GenAITrack />;
      case "mock-interview":
        return <MockInterview />;
      case "resume":
        return <ResumeAnalyzer />;
      case "roadmap":
        return <RoadmapView />;
      case "analytics":
        return <Analytics />;
      case "pdf":
        return <PDFExport />;
      case "profile":
        return <Profile />;
      default:
        return <Dashboard setCurrentPage={setCurrentPage} onDataLoaded={setDashboardData} />;
    }
  };

  return (
    <div className="flex min-h-screen bg-[#0b0f19] text-gray-100 font-sans">
      <Sidebar currentPage={currentPage} setCurrentPage={setCurrentPage} />
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar dashboardData={dashboardData} />
        <main className="flex-1 p-6 overflow-y-auto custom-scrollbar">
          {renderPage()}
        </main>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <MainApp />
    </AuthProvider>
  );
}

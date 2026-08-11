import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { fetchApi } from "../utils/api";
import { User, Target, Award, Shield, Save } from "lucide-react";

export default function Profile() {
  const { user, profile, setProfile } = useAuth();
  const [targetRole, setTargetRole] = useState(profile?.target_role || "Software / Python Developer");
  const [expLevel, setExpLevel] = useState(profile?.experience_level || "INTERMEDIATE");
  const [targetCompanies, setTargetCompanies] = useState(profile?.target_companies?.join(", ") || "Google, Meta, Amazon");
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState("");

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMsg("");
    try {
      const updated = await fetchApi("/auth/me/profile", {
        method: "PUT",
        body: JSON.stringify({
          target_role: targetRole,
          experience_level: expLevel,
          target_companies: targetCompanies.split(",").map((s) => s.trim()).filter(Boolean),
        }),
      });
      setProfile(updated);
      setMsg("Profile updated successfully!");
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="glass-card p-6 rounded-2xl border border-gray-800">
        <div className="flex items-center gap-2 text-xs font-semibold text-blue-400 mb-1">
          <User className="w-4 h-4" />
          <span>Candidate Preferences & Badges</span>
        </div>
        <h1 className="text-2xl font-bold text-white">Profile & Career Settings</h1>
        <p className="text-sm text-gray-400 mt-1">Configure your target role, target companies, and view earned gamification badges.</p>
      </div>

      <div className="glass-card p-6 rounded-2xl border border-gray-800 space-y-4">
        {msg && <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-400 rounded-xl">{msg}</div>}
        <form onSubmit={handleSave} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-gray-300 mb-1">Target Role Track</label>
            <select
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              className="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500"
            >
              <option value="Software / Python Developer">Software / Python Developer</option>
              <option value="AIML / Data Science">AIML / Data Science</option>
              <option value="Generative AI / LLM">Generative AI / LLM</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-300 mb-1">Experience Level</label>
            <select
              value={expLevel}
              onChange={(e) => setExpLevel(e.target.value)}
              className="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500"
            >
              <option value="BEGINNER">BEGINNER (0-2 Years)</option>
              <option value="INTERMEDIATE">INTERMEDIATE (2-5 Years)</option>
              <option value="ADVANCED">ADVANCED (5+ Years)</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-300 mb-1">Target Companies (Comma Separated)</label>
            <input
              type="text"
              value={targetCompanies}
              onChange={(e) => setTargetCompanies(e.target.value)}
              className="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500"
            />
          </div>

          <button
            type="submit"
            disabled={saving}
            className="gradient-bg px-5 py-2.5 rounded-xl text-white font-semibold text-sm shadow-lg shadow-blue-500/20 flex items-center gap-2"
          >
            <Save className="w-4 h-4" />
            <span>{saving ? "Saving..." : "Save Preferences"}</span>
          </button>
        </form>
      </div>
    </div>
  );
}

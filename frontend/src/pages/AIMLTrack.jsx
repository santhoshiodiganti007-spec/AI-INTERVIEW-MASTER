import React, { useState } from "react";
import { Brain, Layers, Cpu, CheckCircle, Sparkles } from "lucide-react";

const AIML_MODULES = [
  {
    title: "XGBoost & Gradient Boosting",
    category: "Machine Learning",
    desc: "Tree regularization, subsampling, shrinkage parameter (eta), and handling high variance.",
    q: "How does XGBoost prevent overfitting compared to standard Gradient Boosting?",
    ans: "XGBoost uses exact greedy/approximate split finding with explicit L1 (alpha) and L2 (lambda) regularization on leaf weights, tree depth caps (max_depth), row/column sub-sampling (subsample, colsample_bytree), and early stopping."
  },
  {
    title: "Deep Learning: ResNet & Batch Normalization",
    category: "Deep Learning",
    desc: "Vanishing gradient resolution, identity skip connections, and internal covariate shift stabilization.",
    q: "Why do Residual Connections (y = f(x) + x) solve vanishing gradients in 100+ layer networks?",
    ans: "During backpropagation, the gradient of (f(x) + x) with respect to x is (df/dx + 1). The constant +1 ensures that the backpropagated gradient never vanishes to zero, allowing error signals to flow back directly through the identity shortcut."
  },
  {
    title: "Model Evaluation & Class Imbalance",
    category: "Statistics & Metrics",
    desc: "ROC-AUC, Precision-Recall AUC, Focal Loss, and SMOTE oversampling.",
    q: "Why is ROC-AUC misleading on 99:1 imbalanced datasets, and why should Precision-Recall AUC be used instead?",
    ans: "ROC-AUC plots True Positive Rate vs False Positive Rate. When negative instances dominate, FPR remains artificially low even with many false positives. PR-AUC focuses directly on Positive Predictive Value (Precision) and Recall, isolating minority class performance."
  }
];

export default function AIMLTrack() {
  const [activeIdx, setActiveIdx] = useState(0);
  const activeModule = AIML_MODULES[activeIdx];

  return (
    <div className="space-y-6">
      <div className="glass-card p-6 rounded-2xl border border-gray-800">
        <div className="flex items-center gap-2 text-xs font-semibold text-purple-400 mb-1">
          <Brain className="w-4 h-4" />
          <span>Core AI/ML Engineer Track</span>
        </div>
        <h1 className="text-2xl font-bold text-white">Machine Learning & Deep Learning Mastery</h1>
        <p className="text-sm text-gray-400 mt-1">Deep conceptual explanations and architecture design scenarios for MNC data science interviews.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Module selector */}
        <div className="space-y-3">
          {AIML_MODULES.map((m, idx) => (
            <div
              key={idx}
              onClick={() => setActiveIdx(idx)}
              className={`p-4 rounded-xl cursor-pointer border transition-all ${
                activeIdx === idx
                  ? "bg-purple-600/20 border-purple-500/40 text-white"
                  : "glass-card text-gray-400 hover:text-gray-200 border-gray-800"
              }`}
            >
              <span className="text-[10px] uppercase font-bold text-purple-400 block mb-1">{m.category}</span>
              <h3 className="font-bold text-sm text-white">{m.title}</h3>
              <p className="text-xs text-gray-400 mt-1 line-clamp-2">{m.desc}</p>
            </div>
          ))}
        </div>

        {/* Detailed Module Breakdown */}
        <div className="md:col-span-2 glass-card p-6 rounded-2xl border border-gray-800 space-y-5">
          <div>
            <span className="text-xs font-bold text-purple-400 uppercase">{activeModule.category}</span>
            <h2 className="text-xl font-bold text-white mt-1">{activeModule.title}</h2>
            <p className="text-xs text-gray-400 mt-1">{activeModule.desc}</p>
          </div>

          <div className="p-4 rounded-xl bg-gray-900 border border-gray-800 space-y-2">
            <h4 className="text-xs font-bold text-blue-400 uppercase">MNC Interview Question Scenario</h4>
            <p className="text-sm font-semibold text-white">{activeModule.q}</p>
          </div>

          <div className="p-4 rounded-xl bg-purple-900/20 border border-purple-500/30 space-y-2">
            <h4 className="text-xs font-bold text-purple-300 uppercase">Model Senior Explanation</h4>
            <p className="text-xs text-gray-200 leading-relaxed">{activeModule.ans}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

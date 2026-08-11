import React, { useState } from "react";
import { Cpu, Sparkles, Database, Layers, ArrowRight } from "lucide-react";
import { fetchApi } from "../utils/api";

const GENAI_SCENARIOS = [
  {
    title: "Production Enterprise RAG System Design",
    topic: "RAG & Vector Retrieval",
    q: "Design a Production RAG System for 10 Million PDF Documents with sub-second latency.",
    architecture: [
      "Ingestion: Unstructured/PDF parser -> Semantic chunking (300 tokens, 15% overlap) + Metadata tags.",
      "Embeddings: BGE-M3 or text-embedding-3-large embedded into Qdrant/Pinecone with HNSW indexing.",
      "Hybrid Search: Dense Vector Cosine Similarity + Sparse BM25 keyword matching via Reciprocal Rank Fusion (RRF).",
      "Reranking: Cross-Encoder (Cohere Rerank) filters top-50 candidates down to top-5 high precision chunks.",
      "LLM & Evaluation: Grounded system prompt with context citations. Evaluation via RAGAS metrics."
    ]
  },
  {
    title: "LLM Fine-Tuning: LoRA & QLoRA Mechanics",
    topic: "LLM Customization",
    q: "Explain Low-Rank Adaptation (LoRA) and NF4 Quantization in QLoRA.",
    architecture: [
      "LoRA freezes base weights W0 and injects trainable rank decomposition matrices A and B: W = W0 + (B x A) * (alpha / r).",
      "QLoRA quantizes base weights W0 to 4-bit NormalFloat (NF4) while keeping LoRA adapters in 16-bit BrainFloatingPoint (bfloat16).",
      "Reduces GPU memory footprint by ~75% with zero degradation in task performance."
    ]
  }
];

export default function GenAITrack() {
  const [activeIdx, setActiveIdx] = useState(0);
  const [ragQuery, setRagQuery] = useState("Explain Scaled Dot-Product Attention in Transformers");
  const [ragResult, setRagResult] = useState(null);
  const [querying, setQuerying] = useState(false);

  const scenario = GENAI_SCENARIOS[activeIdx];

  const handleTestRAG = async () => {
    if (!ragQuery.trim()) return;
    setQuerying(true);
    try {
      const res = await fetchApi("/rag/query", {
        method: "POST",
        body: JSON.stringify({ query: ragQuery }),
      });
      setRagResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setQuerying(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="glass-card p-6 rounded-2xl border border-gray-800">
        <div className="flex items-center gap-2 text-xs font-semibold text-pink-400 mb-1">
          <Cpu className="w-4 h-4" />
          <span>Generative AI / LLM Track</span>
        </div>
        <h1 className="text-2xl font-bold text-white">Transformers, RAG Systems & Agent Architectures</h1>
        <p className="text-sm text-gray-400 mt-1">Master self-attention, hybrid vector retrieval, QLoRA fine-tuning, and RAG evaluation.</p>
      </div>

      {/* RAG Knowledge Base Sandbox */}
      <div className="glass-card p-6 rounded-2xl border border-gray-800 space-y-4">
        <h2 className="text-base font-bold text-white flex items-center gap-2">
          <Database className="w-4 h-4 text-pink-400" />
          <span>Interactive Grounded RAG Knowledge Base Engine</span>
        </h2>
        <div className="flex gap-3">
          <input
            type="text"
            value={ragQuery}
            onChange={(e) => setRagQuery(e.target.value)}
            className="flex-1 bg-gray-900 border border-gray-700 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:border-pink-500"
          />
          <button
            onClick={handleTestRAG}
            disabled={querying}
            className="gradient-bg px-5 py-2 rounded-xl text-white font-semibold text-sm shadow-lg shadow-pink-500/20 flex items-center gap-2"
          >
            <span>{querying ? "Searching..." : "Vector Search"}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

        {ragResult && (
          <div className="p-4 rounded-xl bg-gray-900 border border-gray-800 space-y-3 text-xs">
            <span className="text-emerald-400 font-bold">Retrieved Grounded Context ({ragResult.source_count} sources):</span>
            <p className="text-gray-300 font-mono leading-relaxed whitespace-pre-wrap">{ragResult.grounded_answer}</p>
          </div>
        )}
      </div>

      {/* Architecture Design Scenarios */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="space-y-3">
          {GENAI_SCENARIOS.map((s, idx) => (
            <div
              key={idx}
              onClick={() => setActiveIdx(idx)}
              className={`p-4 rounded-xl cursor-pointer border transition-all ${
                activeIdx === idx
                  ? "bg-pink-600/20 border-pink-500/40 text-white"
                  : "glass-card text-gray-400 hover:text-gray-200 border-gray-800"
              }`}
            >
              <span className="text-[10px] uppercase font-bold text-pink-400 block mb-1">{s.topic}</span>
              <h3 className="font-bold text-sm text-white">{s.title}</h3>
            </div>
          ))}
        </div>

        <div className="md:col-span-2 glass-card p-6 rounded-2xl border border-gray-800 space-y-4">
          <span className="text-xs font-bold text-pink-400 uppercase">{scenario.topic}</span>
          <h2 className="text-lg font-bold text-white">{scenario.title}</h2>
          <p className="text-sm font-semibold text-gray-200">{scenario.q}</p>

          <div className="p-4 rounded-xl bg-gray-900 border border-gray-800 space-y-2">
            <h4 className="text-xs font-bold text-emerald-400 uppercase">Production Architecture Blueprint</h4>
            <ul className="list-disc list-inside text-xs text-gray-300 space-y-1.5 leading-relaxed">
              {scenario.architecture.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

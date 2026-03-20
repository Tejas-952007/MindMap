import { useNavigate } from "react-router";
import { motion } from "motion/react";
import { ArrowRight, Download, RefreshCw } from "lucide-react";
import {
  RadarChart, PolarGrid, PolarAngleAxis, Radar, ResponsiveContainer, Tooltip,
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Cell
} from "recharts";

const BG_CARD = "#1A1A2E";
const BORDER = "rgba(255,255,255,0.07)";
const TEXT = "#E2E8F0";
const MUTED = "#94A3B8";
const INDIGO = "#4F46E5";

const radarData = [
  { category: "Stress Mgmt", score: 72 },
  { category: "Anxiety", score: 65 },
  { category: "Social Health", score: 84 },
  { category: "Sleep Quality", score: 68 },
  { category: "Academic Balance", score: 58 },
  { category: "Self-Esteem", score: 80 },
];

const categoryData = [
  { label: "Social Health", score: 84, color: "#10B981", emoji: "🤝" },
  { label: "Self-Esteem", score: 80, color: "#A5B4FC", emoji: "🌟" },
  { label: "Stress Management", score: 72, color: "#06B6D4", emoji: "🧘" },
  { label: "Sleep Quality", score: 68, color: "#7C3AED", emoji: "😴" },
  { label: "Anxiety Levels", score: 65, color: "#F59E0B", emoji: "😰" },
  { label: "Academic Balance", score: 58, color: "#F43F5E", emoji: "📚" },
];

const strengths = [
  { label: "Strong social connections", emoji: "🤝" },
  { label: "Good self-confidence", emoji: "💪" },
  { label: "Effective stress awareness", emoji: "🧘" },
];

const improvements = [
  { label: "Academic pressure management", emoji: "📚" },
  { label: "Sleep schedule consistency", emoji: "😴" },
  { label: "Anxiety coping strategies", emoji: "🧠" },
];

const recs = [
  { emoji: "🧘", title: "10-min Meditation Daily", desc: "Use apps like Headspace or YouTube — available in Marathi. Even 10 minutes lowers cortisol by 23%.", color: INDIGO, priority: "High" },
  { emoji: "⏰", title: "Pomodoro Study Method", desc: "Study 25 min → 5 min break cycle. Reduces burnout and improves academic balance significantly.", color: "#06B6D4", priority: "High" },
  { emoji: "😴", title: "Sleep Hygiene Protocol", desc: "Fixed bedtime, no screens 45 min before sleep. Blue light disrupts melatonin — use night mode.", color: "#7C3AED", priority: "Medium" },
];

function ScoreGauge({ score }: { score: number }) {
  const r = 70;
  const circ = Math.PI * r;
  const dash = (score / 100) * circ;
  const color = score >= 75 ? "#10B981" : score >= 50 ? "#F59E0B" : "#F43F5E";

  return (
    <div className="relative inline-flex items-center justify-center">
      <svg width="180" height="100" viewBox="0 0 180 100">
        <path d={`M 20 90 A ${r} ${r} 0 0 1 160 90`} stroke="rgba(255,255,255,0.08)" strokeWidth="12" fill="none" strokeLinecap="round" />
        <motion.path
          d={`M 20 90 A ${r} ${r} 0 0 1 160 90`}
          stroke={color}
          strokeWidth="12"
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circ}
          initial={{ strokeDashoffset: circ }}
          animate={{ strokeDashoffset: circ - dash }}
          transition={{ duration: 1.5, ease: "easeOut", delay: 0.4 }}
          style={{ filter: `drop-shadow(0 0 8px ${color})` }}
        />
        <text x="90" y="80" textAnchor="middle"
          style={{ fill: color, fontSize: "28px", fontWeight: 700, fontFamily: "Space Grotesk" }}>
          {score}
        </text>
        <text x="90" y="95" textAnchor="middle" style={{ fill: MUTED, fontSize: "11px" }}>/ 100</text>
      </svg>
    </div>
  );
}

const RadarTooltip = ({ active, payload }: any) => {
  if (active && payload?.length) {
    return (
      <div className="px-3 py-2 rounded-xl text-xs shadow-xl"
        style={{ backgroundColor: "#1A1A2E", border: "1px solid rgba(255,255,255,0.1)", color: TEXT }}>
        <p className="font-semibold">{payload[0]?.payload?.category}</p>
        <p style={{ color: "#A5B4FC" }}>Score: {payload[0]?.value}/100</p>
      </div>
    );
  }
  return null;
};

export function Results() {
  const navigate = useNavigate();
  const overallScore = 74;
  const riskLevel = "Moderate";
  const riskColor = "#F59E0B";

  return (
    <div style={{ backgroundColor: "#0F0F1A", minHeight: "100%" }}>
      <div className="px-6 lg:px-12 py-8">
        <div className="max-w-3xl mx-auto">
          {/* Header */}
          <div className="flex items-start justify-between mb-6 flex-wrap gap-3">
            <div>
              <h1 style={{ color: TEXT, fontFamily: "Space Grotesk", fontSize: "1.5rem", fontWeight: 700 }}>📊 Your Results</h1>
              <p style={{ color: MUTED, fontSize: "0.82rem" }}>Assessment completed • 25 Feb 2026 • Pune, Maharashtra</p>
            </div>
            <div className="flex gap-2">
              <button onClick={() => navigate("/report")}
                className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-medium transition-all hover:opacity-80"
                style={{ background: "linear-gradient(135deg, #4F46E5, #7C3AED)", color: "white" }}>
                <Download className="w-3.5 h-3.5" /> Full Report
              </button>
              <button onClick={() => navigate("/assessment")}
                className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-medium transition-all hover:opacity-80"
                style={{ backgroundColor: "rgba(255,255,255,0.06)", border: `1px solid ${BORDER}`, color: TEXT }}>
                <RefreshCw className="w-3.5 h-3.5" /> Retake
              </button>
            </div>
          </div>

          {/* Score Card */}
          <motion.div initial={{ opacity: 0, scale: 0.96 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.5 }}
            className="rounded-2xl p-6 mb-5"
            style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}`, boxShadow: "0 8px 24px rgba(79,70,229,0.12)" }}>
            <div className="flex flex-col md:flex-row items-center gap-6">
              <div className="flex flex-col items-center">
                <ScoreGauge score={overallScore} />
                <div className="flex items-center gap-2 mt-2">
                  <span className="text-2xl">🙂</span>
                  <span style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1rem" }}>
                    Moderate Wellbeing
                  </span>
                </div>
              </div>
              <div className="flex-1">
                <div className="flex flex-wrap gap-2 mb-4">
                  <span className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold"
                    style={{ backgroundColor: `${riskColor}15`, color: riskColor, border: `1px solid ${riskColor}30` }}>
                    🟡 {riskLevel} Risk
                  </span>
                  <span className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold"
                    style={{ backgroundColor: "rgba(6,182,212,0.1)", color: "#06B6D4", border: "1px solid rgba(6,182,212,0.25)" }}>
                    💻 Online Learner
                  </span>
                  <span className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold"
                    style={{ backgroundColor: "rgba(16,185,129,0.1)", color: "#10B981", border: "1px solid rgba(16,185,129,0.25)" }}>
                    🏫 Pune, Maharashtra
                  </span>
                </div>
                <p className="text-sm leading-relaxed mb-4" style={{ color: MUTED }}>
                  You show <strong style={{ color: TEXT }}>good social health and self-esteem</strong>, but academic pressure and sleep quality need attention. Your online learning environment may be contributing to anxiety.
                </p>
                <div className="grid grid-cols-3 gap-2">
                  {[
                    { label: "Strongest", value: "Social Health", color: "#10B981" },
                    { label: "Needs Work", value: "Academic Balance", color: "#F43F5E" },
                    { label: "Archetype", value: "Digital Native", color: "#06B6D4" },
                  ].map(chip => (
                    <div key={chip.label} className="p-2 rounded-lg text-center"
                      style={{ backgroundColor: `${chip.color}10`, border: `1px solid ${chip.color}20` }}>
                      <p style={{ color: MUTED, fontSize: "0.6rem" }}>{chip.label}</p>
                      <p style={{ color: chip.color, fontSize: "0.72rem", fontWeight: 600 }}>{chip.value}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>

          {/* Radar + Bars */}
          <div className="grid md:grid-cols-2 gap-5 mb-5">
            {/* Radar */}
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }}
              className="rounded-xl p-5" style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}` }}>
              <h3 className="mb-4" style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "0.95rem" }}>
                Wellness Radar
              </h3>
              <div className="h-52">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart data={radarData}>
                    <PolarGrid stroke="rgba(255,255,255,0.07)" strokeDasharray="4 4" />
                    <PolarAngleAxis dataKey="category" tick={{ fontSize: 10, fill: MUTED }} />
                    <Radar name="Score" dataKey="score" stroke={INDIGO} fill={INDIGO} fillOpacity={0.15} strokeWidth={2}
                      dot={{ fill: INDIGO, r: 3, strokeWidth: 2, stroke: "white" }} />
                    <Tooltip content={<RadarTooltip />} />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </motion.div>

            {/* Category Bars */}
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
              className="rounded-xl p-5" style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}` }}>
              <h3 className="mb-4" style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "0.95rem" }}>
                Category Scores
              </h3>
              <div className="space-y-3">
                {categoryData.map((cat) => (
                  <div key={cat.label}>
                    <div className="flex items-center justify-between mb-1">
                      <span className="flex items-center gap-1.5 text-xs" style={{ color: TEXT }}>
                        <span>{cat.emoji}</span>{cat.label}
                      </span>
                      <span style={{ color: cat.color, fontSize: "0.78rem", fontWeight: 700 }}>{cat.score}</span>
                    </div>
                    <div className="h-2 rounded-full overflow-hidden" style={{ backgroundColor: "rgba(255,255,255,0.06)" }}>
                      <motion.div className="h-full rounded-full" style={{ backgroundColor: cat.color }}
                        initial={{ width: 0 }} animate={{ width: `${cat.score}%` }}
                        transition={{ duration: 1, delay: 0.5, ease: "easeOut" }} />
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          </div>

          {/* Strengths & Improvements */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.25 }}
            className="grid md:grid-cols-2 gap-5 mb-5">
            <div className="rounded-xl p-5" style={{ backgroundColor: BG_CARD, border: "1px solid rgba(16,185,129,0.2)" }}>
              <h3 className="mb-3" style={{ color: "#10B981", fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "0.95rem" }}>
                ✨ Strengths
              </h3>
              {strengths.map(s => (
                <div key={s.label} className="flex items-center gap-2 py-2 border-b" style={{ borderColor: "rgba(255,255,255,0.04)" }}>
                  <span className="w-7 h-7 rounded-lg flex items-center justify-center"
                    style={{ backgroundColor: "rgba(16,185,129,0.12)" }}>{s.emoji}</span>
                  <span style={{ color: TEXT, fontSize: "0.82rem" }}>{s.label}</span>
                </div>
              ))}
            </div>
            <div className="rounded-xl p-5" style={{ backgroundColor: BG_CARD, border: "1px solid rgba(245,158,11,0.2)" }}>
              <h3 className="mb-3" style={{ color: "#F59E0B", fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "0.95rem" }}>
                🔧 Areas to Improve
              </h3>
              {improvements.map(s => (
                <div key={s.label} className="flex items-center gap-2 py-2 border-b" style={{ borderColor: "rgba(255,255,255,0.04)" }}>
                  <span className="w-7 h-7 rounded-lg flex items-center justify-center"
                    style={{ backgroundColor: "rgba(245,158,11,0.12)" }}>{s.emoji}</span>
                  <span style={{ color: TEXT, fontSize: "0.82rem" }}>{s.label}</span>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Recommendations */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
            <h2 className="mb-3" style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1rem" }}>
              🎯 Personalised Recommendations
            </h2>
            <div className="space-y-3 mb-6">
              {recs.map((rec, i) => (
                <motion.div key={rec.title} initial={{ opacity: 0, x: -15 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.1 + 0.4 }}
                  className="flex gap-4 p-4 rounded-xl"
                  style={{ backgroundColor: BG_CARD, border: `1px solid ${rec.color}20` }}>
                  <div className="w-10 h-10 rounded-xl flex items-center justify-center text-xl flex-shrink-0"
                    style={{ backgroundColor: `${rec.color}12` }}>
                    {rec.emoji}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between gap-2 mb-1">
                      <h3 style={{ color: TEXT, fontWeight: 600, fontSize: "0.88rem" }}>{rec.title}</h3>
                      <span className="px-2 py-0.5 rounded-full text-xs font-bold flex-shrink-0"
                        style={{ backgroundColor: `${rec.color}15`, color: rec.color }}>{rec.priority}</span>
                    </div>
                    <p style={{ color: MUTED, fontSize: "0.8rem", lineHeight: 1.5 }}>{rec.desc}</p>
                  </div>
                </motion.div>
              ))}
            </div>

            <div className="flex flex-wrap gap-3">
              <button onClick={() => navigate("/report")}
                className="flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold transition-all hover:-translate-y-0.5"
                style={{ background: "linear-gradient(135deg, #4F46E5, #7C3AED)", color: "white", boxShadow: "0 4px 15px rgba(79,70,229,0.3)" }}>
                View Full Report <ArrowRight className="w-4 h-4" />
              </button>
              <button onClick={() => navigate("/parents")}
                className="flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-medium transition-all hover:opacity-80"
                style={{ backgroundColor: "rgba(255,255,255,0.06)", border: `1px solid ${BORDER}`, color: TEXT }}>
                Share with Parent 👨‍👩‍👧
              </button>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}

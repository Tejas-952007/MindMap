import { motion } from "motion/react";
import { Download, Printer, Share2 } from "lucide-react";

const BG_CARD = "#1A1A2E";
const BORDER = "rgba(255,255,255,0.07)";
const TEXT = "#E2E8F0";
const MUTED = "#94A3B8";
const INDIGO = "#4F46E5";

const categoryScores = [
  { label: "Social Health", score: 84, color: "#10B981", emoji: "🤝", status: "Strong", note: "Above average peer connections and communication skills." },
  { label: "Self-Esteem", score: 80, color: "#A5B4FC", emoji: "🌟", status: "Good", note: "Positive self-image with healthy confidence levels." },
  { label: "Stress Management", score: 72, color: "#06B6D4", emoji: "🧘", status: "Moderate", note: "Managing stress adequately; mindfulness could help further." },
  { label: "Sleep Quality", score: 68, color: "#7C3AED", emoji: "😴", status: "Needs Attention", note: "Irregular sleep patterns detected — linked to screen time." },
  { label: "Anxiety Levels", score: 65, color: "#F59E0B", emoji: "😰", status: "Moderate", note: "Exam-related anxiety above average for Pune online learners." },
  { label: "Academic Balance", score: 58, color: "#F43F5E", emoji: "📚", status: "Concern", note: "High academic pressure with limited healthy coping mechanisms." },
];

const lifestyle = [
  { label: "Learning Mode", value: "Online (Full-time)" },
  { label: "Study Hours/Day", value: "7 hours" },
  { label: "Sleep Hours/Night", value: "6.5 hours (below 8 ideal)" },
  { label: "Physical Activity", value: "2-3x per week" },
  { label: "Social Interactions", value: "Weekly (limited)" },
  { label: "Career Clarity", value: "7/10 — Fairly clear" },
  { label: "Family Support", value: "Mostly supportive" },
  { label: "Biggest Concern", value: "Upcoming board exams" },
  { label: "Stress Coping", value: "Music & sleep" },
  { label: "Location", value: "Pune, Maharashtra" },
];

const mlPredictions = [
  { label: "Burnout Risk (next 3 months)", value: "38%", color: "#F59E0B", desc: "Moderate risk. Manageable with lifestyle changes." },
  { label: "Anxiety Escalation Risk", value: "29%", color: "#F43F5E", desc: "Low-moderate. Monitor during exam season." },
  { label: "Academic Recovery Potential", value: "82%", color: "#10B981", desc: "High potential with structured support." },
  { label: "Social Wellbeing Trajectory", value: "↑ Improving", color: "#06B6D4", desc: "Positive trend post-COVID isolation." },
];

export function FullReport() {
  return (
    <div style={{ backgroundColor: "#0F0F1A", minHeight: "100%" }}>
      <div className="px-6 lg:px-12 py-8">
        <div className="max-w-3xl mx-auto">
          {/* Header */}
          <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
            className="flex items-start justify-between flex-wrap gap-4 mb-6">
            <div>
              <h1 style={{ color: TEXT, fontFamily: "Space Grotesk", fontSize: "1.5rem", fontWeight: 700 }}>📑 Full Psychological Report</h1>
              <p style={{ color: MUTED, fontSize: "0.82rem" }}>MindMap AI Analysis • Confidential • 25 February 2026</p>
            </div>
            <div className="flex gap-2">
              <button className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-medium transition-all hover:-translate-y-0.5"
                style={{ background: "linear-gradient(135deg, #4F46E5, #7C3AED)", color: "white", boxShadow: "0 4px 15px rgba(79,70,229,0.3)" }}>
                <Download className="w-3.5 h-3.5" /> Download PDF
              </button>
              <button className="flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-medium"
                style={{ backgroundColor: "rgba(255,255,255,0.06)", border: `1px solid ${BORDER}`, color: TEXT }}>
                <Printer className="w-3.5 h-3.5" />
              </button>
              <button className="flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-medium"
                style={{ backgroundColor: "rgba(255,255,255,0.06)", border: `1px solid ${BORDER}`, color: TEXT }}>
                <Share2 className="w-3.5 h-3.5" />
              </button>
            </div>
          </motion.div>

          {/* Report Banner */}
          <motion.div initial={{ opacity: 0, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.1 }}
            className="rounded-2xl p-6 mb-6 relative overflow-hidden"
            style={{ background: "linear-gradient(135deg, #1e1b4b, #312e81)" }}>
            <div className="absolute inset-0" style={{ background: "radial-gradient(ellipse at top right, rgba(79,70,229,0.3), transparent 60%)" }} />
            <div className="relative flex flex-col md:flex-row items-start md:items-center gap-5">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-10 h-10 rounded-xl flex items-center justify-center text-xl"
                    style={{ background: "linear-gradient(135deg, #4F46E5, #7C3AED)" }}>🧠</div>
                  <div>
                    <p style={{ color: "#A5B4FC", fontSize: "0.72rem", fontWeight: 500 }}>STUDENT ID: MM-2026-PNQ-4821</p>
                    <p style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700 }}>Arjun Patil — Class 12, Pune</p>
                  </div>
                </div>
                <p style={{ color: MUTED, fontSize: "0.82rem", lineHeight: 1.6 }}>
                  This report is generated by MindMap AI based on indirect lifestyle assessment. It is not a clinical diagnosis. Please consult a mental health professional for formal evaluation.
                </p>
              </div>
              <div className="text-center px-5">
                <div style={{ fontFamily: "Space Grotesk", fontSize: "3rem", fontWeight: 800, color: "#F59E0B", lineHeight: 1 }}>74</div>
                <div style={{ color: MUTED, fontSize: "0.72rem" }}>Overall Score</div>
                <div className="mt-1 px-3 py-1 rounded-full text-xs font-bold"
                  style={{ backgroundColor: "rgba(245,158,11,0.15)", color: "#F59E0B" }}>🟡 Moderate</div>
              </div>
            </div>
          </motion.div>

          {/* Section 1: Category Breakdown */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }}
            className="rounded-xl p-6 mb-5" style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}` }}>
            <h2 className="mb-1" style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.05rem" }}>
              1. Category-wise Psychological Analysis
            </h2>
            <div className="h-0.5 w-24 mb-4 rounded-full" style={{ background: "linear-gradient(90deg, #4F46E5, #06B6D4)" }} />
            <div className="space-y-4">
              {categoryScores.map((cat, i) => (
                <div key={cat.label} className="p-4 rounded-xl" style={{ backgroundColor: "rgba(255,255,255,0.03)", border: `1px solid ${cat.color}15` }}>
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <span className="text-lg">{cat.emoji}</span>
                      <div>
                        <h3 style={{ color: TEXT, fontWeight: 600, fontSize: "0.88rem" }}>{cat.label}</h3>
                        <span className="text-xs px-2 py-0.5 rounded-full"
                          style={{ backgroundColor: `${cat.color}12`, color: cat.color }}>{cat.status}</span>
                      </div>
                    </div>
                    <div style={{ fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.4rem", color: cat.color }}>{cat.score}</div>
                  </div>
                  <div className="h-2 rounded-full mb-2 overflow-hidden" style={{ backgroundColor: "rgba(255,255,255,0.05)" }}>
                    <motion.div className="h-full rounded-full" style={{ backgroundColor: cat.color }}
                      initial={{ width: 0 }} animate={{ width: `${cat.score}%` }}
                      transition={{ duration: 1, delay: i * 0.1 + 0.5 }} />
                  </div>
                  <p style={{ color: MUTED, fontSize: "0.78rem" }}>{cat.note}</p>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Section 2: Lifestyle Profile */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
            className="rounded-xl p-6 mb-5" style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}` }}>
            <h2 className="mb-1" style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.05rem" }}>
              2. Student Lifestyle Profile
            </h2>
            <div className="h-0.5 w-24 mb-4 rounded-full" style={{ background: "linear-gradient(90deg, #4F46E5, #06B6D4)" }} />
            <div className="grid md:grid-cols-2 gap-2">
              {lifestyle.map(item => (
                <div key={item.label} className="flex items-start gap-3 p-3 rounded-lg"
                  style={{ backgroundColor: "rgba(255,255,255,0.03)" }}>
                  <div className="flex-1">
                    <p style={{ color: MUTED, fontSize: "0.7rem" }}>{item.label}</p>
                    <p style={{ color: TEXT, fontSize: "0.82rem", fontWeight: 500 }}>{item.value}</p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Section 3: ML Predictions */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.25 }}
            className="rounded-xl p-6 mb-5" style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}` }}>
            <h2 className="mb-1" style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.05rem" }}>
              3. AI Predictive Analysis
            </h2>
            <div className="h-0.5 w-24 mb-2 rounded-full" style={{ background: "linear-gradient(90deg, #4F46E5, #06B6D4)" }} />
            <p className="text-xs mb-4" style={{ color: MUTED }}>Based on 800+ student profiles from Pune — ML confidence: 89%</p>
            <div className="grid md:grid-cols-2 gap-4">
              {mlPredictions.map((pred) => (
                <div key={pred.label} className="p-4 rounded-xl"
                  style={{ backgroundColor: `${pred.color}08`, border: `1px solid ${pred.color}20` }}>
                  <p style={{ color: MUTED, fontSize: "0.72rem", marginBottom: 4 }}>{pred.label}</p>
                  <p style={{ color: pred.color, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.5rem" }}>{pred.value}</p>
                  <p style={{ color: MUTED, fontSize: "0.75rem", marginTop: 4 }}>{pred.desc}</p>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Section 4: Online vs Offline Comparison */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
            className="rounded-xl p-6 mb-5" style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}` }}>
            <h2 className="mb-1" style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.05rem" }}>
              4. Online vs. Offline Comparison (Your Profile)
            </h2>
            <div className="h-0.5 w-24 mb-4 rounded-full" style={{ background: "linear-gradient(90deg, #4F46E5, #06B6D4)" }} />
            <div className="grid grid-cols-3 gap-3">
              {[
                { metric: "Stress Level", online: "High", offline: "Medium", yours: "High", color: "#F43F5E" },
                { metric: "Social Interaction", online: "Low", offline: "High", yours: "Medium", color: "#F59E0B" },
                { metric: "Academic Performance", online: "Variable", offline: "Consistent", yours: "Variable", color: "#06B6D4" },
                { metric: "Sleep Quality", online: "Poor", offline: "Better", yours: "Below Avg", color: "#7C3AED" },
                { metric: "Mental Wellness Score", online: "68 avg", offline: "79 avg", yours: "74", color: "#10B981" },
                { metric: "Burnout Risk", online: "41%", offline: "28%", yours: "38%", color: "#F59E0B" },
              ].map(row => (
                <div key={row.metric} className="col-span-3 grid grid-cols-4 gap-2 p-2 rounded-lg"
                  style={{ backgroundColor: "rgba(255,255,255,0.02)" }}>
                  <span style={{ color: MUTED, fontSize: "0.75rem" }}>{row.metric}</span>
                  <span className="text-center text-xs px-2 py-0.5 rounded-full self-start"
                    style={{ backgroundColor: "rgba(6,182,212,0.1)", color: "#06B6D4" }}>{row.online}</span>
                  <span className="text-center text-xs px-2 py-0.5 rounded-full self-start"
                    style={{ backgroundColor: "rgba(16,185,129,0.1)", color: "#10B981" }}>{row.offline}</span>
                  <span className="text-center text-xs px-2 py-0.5 rounded-full font-bold self-start"
                    style={{ backgroundColor: `${row.color}15`, color: row.color }}>You: {row.yours}</span>
                </div>
              ))}
              <div className="col-span-3 flex gap-4 pt-1">
                {[{ c: "#06B6D4", l: "Online avg" }, { c: "#10B981", l: "Offline avg" }, { c: INDIGO, l: "Your scores" }].map(x => (
                  <div key={x.l} className="flex items-center gap-1">
                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: x.c }} />
                    <span style={{ color: MUTED, fontSize: "0.68rem" }}>{x.l}</span>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>

          {/* Disclaimer */}
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.4 }}
            className="rounded-xl p-4"
            style={{ backgroundColor: "rgba(245,158,11,0.06)", border: "1px solid rgba(245,158,11,0.2)" }}>
            <p className="text-xs leading-relaxed" style={{ color: MUTED }}>
              ⚠️ <strong style={{ color: "#F59E0B" }}>Disclaimer:</strong> This report is generated by MindMap AI for screening purposes only. It does not constitute a clinical diagnosis. For professional mental health support in Pune, contact <strong style={{ color: TEXT }}>iCall: 9152987821</strong> or visit <strong style={{ color: TEXT }}>NIMHANS Digital Academy</strong>. All data is processed anonymously.
            </p>
          </motion.div>
        </div>
      </div>
    </div>
  );
}

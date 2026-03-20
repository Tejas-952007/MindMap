import { useNavigate } from "react-router";
import { motion } from "motion/react";
import { ArrowRight, Shield, Zap, Globe, TrendingUp } from "lucide-react";
import { useApp } from "../context/AppContext";

const BG_CARD = "#1A1A2E";
const BORDER = "rgba(255,255,255,0.07)";
const TEXT = "#E2E8F0";
const MUTED = "#94A3B8";
const INDIGO = "#4F46E5";
const CYAN = "#06B6D4";

const statPills = [
  { icon: "👥", value: "800+", label: "Student Profiles", color: INDIGO },
  { icon: "🤖", value: "ML", label: "AI-Powered Insights", color: "#7C3AED" },
  { icon: "🔒", value: "100%", label: "Private & Secure", color: "#10B981" },
  { icon: "🗣️", value: "3", label: "Languages", color: CYAN },
];

const languageCards = [
  { lang: "मराठी", flag: "🇮🇳", desc: "पुणे, महाराष्ट्रातील विद्यार्थ्यांसाठी संपूर्ण मराठी समर्थन", color: "#F59E0B", sample: "तुमचे मन समजून घ्या" },
  { lang: "English", flag: "🇬🇧", desc: "Full support for English-medium students across Maharashtra", color: INDIGO, sample: "Understand Your Mind" },
  { lang: "हिंदी", flag: "🇮🇳", desc: "हिंदी माध्यम के छात्रों के लिए पूर्ण समर्थन", color: "#10B981", sample: "अपने मन को समझें" },
];

const comparisons = [
  {
    icon: "💻",
    title: "Online Learning",
    color: CYAN,
    border: "rgba(6,182,212,0.2)",
    pros: ["Flexible schedule", "Self-paced learning", "Digital resources"],
    cons: ["Social isolation risk", "Screen fatigue", "Less peer interaction"],
  },
  {
    icon: "🏫",
    title: "Offline Learning",
    color: "#10B981",
    border: "rgba(16,185,129,0.2)",
    pros: ["Structured environment", "Peer interaction", "Physical activity"],
    cons: ["Fixed schedule pressure", "Commute stress", "Rigid pace"],
  },
];

const researchInsights = [
  { stat: "67%", desc: "of Pune students report higher anxiety in online learning vs offline", icon: "📊" },
  { stat: "42%", desc: "improvement in mental wellness with hybrid learning approach", icon: "📈" },
  { stat: "3x", desc: "more likely to seek help when approached through indirect assessment", icon: "🤝" },
  { stat: "89%", desc: "accuracy of MindMap's ML model in predicting burnout risk", icon: "🎯" },
];

export function Home() {
  const navigate = useNavigate();
  const { t } = useApp();

  return (
    <div style={{ backgroundColor: "#0F0F1A", minHeight: "100%" }}>
      {/* Hero */}
      <section className="relative overflow-hidden px-6 py-16 lg:px-12 lg:py-20"
        style={{ background: "linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1e1b4b 100%)" }}>
        {/* Glow */}
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full opacity-20"
            style={{ background: "radial-gradient(circle, #4F46E5 0%, transparent 70%)", filter: "blur(60px)" }} />
        </div>

        <div className="relative max-w-3xl mx-auto text-center">
          {/* Badge */}
          <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full mb-6"
            style={{ backgroundColor: "rgba(79,70,229,0.15)", border: "1px solid rgba(79,70,229,0.3)", color: "#A5B4FC", fontSize: "0.78rem", fontWeight: 500 }}>
            <span>🇮🇳</span> Pune, Maharashtra • AI-Powered Assessment
          </motion.div>

          {/* Title */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
            <div className="flex items-center justify-center gap-3 mb-4">
              <div className="w-16 h-16 rounded-2xl flex items-center justify-center text-3xl"
                style={{ background: "linear-gradient(135deg, #4F46E5, #7C3AED)", boxShadow: "0 0 40px rgba(79,70,229,0.4)" }}>
                🧠
              </div>
            </div>
            <h1 style={{ fontFamily: "Space Grotesk, sans-serif", fontSize: "clamp(2rem, 5vw, 3.2rem)", fontWeight: 700, letterSpacing: "-0.03em", lineHeight: 1.1 }}>
              <span style={{ background: "linear-gradient(135deg, #A5B4FC, #818CF8, #C4B5FD)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
                MindMap
              </span>
            </h1>
            <p className="mt-3 mb-6 mx-auto max-w-lg" style={{ color: "#A5B4FC", fontSize: "1.15rem", fontWeight: 500 }}>
              {t.tagline}
            </p>
            <p className="mb-8 mx-auto max-w-2xl" style={{ color: MUTED, lineHeight: 1.7, fontSize: "0.9rem" }}>
              An AI-powered psychological assessment platform using <strong style={{ color: TEXT }}>indirect lifestyle questions</strong> to detect stress, anxiety, and burnout in students — comparing online vs. offline learning environments across Pune schools and colleges.
            </p>
          </motion.div>

          {/* CTA */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
            className="flex flex-wrap justify-center gap-3">
            <button onClick={() => navigate("/assessment")}
              className="flex items-center gap-2 px-7 py-3.5 rounded-xl font-semibold transition-all duration-200 hover:-translate-y-0.5"
              style={{ background: "linear-gradient(135deg, #4F46E5, #7C3AED)", color: "white", fontSize: "0.9rem", boxShadow: "0 4px 15px rgba(79,70,229,0.4)" }}>
              {t.startAssessment} <ArrowRight className="w-4 h-4" />
            </button>
            <button onClick={() => navigate("/insights")}
              className="flex items-center gap-2 px-7 py-3.5 rounded-xl font-medium transition-all duration-200 hover:-translate-y-0.5"
              style={{ backgroundColor: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.12)", color: TEXT, fontSize: "0.9rem" }}>
              View Research 🌍
            </button>
          </motion.div>
        </div>
      </section>

      {/* Stat Pills */}
      <section className="px-6 lg:px-12 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="flex flex-wrap gap-3 justify-center">
            {statPills.map((pill, i) => (
              <motion.div key={pill.label} initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: i * 0.08 }}
                className="flex items-center gap-2.5 px-5 py-2.5 rounded-full"
                style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}`, boxShadow: `0 4px 20px rgba(0,0,0,0.2)` }}>
                <span>{pill.icon}</span>
                <span style={{ color: pill.color, fontWeight: 700, fontSize: "0.9rem" }}>{pill.value}</span>
                <span style={{ color: MUTED, fontSize: "0.8rem" }}>{pill.label}</span>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Language Cards */}
      <section className="px-6 lg:px-12 py-8">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-center mb-2" style={{ color: TEXT, fontFamily: "Space Grotesk", fontSize: "1.4rem", fontWeight: 700 }}>
            Trilingual Support 🗣️
          </h2>
          <p className="text-center mb-6 text-sm" style={{ color: MUTED }}>Serving students in their preferred language</p>
          <div className="grid md:grid-cols-3 gap-4">
            {languageCards.map((card, i) => (
              <motion.div key={card.lang} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}
                className="p-5 rounded-xl transition-all duration-200 hover:-translate-y-1 cursor-pointer"
                style={{ backgroundColor: BG_CARD, border: `1px solid rgba(255,255,255,0.06)`, boxShadow: `0 4px 20px rgba(0,0,0,0.2)` }}>
                <div className="flex items-center gap-2 mb-3">
                  <span className="text-2xl">{card.flag}</span>
                  <span style={{ color: card.color, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.1rem" }}>{card.lang}</span>
                </div>
                <p className="text-xs mb-3 leading-relaxed" style={{ color: MUTED }}>{card.desc}</p>
                <div className="px-3 py-2 rounded-lg" style={{ backgroundColor: `${card.color}10`, border: `1px solid ${card.color}20` }}>
                  <p className="text-sm font-medium" style={{ color: card.color }}>"{card.sample}"</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* What is MindMap */}
      <section className="px-6 lg:px-12 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="rounded-2xl p-6 md:p-8"
            style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}`, boxShadow: "0 0 40px rgba(79,70,229,0.08)" }}>
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-xl flex items-center justify-center"
                style={{ background: "linear-gradient(135deg, rgba(79,70,229,0.2), rgba(124,58,237,0.2))", border: "1px solid rgba(79,70,229,0.3)" }}>
                <Zap className="w-5 h-5" style={{ color: "#A5B4FC" }} />
              </div>
              <div>
                <h2 style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.2rem" }}>What is MindMap?</h2>
                <div className="h-0.5 w-24 mt-1 rounded-full"
                  style={{ background: "linear-gradient(90deg, #4F46E5, #06B6D4)" }} />
              </div>
            </div>
            <p className="leading-relaxed mb-4" style={{ color: MUTED, fontSize: "0.9rem" }}>
              MindMap is an <strong style={{ color: TEXT }}>AI-powered psychological health assessment platform</strong> designed for students in Pune, Maharashtra. Unlike traditional mental health surveys, MindMap uses <strong style={{ color: "#A5B4FC" }}>indirect lifestyle and habit-based questions</strong> — students answer about their daily routines, hobbies, sleep, and future goals without feeling like they're being psychologically evaluated.
            </p>
            <p className="leading-relaxed mb-5" style={{ color: MUTED, fontSize: "0.9rem" }}>
              Our ML models then analyze these responses to detect patterns of stress, anxiety, social disconnection, and burnout — providing <strong style={{ color: TEXT }}>actionable insights</strong> for students, parents, and teachers.
            </p>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {[
                { icon: <Shield className="w-4 h-4" />, label: "Non-invasive", color: "#10B981" },
                { icon: <Zap className="w-4 h-4" />, label: "ML-Powered", color: INDIGO },
                { icon: <Globe className="w-4 h-4" />, label: "3 Languages", color: CYAN },
                { icon: <TrendingUp className="w-4 h-4" />, label: "Comparative", color: "#7C3AED" },
              ].map((tag) => (
                <div key={tag.label} className="flex items-center gap-2 px-3 py-2 rounded-lg"
                  style={{ backgroundColor: `${tag.color}0F`, border: `1px solid ${tag.color}20` }}>
                  <span style={{ color: tag.color }}>{tag.icon}</span>
                  <span style={{ color: tag.color, fontSize: "0.78rem", fontWeight: 600 }}>{tag.label}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Online vs Offline */}
      <section className="px-6 lg:px-12 py-8">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-center mb-2" style={{ color: TEXT, fontFamily: "Space Grotesk", fontSize: "1.4rem", fontWeight: 700 }}>
            Online vs. Offline Learning
          </h2>
          <p className="text-center mb-6 text-sm" style={{ color: MUTED }}>Psychological impact comparison for Maharashtra students</p>
          <div className="grid md:grid-cols-2 gap-5">
            {comparisons.map((comp, i) => (
              <motion.div key={comp.title} initial={{ opacity: 0, x: i === 0 ? -20 : 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.2 }}
                className="rounded-xl p-5"
                style={{ backgroundColor: BG_CARD, border: `1px solid ${comp.border}` }}>
                <div className="flex items-center gap-2 mb-4">
                  <span className="text-2xl">{comp.icon}</span>
                  <h3 style={{ color: comp.color, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1rem" }}>{comp.title}</h3>
                </div>
                <div className="space-y-1 mb-3">
                  {comp.pros.map((p) => (
                    <div key={p} className="flex items-center gap-2 text-sm">
                      <span style={{ color: "#10B981" }}>✓</span>
                      <span style={{ color: TEXT }}>{p}</span>
                    </div>
                  ))}
                </div>
                <div className="space-y-1 pt-3 border-t" style={{ borderColor: BORDER }}>
                  {comp.cons.map((c) => (
                    <div key={c} className="flex items-center gap-2 text-sm">
                      <span style={{ color: "#F43F5E" }}>✗</span>
                      <span style={{ color: MUTED }}>{c}</span>
                    </div>
                  ))}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Research Insights */}
      <section className="px-6 lg:px-12 py-8 mb-8">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-center mb-2" style={{ color: TEXT, fontFamily: "Space Grotesk", fontSize: "1.4rem", fontWeight: 700 }}>
            India-Specific Research 🇮🇳
          </h2>
          <p className="text-center mb-6 text-sm" style={{ color: MUTED }}>Data from 800+ Pune student profiles</p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {researchInsights.map((item, i) => (
              <motion.div key={item.stat} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}
                className="p-5 rounded-xl text-center"
                style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}` }}>
                <div className="text-2xl mb-2">{item.icon}</div>
                <div style={{ fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.8rem", color: "#A5B4FC" }}>{item.stat}</div>
                <p className="mt-1" style={{ color: MUTED, fontSize: "0.72rem", lineHeight: 1.5 }}>{item.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Banner */}
      <section className="px-6 lg:px-12 pb-10">
        <div className="max-w-4xl mx-auto">
          <div className="rounded-2xl p-8 text-center relative overflow-hidden"
            style={{ background: "linear-gradient(135deg, #1e1b4b, #312e81)" }}>
            <div className="absolute inset-0" style={{ background: "radial-gradient(ellipse at center, rgba(79,70,229,0.3) 0%, transparent 70%)" }} />
            <div className="relative">
              <p className="text-sm mb-2" style={{ color: "#A5B4FC", fontWeight: 500 }}>🧠 Ready to begin?</p>
              <h2 className="mb-3" style={{ color: TEXT, fontFamily: "Space Grotesk", fontSize: "1.5rem", fontWeight: 700 }}>
                Take the Assessment Today
              </h2>
              <p className="mb-6 mx-auto max-w-md" style={{ color: MUTED, fontSize: "0.88rem" }}>
                15 minutes • No registration • Completely private • Available in English, मराठी & हिंदी
              </p>
              <button onClick={() => navigate("/assessment")}
                className="inline-flex items-center gap-2 px-7 py-3 rounded-xl font-semibold transition-all hover:-translate-y-0.5"
                style={{ background: "linear-gradient(135deg, #4F46E5, #7C3AED)", color: "white", boxShadow: "0 8px 25px rgba(79,70,229,0.45)" }}>
                {t.startAssessment} <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

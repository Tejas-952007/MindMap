import { motion } from "motion/react";

const BG_CARD = "#1A1A2E";
const BORDER = "rgba(255,255,255,0.07)";
const TEXT = "#E2E8F0";
const MUTED = "#94A3B8";
const INDIGO = "#4F46E5";

const team = [
  { name: "Dr. Priya Kulkarni", role: "Clinical Psychologist", emoji: "👩‍⚕️", exp: "12 yrs", city: "Pune" },
  { name: "Rahul Deshpande", role: "ML Engineer", emoji: "🧑‍💻", exp: "8 yrs", city: "Pune" },
  { name: "Ananya Joshi", role: "Educational Counsellor", emoji: "👩‍🎓", exp: "7 yrs", city: "Nashik" },
  { name: "Dr. Vikram Patil", role: "Research Psychologist", emoji: "🧑‍🔬", exp: "15 yrs", city: "Mumbai" },
];

const tech = [
  { emoji: "🐍", name: "Python / Streamlit", desc: "Backend & web framework" },
  { emoji: "🤖", name: "Scikit-learn + XGBoost", desc: "ML stress prediction models" },
  { emoji: "📊", name: "Plotly", desc: "Interactive data visualisations" },
  { emoji: "🗄️", name: "Pandas + NumPy", desc: "Data processing pipeline" },
  { emoji: "🔐", name: "Local processing only", desc: "No cloud data transmission" },
  { emoji: "🌐", name: "3 Languages", desc: "English, मराठी, हिंदी" },
];

export function About() {
  return (
    <div style={{ backgroundColor: "#0F0F1A", minHeight: "100%" }}>
      {/* Hero */}
      <div className="px-6 lg:px-12 py-10 relative overflow-hidden"
        style={{ background: "linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1e1b4b 100%)" }}>
        <div className="absolute inset-0" style={{ background: "radial-gradient(ellipse at center, rgba(79,70,229,0.3), transparent 70%)" }} />
        <div className="relative max-w-4xl mx-auto text-center">
          <div className="text-5xl mb-4">🧠</div>
          <h1 style={{ color: TEXT, fontFamily: "Space Grotesk", fontSize: "2rem", fontWeight: 800, letterSpacing: "-0.02em" }}>
            About MindMap
          </h1>
          <p className="mt-3 mx-auto max-w-xl" style={{ color: "#A5B4FC", lineHeight: 1.7, fontSize: "0.9rem" }}>
            India's first AI-powered indirect psychological assessment platform, built for Pune students and families navigating the challenges of online vs. offline learning.
          </p>
          <div className="flex flex-wrap justify-center gap-2 mt-4">
            {["Pune, Maharashtra 🇮🇳", "800+ Profiles", "Free Forever", "WCAG AA Accessible"].map(tag => (
              <span key={tag} className="px-3 py-1 rounded-full text-xs"
                style={{ backgroundColor: "rgba(165,180,252,0.1)", border: "1px solid rgba(165,180,252,0.25)", color: "#A5B4FC" }}>
                {tag}
              </span>
            ))}
          </div>
        </div>
      </div>

      <div className="px-6 lg:px-12 py-8">
        <div className="max-w-3xl mx-auto space-y-6">
          {/* Mission */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
            className="rounded-xl p-6" style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}` }}>
            <h2 className="mb-1" style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.05rem" }}>🎯 Our Mission</h2>
            <div className="h-0.5 w-16 mb-3 rounded-full" style={{ background: "linear-gradient(90deg, #4F46E5, #06B6D4)" }} />
            <p className="leading-relaxed text-sm mb-3" style={{ color: MUTED }}>
              MindMap was born from a critical observation: after COVID-19, thousands of Pune students silently struggled with anxiety, burnout, and social disconnection — but never got help due to <strong style={{ color: TEXT }}>stigma and lack of accessible tools</strong>.
            </p>
            <p className="leading-relaxed text-sm" style={{ color: MUTED }}>
              Our solution: <strong style={{ color: TEXT }}>indirect lifestyle-based assessment</strong>. Instead of asking "are you depressed?", we ask about sleep, hobbies, study habits, and goals. ML models detect patterns. Students get insights without feeling stigmatised.
            </p>
          </motion.div>

          {/* What Makes Us Different */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
            className="rounded-xl p-6" style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}` }}>
            <h2 className="mb-4" style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.05rem" }}>
              ✨ What Makes MindMap Different
            </h2>
            <div className="grid md:grid-cols-2 gap-3">
              {[
                { icon: "🎭", title: "Indirect Assessment", desc: "Lifestyle questions, not clinical surveys. Students don't feel evaluated.", color: INDIGO },
                { icon: "🇮🇳", title: "India-Specific", desc: "Designed for Pune's cultural context — family pressure, exam culture, multilingual.", color: "#F59E0B" },
                { icon: "📊", title: "Comparative Analysis", desc: "Online vs. offline learning psychological impact — a first in India.", color: "#06B6D4" },
                { icon: "👨‍👩‍👧", title: "Ecosystem Approach", desc: "Tools for students, parents, AND teachers. Not just one stakeholder.", color: "#10B981" },
                { icon: "🤖", title: "ML-Powered", desc: "89% accuracy model trained on 800+ Pune student profiles.", color: "#7C3AED" },
                { icon: "🔒", title: "Privacy-First", desc: "All processing local. No names stored. DPDP Act compliant.", color: "#F43F5E" },
              ].map((item, i) => (
                <div key={item.title} className="flex items-start gap-3 p-3 rounded-xl"
                  style={{ backgroundColor: `${item.color}08`, border: `1px solid ${item.color}15` }}>
                  <span className="text-xl">{item.icon}</span>
                  <div>
                    <p style={{ color: item.color, fontWeight: 600, fontSize: "0.82rem" }}>{item.title}</p>
                    <p style={{ color: MUTED, fontSize: "0.75rem" }}>{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Tech Stack */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }}
            className="rounded-xl p-6" style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}` }}>
            <h2 className="mb-4" style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.05rem" }}>🛠️ Technology Stack</h2>
            <div className="grid md:grid-cols-3 gap-3">
              {tech.map(t => (
                <div key={t.name} className="flex items-center gap-2 p-3 rounded-xl"
                  style={{ backgroundColor: "rgba(255,255,255,0.03)", border: `1px solid ${BORDER}` }}>
                  <span className="text-xl">{t.emoji}</span>
                  <div>
                    <p style={{ color: TEXT, fontSize: "0.78rem", fontWeight: 600 }}>{t.name}</p>
                    <p style={{ color: MUTED, fontSize: "0.68rem" }}>{t.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Team */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
            className="rounded-xl p-6" style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}` }}>
            <h2 className="mb-4" style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.05rem" }}>👥 Expert Team</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {team.map((member, i) => (
                <motion.div key={member.name} initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: i * 0.08 + 0.3 }}
                  className="text-center p-4 rounded-xl"
                  style={{ backgroundColor: "rgba(255,255,255,0.03)", border: `1px solid ${BORDER}` }}>
                  <div className="text-3xl mb-2">{member.emoji}</div>
                  <p style={{ color: TEXT, fontSize: "0.8rem", fontWeight: 600 }}>{member.name}</p>
                  <p style={{ color: MUTED, fontSize: "0.68rem", marginTop: 2 }}>{member.role}</p>
                  <div className="flex justify-center gap-1 mt-2 flex-wrap">
                    <span className="px-2 py-0.5 rounded-full text-xs" style={{ backgroundColor: "rgba(79,70,229,0.12)", color: "#A5B4FC" }}>{member.exp}</span>
                    <span className="px-2 py-0.5 rounded-full text-xs" style={{ backgroundColor: "rgba(6,182,212,0.1)", color: "#06B6D4" }}>{member.city}</span>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Methodology */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.25 }}
            className="rounded-xl p-6" style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}` }}>
            <h2 className="mb-4" style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.05rem" }}>🔬 Research Methodology</h2>
            <div className="space-y-3">
              {[
                { emoji: "📋", title: "PHQ-9 (Adapted)", desc: "Depression screening adapted for Indian adolescents with indirect framing." },
                { emoji: "😰", title: "GAD-7 (Adapted)", desc: "Anxiety assessment reimagined as lifestyle & habit questions." },
                { emoji: "📚", title: "Academic Stress Index", desc: "Custom scale developed for Maharashtra board exam culture." },
                { emoji: "🇮🇳", title: "Indian Cultural Validation", desc: "Validated by Pune University's Psychology Department (2024)." },
              ].map(item => (
                <div key={item.title} className="flex items-start gap-3 p-3 rounded-xl"
                  style={{ backgroundColor: "rgba(255,255,255,0.03)" }}>
                  <span className="text-xl">{item.emoji}</span>
                  <div>
                    <p style={{ color: TEXT, fontSize: "0.82rem", fontWeight: 600 }}>{item.title}</p>
                    <p style={{ color: MUTED, fontSize: "0.75rem" }}>{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Disclaimer */}
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }}
            className="rounded-xl p-4"
            style={{ backgroundColor: "rgba(245,158,11,0.06)", border: "1px solid rgba(245,158,11,0.2)" }}>
            <p className="text-xs leading-relaxed" style={{ color: MUTED }}>
              ⚠️ <strong style={{ color: "#F59E0B" }}>Medical Disclaimer:</strong> MindMap is a screening tool only and does NOT constitute clinical diagnosis or medical advice. For professional support in Pune, contact iCall: <strong style={{ color: TEXT }}>9152987821</strong>. All responses are processed anonymously. Compliant with India's DPDP Act 2023.
            </p>
          </motion.div>

          <div className="text-center pb-4" style={{ color: MUTED, fontSize: "0.72rem" }}>
            MindMap v2.0 • Made with ❤️ in Pune, Maharashtra 🇮🇳 • © 2026
          </div>
        </div>
      </div>
    </div>
  );
}

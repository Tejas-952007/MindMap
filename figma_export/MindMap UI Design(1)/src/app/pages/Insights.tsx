import { motion } from "motion/react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  RadialBarChart, RadialBar, BarChart, Bar, Cell
} from "recharts";

const BG_CARD = "#1A1A2E";
const BORDER = "rgba(255,255,255,0.07)";
const TEXT = "#E2E8F0";
const MUTED = "#94A3B8";
const INDIGO = "#4F46E5";
const CYAN = "#06B6D4";
const VIOLET = "#7C3AED";

const covidLineData = [
  { year: "2019", online: 12, offline: 88, hybrid: 0 },
  { year: "2020", online: 78, offline: 18, hybrid: 4 },
  { year: "2021", online: 82, offline: 8, hybrid: 10 },
  { year: "2022", online: 45, offline: 32, hybrid: 23 },
  { year: "2023", online: 28, offline: 48, hybrid: 24 },
  { year: "2024", online: 22, offline: 52, hybrid: 26 },
];

const satisfactionData = [
  { name: "Online Satisfaction", value: 62, fill: CYAN },
  { name: "Offline Satisfaction", value: 78, fill: "#10B981" },
  { name: "Hybrid Satisfaction", value: 84, fill: VIOLET },
];

const stateHybridData = [
  { state: "Pune", adoption: 84 },
  { state: "Mumbai", adoption: 79 },
  { state: "Nashik", adoption: 61 },
  { state: "Nagpur", adoption: 57 },
  { state: "Aurangabad", adoption: 48 },
  { state: "Kolhapur", adoption: 44 },
];

const archetypes = [
  {
    icon: "🏆",
    title: "Overloaded Achievers",
    percent: "28%",
    desc: "High academic performers with suppressed emotional distress. Appear successful but carry significant hidden anxiety.",
    tags: ["High GPA", "Sleep Deprived", "Low Social Life"],
    color: "#F59E0B",
    risk: "Medium-High",
  },
  {
    icon: "📱",
    title: "Digital Natives",
    percent: "35%",
    desc: "Thriving in online environments but showing signs of social withdrawal and real-world interaction anxiety.",
    tags: ["Online Learners", "Tech-Savvy", "Socially Isolated"],
    color: CYAN,
    risk: "Medium",
  },
  {
    icon: "🤝",
    title: "Social Learners",
    percent: "22%",
    desc: "Dependent on peer interaction for motivation. Suffered most during COVID lockdowns. Now recovering.",
    tags: ["Group Learners", "Extroverted", "COVID-Affected"],
    color: "#10B981",
    risk: "Low-Medium",
  },
  {
    icon: "😔",
    title: "Silent Strugglers",
    percent: "15%",
    desc: "Neither performing well academically nor expressing distress. High burnout risk. Most underserved group.",
    tags: ["Low Engagement", "Withdrawn", "High Risk"],
    color: "#F43F5E",
    risk: "High",
  },
];

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="px-3 py-2 rounded-xl shadow-xl text-xs"
        style={{ backgroundColor: "#1A1A2E", border: "1px solid rgba(255,255,255,0.1)", color: TEXT }}>
        <p className="font-semibold mb-1">{label}</p>
        {payload.map((p: any) => (
          <p key={p.dataKey} style={{ color: p.color }}>{p.name}: {p.value}%</p>
        ))}
      </div>
    );
  }
  return null;
};

function SatisfactionGauge({ data }: { data: typeof satisfactionData }) {
  return (
    <div className="grid grid-cols-3 gap-4">
      {data.map((item) => {
        const r = 36;
        const circ = 2 * Math.PI * r;
        const dash = (item.value / 100) * circ;
        return (
          <div key={item.name} className="flex flex-col items-center p-4 rounded-xl"
            style={{ backgroundColor: "rgba(255,255,255,0.03)", border: `1px solid ${BORDER}` }}>
            <svg width="90" height="90" viewBox="0 0 90 90">
              <circle cx="45" cy="45" r={r} stroke="rgba(255,255,255,0.06)" strokeWidth="8" fill="none" />
              <motion.circle
                cx="45" cy="45" r={r}
                stroke={item.fill}
                strokeWidth="8"
                fill="none"
                strokeLinecap="round"
                strokeDasharray={circ}
                initial={{ strokeDashoffset: circ }}
                animate={{ strokeDashoffset: circ - dash }}
                transition={{ duration: 1.5, ease: "easeOut", delay: 0.3 }}
                style={{ transform: "rotate(-90deg)", transformOrigin: "50% 50%" }}
              />
              <text x="45" y="45" textAnchor="middle" dominantBaseline="central"
                style={{ fill: item.fill, fontSize: "18px", fontWeight: 700, fontFamily: "Space Grotesk" }}>
                {item.value}
              </text>
              <text x="45" y="60" textAnchor="middle"
                style={{ fill: MUTED, fontSize: "10px" }}>%</text>
            </svg>
            <p className="text-center mt-1" style={{ color: MUTED, fontSize: "0.7rem", lineHeight: 1.3 }}>
              {item.name.replace(" Satisfaction", "")}
            </p>
          </div>
        );
      })}
    </div>
  );
}

export function Insights() {
  return (
    <div style={{ backgroundColor: "#0F0F1A", minHeight: "100%" }}>
      {/* Hero */}
      <div className="px-6 lg:px-12 py-10 border-b" style={{ borderColor: BORDER }}>
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-2xl">🌍</span>
            <h1 style={{ color: TEXT, fontFamily: "Space Grotesk", fontSize: "1.7rem", fontWeight: 700 }}>Global Context</h1>
          </div>
          <div className="h-0.5 w-32 mb-3 rounded-full" style={{ background: "linear-gradient(90deg, #4F46E5, #06B6D4)" }} />
          <p style={{ color: MUTED, fontSize: "0.9rem" }}>COVID-19 impact on Indian student mental health, learning mode transitions, and Maharashtra 2024 data</p>
        </div>
      </div>

      <div className="px-6 lg:px-12 py-8">
        <div className="max-w-4xl mx-auto space-y-8">
          {/* COVID Line Chart */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
            className="rounded-xl p-6" style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}` }}>
            <h2 className="mb-1" style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.05rem" }}>
              India Learning Mode Shift 2019–2024
            </h2>
            <p className="text-xs mb-5" style={{ color: MUTED }}>% students in each learning mode — COVID-19 impact visualization</p>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={covidLineData}>
                  <CartesianGrid stroke="rgba(255,255,255,0.05)" strokeDasharray="4 4" />
                  <XAxis dataKey="year" tick={{ fill: MUTED, fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fill: MUTED, fontSize: 11 }} axisLine={false} tickLine={false} unit="%" />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend wrapperStyle={{ color: MUTED, fontSize: "12px" }} />
                  <Line type="monotone" dataKey="online" name="Online" stroke={CYAN} strokeWidth={2.5} dot={{ r: 4, fill: CYAN }} />
                  <Line type="monotone" dataKey="offline" name="Offline" stroke="#10B981" strokeWidth={2.5} dot={{ r: 4, fill: "#10B981" }} />
                  <Line type="monotone" dataKey="hybrid" name="Hybrid" stroke={VIOLET} strokeWidth={2.5} dot={{ r: 4, fill: VIOLET }} strokeDasharray="5 3" />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-4 p-3 rounded-lg text-xs" style={{ backgroundColor: "rgba(79,70,229,0.08)", border: "1px solid rgba(79,70,229,0.15)", color: "#A5B4FC" }}>
              📌 COVID-19 forced 78% of students online in 2020. Gradual return to offline started 2022. Hybrid model now dominant in Pune colleges.
            </div>
          </motion.div>

          {/* Satisfaction Gauges */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
            className="rounded-xl p-6" style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}` }}>
            <h2 className="mb-1" style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.05rem" }}>
              Maharashtra Student Satisfaction 2024
            </h2>
            <p className="text-xs mb-5" style={{ color: MUTED }}>Self-reported satisfaction scores by learning mode (n=800 students, Pune)</p>
            <SatisfactionGauge data={satisfactionData} />
            <div className="grid grid-cols-3 gap-3 mt-4">
              {[
                { label: "Online students report loneliness", val: "71%", color: "#F43F5E" },
                { label: "Prefer hybrid for academics", val: "84%", color: "#10B981" },
                { label: "Want mental health support", val: "68%", color: INDIGO },
              ].map(s => (
                <div key={s.label} className="text-center p-3 rounded-lg"
                  style={{ backgroundColor: "rgba(255,255,255,0.03)", border: `1px solid ${BORDER}` }}>
                  <div style={{ color: s.color, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.4rem" }}>{s.val}</div>
                  <p style={{ color: MUTED, fontSize: "0.68rem", marginTop: 4, lineHeight: 1.4 }}>{s.label}</p>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Hybrid Adoption Bar Chart */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }}
            className="rounded-xl p-6" style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}` }}>
            <h2 className="mb-1" style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.05rem" }}>
              Hybrid Learning Adoption by City — Maharashtra
            </h2>
            <p className="text-xs mb-5" style={{ color: MUTED }}>% of institutions offering hybrid model (2024)</p>
            <div className="h-52">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={stateHybridData} layout="vertical">
                  <CartesianGrid stroke="rgba(255,255,255,0.04)" strokeDasharray="4 4" horizontal={false} />
                  <XAxis type="number" tick={{ fill: MUTED, fontSize: 11 }} axisLine={false} tickLine={false} unit="%" />
                  <YAxis type="category" dataKey="state" tick={{ fill: MUTED, fontSize: 11 }} axisLine={false} tickLine={false} width={80} />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar dataKey="adoption" name="Hybrid Adoption" radius={[0, 6, 6, 0]}>
                    {stateHybridData.map((_, i) => (
                      <Cell key={i} fill={i === 0 ? INDIGO : i === 1 ? VIOLET : CYAN} opacity={1 - i * 0.1} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </motion.div>

          {/* Student Archetypes */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
            <h2 className="mb-1" style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.05rem" }}>
              Student Archetypes in Pune Schools
            </h2>
            <p className="text-xs mb-4" style={{ color: MUTED }}>ML-identified psychological profiles from assessment data</p>
            <div className="grid md:grid-cols-2 gap-4">
              {archetypes.map((arch, i) => (
                <motion.div key={arch.title} initial={{ opacity: 0, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: i * 0.08 + 0.2 }}
                  className="p-5 rounded-xl"
                  style={{ backgroundColor: BG_CARD, border: `1px solid ${arch.color}25` }}>
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <span className="text-2xl">{arch.icon}</span>
                      <div>
                        <h3 style={{ color: arch.color, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "0.95rem" }}>{arch.title}</h3>
                        <span style={{ color: arch.color, fontSize: "1.4rem", fontWeight: 700, fontFamily: "Space Grotesk" }}>{arch.percent}</span>
                        <span style={{ color: MUTED, fontSize: "0.7rem" }}> of students</span>
                      </div>
                    </div>
                    <span className="px-2 py-0.5 rounded-full text-xs font-semibold"
                      style={{ backgroundColor: `${arch.color}15`, color: arch.color }}>
                      {arch.risk} Risk
                    </span>
                  </div>
                  <p className="text-xs leading-relaxed mb-3" style={{ color: MUTED }}>{arch.desc}</p>
                  <div className="flex flex-wrap gap-1.5">
                    {arch.tags.map(tag => (
                      <span key={tag} className="px-2 py-0.5 rounded-full text-xs"
                        style={{ backgroundColor: `${arch.color}10`, color: arch.color, border: `1px solid ${arch.color}20` }}>
                        {tag}
                      </span>
                    ))}
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}

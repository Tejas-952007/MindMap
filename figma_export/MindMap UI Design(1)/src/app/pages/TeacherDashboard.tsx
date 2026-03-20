import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Upload, FileText, Users, AlertTriangle, TrendingUp, Eye } from "lucide-react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line, Legend
} from "recharts";

const BG_CARD = "#1A1A2E";
const BORDER = "rgba(255,255,255,0.07)";
const TEXT = "#E2E8F0";
const MUTED = "#94A3B8";
const INDIGO = "#4F46E5";
const CYAN = "#06B6D4";

const classStressData = [
  { grade: "8th", low: 28, moderate: 45, high: 27 },
  { grade: "9th", low: 22, moderate: 41, high: 37 },
  { grade: "10th", low: 15, moderate: 38, high: 47 },
  { grade: "11th", low: 20, moderate: 36, high: 44 },
  { grade: "12th", low: 10, moderate: 29, high: 61 },
];

const learningModeData = [
  { name: "Online", value: 38, color: CYAN },
  { name: "Offline", value: 42, color: "#10B981" },
  { name: "Hybrid", value: 20, color: "#7C3AED" },
];

const weeklyTrend = [
  { week: "Week 1", wellness: 72, anxiety: 32 },
  { week: "Week 2", wellness: 69, anxiety: 38 },
  { week: "Week 3", wellness: 65, anxiety: 45 },
  { week: "Week 4", wellness: 68, anxiety: 41 },
  { week: "Week 5", wellness: 71, anxiety: 35 },
  { week: "Week 6", wellness: 74, anxiety: 30 },
];

const mockStudents = [
  { id: "MM-001", name: "Arjun P.", grade: "12th", mode: "Online", score: 58, risk: "High", concern: "Exam anxiety", color: "#F43F5E" },
  { id: "MM-002", name: "Sneha K.", grade: "11th", mode: "Hybrid", score: 74, risk: "Moderate", concern: "Academic pressure", color: "#F59E0B" },
  { id: "MM-003", name: "Rohan D.", grade: "10th", mode: "Offline", score: 82, risk: "Low", concern: "None significant", color: "#10B981" },
  { id: "MM-004", name: "Priya M.", grade: "12th", mode: "Online", score: 61, risk: "High", concern: "Social isolation", color: "#F43F5E" },
  { id: "MM-005", name: "Aditya S.", grade: "9th", mode: "Offline", score: 88, risk: "Low", concern: "None", color: "#10B981" },
  { id: "MM-006", name: "Anjali R.", grade: "11th", mode: "Online", score: 67, risk: "Moderate", concern: "Sleep issues", color: "#F59E0B" },
  { id: "MM-007", name: "Vivek N.", grade: "10th", mode: "Hybrid", score: 55, risk: "High", concern: "Family stress", color: "#F43F5E" },
  { id: "MM-008", name: "Kavya T.", grade: "8th", mode: "Offline", score: 91, risk: "Low", concern: "None", color: "#10B981" },
];

const classStats = [
  { label: "Total Students", value: "800", icon: "👥", color: INDIGO },
  { label: "High Risk", value: "127", icon: "🚨", color: "#F43F5E" },
  { label: "Moderate Risk", value: "284", icon: "⚠️", color: "#F59E0B" },
  { label: "Low Risk", value: "389", icon: "✅", color: "#10B981" },
];

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload?.length) {
    return (
      <div className="px-3 py-2 rounded-xl shadow-xl text-xs"
        style={{ backgroundColor: "#1A1A2E", border: "1px solid rgba(255,255,255,0.1)", color: TEXT }}>
        <p className="font-semibold mb-1">{label}</p>
        {payload.map((p: any) => (
          <p key={p.dataKey} style={{ color: p.color || p.fill }}>{p.name}: {p.value}{typeof p.value === "number" && p.name !== "Score" ? "%" : ""}</p>
        ))}
      </div>
    );
  }
  return null;
};

export function TeacherDashboard() {
  const [dataLoaded, setDataLoaded] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [selectedStudent, setSelectedStudent] = useState<typeof mockStudents[0] | null>(null);
  const [filterRisk, setFilterRisk] = useState("All");

  function loadDemo() {
    setUploading(true);
    setTimeout(() => { setUploading(false); setDataLoaded(true); }, 1800);
  }

  const filtered = filterRisk === "All" ? mockStudents : mockStudents.filter(s => s.risk === filterRisk);

  return (
    <div style={{ backgroundColor: "#0F0F1A", minHeight: "100%" }}>
      <div className="px-6 lg:px-12 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="flex items-start justify-between flex-wrap gap-4 mb-6">
            <div>
              <h1 style={{ color: TEXT, fontFamily: "Space Grotesk", fontSize: "1.5rem", fontWeight: 700 }}>
                👩‍🏫 Teacher Dashboard
              </h1>
              <p style={{ color: MUTED, fontSize: "0.85rem" }}>Class-level mental wellness analysis • Pune Schools 2024–25</p>
            </div>
            {dataLoaded && (
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-full"
                style={{ backgroundColor: "rgba(16,185,129,0.1)", border: "1px solid rgba(16,185,129,0.2)", color: "#10B981", fontSize: "0.75rem" }}>
                ✓ 800 profiles loaded
              </div>
            )}
          </div>

          {/* Upload / Demo Section */}
          <AnimatePresence>
            {!dataLoaded && (
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, scale: 0.97 }}
                className="rounded-2xl p-8 mb-6 text-center"
                style={{ backgroundColor: BG_CARD, border: `2px dashed rgba(79,70,229,0.3)` }}>
                {uploading ? (
                  <div className="flex flex-col items-center gap-4">
                    <div className="w-14 h-14 rounded-2xl flex items-center justify-center"
                      style={{ background: "linear-gradient(135deg, #4F46E5, #7C3AED)" }}>
                      <motion.div animate={{ rotate: 360 }} transition={{ duration: 1, repeat: Infinity, ease: "linear" }}>
                        <Upload className="w-7 h-7 text-white" />
                      </motion.div>
                    </div>
                    <div>
                      <p style={{ color: TEXT, fontWeight: 600 }}>Processing 800 student profiles...</p>
                      <p style={{ color: MUTED, fontSize: "0.82rem" }}>Running ML analysis • Pune schools dataset</p>
                    </div>
                    <div className="w-48 h-2 rounded-full overflow-hidden" style={{ backgroundColor: "rgba(255,255,255,0.07)" }}>
                      <motion.div className="h-full rounded-full"
                        style={{ background: "linear-gradient(90deg, #4F46E5, #06B6D4)" }}
                        animate={{ width: ["0%", "100%"] }}
                        transition={{ duration: 1.6, ease: "easeOut" }} />
                    </div>
                  </div>
                ) : (
                  <>
                    <div className="w-14 h-14 rounded-2xl flex items-center justify-center mx-auto mb-4"
                      style={{ backgroundColor: "rgba(79,70,229,0.12)", border: "1px solid rgba(79,70,229,0.25)" }}>
                      <Upload className="w-7 h-7" style={{ color: "#A5B4FC" }} />
                    </div>
                    <h2 className="mb-1" style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.1rem" }}>
                      Upload Class Data
                    </h2>
                    <p className="mb-5 mx-auto max-w-sm" style={{ color: MUTED, fontSize: "0.82rem" }}>
                      Upload a CSV or Excel file with student assessment responses, or use our demo dataset of 800 Pune students.
                    </p>
                    <div className="flex flex-wrap gap-3 justify-center">
                      <button className="flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-medium transition-all hover:-translate-y-0.5"
                        style={{ backgroundColor: "rgba(255,255,255,0.06)", border: `1px solid ${BORDER}`, color: TEXT }}>
                        <FileText className="w-4 h-4" /> Upload CSV / Excel
                      </button>
                      <button onClick={loadDemo}
                        className="flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold transition-all hover:-translate-y-0.5"
                        style={{ background: "linear-gradient(135deg, #4F46E5, #7C3AED)", color: "white", boxShadow: "0 4px 15px rgba(79,70,229,0.3)" }}>
                        <Users className="w-4 h-4" /> Load Demo (800 Students)
                      </button>
                    </div>
                    <p className="mt-4" style={{ color: MUTED, fontSize: "0.72rem" }}>
                      🔒 All student data is anonymised. No personal identifiers stored.
                    </p>
                  </>
                )}
              </motion.div>
            )}
          </AnimatePresence>

          {/* Dashboard Content */}
          {dataLoaded && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
              {/* Stat Cards */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                {classStats.map((stat, i) => (
                  <motion.div key={stat.label} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }}
                    className="rounded-xl p-4" style={{ backgroundColor: BG_CARD, border: `1px solid ${stat.color}20` }}>
                    <div className="flex items-center gap-2 mb-2">
                      <span>{stat.icon}</span>
                      <span style={{ color: MUTED, fontSize: "0.7rem" }}>{stat.label}</span>
                    </div>
                    <div style={{ fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.8rem", color: stat.color }}>{stat.value}</div>
                  </motion.div>
                ))}
              </div>

              {/* Charts Row */}
              <div className="grid md:grid-cols-2 gap-5 mb-6">
                {/* Stress by Grade */}
                <div className="rounded-xl p-5" style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}` }}>
                  <h3 className="mb-1" style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "0.95rem" }}>
                    Stress Levels by Grade
                  </h3>
                  <p className="text-xs mb-4" style={{ color: MUTED }}>% of students per risk level</p>
                  <div className="h-44">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={classStressData}>
                        <CartesianGrid stroke="rgba(255,255,255,0.04)" strokeDasharray="4 4" />
                        <XAxis dataKey="grade" tick={{ fill: MUTED, fontSize: 11 }} axisLine={false} tickLine={false} />
                        <YAxis tick={{ fill: MUTED, fontSize: 11 }} axisLine={false} tickLine={false} unit="%" />
                        <Tooltip content={<CustomTooltip />} />
                        <Bar dataKey="low" name="Low" stackId="a" fill="#10B981" radius={[0, 0, 0, 0]} />
                        <Bar dataKey="moderate" name="Moderate" stackId="a" fill="#F59E0B" />
                        <Bar dataKey="high" name="High" stackId="a" fill="#F43F5E" radius={[4, 4, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                {/* Learning Mode Pie */}
                <div className="rounded-xl p-5" style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}` }}>
                  <h3 className="mb-1" style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "0.95rem" }}>
                    Learning Mode Distribution
                  </h3>
                  <p className="text-xs mb-3" style={{ color: MUTED }}>Class breakdown by learning environment</p>
                  <div className="flex items-center gap-4">
                    <div className="h-44 flex-1">
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie data={learningModeData} cx="50%" cy="50%" innerRadius={45} outerRadius={72} dataKey="value" strokeWidth={0}>
                            {learningModeData.map((entry, i) => <Cell key={i} fill={entry.color} />)}
                          </Pie>
                          <Tooltip content={<CustomTooltip />} />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                    <div className="space-y-2">
                      {learningModeData.map(item => (
                        <div key={item.name} className="flex items-center gap-2">
                          <div className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: item.color }} />
                          <span style={{ color: MUTED, fontSize: "0.75rem" }}>{item.name}</span>
                          <span style={{ color: item.color, fontWeight: 700, fontSize: "0.8rem" }}>{item.value}%</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* Weekly Wellness Trend */}
              <div className="rounded-xl p-5 mb-6" style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}` }}>
                <h3 className="mb-1" style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "0.95rem" }}>
                  Class Wellness Trend — Last 6 Weeks
                </h3>
                <p className="text-xs mb-4" style={{ color: MUTED }}>Average wellness score vs. anxiety index</p>
                <div className="h-44">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={weeklyTrend}>
                      <CartesianGrid stroke="rgba(255,255,255,0.04)" strokeDasharray="4 4" />
                      <XAxis dataKey="week" tick={{ fill: MUTED, fontSize: 11 }} axisLine={false} tickLine={false} />
                      <YAxis tick={{ fill: MUTED, fontSize: 11 }} axisLine={false} tickLine={false} />
                      <Tooltip content={<CustomTooltip />} />
                      <Legend wrapperStyle={{ color: MUTED, fontSize: "11px" }} />
                      <Line type="monotone" dataKey="wellness" name="Wellness Score" stroke="#10B981" strokeWidth={2.5} dot={{ r: 3, fill: "#10B981" }} />
                      <Line type="monotone" dataKey="anxiety" name="Anxiety Index" stroke="#F43F5E" strokeWidth={2.5} dot={{ r: 3, fill: "#F43F5E" }} strokeDasharray="5 3" />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Student Table */}
              <div className="rounded-xl overflow-hidden" style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}` }}>
                <div className="px-5 py-4 flex items-center justify-between border-b flex-wrap gap-3" style={{ borderColor: BORDER }}>
                  <h3 style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "0.95rem" }}>
                    Individual Student Profiles
                  </h3>
                  <div className="flex gap-2">
                    {["All", "High", "Moderate", "Low"].map(f => (
                      <button key={f} onClick={() => setFilterRisk(f)}
                        className="px-3 py-1 rounded-lg text-xs font-medium transition-all"
                        style={{
                          backgroundColor: filterRisk === f ? INDIGO : "rgba(255,255,255,0.05)",
                          color: filterRisk === f ? "white" : MUTED,
                          border: filterRisk === f ? "none" : `1px solid ${BORDER}`,
                        }}>
                        {f}
                      </button>
                    ))}
                  </div>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr style={{ backgroundColor: "rgba(255,255,255,0.02)" }}>
                        {["Student", "Grade", "Mode", "Score", "Risk", "Concern", "Action"].map(h => (
                          <th key={h} className="px-4 py-3 text-left text-xs font-semibold" style={{ color: MUTED }}>{h}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {filtered.map((student, i) => (
                        <motion.tr key={student.id} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.05 }}
                          className="border-t hover:bg-white/5 transition-colors cursor-pointer"
                          style={{ borderColor: "rgba(255,255,255,0.04)" }}
                          onClick={() => setSelectedStudent(student === selectedStudent ? null : student)}>
                          <td className="px-4 py-3">
                            <div className="flex items-center gap-2">
                              <div className="w-7 h-7 rounded-full flex items-center justify-center text-xs"
                                style={{ background: "linear-gradient(135deg, #4F46E5, #7C3AED)", color: "white" }}>
                                {student.name[0]}
                              </div>
                              <div>
                                <p style={{ color: TEXT, fontSize: "0.8rem" }}>{student.name}</p>
                                <p style={{ color: MUTED, fontSize: "0.65rem" }}>{student.id}</p>
                              </div>
                            </div>
                          </td>
                          <td className="px-4 py-3 text-xs" style={{ color: MUTED }}>{student.grade}</td>
                          <td className="px-4 py-3">
                            <span className="px-2 py-0.5 rounded-full text-xs"
                              style={{ backgroundColor: "rgba(6,182,212,0.1)", color: CYAN }}>{student.mode}</span>
                          </td>
                          <td className="px-4 py-3">
                            <span style={{ color: student.color, fontWeight: 700, fontSize: "0.9rem", fontFamily: "Space Grotesk" }}>{student.score}</span>
                          </td>
                          <td className="px-4 py-3">
                            <span className="px-2 py-0.5 rounded-full text-xs font-semibold"
                              style={{ backgroundColor: `${student.color}12`, color: student.color }}>{student.risk}</span>
                          </td>
                          <td className="px-4 py-3 text-xs" style={{ color: MUTED }}>{student.concern}</td>
                          <td className="px-4 py-3">
                            <button className="p-1.5 rounded-lg transition-colors hover:bg-white/10"
                              style={{ color: MUTED }}>
                              <Eye className="w-3.5 h-3.5" />
                            </button>
                          </td>
                        </motion.tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                {selectedStudent && (
                  <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }}
                    className="border-t p-5" style={{ borderColor: `${selectedStudent.color}30`, backgroundColor: `${selectedStudent.color}06` }}>
                    <div className="flex items-start justify-between mb-3">
                      <h4 style={{ color: TEXT, fontWeight: 700 }}>🔍 {selectedStudent.name} — Detailed View</h4>
                      <span className="px-2 py-0.5 rounded-full text-xs font-bold"
                        style={{ backgroundColor: `${selectedStudent.color}15`, color: selectedStudent.color }}>
                        {selectedStudent.risk} Risk
                      </span>
                    </div>
                    <div className="grid md:grid-cols-3 gap-3">
                      {[
                        { label: "Wellness Score", value: `${selectedStudent.score}/100`, color: selectedStudent.color },
                        { label: "Learning Mode", value: selectedStudent.mode, color: CYAN },
                        { label: "Primary Concern", value: selectedStudent.concern, color: "#F59E0B" },
                      ].map(item => (
                        <div key={item.label} className="p-3 rounded-xl"
                          style={{ backgroundColor: "rgba(255,255,255,0.03)", border: `1px solid ${BORDER}` }}>
                          <p style={{ color: MUTED, fontSize: "0.68rem" }}>{item.label}</p>
                          <p style={{ color: item.color, fontWeight: 600, fontSize: "0.85rem" }}>{item.value}</p>
                        </div>
                      ))}
                    </div>
                    {selectedStudent.risk === "High" && (
                      <div className="mt-3 p-3 rounded-xl flex items-start gap-2"
                        style={{ backgroundColor: "rgba(244,63,94,0.08)", border: "1px solid rgba(244,63,94,0.2)" }}>
                        <AlertTriangle className="w-4 h-4 flex-shrink-0 mt-0.5" style={{ color: "#F43F5E" }} />
                        <p style={{ color: TEXT, fontSize: "0.78rem" }}>
                          <strong style={{ color: "#F43F5E" }}>Recommended Action:</strong> Schedule a private counselling session. Contact school counsellor or refer to iCall: 9152987821.
                        </p>
                      </div>
                    )}
                  </motion.div>
                )}
              </div>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}

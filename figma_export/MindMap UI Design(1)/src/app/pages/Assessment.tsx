import { useState } from "react";
import { useNavigate } from "react-router";
import { motion, AnimatePresence } from "motion/react";
import { ArrowLeft, ArrowRight, Check } from "lucide-react";
import { useApp } from "../context/AppContext";

const BG_CARD = "#1A1A2E";
const BORDER = "rgba(255,255,255,0.07)";
const TEXT = "#E2E8F0";
const MUTED = "#94A3B8";
const INDIGO = "#4F46E5";

const tabs = [
  { id: "about", label: "About You", labelMr: "तुमच्याबद्दल", labelHi: "आपके बारे में", emoji: "👤", color: INDIGO },
  { id: "study", label: "Study Habits", labelMr: "अभ्यास सवयी", labelHi: "अध्ययन आदतें", emoji: "📚", color: "#7C3AED" },
  { id: "daily", label: "Daily Life", labelMr: "दैनंदिन जीवन", labelHi: "दैनिक जीवन", emoji: "🌅", color: "#06B6D4" },
  { id: "activities", label: "Activities", labelMr: "उपक्रम", labelHi: "गतिविधियां", emoji: "🎯", color: "#10B981" },
  { id: "future", label: "Your Future", labelMr: "तुमचे भविष्य", labelHi: "आपका भविष्य", emoji: "🌟", color: "#F59E0B" },
];

type FormData = Record<string, any>;

export function Assessment() {
  const navigate = useNavigate();
  const { language } = useApp();
  const [activeTab, setActiveTab] = useState(0);
  const [form, setForm] = useState<FormData>({
    learningMode: "", grade: "", city: "Pune", internet: "",
    studyHours: 4, breakFreq: "", preferTime: "", resourceType: "",
    behindFeeling: "",
    sleepHours: 7, wakeTime: "", mealReg: "", physActivity: "", screenTime: 3,
    hobbies: [], socialAct: "", familyTime: "", creativeAct: "", sports: "",
    careerClarity: 5, familySupport: "", biggestConcern: "", stressCopier: "", goals: "",
  });

  function getTabLabel(tab: typeof tabs[0]) {
    if (language === "mr") return tab.labelMr;
    if (language === "hi") return tab.labelHi;
    return tab.label;
  }

  function update(key: string, value: any) {
    setForm(f => ({ ...f, [key]: value }));
  }

  const progress = ((activeTab + 1) / tabs.length) * 100;

  const inputStyle = {
    backgroundColor: "rgba(255,255,255,0.05)",
    border: `1px solid ${BORDER}`,
    borderRadius: "8px",
    color: TEXT,
    padding: "10px 12px",
    width: "100%",
    fontSize: "0.875rem",
    outline: "none",
  };

  const selectStyle = { ...inputStyle, cursor: "pointer" };

  function RadioGroup({ name, options, value, onChange }: { name: string; options: { value: string; label: string; emoji?: string }[]; value: string; onChange: (v: string) => void }) {
    return (
      <div className="flex flex-wrap gap-2">
        {options.map(opt => (
          <button key={opt.value} onClick={() => onChange(opt.value)}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-sm transition-all duration-200"
            style={{
              backgroundColor: value === opt.value ? `${INDIGO}20` : "rgba(255,255,255,0.04)",
              border: value === opt.value ? `1.5px solid ${INDIGO}` : `1px solid ${BORDER}`,
              color: value === opt.value ? "#A5B4FC" : MUTED,
            }}>
            {opt.emoji && <span>{opt.emoji}</span>}
            {opt.label}
          </button>
        ))}
      </div>
    );
  }

  function SliderField({ label, name, min, max, unit, value }: { label: string; name: string; min: number; max: number; unit: string; value: number }) {
    return (
      <div>
        <div className="flex justify-between items-center mb-2">
          <label style={{ color: TEXT, fontSize: "0.875rem", fontWeight: 500 }}>{label}</label>
          <span className="px-2 py-0.5 rounded-full text-xs font-bold"
            style={{ backgroundColor: `${INDIGO}20`, color: "#A5B4FC" }}>{value} {unit}</span>
        </div>
        <input type="range" min={min} max={max} value={value}
          onChange={e => update(name, parseInt(e.target.value))}
          className="w-full h-2 rounded-full appearance-none cursor-pointer"
          style={{ accentColor: INDIGO }} />
        <div className="flex justify-between mt-1" style={{ color: MUTED, fontSize: "0.7rem" }}>
          <span>{min} {unit}</span><span>{max} {unit}</span>
        </div>
      </div>
    );
  }

  function FieldLabel({ children }: { children: React.ReactNode }) {
    return <label className="block mb-2" style={{ color: TEXT, fontSize: "0.875rem", fontWeight: 500 }}>{children}</label>;
  }

  function FormField({ children }: { children: React.ReactNode }) {
    return <div className="space-y-2">{children}</div>;
  }

  const tabContent = {
    about: (
      <div className="space-y-5">
        <div className="grid md:grid-cols-2 gap-4">
          <FormField>
            <FieldLabel>What class/year are you in? 🎓</FieldLabel>
            <select style={selectStyle} value={form.grade} onChange={e => update("grade", e.target.value)}>
              <option value="">Select grade</option>
              {["Class 9", "Class 10", "Class 11", "Class 12", "FY College", "SY College", "TY College", "PG"].map(g => <option key={g}>{g}</option>)}
            </select>
          </FormField>
          <FormField>
            <FieldLabel>Your city 📍</FieldLabel>
            <select style={selectStyle} value={form.city} onChange={e => update("city", e.target.value)}>
              {["Pune", "Pimpri-Chinchwad", "Nashik", "Aurangabad", "Nagpur", "Mumbai", "Other"].map(c => <option key={c}>{c}</option>)}
            </select>
          </FormField>
        </div>
        <FormField>
          <FieldLabel>How are you currently learning? 💻</FieldLabel>
          <RadioGroup name="learningMode" value={form.learningMode} onChange={v => update("learningMode", v)}
            options={[
              { value: "online", label: "Fully Online", emoji: "💻" },
              { value: "offline", label: "Fully Offline", emoji: "🏫" },
              { value: "hybrid", label: "Hybrid Mix", emoji: "🔀" },
            ]} />
        </FormField>
        <FormField>
          <FieldLabel>How stable is your internet at home? 📶</FieldLabel>
          <RadioGroup name="internet" value={form.internet} onChange={v => update("internet", v)}
            options={[
              { value: "excellent", label: "Excellent" },
              { value: "good", label: "Good" },
              { value: "average", label: "Average" },
              { value: "poor", label: "Poor / Inconsistent" },
            ]} />
        </FormField>
        <div className="p-4 rounded-xl" style={{ backgroundColor: "rgba(79,70,229,0.07)", border: "1px solid rgba(79,70,229,0.15)" }}>
          <p className="text-xs leading-relaxed" style={{ color: "#A5B4FC" }}>
            🔒 <strong>Privacy note:</strong> You don't need to share your name or personal details. All responses are anonymous and used only for mental wellness analysis.
          </p>
        </div>
      </div>
    ),
    study: (
      <div className="space-y-5">
        <SliderField label="How many hours do you study on a typical day?" name="studyHours" min={0} max={14} unit="hrs" value={form.studyHours} />
        <FormField>
          <FieldLabel>How often do you take proper breaks while studying? ☕</FieldLabel>
          <RadioGroup name="breakFreq" value={form.breakFreq} onChange={v => update("breakFreq", v)}
            options={[
              { value: "never", label: "Never", emoji: "😰" },
              { value: "rarely", label: "Rarely" },
              { value: "sometimes", label: "Sometimes", emoji: "🙂" },
              { value: "regularly", label: "Regularly", emoji: "😊" },
            ]} />
        </FormField>
        <FormField>
          <FieldLabel>When do you study best? ⏰</FieldLabel>
          <RadioGroup name="preferTime" value={form.preferTime} onChange={v => update("preferTime", v)}
            options={[
              { value: "morning", label: "Early Morning", emoji: "🌅" },
              { value: "afternoon", label: "Afternoon" },
              { value: "evening", label: "Evening", emoji: "🌆" },
              { value: "night", label: "Late Night", emoji: "🌙" },
            ]} />
        </FormField>
        <FormField>
          <FieldLabel>What resources do you rely on more? 📖</FieldLabel>
          <RadioGroup name="resourceType" value={form.resourceType} onChange={v => update("resourceType", v)}
            options={[
              { value: "textbook", label: "Textbooks / Notes", emoji: "📚" },
              { value: "youtube", label: "YouTube / Videos", emoji: "▶️" },
              { value: "both", label: "Both equally" },
              { value: "coaching", label: "Coaching classes" },
            ]} />
        </FormField>
        <FormField>
          <FieldLabel>How often do you feel behind in your studies? 😟</FieldLabel>
          <RadioGroup name="behindFeeling" value={form.behindFeeling} onChange={v => update("behindFeeling", v)}
            options={[
              { value: "always", label: "Always", emoji: "😰" },
              { value: "often", label: "Often" },
              { value: "sometimes", label: "Sometimes" },
              { value: "rarely", label: "Rarely", emoji: "😊" },
            ]} />
        </FormField>
      </div>
    ),
    daily: (
      <div className="space-y-5">
        <SliderField label="How many hours of sleep do you get on average? 😴" name="sleepHours" min={2} max={12} unit="hrs" value={form.sleepHours} />
        <FormField>
          <FieldLabel>What time do you usually wake up? ⏰</FieldLabel>
          <RadioGroup name="wakeTime" value={form.wakeTime} onChange={v => update("wakeTime", v)}
            options={[
              { value: "before6", label: "Before 6 AM", emoji: "🌄" },
              { value: "6to8", label: "6–8 AM" },
              { value: "8to10", label: "8–10 AM" },
              { value: "after10", label: "After 10 AM", emoji: "😴" },
            ]} />
        </FormField>
        <FormField>
          <FieldLabel>How regular are your meals? 🍱</FieldLabel>
          <RadioGroup name="mealReg" value={form.mealReg} onChange={v => update("mealReg", v)}
            options={[
              { value: "always", label: "Always on time", emoji: "✅" },
              { value: "mostly", label: "Mostly regular" },
              { value: "skip", label: "Skip meals often", emoji: "⚠️" },
              { value: "irregular", label: "Very irregular" },
            ]} />
        </FormField>
        <FormField>
          <FieldLabel>How physically active are you? 🏃</FieldLabel>
          <RadioGroup name="physActivity" value={form.physActivity} onChange={v => update("physActivity", v)}
            options={[
              { value: "daily", label: "Daily exercise", emoji: "💪" },
              { value: "few", label: "Few times/week" },
              { value: "occasionally", label: "Occasionally" },
              { value: "sedentary", label: "Mostly sitting", emoji: "🪑" },
            ]} />
        </FormField>
        <SliderField label="Non-study screen time per day (social media, entertainment) 📱" name="screenTime" min={0} max={12} unit="hrs" value={form.screenTime} />
      </div>
    ),
    activities: (
      <div className="space-y-5">
        <FormField>
          <FieldLabel>Which hobbies do you actively pursue? 🎨</FieldLabel>
          <div className="flex flex-wrap gap-2">
            {["Reading 📚", "Music 🎵", "Drawing/Art 🎨", "Gaming 🎮", "Cooking 🍳", "Writing ✍️", "Photography 📸", "Dancing 💃", "None"].map(h => {
              const isSelected = form.hobbies.includes(h);
              return (
                <button key={h} onClick={() => {
                  const next = isSelected ? form.hobbies.filter((x: string) => x !== h) : [...form.hobbies, h];
                  update("hobbies", next);
                }}
                  className="px-3 py-1.5 rounded-xl text-xs transition-all"
                  style={{
                    backgroundColor: isSelected ? "rgba(16,185,129,0.15)" : "rgba(255,255,255,0.04)",
                    border: isSelected ? "1.5px solid #10B981" : `1px solid ${BORDER}`,
                    color: isSelected ? "#10B981" : MUTED,
                  }}>{h}</button>
              );
            })}
          </div>
        </FormField>
        <FormField>
          <FieldLabel>How often do you hang out with friends in person? 🤝</FieldLabel>
          <RadioGroup name="socialAct" value={form.socialAct} onChange={v => update("socialAct", v)}
            options={[
              { value: "daily", label: "Almost daily", emoji: "🤩" },
              { value: "weekly", label: "Weekly" },
              { value: "rarely", label: "Rarely", emoji: "😔" },
              { value: "never", label: "Almost never", emoji: "😟" },
            ]} />
        </FormField>
        <FormField>
          <FieldLabel>How much quality time do you spend with family? 👨‍👩‍👧</FieldLabel>
          <RadioGroup name="familyTime" value={form.familyTime} onChange={v => update("familyTime", v)}
            options={[
              { value: "lot", label: "A lot", emoji: "❤️" },
              { value: "some", label: "Decent amount" },
              { value: "little", label: "Very little" },
              { value: "none", label: "Barely at all", emoji: "😔" },
            ]} />
        </FormField>
        <FormField>
          <FieldLabel>Do you participate in sports or outdoor games? 🏏</FieldLabel>
          <RadioGroup name="sports" value={form.sports} onChange={v => update("sports", v)}
            options={[
              { value: "daily", label: "Daily", emoji: "🏆" },
              { value: "weekly", label: "Weekly" },
              { value: "rarely", label: "Rarely" },
              { value: "never", label: "Never", emoji: "❌" },
            ]} />
        </FormField>
      </div>
    ),
    future: (
      <div className="space-y-5">
        <div>
          <div className="flex justify-between items-center mb-2">
            <label style={{ color: TEXT, fontSize: "0.875rem", fontWeight: 500 }}>
              How clear are you about your career path? 🎯
            </label>
            <span className="px-2 py-0.5 rounded-full text-xs font-bold"
              style={{ backgroundColor: "rgba(245,158,11,0.15)", color: "#F59E0B" }}>
              {form.careerClarity}/10
            </span>
          </div>
          <input type="range" min={1} max={10} value={form.careerClarity}
            onChange={e => update("careerClarity", parseInt(e.target.value))}
            className="w-full h-2 rounded-full appearance-none cursor-pointer"
            style={{ accentColor: "#F59E0B" }} />
          <div className="flex justify-between mt-1" style={{ color: MUTED, fontSize: "0.7rem" }}>
            <span>😕 Very Confused</span><span>😊 Very Clear</span>
          </div>
        </div>
        <FormField>
          <FieldLabel>How supportive is your family about your career choices? 💝</FieldLabel>
          <RadioGroup name="familySupport" value={form.familySupport} onChange={v => update("familySupport", v)}
            options={[
              { value: "very", label: "Very supportive", emoji: "❤️" },
              { value: "mostly", label: "Mostly supportive" },
              { value: "neutral", label: "Neutral" },
              { value: "pressure", label: "They pressure me", emoji: "😰" },
            ]} />
        </FormField>
        <FormField>
          <FieldLabel>What's your biggest concern right now? 💭</FieldLabel>
          <RadioGroup name="biggestConcern" value={form.biggestConcern} onChange={v => update("biggestConcern", v)}
            options={[
              { value: "exams", label: "Upcoming exams", emoji: "📝" },
              { value: "career", label: "Career path", emoji: "🎯" },
              { value: "relationships", label: "Relationships" },
              { value: "finances", label: "Family finances", emoji: "💰" },
              { value: "health", label: "Health", emoji: "❤️" },
              { value: "nothing", label: "Nothing major", emoji: "😊" },
            ]} />
        </FormField>
        <FormField>
          <FieldLabel>When you feel stressed, what helps you feel better? 🌿</FieldLabel>
          <RadioGroup name="stressCopier" value={form.stressCopier} onChange={v => update("stressCopier", v)}
            options={[
              { value: "talk", label: "Talking to someone", emoji: "💬" },
              { value: "music", label: "Music / Entertainment", emoji: "🎵" },
              { value: "exercise", label: "Exercise", emoji: "🏃" },
              { value: "sleep", label: "Sleep", emoji: "😴" },
              { value: "nothing", label: "Nothing helps", emoji: "😔" },
            ]} />
        </FormField>
        <FormField>
          <FieldLabel>What's one goal you want to achieve this year? ✨ (Optional)</FieldLabel>
          <input type="text" placeholder="e.g., Score 85%+ in boards, learn guitar, improve fitness..."
            value={form.goals} onChange={e => update("goals", e.target.value)}
            style={{ ...inputStyle }} />
        </FormField>
      </div>
    ),
  };

  return (
    <div style={{ backgroundColor: "#0F0F1A", minHeight: "100%" }}>
      <div className="px-6 lg:px-12 py-8">
        <div className="max-w-2xl mx-auto">
          {/* Header */}
          <div className="mb-6">
            <h1 className="mb-1" style={{ color: TEXT, fontFamily: "Space Grotesk", fontSize: "1.5rem", fontWeight: 700 }}>
              📝 Student Assessment
            </h1>
            <p style={{ color: MUTED, fontSize: "0.85rem" }}>
              Answer naturally — no right or wrong answers. This helps us understand your lifestyle.
            </p>
          </div>

          {/* Progress */}
          <div className="mb-6">
            <div className="flex justify-between items-center mb-2">
              <span style={{ color: MUTED, fontSize: "0.78rem" }}>Step {activeTab + 1} of {tabs.length}</span>
              <span style={{ color: "#A5B4FC", fontSize: "0.78rem", fontWeight: 600 }}>{Math.round(progress)}% Complete</span>
            </div>
            <div className="h-1.5 rounded-full overflow-hidden" style={{ backgroundColor: "rgba(255,255,255,0.07)" }}>
              <motion.div className="h-full rounded-full"
                style={{ background: "linear-gradient(90deg, #4F46E5, #06B6D4)" }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.5 }} />
            </div>
          </div>

          {/* Tab Bar */}
          <div className="flex gap-1.5 mb-6 overflow-x-auto pb-1" style={{ scrollbarWidth: "none" }}>
            {tabs.map((tab, i) => (
              <button key={tab.id} onClick={() => setActiveTab(i)}
                className="flex items-center gap-1.5 px-3 py-2 flex-shrink-0 transition-all duration-200"
                style={{
                  borderRadius: "8px 8px 0 0",
                  backgroundColor: activeTab === i ? BG_CARD : "rgba(255,255,255,0.03)",
                  border: activeTab === i ? `1px solid ${tab.color}40` : `1px solid transparent`,
                  borderBottom: activeTab === i ? `2px solid ${tab.color}` : "1px solid transparent",
                  color: activeTab === i ? tab.color : MUTED,
                }}>
                {i < activeTab ? (
                  <span className="w-4 h-4 rounded-full flex items-center justify-center"
                    style={{ backgroundColor: "#10B981", fontSize: "0.6rem" }}>
                    <Check className="w-2.5 h-2.5 text-white" />
                  </span>
                ) : <span style={{ fontSize: "0.9rem" }}>{tab.emoji}</span>}
                <span style={{ fontSize: "0.72rem", fontWeight: 500 }}>{getTabLabel(tab)}</span>
              </button>
            ))}
          </div>

          {/* Form Card */}
          <AnimatePresence mode="wait">
            <motion.div key={activeTab}
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -30 }}
              transition={{ duration: 0.3 }}
              className="rounded-xl p-6 mb-5"
              style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}`, boxShadow: "0 8px 24px rgba(79,70,229,0.08)" }}>
              <div className="flex items-center gap-2 mb-5">
                <span className="text-xl">{tabs[activeTab].emoji}</span>
                <h2 style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.05rem" }}>
                  {getTabLabel(tabs[activeTab])}
                </h2>
              </div>
              {tabContent[tabs[activeTab].id as keyof typeof tabContent]}
            </motion.div>
          </AnimatePresence>

          {/* Navigation */}
          <div className="flex gap-3">
            <button onClick={() => setActiveTab(Math.max(0, activeTab - 1))} disabled={activeTab === 0}
              className="flex items-center gap-2 px-5 py-3 rounded-xl text-sm font-medium transition-all"
              style={{
                backgroundColor: activeTab === 0 ? "rgba(255,255,255,0.02)" : "rgba(255,255,255,0.06)",
                border: `1px solid ${BORDER}`,
                color: activeTab === 0 ? "rgba(255,255,255,0.2)" : TEXT,
                cursor: activeTab === 0 ? "not-allowed" : "pointer",
              }}>
              <ArrowLeft className="w-4 h-4" /> Back
            </button>
            <button
              onClick={() => activeTab < tabs.length - 1 ? setActiveTab(activeTab + 1) : navigate("/results")}
              className="flex-1 flex items-center justify-center gap-2 px-5 py-3 rounded-xl text-sm font-semibold transition-all hover:-translate-y-0.5"
              style={{
                background: "linear-gradient(135deg, #4F46E5, #7C3AED)",
                color: "white",
                boxShadow: "0 4px 15px rgba(79,70,229,0.3)",
              }}>
              {activeTab < tabs.length - 1 ? (
                <><span>Next: {getTabLabel(tabs[activeTab + 1])}</span><ArrowRight className="w-4 h-4" /></>
              ) : (
                <><span>Submit & See Results 🎉</span><ArrowRight className="w-4 h-4" /></>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

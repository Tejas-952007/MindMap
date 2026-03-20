import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Send, Bot, User, ChevronDown, ChevronUp } from "lucide-react";

const BG_CARD = "#1A1A2E";
const BORDER = "rgba(255,255,255,0.07)";
const TEXT = "#E2E8F0";
const MUTED = "#94A3B8";
const INDIGO = "#4F46E5";
const VIOLET = "#7C3AED";

type Message = { role: "user" | "bot"; text: string; time: string };

const initialMessages: Message[] = [
  {
    role: "bot",
    text: "Namaste! 🙏 I'm the MindMap Parent AI Advisor. I can help you understand your child's mental health report, explain warning signs, and guide conversations. What would you like to know?",
    time: "10:00 AM",
  },
];

const quickReplies = [
  "What does the Moderate Risk score mean?",
  "How do I talk to my child about stress?",
  "My child refuses to go to school — what should I do?",
  "Is online learning bad for mental health?",
  "How can I reduce exam pressure at home?",
];

const botResponses: Record<string, string> = {
  "What does the Moderate Risk score mean?": "A Moderate Risk score (like your child's 74/100) means they're managing reasonably well but showing some vulnerability areas. It's like a yellow signal — not an emergency, but worth your attention. The key areas to focus on are academic pressure and sleep quality. This doesn't mean anything is 'wrong' with your child — it simply means they could benefit from some targeted support.",
  "How do I talk to my child about stress?": "Great question! Instead of asking 'Are you stressed?', try indirect approaches:\n\n• 'What was the best part of your day?'\n• 'Is there anything I can help make easier for you?'\n• 'I noticed you seem a bit tired lately — how can I support you?'\n\nThe key is listening without immediately trying to fix things. Validation before advice. Say 'I understand why you feel that way' before offering solutions.",
  "My child refuses to go to school — what should I do?": "School refusal in Indian students is often linked to exam anxiety, peer conflict, or academic shame. Do NOT force them — this worsens anxiety. Instead:\n\n1. Stay calm and curious (not angry)\n2. Ask 'What's making school feel hard right now?'\n3. Contact the school counsellor first\n4. Rule out bullying\n5. If persistent (3+ days), consult a child psychologist\n\nIn Pune, you can reach Childline: 1098 for immediate guidance.",
  "Is online learning bad for mental health?": "Research from Pune schools shows online learners score 11 points lower on mental wellness on average. The main issues are: social isolation (↓43% peer interaction), screen fatigue, blurred study-home boundaries, and reduced physical activity. However, some students — especially introverts or those with social anxiety — actually do better online. It's about finding the right balance and structure at home.",
  "How can I reduce exam pressure at home?": "Board exam pressure is one of the top mental health triggers in Indian homes. Here's what research shows actually helps:\n\n✅ Focus on effort over grades ('I'm proud you worked hard' not 'Get 90%+')\n✅ Maintain normal meal and sleep schedules\n✅ Allow 1 hour of completely free time daily\n✅ Avoid comparing to siblings or neighbours' children\n✅ Discuss career options beyond JEE/NEET — there are 200+ fulfilling paths\n\nRigid pressure increases cortisol, which actually reduces memory and performance.",
};

function getResponse(msg: string): string {
  for (const key of Object.keys(botResponses)) {
    if (msg.toLowerCase().includes(key.toLowerCase().slice(0, 20))) return botResponses[key];
  }
  return "That's an important concern. Based on MindMap data from 800+ Pune students, parent involvement is the #1 protective factor for student mental health. I'd recommend:\n\n1. Schedule a weekly 15-minute 'check-in' with your child\n2. Keep these conversations judgment-free\n3. If you're concerned about serious issues, contact iCall helpline: 9152987821\n\nWould you like specific advice for any particular situation?";
}

const faqCards = [
  {
    q: "My child studies 10+ hours but still fails — is this a mental health issue?",
    a: "Often yes. Excessive studying without results can indicate anxiety-driven studying (reading without retention), depression affecting memory, or undiagnosed learning differences like dyslexia. Quality > Quantity. Try structured study with breaks (Pomodoro method) and consult the school counsellor.",
    color: "#F43F5E",
    emoji: "📚",
  },
  {
    q: "My daughter is always on her phone — how worried should I be?",
    a: "Healthy screen time for teens is 2-3 hrs/day (non-study). Red flags: using phone at 2-3 AM, crying/anger when phone removed, neglecting all offline activities. Use family screen time agreements, not confiscation. Check if she's using it for social connection (good) or escapism from anxiety (needs attention).",
    color: "#F59E0B",
    emoji: "📱",
  },
  {
    q: "My son cries before school every morning — is this normal?",
    a: "Occasional crying (especially near exams) is normal. Daily crying is not and needs attention. Possible causes: separation anxiety, bullying, academic shame, social anxiety, or depression. Start by talking openly, then contact school authorities, then consult a child psychologist if it persists 2+ weeks.",
    color: "#06B6D4",
    emoji: "😢",
  },
  {
    q: "How do I know if my child needs professional help?",
    a: "Seek professional help if you notice: changes lasting 2+ weeks, sleep or eating disruption, withdrawal from friends/family, talk of hopelessness, or academic performance decline. In Pune, visit NIMHANS-affiliated clinics or call Vandrevala Foundation: 1860-2662-345 (24/7 free helpline in Hindi/English).",
    color: "#10B981",
    emoji: "🏥",
  },
];

const conversationGuide = [
  {
    situation: "Child says 'I hate school'",
    wrong: "Don't say: 'You have to go, stop being dramatic'",
    right: "Try: 'What's happening at school that makes you feel that way?'",
    color: "#F43F5E",
  },
  {
    situation: "Child gets poor exam results",
    wrong: "Don't say: 'Your cousin scored 95% — why can't you?'",
    right: "Try: 'I know you worked hard. Let's figure out what to focus on next time together.'",
    color: "#F59E0B",
  },
  {
    situation: "Child seems withdrawn and sad",
    wrong: "Don't say: 'Stop being sad, you have nothing to worry about'",
    right: "Try: 'I've noticed you seem a little quiet. I'm here whenever you want to talk.'",
    color: "#06B6D4",
  },
  {
    situation: "Child says 'I can't do this anymore'",
    wrong: "Don't say: 'You're being dramatic'",
    right: "Try: 'That sounds really hard. Tell me everything — I'm listening.' Then get professional support.",
    color: "#10B981",
  },
];

export function ParentsGuidance() {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [openFaq, setOpenFaq] = useState<number | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  function sendMessage(text?: string) {
    const msg = text || input.trim();
    if (!msg) return;
    const now = new Date().toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit" });
    setMessages(m => [...m, { role: "user", text: msg, time: now }]);
    setInput("");
    setIsTyping(true);
    setTimeout(() => {
      setIsTyping(false);
      setMessages(m => [...m, { role: "bot", text: getResponse(msg), time: new Date().toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit" }) }]);
    }, 1500 + Math.random() * 800);
  }

  return (
    <div style={{ backgroundColor: "#0F0F1A", minHeight: "100%" }}>
      <div className="px-6 lg:px-12 py-8">
        <div className="max-w-3xl mx-auto">
          {/* Header */}
          <div className="mb-6">
            <h1 style={{ color: TEXT, fontFamily: "Space Grotesk", fontSize: "1.5rem", fontWeight: 700 }}>
              👨‍👩‍👧 Parent Guide & AI Advisor
            </h1>
            <p style={{ color: MUTED, fontSize: "0.85rem" }}>AI-powered guidance for Indian parents to support their child's mental health journey</p>
          </div>

          {/* Chatbot */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
            className="rounded-2xl overflow-hidden mb-6"
            style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}`, boxShadow: "0 8px 24px rgba(79,70,229,0.1)" }}>
            {/* Chat Header */}
            <div className="px-5 py-3 flex items-center gap-3 border-b"
              style={{ background: "linear-gradient(135deg, rgba(79,70,229,0.15), rgba(124,58,237,0.1))", borderColor: "rgba(79,70,229,0.2)" }}>
              <div className="w-9 h-9 rounded-xl flex items-center justify-center"
                style={{ background: "linear-gradient(135deg, #4F46E5, #7C3AED)" }}>
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div>
                <p style={{ color: TEXT, fontWeight: 600, fontSize: "0.88rem" }}>MindMap Parent AI Advisor</p>
                <p style={{ color: "#10B981", fontSize: "0.68rem" }}>● Online • Trained on 800+ Pune student profiles</p>
              </div>
            </div>

            {/* Messages */}
            <div className="p-4 space-y-3 overflow-y-auto" style={{ maxHeight: "340px" }}>
              {messages.map((msg, i) => (
                <motion.div key={i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                  className={`flex gap-2.5 ${msg.role === "user" ? "flex-row-reverse" : "flex-row"}`}>
                  <div className={`w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0 text-xs`}
                    style={{ background: msg.role === "bot" ? "linear-gradient(135deg, #4F46E5, #7C3AED)" : "rgba(255,255,255,0.1)" }}>
                    {msg.role === "bot" ? <Bot className="w-4 h-4 text-white" /> : <User className="w-4 h-4" style={{ color: TEXT }} />}
                  </div>
                  <div className={`max-w-[75%]`}>
                    <div className="px-4 py-3 rounded-2xl text-xs leading-relaxed whitespace-pre-line"
                      style={{
                        backgroundColor: msg.role === "bot" ? "rgba(79,70,229,0.12)" : "rgba(255,255,255,0.07)",
                        border: msg.role === "bot" ? "1px solid rgba(79,70,229,0.2)" : `1px solid ${BORDER}`,
                        color: TEXT,
                        borderRadius: msg.role === "bot" ? "4px 16px 16px 16px" : "16px 4px 16px 16px",
                      }}>
                      {msg.text}
                    </div>
                    <p style={{ color: MUTED, fontSize: "0.6rem", marginTop: 3, textAlign: msg.role === "user" ? "right" : "left" }}>{msg.time}</p>
                  </div>
                </motion.div>
              ))}
              {isTyping && (
                <div className="flex gap-2.5">
                  <div className="w-7 h-7 rounded-full flex items-center justify-center" style={{ background: "linear-gradient(135deg, #4F46E5, #7C3AED)" }}>
                    <Bot className="w-4 h-4 text-white" />
                  </div>
                  <div className="px-4 py-3 rounded-2xl flex items-center gap-1"
                    style={{ backgroundColor: "rgba(79,70,229,0.12)", border: "1px solid rgba(79,70,229,0.2)" }}>
                    {[0, 1, 2].map(i => (
                      <motion.div key={i} className="w-1.5 h-1.5 rounded-full"
                        style={{ backgroundColor: "#A5B4FC" }}
                        animate={{ opacity: [0.3, 1, 0.3], scale: [0.8, 1.2, 0.8] }}
                        transition={{ duration: 1, repeat: Infinity, delay: i * 0.2 }} />
                    ))}
                  </div>
                </div>
              )}
              <div ref={bottomRef} />
            </div>

            {/* Quick Replies */}
            <div className="px-4 py-2 border-t border-b overflow-x-auto flex gap-2" style={{ borderColor: BORDER, scrollbarWidth: "none" }}>
              {quickReplies.map(reply => (
                <button key={reply} onClick={() => sendMessage(reply)}
                  className="flex-shrink-0 px-3 py-1.5 rounded-full text-xs transition-all hover:opacity-80 whitespace-nowrap"
                  style={{ backgroundColor: "rgba(79,70,229,0.1)", border: "1px solid rgba(79,70,229,0.2)", color: "#A5B4FC" }}>
                  {reply}
                </button>
              ))}
            </div>

            {/* Input */}
            <div className="p-4 flex gap-2">
              <input
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === "Enter" && sendMessage()}
                placeholder="Ask about your child's report, warning signs, or how to help..."
                className="flex-1 px-4 py-2.5 rounded-xl text-sm outline-none transition-all"
                style={{
                  backgroundColor: "rgba(255,255,255,0.05)",
                  border: `1px solid ${BORDER}`,
                  color: TEXT,
                  fontSize: "0.82rem",
                }}
              />
              <button onClick={() => sendMessage()}
                className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 transition-all hover:-translate-y-0.5"
                style={{ background: "linear-gradient(135deg, #4F46E5, #7C3AED)", boxShadow: "0 4px 15px rgba(79,70,229,0.3)" }}>
                <Send className="w-4 h-4 text-white" />
              </button>
            </div>
          </motion.div>

          {/* Conversation Guide */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
            className="rounded-xl p-5 mb-6" style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}` }}>
            <h2 className="mb-1" style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.05rem" }}>
              💬 Situation-by-Situation Conversation Guide
            </h2>
            <p className="text-xs mb-4" style={{ color: MUTED }}>What to say (and not say) in challenging moments</p>
            <div className="space-y-3">
              {conversationGuide.map((item) => (
                <div key={item.situation} className="rounded-xl overflow-hidden"
                  style={{ border: `1px solid ${item.color}20` }}>
                  <div className="px-4 py-2.5"
                    style={{ backgroundColor: `${item.color}10` }}>
                    <p style={{ color: item.color, fontWeight: 600, fontSize: "0.82rem" }}>🎭 {item.situation}</p>
                  </div>
                  <div className="grid md:grid-cols-2 divide-y md:divide-y-0 md:divide-x" style={{ divideColor: BORDER }}>
                    <div className="px-4 py-3">
                      <p style={{ color: "#F43F5E", fontSize: "0.7rem", fontWeight: 600, marginBottom: 4 }}>❌ AVOID</p>
                      <p style={{ color: MUTED, fontSize: "0.78rem", lineHeight: 1.5 }}>{item.wrong}</p>
                    </div>
                    <div className="px-4 py-3">
                      <p style={{ color: "#10B981", fontSize: "0.7rem", fontWeight: 600, marginBottom: 4 }}>✅ TRY THIS</p>
                      <p style={{ color: TEXT, fontSize: "0.78rem", lineHeight: 1.5 }}>{item.right}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* FAQ Cards */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }}>
            <h2 className="mb-4" style={{ color: TEXT, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "1.05rem" }}>
              ❓ Frequently Asked Questions
            </h2>
            <div className="space-y-3">
              {faqCards.map((faq, i) => (
                <div key={i} className="rounded-xl overflow-hidden"
                  style={{ backgroundColor: BG_CARD, border: `1px solid ${faq.color}20` }}>
                  <button onClick={() => setOpenFaq(openFaq === i ? null : i)}
                    className="w-full flex items-center justify-between gap-3 px-5 py-4 text-left"
                    style={{ color: TEXT }}>
                    <div className="flex items-center gap-3">
                      <span className="text-xl flex-shrink-0">{faq.emoji}</span>
                      <span style={{ fontSize: "0.82rem", fontWeight: 500 }}>{faq.q}</span>
                    </div>
                    {openFaq === i
                      ? <ChevronUp className="w-4 h-4 flex-shrink-0" style={{ color: faq.color }} />
                      : <ChevronDown className="w-4 h-4 flex-shrink-0" style={{ color: MUTED }} />}
                  </button>
                  <AnimatePresence>
                    {openFaq === i && (
                      <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }} exit={{ height: 0, opacity: 0 }}
                        className="overflow-hidden">
                        <div className="px-5 pb-4 pt-1 border-t" style={{ borderColor: BORDER }}>
                          <p style={{ color: MUTED, fontSize: "0.8rem", lineHeight: 1.6 }}>{faq.a}</p>
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Emergency contacts */}
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }}
            className="mt-6 rounded-xl p-5"
            style={{ backgroundColor: "rgba(244,63,94,0.06)", border: "1px solid rgba(244,63,94,0.2)" }}>
            <h3 className="mb-3" style={{ color: "#F43F5E", fontFamily: "Space Grotesk", fontWeight: 700, fontSize: "0.95rem" }}>
              🆘 Crisis Helplines — Pune / Maharashtra
            </h3>
            <div className="grid md:grid-cols-2 gap-3">
              {[
                { name: "iCall (TISS)", number: "9152987821", hours: "Mon–Sat 8 AM–10 PM" },
                { name: "Vandrevala Foundation", number: "1860-2662-345", hours: "24/7" },
                { name: "NIMHANS Helpline", number: "080-46110007", hours: "Mon–Sat 9 AM–5 PM" },
                { name: "Childline India", number: "1098", hours: "24/7" },
              ].map(h => (
                <div key={h.name} className="flex items-center gap-3 p-3 rounded-xl"
                  style={{ backgroundColor: "rgba(244,63,94,0.05)", border: "1px solid rgba(244,63,94,0.1)" }}>
                  <span className="text-lg">📞</span>
                  <div>
                    <p style={{ color: TEXT, fontSize: "0.8rem", fontWeight: 600 }}>{h.name}</p>
                    <p style={{ color: "#F43F5E", fontSize: "0.78rem", fontWeight: 700 }}>{h.number}</p>
                    <p style={{ color: MUTED, fontSize: "0.68rem" }}>{h.hours}</p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}

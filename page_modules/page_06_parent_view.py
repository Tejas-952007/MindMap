"""Page 6 – Parent Guide: AI-powered parent advisor chatbot"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.translations import t
from utils.ai_parent_advisor import get_ai_response, has_api_key, CHAT_UI



# ── Scenario-based conversation guide ────────────────────────
SCENARIOS = [
    {
        "trigger": "Mulane sanga ki mala abhyas nahi karanyachi icha nahi / My child says they don't feel like studying",
        "trigger_en": "Child says: 'I don't feel like studying at all'",
        "dont": "DON'T say: 'Tumhi lazy ahat. Baghaat tya mulala, kiti dhilai nahi.' (Don't call them lazy or compare)",
        "do_say": "SAY THIS: 'Okay, mala sangshil ka ka? Abhyas chodun baaher jaauya 10 minutes – bhari aahe.' (Acknowledge, then gently redirect with movement)",
        "why": "Why it works: Students lose motivation when stressed. Forcing creates resistance. A 10-minute break + empathy often resets them faster than pressure.",
        "next_step": "After the break, ask: 'Konti ek gosht aaj karu shaktos? Ekach.' (Which ONE thing can you do today?) — Small wins rebuild momentum.",
        "icon": "😓"
    },
    {
        "trigger": "Mulane marks kami aalet / Child got lower marks than expected",
        "trigger_en": "Child brings home lower grades",
        "dont": "DON'T say: 'Itke kami marks? Kayach zale tumha? Navya varshi la kahi change dzalna hoga.' (Don't shame about marks)",
        "do_say": "SAY THIS: 'Marks baghtoy mi. Tuzya effort la mhanto I respect karto. Aata saang – ksha vishayat help laagel?' (Respect effort, ask for help areas)",
        "why": "Why it works: Shame triggers cortisol (stress hormone) which blocks learning. Curiosity triggers dopamine which opens learning pathways.",
        "next_step": "Together, identify ONE subject to focus on. Offer to arrange a tutor or peer study group for just that subject.",
        "icon": "📋"
    },
    {
        "trigger": "Mul raat uthun abhyas karta / Child studies till late night",
        "trigger_en": "Child is studying until 1–2 AM regularly",
        "dont": "DON'T say: 'Chhan ahe! Mehnat karto!' (Don't praise sleep deprivation as dedication)",
        "do_say": "SAY THIS: 'Arya, tuzya dedication la salute. Pan research sangato ki 7 taas zop nahi milali tar memory consolidation nahi hote. Aaj 11:30 la zhop – udhya sharp rahashil.' (Educate about sleep science)",
        "why": "Why it works: Sleep deprivation reduces learning efficiency by 40%. Students who sleep 7+ hours retain 60% more than those who don't.",
        "next_step": "Set a family 'lights out rule' at 11 PM for everyone — modeling behaviour is more effective than instructions.",
        "icon": "🌙"
    },
    {
        "trigger": "Mul swatahch room madhun baher yet nahi / Child doesn't come out of their room",
        "trigger_en": "Child is isolated in their room for days",
        "dont": "DON'T: Knock frequently asking about studies. Don't take it personally as rejection.",
        "do_say": "SAY THIS: Simply knock once and say: 'Chai banvliy. Yenar ka 5 minutes?' (No study talk — just connection). If no: slip a note under the door: 'Tu theek aahes? Kami bol nako. Tuzya baajune ahe mi.'",
        "why": "Why it works: Social withdrawal is a stress response. Forced interaction increases anxiety. Low-pressure invitations rebuild the bridge.",
        "next_step": "Suggest a family walk or drive without any agenda. Movement + fresh air naturally reduces isolation. No study talk during this time.",
        "icon": "🚪"
    },
    {
        "trigger": "Mul nonstop phone vapartat / Child is on phone all day",
        "trigger_en": "Child seems addicted to phone, studying decreasing",
        "dont": "DON'T: Snatch the phone or set harsh rules suddenly. This creates conflict and drives secret use.",
        "do_say": "SAY THIS: 'Mala tech samajta nahi jarasa. Mala dakhavashil ka tu kaye baghatos itke? Genuinely curious ahe mi.' (Show curiosity instead of criticism)",
        "why": "Why it works: Phone overuse is often dopamine-seeking behaviour caused by stress avoidance. Understanding what they watch/play reveals what they're escaping from.",
        "next_step": "Together create a 'phone parking station' — phones charge in the living room after 10 PM. Frame it as a family rule, not a punishment targeting only them.",
        "icon": "📱"
    },
    {
        "trigger": "Mul saglyanna irritating watat / Child is irritable and snapping at everyone",
        "trigger_en": "Child is short-tempered and reactive",
        "dont": "DON'T say: 'Respect nahi ka? Aplyakarun shikanato. Ashich waagto ka?' (Don't escalate during their reactive state)",
        "do_say": "WAIT for calm moment, then say: 'Kaal ekda tuzya reaction ne mala kaahi vaatla. Tuzya baajune aahe mi — saang kahi stress ahe ka?' (Address it during calm, not conflict)",
        "why": "Why it works: Irritability is often the visible symptom of invisible stress overload. Reactive scolding confirms they're alone. Patient curiosity opens the door.",
        "next_step": "If irritability persists 2+ weeks, consider one session with a counsellor framed as: 'This is for YOUR benefit, not because something is wrong with you.'",
        "icon": "😤"
    },
]

CONCERN_GUIDE = [
    ("🔴 High Risk — Act Now", [
        "Talking about wanting to 'give up', 'disappear', or 'not be here'",
        "Complete withdrawal from ALL social contact for 7+ days",
        "Refusing to eat or sleeping 14+ hours daily",
        "Self-harm marks or signs on body",
    ], "#F43F5E",
     "iCall (TISS): 9152987821 | Vandrevala Foundation: 1860-2662-345 (24/7)"),
    ("🟡 Monitor Closely — Talk this week", [
        "Crying frequently without clear reason",
        "Repeated physical complaints (headaches, stomach aches) with no medical cause",
        "Sudden drop in grades combined with increased isolation",
        "Giving away possessions or saying dramatic goodbyes",
    ], "#F59E0B",
     "College counsellor appointment + more frequent low-pressure check-ins"),
    ("🟢 Normal Stress — Support with routine", [
        "Mood swings during exam season",
        "Occasionally skipping meals before exams",
        "Wanting more alone time than usual for 1–2 weeks",
        "Mild irritability when tired",
    ], "#10B981",
     "Maintain routine, increase positive family time, ensure good sleep & meals"),
]



# ── AI Chatbot renderer ───────────────────────────────────────────────────────
def _render_chatbot(lang: str = "en"):
    """Renders the AI-powered Parent Advisor chatbot using Gemini."""

    ans    = st.session_state.get("answers", {})
    scores = st.session_state.get("scores",  {})
    child_name = ans.get("name", "")

    ui = CHAT_UI

    # ── Section header ─────────────────────────────────────────
    api_ok = has_api_key()
    badge_color = "#10B981" if api_ok else "#F59E0B"
    badge_text  = ("🟢 AI Active" if lang == "en" else
                   "🟢 AI सक्रिय" if lang == "mr" else "🟢 AI सक्रिय") if api_ok else (
                   "🟡 Fallback Mode" if lang == "en" else
                   "🟡 फॉलबॅक मोड" if lang == "mr" else "🟡 फ़ॉलबैक मोड")

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0F0A2E,#1E1B4B,#0F2027);
                border:1px solid #6366F150; border-radius:20px;
                padding:24px 28px 16px; margin-bottom:16px;
                box-shadow:0 4px 24px rgba(99,102,241,0.15);">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
            <div style="display:flex;align-items:center;gap:12px;">
                <span style="font-size:2rem;">🤖</span>
                <div>
                    <h3 style="font-family:'Space Grotesk',sans-serif;color:#A5B4FC;
                               margin:0;font-size:1.15rem;">
                        {ui['title'].get(lang, ui['title']['en'])}
                    </h3>
                    <p style="color:#64748B;font-size:0.78rem;margin:2px 0 0;">
                        {ui['subtitle'].get(lang, ui['subtitle']['en'])}
                    </p>
                </div>
            </div>
            <span style="background:{badge_color}20;color:{badge_color};
                         border:1px solid {badge_color}50;border-radius:20px;
                         padding:4px 12px;font-size:0.72rem;font-weight:700;">
                {badge_text}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # API key warning
    if not api_ok:
        st.warning(ui["no_key_warning"].get(lang, ui["no_key_warning"]["en"]))

    # ── Session state init ─────────────────────────────────────
    if "parent_chat_msgs" not in st.session_state:
        st.session_state.parent_chat_msgs = []          # display list: {"role", "text"}
        st.session_state.parent_chat_openai = []        # OpenAI history: {"role", "content"}
        # Greeting
        st.session_state.parent_chat_msgs.append({
            "role": "bot",
            "text": ui["greeting"].get(lang, ui["greeting"]["en"]),
        })

    # ── Chat display ───────────────────────────────────────────
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.parent_chat_msgs:
            if msg["role"] == "user":
                with st.chat_message("user", avatar="👨‍👩‍👧"):
                    st.markdown(msg["text"])
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(msg["text"])

    # ── Input ──────────────────────────────────────────────────
    col_in, col_clr = st.columns([6, 1])
    with col_in:
        user_input = st.chat_input(
            placeholder=ui["placeholder"].get(lang, ui["placeholder"]["en"]),
            key="parent_ai_chat_input",
        )
    with col_clr:
        st.write("")
        if st.button(ui["clear"].get(lang, "🗑️"), key="parent_ai_clear",
                     use_container_width=True):
            st.session_state.parent_chat_msgs   = []
            st.session_state.parent_chat_openai = []
            st.session_state.parent_chat_msgs.append({
                "role": "bot",
                "text": ui["greeting"].get(lang, ui["greeting"]["en"]),
            })
            st.rerun()

    # ── Process new message ────────────────────────────────────
    if user_input and user_input.strip():
        txt = user_input.strip()

        # Add user message to display
        st.session_state.parent_chat_msgs.append({"role": "user", "text": txt})

        # Show thinking spinner, call AI
        with st.spinner(ui["thinking"].get(lang, "🧠 Analysing...")):
            ai_reply = get_ai_response(
                conversation_history=st.session_state.parent_chat_openai,
                user_message=txt,
                lang=lang,
                child_name=child_name,
                child_scores=scores if scores else None,
            )

        # Update OpenAI conversation history (user + assistant turns)
        st.session_state.parent_chat_openai.append({"role": "user",      "content": txt})
        st.session_state.parent_chat_openai.append({"role": "assistant", "content": ai_reply})

        # Keep history manageable (last 10 turns = 20 entries)
        if len(st.session_state.parent_chat_openai) > 20:
            st.session_state.parent_chat_openai = st.session_state.parent_chat_openai[-20:]

        # Add bot reply to display
        st.session_state.parent_chat_msgs.append({"role": "bot", "text": ai_reply})
        st.rerun()




def show(lang: str = "en"):

    ans    = st.session_state.get("answers", {})
    scores = st.session_state.get("scores",  {})
    submitted = st.session_state.get("submitted", False)

    name = ans.get("name", "") or (
        "your child" if lang == "en" else
        "तुमचे मूल"  if lang == "mr" else
        "आपका बच्चा"
    )

    # ── Page header ───────────────────────────────────────────
    st.markdown(f"""
    <div class="mm-hero" style="margin-bottom:20px;">
        <div style="font-size:2rem;">👨‍👩‍👧</div>
        <h2 style="font-family:'Space Grotesk',sans-serif;color:#A5B4FC;
                   margin:8px 0 4px;font-size:1.6rem;">
            {t('parent_title', lang)}
        </h2>
        <p style="color:#94A3B8;font-size:0.88rem;margin:0;">
            {"Talk to our AI advisor about your child's behaviour — in English, Marathi, or Hindi."
             if lang == "en" else
             "तुमच्या मुलाच्या वागणुकीबद्दल आमच्या AI सल्लागाराशी बोला — मराठी, इंग्रजी किंवा हिंदीमध्ये."
             if lang == "mr" else
             "अपने बच्चे के व्यवहार के बारे में हमारे AI सलाहकार से बात करें — हिंदी, मराठी या अंग्रेज़ी में."}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── AI Chatbot — always visible ───────────────────────────
    _render_chatbot(lang)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Assessment snapshot — only if submitted ───────────────
    if submitted and scores:
        stress_index  = scores.get("stress_index", 0.5)
        overall       = scores.get("overall_health", 70)
        overall_color = "#10B981" if overall >= 70 else "#F59E0B" if overall >= 45 else "#F43F5E"
        stress_label  = ("high" if stress_index > 0.60 else
                         "moderate" if stress_index > 0.35 else "low")

        st.markdown(f"""
        <div class="mm-section-title">
            📊 {name}{"'s" if lang=="en" else " चे" if lang=="mr" else " का"} Assessment Snapshot
        </div>""", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        metrics = [
            ("😴 Sleep",      f"{ans.get('sleep_hours',7)}h/night",
             "✅ Good"      if ans.get("sleep_hours",7)>=7  else "⚠️ Low",
             "#10B981"      if ans.get("sleep_hours",7)>=7  else "#F59E0B"),
            ("👥 Friends",    f"{ans.get('friends_count',5)} close",
             "✅ Connected" if ans.get("friends_count",5)>=3 else "⚠️ Isolated",
             "#10B981"      if ans.get("friends_count",5)>=3 else "#F43F5E"),
            ("📱 Screen",     f"{ans.get('phone_hours',3)}h/day",
             "✅ Balanced"  if ans.get("phone_hours",3)<=4  else "⚠️ High",
             "#10B981"      if ans.get("phone_hours",3)<=4  else "#F43F5E"),
            ("🎯 Motivation", f"{scores.get('motivation_score',50):.0f}/100",
             "✅ Motivated" if scores.get("motivation_score",50)>=50 else "⚠️ Low",
             "#10B981"      if scores.get("motivation_score",50)>=50 else "#F59E0B"),
        ]
        for col, (label, val, status, color) in zip([c1,c2,c3,c4], metrics):
            with col:
                st.markdown(f"""
                <div class="mm-card" style="text-align:center;border-color:{color}40;">
                    <div style="font-size:1rem;font-weight:700;color:{color};">{label}</div>
                    <div style="font-size:1.2rem;font-weight:800;color:{color};margin:4px 0;
                                font-family:'Space Grotesk',sans-serif;">{val}</div>
                    <div style="font-size:0.75rem;color:#94A3B8;">{status}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        # Soft nudge — not a blocker
        st.info(
            "💡 **Tip:** Complete the student assessment to also see personalised scores alongside the chatbot advice."
            if lang == "en" else
            "💡 **टीप:** विद्यार्थी मूल्यमापन पूर्ण केल्यास AI सल्ल्यासोबत वैयक्तिक गुण देखील दिसतील."
            if lang == "mr" else
            "💡 **सुझाव:** छात्र मूल्यांकन पूरा करें तो AI सलाह के साथ व्यक्तिगत स्कोर भी दिखेंगे."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Parent Advisor Chatbot (already rendered above) ───────
    # Situation guide always shown below

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Situation Guide ───────────────────────────────────────
    st.markdown('<div class="mm-section-title">💬 Situation-by-Situation Conversation Guide</div>',
                unsafe_allow_html=True)
    st.markdown("""<div style="color:#64748B;font-size:0.82rem;margin-bottom:12px;">
    Click on each situation to see exactly what to say and do — based on your child's psychological profile.
    </div>""", unsafe_allow_html=True)

    for scenario in SCENARIOS:
        with st.expander(f"{scenario['icon']} {scenario['trigger_en']}", expanded=False):
            col_dont, col_do = st.columns(2)
            with col_dont:
                st.markdown(f"""
                <div class="mm-card" style="border-color:rgba(244,63,94,0.3);
                            background:rgba(244,63,94,0.05);min-height:90px;">
                    <div style="font-weight:700;color:#F87171;font-size:0.85rem;margin-bottom:6px;">❌ {scenario['dont'].split(':')[0]}</div>
                    <div style="color:#CBD5E1;font-size:0.83rem;line-height:1.5;font-style:italic;">
                        "{scenario['dont'].split(':', 1)[1].strip() if ':' in scenario['dont'] else scenario['dont']}"
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_do:
                st.markdown(f"""
                <div class="mm-card" style="border-color:rgba(16,185,129,0.3);
                            background:rgba(16,185,129,0.05);min-height:90px;">
                    <div style="font-weight:700;color:#34D399;font-size:0.85rem;margin-bottom:6px;">✅ {scenario['do_say'].split(':')[0]}</div>
                    <div style="color:#CBD5E1;font-size:0.83rem;line-height:1.5;font-style:italic;">
                        "{scenario['do_say'].split(':', 1)[1].strip() if ':' in scenario['do_say'] else scenario['do_say']}"
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style="margin-top:8px;padding:10px 14px;background:rgba(79,70,229,0.08);
                        border-radius:8px;border-left:3px solid #4F46E5;font-size:0.85rem;color:#CBD5E1;line-height:1.5;">
                🔬 <strong style="color:#A5B4FC;">Why it works:</strong> {scenario['why']}
            </div>
            <div style="margin-top:6px;padding:10px 14px;background:rgba(245,158,11,0.06);
                        border-radius:8px;border-left:3px solid #F59E0B;font-size:0.85rem;color:#FCD34D;line-height:1.5;">
                ➡️ <strong>Next step:</strong> {scenario['next_step']}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Concern levels ────────────────────────────────────────
    st.markdown('<div class="mm-section-title">⚠️ When to Be Concerned — Severity Guide</div>',
                unsafe_allow_html=True)

    for title, signs, color, action in CONCERN_GUIDE:
        st.markdown(f"""
        <div class="mm-card" style="border-color:{color}40;margin-bottom:8px;">
            <div style="font-weight:700;color:{color};font-size:0.92rem;margin-bottom:8px;">{title}</div>
            <div style="display:flex;gap:16px;flex-wrap:wrap;">
                <div style="flex:2;min-width:200px;">
                    {"".join(f'<div style="color:#CBD5E1;font-size:0.83rem;padding:3px 0;border-bottom:1px solid rgba(255,255,255,0.04);">• {s}</div>' for s in signs)}
                </div>
                <div style="flex:1;min-width:160px;background:{color}12;border-radius:8px;padding:10px 12px;">
                    <div style="font-size:0.75rem;font-weight:700;color:{color};margin-bottom:4px;">ACTION</div>
                    <div style="font-size:0.8rem;color:#CBD5E1;line-height:1.5;">{action}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Profile-specific advice ───────────────────────────────
    if submitted and scores:
        st.markdown('<div class="mm-section-title">🎯 Personalised Advice for Your Child</div>',
                    unsafe_allow_html=True)

        preds = st.session_state.get("predictions", {})
        recs  = st.session_state.get("recs", {})
        at_risk = preds.get("at_risk_flag", 0)
        lm = recs.get("learning_mode", "Hybrid")
        archetype = recs.get("archetype_name", "")
        strengths = recs.get("strengths", [])
        areas = recs.get("areas_to_improve", [])

        st.markdown(f"""
        <div class="mm-card">
            <div style="font-size:0.9rem;line-height:1.8;color:#CBD5E1;">
            Based on {name}'s assessment:<br><br>
            🎓 <strong style="color:#A5B4FC;">Ideal learning mode:</strong> {lm} —
            {"Support their need for structure and face-to-face interaction. Ensure they attend classes regularly." if lm=="Offline" else
             "Support their self-paced digital learning. Ensure they have a quiet, dedicated study space at home." if lm=="Online" else
             "Support both online and offline learning. Don't push them toward just one mode."}<br><br>
            🧠 <strong style="color:#A5B4FC;">Archetype:</strong> {archetype} —
            {"They likely put immense pressure on themselves. Your role is to give them PERMISSION to rest." if "Achiever" in archetype else
             "They need help finding their 'why'. Discuss their interests, not just their marks." if "Drifter" in archetype else
             "They need gentle confidence-building. Praise small wins loudly and publicly." if "Struggler" in archetype else
             "They thrive with social connection. Help them organise study groups at home." if "Social" in archetype else
             "They're digitally independent. Trust their online learning, just monitor screen time." if "Digital" in archetype else
             "They're generally balanced. Keep supporting their routine."}<br><br>
            💪 <strong style="color:#10B981;">Their strengths</strong> (celebrate these!): {', '.join(strengths)}<br>
            🌱 <strong style="color:#F59E0B;">Where they need support:</strong> {', '.join(areas)}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if at_risk:
            st.markdown("""
            <div class="risk-alert" style="margin-top:12px;">
            🤝 <strong>Special note for you:</strong> Your child's profile has some early warning indicators.
            Please schedule a calm, one-on-one conversation this week — not about studies, just about them.
            A college counsellor appointment would also be very beneficial within the next 2 weeks.
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Family activities ─────────────────────────────────────
    st.markdown('<div class="mm-section-title">🌈 Recommended Family Activities (Pune)</div>',
                unsafe_allow_html=True)
    acts_cols = st.columns(3)
    activities = [
        ("🌿", "Morning walk", "Vetal Tekdi or Pashan Lake — 30 min, no phones, no study talk"),
        ("🎲", "Board game night", "Catan, Scrabble or chess — once a week, builds bonding without pressure"),
        ("🍳", "Cook together", "A shared non-academic activity that builds warmth and routine"),
        ("🚴", "Weekend cycling", "FC Road or Viman Nagar lanes — light exercise reduces cortisol"),
        ("🎬", "Movie night", "A feel-good Hindi/Marathi film — shared experience builds family bonds"),
        ("📸", "Heritage walk", "Shaniwar Wada, Aga Khan Palace — stimulates curiosity, not academics"),
    ]
    for i, (icon, title, desc) in enumerate(activities):
        with acts_cols[i % 3]:
            st.markdown(f"""
            <div class="mm-card" style="min-height:90px;">
                <div style="font-size:1.3rem;">{icon}</div>
                <div style="font-weight:700;color:#A5B4FC;font-size:0.85rem;margin:4px 0;">{title}</div>
                <div style="font-size:0.78rem;color:#94A3B8;line-height:1.4;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Helplines ─────────────────────────────────────────────
    st.markdown("""
    <div class="mm-card" style="border-color:rgba(244,63,94,0.25);">
        <div style="font-weight:700;color:#F87171;margin-bottom:8px;font-size:0.9rem;">📞 Professional Helplines — Maharashtra</div>
        <div style="font-size:0.83rem;color:#CBD5E1;line-height:1.9;">
        📞 <strong>iCall (TISS)</strong>: 9152987821 &nbsp;(Mon–Sat, 8AM–10PM, Free)<br>
        📞 <strong>Vandrevala Foundation</strong>: 1860-2662-345 &nbsp;(24/7, Free)<br>
        📞 <strong>iCall WhatsApp</strong>: +91 9152987821<br>
        🏥 <strong>Symbiosis Centre for Emotional Wellbeing, Pune</strong>: Visit SCMS website<br>
        🏥 <strong>NIMHANS Connect</strong>: nimhansconnect@nimhans.ac.in
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Download Parent Guide ─────────────────────────────────
    if submitted and scores:
        _sl = "high" if scores.get("stress_index", 0.5) > 0.6 else \
              "moderate" if scores.get("stress_index", 0.5) > 0.35 else "low"
        _overall = scores.get("overall_health", 70)

        _warnings = []
        if scores.get("stress_index", 0) > 0.65:
            _warnings.append("Frequently appearing tired, withdrawn, or irritable")
        if scores.get("anxiety_level", 0) > 65:
            _warnings.append("Difficulty sleeping or waking up with worries")
        if scores.get("social_isolation", 0) > 6:
            _warnings.append("Spending increasing time alone")
        if scores.get("motivation_score", 50) < 35:
            _warnings.append("Losing interest in activities they previously enjoyed")
        if not _warnings:
            _warnings.append("No major warning signs detected at this time")

        parent_guide_text = f"""PARENT GUIDE - UNDERSTANDING YOUR CHILD
Student: {name}
======================================================

HOW YOUR CHILD IS DOING
------------------------------------------------------
{name} is currently experiencing {_sl} stress levels.
Overall wellbeing score: {_overall}/100.

WHAT YOU CAN DO
------------------------------------------------------
SAY:
  - "I'm proud of your effort, not just your grades."
  - "Is there anything I can do to make things easier?"
  - "It's okay to take breaks - rest is part of success."

DON'T SAY:
  - Don't compare them to siblings or classmates.
  - Avoid asking about exam results immediately.
  - Don't make study the only dinner conversation topic.

WARNING SIGNS
------------------------------------------------------
{chr(10).join('  ! ' + w for w in _warnings)}

HELPLINES
------------------------------------------------------
  - iCall (TISS): 9152987821 (Mon-Sat, 8AM-10PM)
  - Vandrevala Foundation: 1860-2662-345 (24/7)
""".strip()

        st.download_button(
            "⬇️ Download Parent Guide",
            data=parent_guide_text,
            file_name=f"{name.replace(' ', '_')}_parent_guide.txt",
            mime="text/plain",
            use_container_width=True,
            key="dl_parent_guide_txt",
        )

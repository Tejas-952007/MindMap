"""Page 5 – Full Psychological Report with PDF Download"""
import streamlit as st
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.translations import t


def show(lang: str = "en"):
    ans = st.session_state.answers
    scores = st.session_state.scores
    recs = st.session_state.recs
    preds = st.session_state.predictions

    name = ans.get("name", "Student")

    st.markdown(f"""
    <div class="mm-hero" style="padding:28px; margin-bottom:24px;">
        <div style="font-size:2rem;">📄</div>
        <h2 style="font-family:'Space Grotesk',sans-serif;color:#A5B4FC;margin:10px 0 4px;">
            {t('report_title', lang)}
        </h2>
        <p style="color:#64748B;font-size:0.88rem;margin:0;">
            {name} &nbsp;·&nbsp; {t('report_generated', lang)}&nbsp;·&nbsp;
            <span style="color:#F59E0B;">{t('not_clinical', lang)}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Executive summary
    overall = scores.get("overall_health", 70)
    overall_color = "#10B981" if overall >= 70 else "#F59E0B" if overall >= 45 else "#F43F5E"
    stress_pct = round(scores.get("stress_index", 0.5) * 100, 1)

    with st.expander("📋 1. Executive Summary", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        metrics = [
            ("Overall Health", f"{overall}/100", overall_color),
            ("Stress Index", f"{stress_pct}%", "#F43F5E" if stress_pct > 60 else "#F59E0B" if stress_pct > 35 else "#10B981"),
            ("Anxiety Level", f"{scores.get('anxiety_level',50):.0f}/100", "#F59E0B"),
            ("Motivation", f"{scores.get('motivation_score',50):.0f}/100", "#4F46E5"),
        ]
        for col, (label, val, color) in zip([c1, c2, c3, c4], metrics):
            with col:
                st.markdown(f"""
                <div class="mm-card" style="text-align:center;border-color:{color}40;">
                    <div style="font-size:1.5rem;font-weight:800;color:{color};
                                font-family:'Space Grotesk',sans-serif;">{val}</div>
                    <div style="font-size:0.78rem;color:#64748B;margin-top:4px;">{label}</div>
                </div>
                """, unsafe_allow_html=True)

    # Learning mode assessment
    with st.expander("🌐 2. Learning Mode Assessment"):
        lm = recs.get("learning_mode", "Hybrid")
        lm_colors = {"Online": "#4F46E5", "Offline": "#10B981", "Hybrid": "#F59E0B"}
        lm_c = lm_colors.get(lm, "#4F46E5")
        st.markdown(f"""
        <div style="margin:12px 0;">
            <span class="result-badge" style="background:rgba(79,70,229,0.1);border-color:{lm_c}60;">
                {recs.get('learning_mode_icon','🔀')} Recommended: <strong style="color:{lm_c};">{lm} Learning</strong>
                &nbsp;(AI Confidence: {preds.get('learning_mode_confidence',72):.0f}%)
            </span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**Explanation:** {recs.get('learning_mode_desc', '')}")
        st.markdown("**Quick Tips for Your Mode:**")
        for tip in recs.get("learning_mode_tips", []):
            st.markdown(f"  • {tip}")

    # Stress & anxiety analysis
    with st.expander("🧠 3. Stress & Anxiety Analysis"):
        st.markdown(f"""
        | Metric | Score | Interpretation |
        |--------|-------|----------------|
        | Stress Index | {stress_pct}% | {'🔴 High — needs attention' if stress_pct > 60 else '🟡 Moderate — manageable' if stress_pct > 35 else '🟢 Low — great balance'} |
        | Anxiety Level | {scores.get('anxiety_level',50):.0f}/100 | {'🔴 Elevated anxiety' if scores.get('anxiety_level',50) > 65 else '🟡 Some anxiety present' if scores.get('anxiety_level',50) > 40 else '🟢 Calm baseline'} |
        | Sleep Hours/Night | {ans.get('sleep_hours',7)} hrs | {'🔴 Under-sleeping — critical' if ans.get('sleep_hours',7) < 5 else '🟡 Slightly below ideal' if ans.get('sleep_hours',7) < 7 else '🟢 Healthy sleep pattern'} |
        | Racing Mind at Night | {ans.get('sleep_racing','Sometimes')} | Sleep quality indicator |
        | Exam Day Feeling | {'Blank & scattered ⚠️' if ans.get('exam_blank',0) else 'Sharp & ready ✅'} | Exam anxiety indicator |
        """)
        sleep_tip = ""
        if ans.get("sleep_hours", 7) < 6:
            sleep_tip = "⚠️ **Priority:** Your sleep is below 6 hours — this is a key driver of stress and poor memory consolidation. Set a hard bedtime of 10:30 PM for the next 30 days."
        elif ans.get("sleep_hours", 7) >= 8:
            sleep_tip = "✅ **Great sleep pattern!** Maintain your sleep schedule as it's one of your strongest assets."
        if sleep_tip:
            st.markdown(sleep_tip)

    # Motivation & self-efficacy
    with st.expander("💡 4. Motivation & Self-Efficacy Profile"):
        mot = scores.get("motivation_score", 50)
        mot_type = "Intrinsic" if "curiosity" in str(ans.get("motivators", [])).lower() else "Extrinsic"
        st.markdown(f"""
        **Motivation Score:** {mot:.0f}/100 &nbsp;·&nbsp; **Primary Motivation Type:** {mot_type}

        **Motivation Drivers Identified:**
        """)
        motivators = ans.get("motivators", [])
        if motivators:
            for m in motivators:
                st.markdown(f"  • {m}")
        else:
            st.markdown("  • No strong motivators selected — consider goal-setting workshops")

        st.markdown(f"""
        **Confidence Level:** {ans.get('confidence', 3)}/5 &nbsp;·&nbsp;
        **Goal-Setting Frequency:** {ans.get('goal_setting_freq', 'Sometimes')}

        **Self-Efficacy Assessment:**
        {
            "🌱 Your self-confidence is developing. Remember: confidence is built through action, not waiting for it. Start with tiny wins and celebrate each one."
            if ans.get('confidence', 3) <= 2 else
            "🙂 You have a moderate level of confidence. Focus on learning from mistakes rather than avoiding them — that's where growth happens."
            if ans.get('confidence', 3) == 3 else
            "💪 Strong self-efficacy! You believe in your abilities. Channel this into consistent daily effort and you'll be unstoppable."
        }
        """)

    # Social & environmental factors
    with st.expander("🤝 5. Social & Environmental Factors"):
        soc_iso = scores.get("social_isolation", 5)
        soc_color = "#F43F5E" if soc_iso > 7 else "#F59E0B" if soc_iso > 4 else "#10B981"
        st.markdown(f"""
        | Factor | Value | Notes |
        |--------|-------|-------|
        | Social Isolation Index | {soc_iso}/10 | {'High isolation — social support urgently needed' if soc_iso > 7 else 'Moderate — could benefit from more connection' if soc_iso > 4 else 'Good social connectedness'} |
        | Living Situation | {ans.get('living_situation','Home')} | {'Hostel/PG may reduce family support — build friend network' if ans.get('living_situation','Home') != 'Home' else 'Family support available — leverage it'} |
        | Financial Stress | {ans.get('financial_stress','Moderate')} | {'May be contributing to overall stress' if ans.get('financial_stress','Moderate') in ['Tight','Financially Struggling'] else 'Financial situation is stable'} |
        | Close Friends in Class | {ans.get('friends_count', 5)} | {'Build at least 3-5 trusted academic relationships' if ans.get('friends_count',5) < 3 else 'Healthy social network'} |
        | Social Interaction Freq | {ans.get('social_freq','Occasionally (a few times/month)')} | Social engagement metric |
        """)

    # Academic risk assessment
    with st.expander("⚡ 6. Academic Risk Assessment"):
        at_risk = preds.get("at_risk_flag", 0)
        if at_risk:
            st.markdown("""
            <div class="risk-alert">
            ⚠️ <strong>Early Warning Detected</strong><br><br>
            Certain patterns in your academic and psychological profile suggest you may benefit from
            proactive support. This is NOT a judgment — it's an opportunity to get ahead of challenges
            before they become bigger problems.<br><br>
            <strong>Recommended action:</strong> Speak with your college's student welfare officer
            or academic counsellor within the next 2 weeks.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success("✅ **Low Academic Risk** — Your current academic trajectory looks stable.")

        st.markdown(f"""
        **SGPA:** {ans.get('sgpa', 7.0):.1f}/10 &nbsp;·&nbsp;
        **ATKT Status:** {'⚠️ Yes — backlog present' if ans.get('atkt',0) else '✅ No backlog'} &nbsp;·&nbsp;
        **Daily Study Hours:** {ans.get('study_hours', 4)} hrs
        """)

    # Student archetype
    with st.expander(f"{recs.get('archetype_emoji','🎭')} 7. Student Archetype Profile"):
        arch_color = recs.get("archetype_color", "#06B6D4")
        st.markdown(f"""
        <div class="mm-card" style="border-color:{arch_color}60;margin-bottom:16px;">
            <div style="font-size:2rem;">{recs.get('archetype_emoji','🎭')}</div>
            <div style="font-size:1.2rem;font-weight:700;color:{arch_color};margin:8px 0;">
                {recs.get('archetype_name','Balanced Learner')}
            </div>
            <div style="color:#CBD5E1;line-height:1.7;">{recs.get('archetype_desc','')}</div>
        </div>
        """, unsafe_allow_html=True)

    # 30/60/90 action plan
    with st.expander("🗺️ 8. Personalised 30/60/90 Day Action Plan"):
        roadmap = recs.get("roadmap", {})
        for phase, label, color in [
            ("30_days", "First 30 Days – Build the Foundation", "#4F46E5"),
            ("60_days", "Days 31–60 – Deepen & Develop", "#10B981"),
            ("90_days", "Days 61–90 – Accelerate & Lead", "#F59E0B"),
        ]:
            st.markdown(f"**{label}**")
            for item in roadmap.get(phase, []):
                st.markdown(f"  ✅ {item}")
            st.markdown("")

    # Professional referral note
    if preds.get("at_risk_flag", 0):
        with st.expander("🏥 9. Professional Referral Note (Counsellor Section)"):
            st.markdown(f"""
            **REFERRAL NOTE – For Counsellor/Psychiatrist Use**

            *Student:* {name} &nbsp;·&nbsp; *Date:* 24 February 2026

            This student has been flagged by the MindMap AI system based on the following indicators:
            - Stress Index: {stress_pct}% (above threshold)
            - Academic Risk Flag: Positive
            - ATKT/SGPA pattern: {'Present' if ans.get('atkt',0) else 'SGPA below threshold'}
            - Sleep Hours: {ans.get('sleep_hours',7)} hrs/night

            **Important:** This is a screening tool output only and must NOT be used as a
            standalone clinical assessment. Please conduct a full clinical evaluation following
            standard psychological assessment protocols.

            Suggested assessment tools: PHQ-9, GAD-7, PSS-10 (Indian standardised versions)
            """)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Download Section ──────────────────────────────────────
    st.markdown('<div class="mm-section-title">📥 Download Your Report</div>', unsafe_allow_html=True)

    # ── Build Student Report Text (inline – no external import) ──
    _lm = recs.get("learning_mode", "Hybrid")
    _arch = recs.get("archetype_name", "Balanced Learner")
    _stress_pct = round(scores.get("stress_index", 0.5) * 100, 1)
    _overall = scores.get("overall_health", 70)

    _roadmap = recs.get("roadmap", {})
    _30 = "\n".join("  - " + s for s in _roadmap.get("30_days", ["Set a study routine"]))
    _60 = "\n".join("  - " + s for s in _roadmap.get("60_days", ["Complete one course"]))
    _90 = "\n".join("  - " + s for s in _roadmap.get("90_days", ["Build a project"]))

    student_report_text = f"""PSYCHOLOGICAL ASSESSMENT REPORT
Student: {name}
Overall Psychological Health Score: {_overall}/100
======================================================

EXECUTIVE SUMMARY
------------------------------------------------------
{name} demonstrates a {recs.get('stress_level','Medium')} stress profile with an overall
psychological health score of {_overall}/100.

LEARNING MODE ASSESSMENT
------------------------------------------------------
Recommended Mode: {_lm}
{recs.get('learning_mode_desc','')}

STRESS & ANXIETY ANALYSIS
------------------------------------------------------
Stress Index: {_stress_pct}%
Anxiety Level: {scores.get('anxiety_level', 50)}/100
Sleep Quality: {ans.get('sleep_hours', 7)} hours/night

MOTIVATION & SELF-EFFICACY PROFILE
------------------------------------------------------
Motivation Score: {scores.get('motivation_score', 50)}/100
Confidence Level: {ans.get('confidence', 3)}/5

SOCIAL & ENVIRONMENTAL FACTORS
------------------------------------------------------
Social Isolation Index: {scores.get('social_isolation', 5)}/10
Living Situation: {ans.get('living_situation', 'Home')}
Financial Situation: {ans.get('financial_stress', 'Moderate')}

ACADEMIC RISK ASSESSMENT
------------------------------------------------------
Risk Flag: {'AT RISK - Please consult college counsellor' if scores.get('academic_risk_flag') else 'LOW RISK'}
SGPA: {ans.get('sgpa', 7.0)}
ATKT Status: {'Yes' if ans.get('atkt') else 'No'}

STUDENT ARCHETYPE
------------------------------------------------------
Archetype: {_arch}
{recs.get('archetype_desc','')}

Identified Strengths: {', '.join(recs.get('strengths', []))}
Areas for Growth: {', '.join(recs.get('areas_to_improve', []))}

30/60/90 DAY ACTION PLAN
------------------------------------------------------
First 30 Days:
{_30}

Days 31-60:
{_60}

Days 61-90:
{_90}

DISCLAIMER
------------------------------------------------------
This report is generated by an AI-powered assessment tool and is intended
for self-reflection and educational guidance only. It does not constitute
a clinical diagnosis. Please consult a qualified mental health professional
for personalised clinical assessment.
""".strip()

    # ── Build Parent Report Text (inline) ──
    _sl = "high" if scores.get("stress_index", 0.5) > 0.6 else \
          "moderate" if scores.get("stress_index", 0.5) > 0.35 else "low"

    _warnings = []
    if scores.get("stress_index", 0) > 0.65:
        _warnings.append("Frequently appearing tired, withdrawn, or irritable")
    if scores.get("anxiety_level", 0) > 65:
        _warnings.append("Difficulty sleeping or waking up with worries")
    if scores.get("social_isolation", 0) > 6:
        _warnings.append("Spending increasing time alone, avoiding social interaction")
    if scores.get("motivation_score", 50) < 35:
        _warnings.append("Losing interest in subjects or activities they previously enjoyed")
    if not _warnings:
        _warnings.append("No major warning signs detected at this time")

    parent_report_text = f"""PARENT GUIDE - UNDERSTANDING YOUR CHILD
Student: {name}
======================================================

HOW YOUR CHILD IS DOING
------------------------------------------------------
Based on the assessment, {name} is currently experiencing {_sl} stress levels.
Their overall wellbeing score is {_overall}/100.

WHAT THIS MEANS BEHAVIOURALLY
------------------------------------------------------
{"Your child may need additional emotional support right now." if _sl == "high" else "Your child is managing reasonably well." if _sl == "moderate" else "Your child appears to be in a good psychological state."}

WHAT YOU CAN DO - Practical Guidance
------------------------------------------------------
WHAT TO SAY:
  - "I'm proud of your effort, not just your grades."
  - "Is there anything I can do to make things easier for you?"
  - "It's okay to take breaks - rest is part of success."

WHAT NOT TO SAY:
  - Do not compare them to siblings, cousins, or classmates.
  - Avoid asking about exam results immediately after they come home.
  - Do not make study the only topic of dinner conversation.

WARNING SIGNS TO WATCH FOR
------------------------------------------------------
{chr(10).join("  ! " + w for w in _warnings)}

WHEN TO SEEK PROFESSIONAL HELP
------------------------------------------------------
If your child:
  - Refuses to attend college/school for more than 3 consecutive days
  - Expresses feelings of hopelessness or worthlessness
  - Shows significant changes in eating or sleeping patterns

Contact:
  - College counsellor or student welfare officer
  - iCall (TISS Pune): 9152987821 | Vandrevala Foundation: 1860-2662-345 (24/7)
""".strip()

    # ── Download Buttons (Direct – no generation step needed) ──
    col_dl1, col_dl2 = st.columns(2)

    with col_dl1:
        st.markdown("""<div class="mm-card" style="text-align:center;border-color:rgba(79,70,229,0.3);">
            <div style="font-size:1.8rem;margin-bottom:6px;">📄</div>
            <div style="font-weight:700;color:#A5B4FC;font-size:0.95rem;">Student Report</div>
            <div style="font-size:0.78rem;color:#64748B;margin-top:4px;">Full psychological assessment</div>
        </div>""", unsafe_allow_html=True)

        # Text download (always works)
        st.download_button(
            "⬇️ Download Student Report",
            data=student_report_text,
            file_name=f"{name.replace(' ','_')}_mindmap_report.txt",
            mime="text/plain",
            use_container_width=True,
            key="dl_student_txt",
        )

        # Try PDF too
        try:
            from fpdf import FPDF
            _pdf_ok = True
        except ImportError:
            _pdf_ok = False

        if _pdf_ok:
            try:
                from utils.report_generator import generate_pdf
                import uuid
                uid = uuid.uuid4().hex
                pdf_path = generate_pdf(student_report_text, f"/tmp/student_report_{uid}.pdf")
                with open(pdf_path, "rb") as f:
                    pdf_bytes = f.read()
                import os
                os.remove(pdf_path) # Clean up temp file
                st.download_button(
                    "📄 Download as PDF",
                    data=pdf_bytes,
                    file_name=f"{name.replace(' ','_')}_mindmap_report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="dl_student_pdf2",
                )
            except Exception as e:
                st.error(f"PDF generation failed: {e}")

    with col_dl2:
        st.markdown("""<div class="mm-card" style="text-align:center;border-color:rgba(16,185,129,0.3);">
            <div style="font-size:1.8rem;margin-bottom:6px;">👨‍👩‍👧</div>
            <div style="font-weight:700;color:#10B981;font-size:0.95rem;">Parent Guide</div>
            <div style="font-size:0.78rem;color:#64748B;margin-top:4px;">Guidance for parents</div>
        </div>""", unsafe_allow_html=True)

        # Text download (always works)
        st.download_button(
            "⬇️ Download Parent Guide",
            data=parent_report_text,
            file_name=f"{name.replace(' ','_')}_parent_guide.txt",
            mime="text/plain",
            use_container_width=True,
            key="dl_parent_txt",
        )

        if _pdf_ok:
            try:
                from utils.report_generator import generate_pdf
                import uuid
                uid = uuid.uuid4().hex
                pdf_path = generate_pdf(parent_report_text, f"/tmp/parent_report_{uid}.pdf")
                with open(pdf_path, "rb") as f:
                    pdf_bytes = f.read()
                import os
                os.remove(pdf_path) # Clean up temp file
                st.download_button(
                    "📄 Download as PDF",
                    data=pdf_bytes,
                    file_name=f"{name.replace(' ','_')}_parent_guide.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="dl_parent_pdf2",
                )
            except Exception as e:
                st.error(f"PDF generation failed: {e}")

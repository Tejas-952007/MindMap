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

    # PDF Download
    st.markdown('<div class="mm-section-title">📥 Download Your Report</div>', unsafe_allow_html=True)

    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        if st.button("📄 Generate PDF Report", key="gen_pdf", use_container_width=True):
            with st.spinner("Generating PDF..."):
                try:
                    from utils.recommender import generate_student_report
                    from utils.report_generator import generate_pdf
                    report_text = generate_student_report(ans, scores, recs)
                    pdf_path = generate_pdf(report_text, "/tmp/student_report.pdf")
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            "⬇️ Download Student Report PDF",
                            data=f.read(),
                            file_name=f"{name.replace(' ','_')}_mindmap_report.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                        )
                except Exception as e:
                    st.error(f"PDF generation failed: {e}")

    with col_dl2:
        if st.button("📝 Generate Parent PDF", key="gen_parent_pdf", use_container_width=True):
            with st.spinner("Generating Parent Report PDF..."):
                try:
                    from utils.recommender import generate_parent_report
                    from utils.report_generator import generate_pdf
                    parent_text = generate_parent_report(ans, scores)
                    pdf_path = generate_pdf(parent_text, "/tmp/parent_report.pdf")
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            "⬇️ Download Parent Report PDF",
                            data=f.read(),
                            file_name=f"{name.replace(' ','_')}_parent_guide.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                        )
                except Exception as e:
                    st.error(f"PDF generation failed: {e}")

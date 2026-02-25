"""Page 4 – AI Results Dashboard"""
import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.translations import t


def _gauge(value, title, max_val=100, color_thresholds=None):
    if color_thresholds is None:
        color_thresholds = [(33, "#10B981"), (66, "#F59E0B"), (100, "#F43F5E")]

    bar_color = color_thresholds[-1][1]
    for threshold, color in color_thresholds:
        if value <= threshold:
            bar_color = color
            break

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"color": "#CBD5E1", "size": 14}},
        gauge={
            "axis": {"range": [0, max_val], "tickfont": {"color": "#64748B", "size": 10}},
            "bar": {"color": bar_color, "thickness": 0.3},
            "bgcolor": "#1A1A2E",
            "bordercolor": "#334155",
            "steps": [
                {"range": [0, max_val * 0.33], "color": "#0F172A"},
                {"range": [max_val * 0.33, max_val * 0.66], "color": "#0F172A"},
                {"range": [max_val * 0.66, max_val], "color": "#0F172A"},
            ],
            "threshold": {
                "line": {"color": bar_color, "width": 3},
                "thickness": 0.8,
                "value": value,
            },
        },
        number={"font": {"color": bar_color, "size": 28, "family": "Space Grotesk"},
                "suffix": "%" if max_val == 100 else ""},
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=40, b=10),
        height=220,
    )
    return fig


def show(lang: str = "en"):
    ans = st.session_state.answers
    scores = st.session_state.scores
    preds = st.session_state.predictions
    recs = st.session_state.recs

    name = ans.get("name", "Student")
    lm = recs.get("learning_mode", "Hybrid")
    lm_icon = recs.get("learning_mode_icon", "🔀")
    lm_conf = preds.get("learning_mode_confidence", 72)
    arch_name = recs.get("archetype_name", "The Balanced Learner")
    arch_emoji = recs.get("archetype_emoji", "⚖️")
    arch_color = recs.get("archetype_color", "#06B6D4")
    stress_level = recs.get("stress_level", "Medium")
    stress_index = scores.get("stress_index", 0.5)
    overall = scores.get("overall_health", 70)
    at_risk = preds.get("at_risk_flag", 0)

    # ── Hero greeting ─────────────────────────────────────────
    overall_color = "#10B981" if overall >= 70 else "#F59E0B" if overall >= 45 else "#F43F5E"
    st.markdown(f"""
    <div class="mm-hero" style="padding:32px 28px; margin-bottom:28px;">
        <div style="font-size:2.5rem; margin-bottom:12px;">🎯</div>
        <h2 style="font-family:'Space Grotesk',sans-serif; font-size:1.8rem;
                   background:linear-gradient(135deg,#A5B4FC,#818CF8,#C4B5FD);
                   -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0 0 8px;">
            {t('results_hi', lang, name=name)}
        </h2>
        <p style="color:#94A3B8; font-size:0.92rem; margin:0;">
            {t('results_sub', lang)}
        </p>
        <div style="margin-top:16px;">
            <span class="mm-stat" style="color:{overall_color}; border-color:{overall_color}40;">
                💚 {t('overall_health', lang)}: {overall}/100
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── At-risk alert ─────────────────────────────────────────
    if at_risk:
        st.markdown(f"""
        <div class="risk-alert" style="margin-bottom:20px;">
            {t('at_risk_msg', lang)}<br><br>
            <strong>Pune Helplines:</strong> iCall (TISS): <code>9152987821</code> &nbsp;|&nbsp;
            Vandrevala Foundation: <code>1860-2662-345</code> (24/7)
        </div>
        """, unsafe_allow_html=True)

    # ── Learning Mode + Archetype ─────────────────────────────
    col_lm, col_arch = st.columns(2)

    with col_lm:
        lm_colors = {"Online": "#4F46E5", "Offline": "#10B981", "Hybrid": "#F59E0B"}
        lm_c = lm_colors.get(lm, "#4F46E5")
        st.markdown(f"""
        <div class="mm-card" style="border-color:{lm_c}40; min-height:180px;">
            <div style="font-size:2.2rem; margin-bottom:8px;">{lm_icon}</div>
            <div style="font-size:0.78rem; text-transform:uppercase; letter-spacing:1px;
                        color:#64748B; margin-bottom:4px;">{t('rec_learning_mode', lang)}</div>
            <div style="font-size:1.6rem; font-weight:800; color:{lm_c};
                        font-family:'Space Grotesk',sans-serif;">{lm} Learning</div>
            <div style="font-size:0.82rem; color:#94A3B8; margin:8px 0;">
                {t('ai_confidence', lang)}: <strong style="color:{lm_c};">{lm_conf:.0f}%</strong>
            </div>
            <div style="font-size:0.88rem; color:#CBD5E1; line-height:1.5;">
                {recs.get('learning_mode_desc','')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_arch:
        st.markdown(f"""
        <div class="mm-card" style="border-color:{arch_color}40; min-height:180px;">
            <div style="font-size:2.2rem; margin-bottom:8px;">{arch_emoji}</div>
            <div style="font-size:0.78rem; text-transform:uppercase; letter-spacing:1px;
                        color:#64748B; margin-bottom:4px;">{t('your_archetype', lang)}</div>
            <div style="font-size:1.4rem; font-weight:800; color:{arch_color};
                        font-family:'Space Grotesk',sans-serif;">{arch_name}</div>
            <div style="font-size:0.88rem; color:#CBD5E1; margin-top:8px; line-height:1.5;">
                {recs.get('archetype_desc','')[:180]}...
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Gauges ────────────────────────────────────────────────
    st.markdown(f'<div class="mm-section-title">📊 {t("psych_dashboard", lang)}</div>',
                unsafe_allow_html=True)

    g1, g2, g3, g4 = st.columns(4)
    with g1:
        st.plotly_chart(_gauge(round(stress_index * 100), t("stress_level", lang),
                               color_thresholds=[(33, "#10B981"), (55, "#F59E0B"), (75, "#F97316"), (100, "#F43F5E")]),
                        use_container_width=True)
    with g2:
        st.plotly_chart(_gauge(round(scores.get("anxiety_level", 50)), t("anxiety_level", lang),
                               color_thresholds=[(35, "#10B981"), (60, "#F59E0B"), (80, "#F97316"), (100, "#F43F5E")]),
                        use_container_width=True)
    with g3:
        st.plotly_chart(_gauge(round(scores.get("motivation_score", 50)), t("motivation", lang),
                               color_thresholds=[(40, "#F43F5E"), (65, "#F59E0B"), (100, "#10B981")]),
                        use_container_width=True)
    with g4:
        st.plotly_chart(_gauge(overall, t("overall_health", lang),
                               color_thresholds=[(45, "#F43F5E"), (65, "#F59E0B"), (100, "#10B981")]),
                        use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Strengths & Areas ─────────────────────────────────────
    col_str, col_imp = st.columns(2)
    with col_str:
        st.markdown(f'<div class="mm-section-title">💪 {t("your_strengths", lang)}</div>', unsafe_allow_html=True)
        strengths = recs.get("strengths", ["Dedicated", "Curious", "Resilient"])
        chips = " ".join(f'<span class="strength-chip">✅ {s}</span>' for s in strengths)
        st.markdown(f"<div style='margin-bottom:12px;'>{chips}</div>", unsafe_allow_html=True)

    with col_imp:
        st.markdown(f'<div class="mm-section-title">🌱 {t("areas_improve", lang)}</div>', unsafe_allow_html=True)
        areas = recs.get("areas_to_improve", ["Consistency", "Work-life balance"])
        chips2 = " ".join(f'<span class="improve-chip">🎯 {a}</span>' for a in areas)
        st.markdown(f"<div style='margin-bottom:12px;'>{chips2}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Recommendation Cards ──────────────────────────────────
    st.markdown('<div class="mm-section-title">🎁 Personalised Recommendations</div>',
                unsafe_allow_html=True)

    with st.expander(f"📅 {t('daily_routine', lang)}", expanded=True):
        routine = recs.get("daily_routine", "No routine data available")
        routine_steps = [s.strip() for s in routine.split("|") if s.strip()]
        for step in routine_steps:
            parts = step.split(" ", 1)
            time_part = parts[0] if len(parts) > 1 else ""
            activity = parts[1] if len(parts) > 1 else step
            st.markdown(f"""
            <div style="display:flex; gap:16px; align-items:flex-start;
                        padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.05);">
                <div style="font-weight:700; color:#818CF8; min-width:90px; font-size:0.88rem;">
                    {time_part}</div>
                <div style="color:#CBD5E1; font-size:0.9rem;">{activity}</div>
            </div>
            """, unsafe_allow_html=True)

    with st.expander("🧘 Stress Relief Activities"):
        cols_s = st.columns(3)
        for i, tip in enumerate(recs.get("stress_tips", [])):
            with cols_s[i % 3]:
                st.markdown(f"""
                <div class="mm-card" style="text-align:center; min-height:100px;">
                    <div style="font-size:1.5rem; margin-bottom:8px;">
                        {"🌿" if i==0 else "💪" if i==1 else "📓"}
                    </div>
                    <div style="font-size:0.85rem; color:#CBD5E1; line-height:1.5;">{tip}</div>
                </div>
                """, unsafe_allow_html=True)

    with st.expander("📚 Book Recommendations"):
        for book in recs.get("books", []):
            st.markdown(f"""
            <div style="display:flex; gap:12px; align-items:center; padding:10px 0;
                        border-bottom:1px solid rgba(255,255,255,0.05);">
                <div style="font-size:1.5rem;">📖</div>
                <div style="color:#CBD5E1; font-size:0.93rem;">{book}</div>
            </div>
            """, unsafe_allow_html=True)

    with st.expander("🎮 Games & Puzzles for Focus"):
        for game in recs.get("games", []):
            st.markdown(f"<div style='padding:6px 0;color:#CBD5E1;'>🕹️ {game}</div>",
                        unsafe_allow_html=True)

    with st.expander("💻 EdTech Platform Suggestions"):
        for et in recs.get("edtech", []):
            st.markdown(f"<div style='padding:6px 0;color:#CBD5E1;'>🔗 {et}</div>",
                        unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Study strategy ────────────────────────────────────────
    st.markdown('<div class="mm-section-title">🎓 Personalised Study Strategy</div>',
                unsafe_allow_html=True)
    for tip in recs.get("study_strategy", []):
        st.markdown(f"""
        <div style="display:flex; gap:12px; align-items:flex-start; padding:8px 0;
                    border-bottom:1px solid rgba(255,255,255,0.05);">
            <div style="color:#CBD5E1; font-size:0.93rem; line-height:1.5;">{tip}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 90-day roadmap ────────────────────────────────────────
    st.markdown('<div class="mm-section-title">🗺️ Your 30/60/90 Day Roadmap</div>',
                unsafe_allow_html=True)
    roadmap = recs.get("roadmap", {})
    cols_rm = st.columns(3)
    rm_data = [
        (t("roadmap_30", lang), roadmap.get("30_days", []), "#4F46E5"),
        (t("roadmap_60", lang), roadmap.get("60_days", []), "#10B981"),
        (t("roadmap_90", lang), roadmap.get("90_days", []), "#F59E0B"),
    ]
    for col, (title, items, color) in zip(cols_rm, rm_data):
        with col:
            st.markdown(f"""
            <div class="mm-card" style="border-color:{color}40;">
                <div style="font-weight:700; color:{color}; margin-bottom:12px; font-size:0.92rem;">
                    📌 {title}
                </div>
                {"".join(f'<div style="color:#CBD5E1;font-size:0.85rem;padding:5px 0;line-height:1.4;border-bottom:1px solid rgba(255,255,255,0.05);">• {item}</div>' for item in items)}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    btn_c = st.columns([1, 1, 1])
    with btn_c[0]:
        _r2r = {"en": "📄 Full Psychological Report", "mr": "📄 संपूर्ण अहवाल", "hi": "📄 पूरी रिपोर्ट"}
        if st.button(_r2r.get(lang, _r2r["en"]), use_container_width=True, key="res_to_report"):
            st.session_state.nav_page = "Report"
            st.rerun()
    with btn_c[1]:
        _r2p = {"en": "👨‍👩‍👧 Parent Guide", "mr": "👨‍👩‍👧 पालक मार्गदर्शन", "hi": "👨‍👩‍👧 अभिभावक गाइड"}
        if st.button(_r2p.get(lang, _r2p["en"]), use_container_width=True, key="res_to_parent"):
            st.session_state.nav_page = "Parent"
            st.rerun()
    with btn_c[2]:
        _retake = {"en": "🔄 Retake Assessment", "mr": "🔄 पुन्हा मूल्यांकन करा", "hi": "🔄 मूल्यांकन पुनर्करें"}
        if st.button(_retake.get(lang, _retake["en"]), use_container_width=True, key="res_retake"):
            st.session_state.submitted = False
            st.session_state.nav_page = "Assessment"
            st.rerun()

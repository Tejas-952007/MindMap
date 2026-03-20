"""Page 2 – Global Context: Charts & Hybrid Learning (Enhanced UI)"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.translations import t


CHART_TEMPLATE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#CBD5E1", family="Inter, sans-serif"),
    margin=dict(l=20, r=20, t=50, b=20),
)


def show(lang: str = "en"):
    # ── Page Hero ──────────────────────────────────────────────
    st.markdown(f"""
    <div style="margin-bottom:28px;">
        <div class="mm-section-title" style="font-size:1.4rem; margin-bottom:6px;">
            🌍 {t("global_title", lang)}
        </div>
        <div style="color:#64748B; font-size:0.92rem; line-height:1.6;">
            {t('global_sub', lang)}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Choropleth ─────────────────────────────────────────────
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
        <span style="font-size:1.3rem;">🗺️</span>
        <span style="font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:1.05rem;
                     color:#E2E8F0;">Online Learning Adoption by Country (%)</span>
    </div>
    """, unsafe_allow_html=True)

    countries = {
        "United States": 78, "United Kingdom": 72, "Canada": 70,
        "Australia": 68, "China": 65, "India": 55, "Germany": 60,
        "Brazil": 45, "South Africa": 35, "Japan": 58,
        "South Korea": 75, "France": 62, "Russia": 50,
        "Mexico": 40, "Indonesia": 42, "Nigeria": 28,
        "Pakistan": 32, "Bangladesh": 30, "Philippines": 38, "Vietnam": 44,
    }
    df_map = pd.DataFrame({"Country": list(countries.keys()),
                           "Adoption Rate": list(countries.values())})
    fig_map = px.choropleth(
        df_map, locations="Country", locationmode="country names",
        color="Adoption Rate",
        color_continuous_scale=[[0, "#0F0D2E"], [0.3, "#312E81"], [0.6, "#4F46E5"], [1, "#06B6D4"]],
        range_color=[20, 80],
        title=""
    )
    fig_map.update_layout(**CHART_TEMPLATE, height=400,
                          coloraxis_colorbar=dict(
                              title=dict(text="Adoption %", font=dict(color="#94A3B8", size=11)),
                              tickfont=dict(color="#94A3B8", size=10),
                              bgcolor="rgba(0,0,0,0)",
                              outlinewidth=0,
                          ))
    fig_map.update_geos(
        bgcolor="rgba(0,0,0,0)", showcoastlines=True, coastlinecolor="#1E293B",
        showland=True, landcolor="#12121F", showocean=True, oceancolor="#07070F",
        showframe=False, showcountries=True, countrycolor="#1E293B",
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # ── Bar chart ──────────────────────────────────────────────
    with col1:
        st.markdown("""
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
            <span style="font-size:1.1rem;">📊</span>
            <span style="font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:0.95rem;
                         color:#E2E8F0;">India vs Global: Online Learning Preference</span>
        </div>
        """, unsafe_allow_html=True)

        categories = ["School (9-12th)", "UG Engineering", "UG Arts/Commerce",
                      "Postgraduate", "Working Professionals"]
        india_vals = [38, 55, 48, 65, 78]
        global_vals = [45, 63, 52, 71, 82]

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(name="India", x=categories, y=india_vals,
                                 marker_color="#4F46E5",
                                 marker_line=dict(width=0),
                                 text=india_vals,
                                 textposition="outside", textfont=dict(color="#A5B4FC", size=11)))
        fig_bar.add_trace(go.Bar(name="Global", x=categories, y=global_vals,
                                 marker_color="#06B6D4",
                                 marker_line=dict(width=0),
                                 text=global_vals,
                                 textposition="outside", textfont=dict(color="#67E8F9", size=11)))
        fig_bar.update_layout(
            **CHART_TEMPLATE, barmode="group", height=400,
            xaxis=dict(showgrid=False, tickfont=dict(size=9, color="#94A3B8")),
            yaxis=dict(showgrid=True, gridcolor="#1E293B", gridwidth=0.5,
                       title=dict(text="% preferring online", font=dict(size=11, color="#64748B"))),
            legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.12,
                        font=dict(size=11)),
            bargap=0.2,
            bargroupgap=0.1,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── Pie chart ─────────────────────────────────────────────
    with col2:
        st.markdown("""
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
            <span style="font-size:1.1rem;">🥧</span>
            <span style="font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:0.95rem;
                         color:#E2E8F0;">India 2024: Learning Mode Distribution</span>
        </div>
        """, unsafe_allow_html=True)

        fig_pie = go.Figure(go.Pie(
            labels=["Pure Online", "Pure Offline", "Hybrid"],
            values=[22, 38, 40],
            hole=0.6,
            marker=dict(colors=["#4F46E5", "#10B981", "#F59E0B"],
                        line=dict(color="#07070F", width=3)),
            textfont=dict(size=12, color="white"),
            hovertemplate="<b>%{label}</b><br>%{value}%<extra></extra>",
        ))
        fig_pie.update_layout(**CHART_TEMPLATE, height=400,
                              annotations=[dict(text="<b>India</b><br>2024", x=0.5, y=0.5,
                                                font_size=14, font_color="#CBD5E1",
                                                showarrow=False)],
                              legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=-0.05,
                                          font=dict(size=11)))
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    # ── Line chart – COVID impact ─────────────────────────────
    with col3:
        st.markdown("""
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
            <span style="font-size:1.1rem;">📈</span>
            <span style="font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:0.95rem;
                         color:#E2E8F0;">COVID Impact on Learning Mode Shift (India)</span>
        </div>
        """, unsafe_allow_html=True)

        years = [2018, 2019, 2020, 2021, 2022, 2023, 2024]
        online = [20, 22, 65, 78, 68, 58, 55]
        offline = [78, 76, 28, 15, 25, 35, 40]
        hybrid_actual = [100 - o - of for o, of in zip(online, offline)]

        def hex_rgba(h, alpha):
            h = h.lstrip("#")
            r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
            return f"rgba({r},{g},{b},{alpha})"

        fig_line = go.Figure()
        for trace_name, vals, color in [
            ("Online", online, "#4F46E5"),
            ("Offline", offline, "#10B981"),
            ("Hybrid", hybrid_actual, "#F59E0B"),
        ]:
            fig_line.add_trace(go.Scatter(
                x=years, y=vals, name=trace_name, mode="lines+markers",
                line=dict(color=color, width=2.5, shape='spline'),
                marker=dict(size=7, line=dict(width=1, color='#07070F')),
                fill="tonexty" if trace_name == "Hybrid" else None,
                fillcolor=hex_rgba(color, 0.08) if trace_name == "Hybrid" else None,
                hovertemplate=f"<b>{trace_name}</b><br>%{{y}}%<extra></extra>",
            ))
        fig_line.add_vline(x=2020, line_dash="dot", line_color="#F43F5E", line_width=1.5,
                           annotation_text="COVID-19", annotation_font_color="#F43F5E",
                           annotation_font_size=11)
        fig_line.update_layout(
            **CHART_TEMPLATE, height=380,
            xaxis=dict(showgrid=False, tickfont=dict(color="#94A3B8")),
            yaxis=dict(showgrid=True, gridcolor="#1E293B", gridwidth=0.5,
                       title=dict(text="% students", font=dict(size=11, color="#64748B")),
                       range=[0, 100]),
            legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.12,
                        font=dict(size=11)),
        )
        st.plotly_chart(fig_line, use_container_width=True)

    # ── Radial gauges – Satisfaction ─────────────────────────
    with col4:
        st.markdown("""
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
            <span style="font-size:1.1rem;">📡</span>
            <span style="font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:0.95rem;
                         color:#E2E8F0;">Student Satisfaction Rate (Maharashtra, 2024)</span>
        </div>
        """, unsafe_allow_html=True)

        fig_gauge = go.Figure()
        for i, (mode, val, color) in enumerate([
            ("Online", 62, "#4F46E5"),
            ("Offline", 71, "#10B981"),
            ("Hybrid", 84, "#F59E0B"),
        ]):
            fig_gauge.add_trace(go.Indicator(
                mode="gauge+number",
                value=val,
                title={"text": mode, "font": {"color": color, "size": 13}},
                gauge={
                    "axis": {"range": [0, 100], "tickfont": {"color": "#475569", "size": 9}},
                    "bar": {"color": color, "thickness": 0.35},
                    "bgcolor": "#12121F",
                    "bordercolor": "#1E293B",
                    "borderwidth": 1,
                    "steps": [
                        {"range": [0, 50], "color": "#0A0A14"},
                        {"range": [50, 75], "color": "#0F0F1A"},
                        {"range": [75, 100], "color": "#12121F"},
                    ],
                },
                number={"suffix": "%", "font": {"color": color, "size": 20,
                                                 "family": "Space Grotesk"}},
                domain={"x": [i / 3, (i + 1) / 3 - 0.02], "y": [0, 1]},
            ))
        fig_gauge.update_layout(**CHART_TEMPLATE, height=380)
        st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Divider ────────────────────────────────────────────────
    st.markdown("""
    <div style="height:1px; background:linear-gradient(90deg, transparent, rgba(99,102,241,0.15), transparent);
                margin:8px 0 24px;"></div>
    """, unsafe_allow_html=True)

    # ── Hybrid Learning Deep Dive ─────────────────────────────
    st.markdown("""
    <div class="mm-section-title" style="font-size:1.25rem;">
        🔀 The Rise of Hybrid Learning
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="mm-card" style="margin-bottom:24px; border-left:3px solid #F59E0B;">
        <p style="font-size:1rem; line-height:1.85; color:#CBD5E1; margin:0 0 16px 0;">
        <strong style="color:#A5B4FC;">Hybrid Learning</strong> combines the best of both worlds —
        the <em>flexibility and resource richness of online platforms</em> with the
        <em>social engagement and structure of offline classrooms</em>.
        Post-COVID, this has emerged as the most psychologically healthy learning mode for most students
        in Pune's engineering and postgraduate ecosystem.
        </p>
        <div style="padding:14px 18px;
                    background:rgba(245,158,11,0.06); border-radius:10px;
                    border:1px solid rgba(245,158,11,0.15); font-size:0.9rem; color:#FCD34D;">
        📊 <strong>67% of Pune engineering students</strong> prefer a hybrid approach post-COVID —
        citing better work-life-study balance and reduced commute stress as key reasons.
        </div>
    </div>
    """, unsafe_allow_html=True)

    arch_cols = st.columns(3)
    archetypes = [
        ("🏆", "Overloaded Achievers",
         "Benefit from hybrid: use online for flexibility, offline for accountability",
         "#F59E0B", "rgba(245,158,11,0.06)"),
        ("💻", "Digital Natives",
         "Thrive online but need occasional offline anchor for collaboration",
         "#8B5CF6", "rgba(139,92,246,0.06)"),
        ("🤝", "Social Learners",
         "Need offline interaction but benefit from online resources for revision",
         "#10B981", "rgba(16,185,129,0.06)"),
    ]
    for col, (emoji, name, desc, color, bg) in zip(arch_cols, archetypes):
        with col:
            st.markdown(f"""
            <div class="mm-card" style="border-color:{color}20; text-align:center;
                        background: linear-gradient(160deg, {bg}, var(--bg-card));">
                <div style="font-size:2.2rem; margin-bottom:8px;
                            filter: drop-shadow(0 0 8px {color}30);">{emoji}</div>
                <div style="font-weight:700; color:{color}; margin:8px 0 8px;
                            font-family:'Space Grotesk',sans-serif; font-size:0.95rem;">{name}</div>
                <div style="font-size:0.83rem; color:#94A3B8; line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CTA ────────────────────────────────────────────────────
    col_btn = st.columns([1, 2, 1])
    with col_btn[1]:
        _cta_g = {
            "en": "📝 Take the Assessment Now →",
            "mr": "📝 आता मूल्यांकन करा →",
            "hi": "📝 अभी मूल्यांकन करें →"
        }
        if st.button(_cta_g.get(lang, _cta_g["en"]), key="global_cta", use_container_width=True):
            st.session_state.nav_page = "Assessment"
            st.rerun()

"""Page 7 – Teacher Dashboard: Class Upload + Individual Student Analysis"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from utils.translations import t


CHART_TMPL = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#CBD5E1", family="Inter"),
    margin=dict(l=16, r=16, t=36, b=16),
)


# ───────────────────────── Scoring Engine ───────────────────────
def score_student_row(row: dict, col_map: dict) -> dict:
    """Convert uploaded row to psychological scores using teacher-selected columns."""

    def get(field, default=0):
        mapped = col_map.get(field)
        if mapped and mapped in row:
            val = row[mapped]
            try:
                return float(val)
            except (ValueError, TypeError):
                # Handle categorical: convert common strings to numbers
                mapping = {
                    "low": 0.2, "moderate": 0.5, "high": 0.8, "critical": 1.0,
                    "never": 0, "sometimes": 1, "often": 2, "always": 3,
                    "yes": 1, "no": 0, "true": 1, "false": 0,
                }
                return mapping.get(str(val).lower(), default)
        return default

    stress_index = min(1.0, (
        get("stress_score", 0.5) * 0.3 +
        ((10 - get("sleep_hours", 7)) / 10) * 0.25 +
        get("overwhelm", 3) / 10 * 0.25 +
        (1 - get("sgpa", 7) / 10) * 0.20
    ))

    anxiety_level = min(100, (
        get("overwhelm", 3) * 9 +
        get("stress_score", 0.5) * 25 +
        (10 - get("sleep_hours", 7)) * 4
    ))

    motivation_score = max(0, min(100, (
        get("sgpa", 7) * 8 +
        get("study_hours", 4) * 4 +
        (5 - get("overwhelm", 3)) * 6 +
        20
    )))

    social_isolation = max(0, min(10, (
        10 - get("friends_count", 5) -
        get("social_freq", 2)
    )))

    overall_health = max(0, min(100, (
        motivation_score * 0.35 +
        (1 - stress_index) * 100 * 0.35 +
        get("sleep_hours", 7) / 9 * 100 * 0.30
    )))

    at_risk = 1 if (stress_index > 0.65 or overall_health < 40 or get("atkt", 0) > 0) else 0

    return {
        "stress_index": round(stress_index, 3),
        "stress_pct": round(stress_index * 100, 1),
        "anxiety_level": round(anxiety_level, 1),
        "motivation_score": round(motivation_score, 1),
        "social_isolation": round(social_isolation, 1),
        "overall_health": round(overall_health, 1),
        "at_risk": at_risk,
    }


def generate_student_recommendation(row_dict: dict, scores: dict, col_map: dict) -> str:
    """Generate a short text recommendation for one student."""
    name_col = col_map.get("name", "")
    name = row_dict.get(name_col, "Student") if name_col else "Student"
    at_risk = scores["at_risk"]
    stress = scores["stress_pct"]
    health = scores["overall_health"]
    mot = scores["motivation_score"]

    lines = [f"📋 {name} — Overall Health: {health}/100"]

    if at_risk:
        lines.append("⚠️ AT-RISK: Requires personal counsellor check-in within 2 weeks.")
    if stress > 65:
        lines.append(f"🔴 Stress {stress}% — Very high. Suggest workload adjustment and sleep hygiene counselling.")
    elif stress > 40:
        lines.append(f"🟡 Stress {stress}% — Moderate. Monitor and provide structured assignment deadlines.")
    else:
        lines.append(f"🟢 Stress {stress}% — Low. Keep up positive reinforcement.")

    if mot < 40:
        lines.append("🎯 Low Motivation — Consider 1-on-1 goal-setting session with mentor.")
    elif mot < 60:
        lines.append("🎯 Moderate Motivation — Encourage peer study groups and project-based work.")
    else:
        lines.append("🎯 High Motivation — Offer advanced/elective opportunities to channel energy.")

    if scores["social_isolation"] > 6:
        lines.append("👥 High Isolation — Assign to a peer study group or buddy programme.")

    return "\n".join(lines)


# ───────────────────────── Main Page ────────────────────────────
def show(lang: str = "en"):
    st.markdown(f"""
    <div class="mm-hero" style="margin-bottom:20px;">
        <div style="font-size:2rem;">🏫</div>
        <h2 style="font-family:'Space Grotesk',sans-serif;color:#A5B4FC;margin:8px 0 4px;font-size:1.6rem;">
            {t('teacher_title', lang)}
        </h2>
        <p style="color:#94A3B8;font-size:0.88rem;margin:0;">
            {t('teacher_sub', lang)}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["📤 Upload Class Data", "📊 Class Analysis", "👤 Individual Students"])

    # ═══════════════════════════════════════════════════════════
    with tab1:
        st.markdown("### Upload Your Class Dataset")
        st.markdown("""
        <div class="mm-card" style="margin-bottom:16px;">
        <strong>Instructions:</strong><br>
        1. Upload a <code>.csv</code> or <code>.xlsx</code> file with one row per student.<br>
        2. Map your column names to the fields below (you choose which columns correspond to what).<br>
        3. Even if your dataset only has some fields, the system will work with what's available.<br>
        4. All analysis is done locally — no student data leaves your device.
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload Class CSV / Excel",
            type=["csv", "xlsx"],
            key="teacher_upload",
            help="Supports .csv and .xlsx files. One row per student."
        )

        if uploaded_file:
            try:
                if uploaded_file.name.endswith(".xlsx"):
                    df = pd.read_excel(uploaded_file)
                else:
                    df = pd.read_csv(uploaded_file)

                st.success(f"✅ Loaded {len(df)} students, {len(df.columns)} columns")
                st.dataframe(df.head(5), use_container_width=True, height=200)

                st.markdown("### 🔗 Map Your Columns")
                st.markdown("<div style='color:#64748B;font-size:0.82rem;margin-bottom:10px;'>Select which columns in your file correspond to each field. Leave as '– Not in dataset –' if absent.</div>", unsafe_allow_html=True)

                cols = ["– Not in dataset –"] + list(df.columns)

                FIELDS = {
                    "name": "Student Name / Roll No",
                    "sgpa": "SGPA / Grade (numeric, e.g. 7.5)",
                    "study_hours": "Daily Study Hours (numeric)",
                    "sleep_hours": "Sleep Hours per Night (numeric)",
                    "stress_score": "Stress Score (0–1 or 0–10)",
                    "overwhelm": "Overwhelm / Anxiety Rating (0–5 or 0–10)",
                    "friends_count": "Number of Close Friends (numeric)",
                    "phone_hours": "Phone/Screen Hours per Day (numeric)",
                    "atkt": "ATKT / Backlog (0=No, 1=Yes)",
                    "social_freq": "Social Interaction Frequency (0–5 or daily/weekly etc.)",
                    "gender": "Gender Column",
                    "student_type": "Student Category (Engineering, Arts, etc.)",
                    "living_situation": "Living Situation (Home/Hostel/PG)",
                    "financial_stress": "Financial Stress (Low/Moderate/High)",
                }

                col_map = {}
                col_pairs = list(FIELDS.items())
                for i in range(0, len(col_pairs), 2):
                    c1, c2 = st.columns(2)
                    for col_widget, (field_key, field_label) in zip([c1, c2], col_pairs[i:i+2]):
                        with col_widget:
                            selected = st.selectbox(
                                field_label,
                                options=cols,
                                key=f"colmap_{field_key}",
                                index=0
                            )
                            if selected != "– Not in dataset –":
                                col_map[field_key] = selected

                st.markdown("<br>", unsafe_allow_html=True)

                if st.button("🔍 Analyse Class", key="run_analysis", use_container_width=True, type="primary"):
                    with st.spinner("Analysing all students..."):
                        results = []
                        for _, row in df.iterrows():
                            row_dict = row.to_dict()
                            sc = score_student_row(row_dict, col_map)
                            sc["_recommendation"] = generate_student_recommendation(row_dict, sc, col_map)

                            # Add original columns
                            name_col = col_map.get("name", "")
                            sc["_name"] = str(row_dict.get(name_col, f"Student_{_}")) if name_col else f"Student_{_}"
                            results.append(sc)

                        result_df = pd.DataFrame(results)
                        result_df.insert(0, "Student", result_df.pop("_name"))
                        result_df["Recommendation"] = result_df.pop("_recommendation")

                        st.session_state["teacher_df"] = result_df
                        st.session_state["teacher_raw_df"] = df
                        st.session_state["teacher_col_map"] = col_map
                        st.success(f"✅ Analysis complete for {len(result_df)} students!")
                        st.info("👆 Switch to the **Class Analysis** or **Individual Students** tab to view results.")

            except Exception as e:
                st.error(f"❌ Error reading file: {e}")
                import traceback
                st.code(traceback.format_exc())

        else:
            # Show demo with existing data
            st.markdown("---")
            st.markdown("### 📂 Or Use Our Demo Dataset (800 Pune Students)")
            if st.button("▶️ Load Demo Dataset & Analyse", key="demo_data", use_container_width=True):
                data_path = os.path.join(ROOT, "data", "student_data.csv")
                if os.path.exists(data_path):
                    df = pd.read_csv(data_path)
                    # Auto-map for demo data
                    demo_map = {
                        "name": "student_id" if "student_id" in df.columns else None,
                        "sgpa": "sgpa", "study_hours": "study_hours",
                        "sleep_hours": "sleep_hours", "stress_score": "stress_base",
                        "overwhelm": "overwhelm", "friends_count": "friends_count",
                        "phone_hours": "phone_hours", "atkt": "atkt",
                        "gender": "gender", "student_type": "student_type",
                    }
                    demo_map = {k: v for k, v in demo_map.items() if v and v in df.columns}

                    results = []
                    for idx, row in df.iterrows():
                        row_dict = row.to_dict()
                        sc = score_student_row(row_dict, demo_map)
                        sc["_recommendation"] = generate_student_recommendation(row_dict, sc, demo_map)
                        sc["_name"] = f"Student_{idx+1}"
                        if "student_type" in demo_map and demo_map["student_type"] in row_dict:
                            sc["_category"] = row_dict[demo_map["student_type"]]
                        results.append(sc)

                    result_df = pd.DataFrame(results)
                    result_df.insert(0, "Student", result_df.pop("_name"))
                    if "_category" in result_df.columns:
                        result_df.insert(1, "Category", result_df.pop("_category"))
                    result_df["Recommendation"] = result_df.pop("_recommendation")

                    st.session_state["teacher_df"] = result_df
                    st.session_state["teacher_raw_df"] = df
                    st.session_state["teacher_col_map"] = demo_map
                    st.success(f"✅ Demo analysis complete — {len(result_df)} students!")
                    st.info("👆 Switch to **Class Analysis** or **Individual Students** tab.")
                else:
                    st.error("Demo dataset not found. Please run `python generate_data_and_train.py` first.")

    # ═══════════════════════════════════════════════════════════
    with tab2:
        result_df = st.session_state.get("teacher_df")
        if result_df is None:
            st.info("📤 Please upload data in the first tab to see class analysis.")
            return

        st.markdown("### 📊 Class-Level Overview")

        n = len(result_df)
        at_risk_n = result_df["at_risk"].sum()
        high_stress_n = (result_df["stress_pct"] > 60).sum()
        avg_health = result_df["overall_health"].mean()
        avg_sleep_col = result_df.get("sleep_hours")  # may not exist in result_df

        m1, m2, m3, m4 = st.columns(4)
        for col, (val, label, color) in zip(
            [m1, m2, m3, m4],
            [
                (str(n), "Total Students", "#4F46E5"),
                (str(at_risk_n), "At-Risk Students ⚠️", "#F43F5E"),
                (str(high_stress_n), "High Stress (>60%)", "#F97316"),
                (f"{avg_health:.1f}/100", "Avg Overall Health", "#10B981" if avg_health >= 65 else "#F59E0B"),
            ]
        ):
            with col:
                st.markdown(f"""
                <div class="mm-card" style="text-align:center;border-color:{color}40;">
                    <div style="font-size:1.4rem;font-weight:800;color:{color};font-family:'Space Grotesk',sans-serif;">{val}</div>
                    <div style="font-size:0.75rem;color:#64748B;margin-top:4px;line-height:1.3;">{label}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)

        # Stress distribution
        with col_a:
            st.markdown("**Stress Level Distribution**")
            bins = [0, 30, 50, 70, 100]
            labels_s = ["Low (<30%)", "Moderate (30-50%)", "High (50-70%)", "Critical (>70%)"]
            colors_s = ["#10B981", "#F59E0B", "#F97316", "#F43F5E"]
            counts_s = pd.cut(result_df["stress_pct"], bins=bins, labels=labels_s).value_counts()
            fig_s = go.Figure(go.Bar(
                x=labels_s,
                y=[counts_s.get(l, 0) for l in labels_s],
                marker_color=colors_s,
                text=[counts_s.get(l, 0) for l in labels_s],
                textposition="outside",
                textfont=dict(color="#CBD5E1"),
            ))
            fig_s.update_layout(**CHART_TMPL, height=280,
                                xaxis=dict(showgrid=False, tickfont=dict(size=10)),
                                yaxis=dict(showgrid=True, gridcolor="#1E293B"))
            st.plotly_chart(fig_s, use_container_width=True)

        # Overall health distribution
        with col_b:
            st.markdown("**Overall Health Score Distribution**")
            fig_h = go.Figure(go.Histogram(
                x=result_df["overall_health"],
                nbinsx=20,
                marker_color="#4F46E5",
                opacity=0.85,
            ))
            fig_h.add_vline(x=result_df["overall_health"].mean(), line_dash="dot",
                            line_color="#F59E0B",
                            annotation_text=f"Avg: {result_df['overall_health'].mean():.1f}",
                            annotation_font_color="#F59E0B")
            fig_h.update_layout(**CHART_TMPL, height=280,
                                xaxis=dict(showgrid=False, title="Health Score"),
                                yaxis=dict(showgrid=True, gridcolor="#1E293B", title="Count"))
            st.plotly_chart(fig_h, use_container_width=True)

        # Category breakdown (if available)
        if "Category" in result_df.columns:
            st.markdown("**Stress by Student Category**")
            cat_stress = result_df.groupby("Category")["stress_pct"].mean().sort_values(ascending=True).reset_index()
            fig_cat = go.Figure(go.Bar(
                x=cat_stress["stress_pct"], y=cat_stress["Category"],
                orientation="h",
                marker=dict(
                    color=cat_stress["stress_pct"],
                    colorscale=[[0, "#10B981"], [0.5, "#F59E0B"], [1, "#F43F5E"]],
                    showscale=False,
                ),
                text=[f"{v:.1f}%" for v in cat_stress["stress_pct"]],
                textposition="outside",
                textfont=dict(color="#CBD5E1"),
            ))
            fig_cat.update_layout(**CHART_TMPL, height=300,
                                  xaxis=dict(showgrid=True, gridcolor="#1E293B", range=[0, 105]),
                                  yaxis=dict(showgrid=False))
            st.plotly_chart(fig_cat, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # At-risk table
        st.markdown("### 🚨 Priority List — Students Needing Attention")
        at_risk_df = result_df[result_df["at_risk"] == 1].copy()
        if len(at_risk_df) > 0:
            display_cols = ["Student"] + (["Category"] if "Category" in at_risk_df.columns else []) + [
                "overall_health", "stress_pct", "anxiety_level", "motivation_score", "social_isolation"
            ]
            display_cols = [c for c in display_cols if c in at_risk_df.columns]
            show_df = at_risk_df[display_cols].sort_values("overall_health").rename(columns={
                "overall_health": "Health", "stress_pct": "Stress%",
                "anxiety_level": "Anxiety", "motivation_score": "Motivation",
                "social_isolation": "Isolation"
            })
            st.dataframe(show_df, use_container_width=True, height=min(300, 40 + len(show_df)*38))
            st.caption(f"⚠️ {len(at_risk_df)} students flagged at-risk (anonymous IDs only — no real names stored)")
        else:
            st.success("✅ No students flagged at-risk based on uploaded data!")

        st.markdown("<br>", unsafe_allow_html=True)

        # Download full analysis
        st.markdown("### 📥 Export Full Class Report")
        export_df = result_df.drop(columns=["Recommendation"], errors="ignore")
        csv_bytes = export_df.to_csv(index=False).encode()
        st.download_button(
            "⬇️ Download Class Analysis CSV",
            data=csv_bytes,
            file_name="class_psychological_analysis.csv",
            mime="text/csv",
            use_container_width=True,
        )

        # Download at-risk list
        if len(at_risk_df) > 0:
            at_risk_csv = at_risk_df.drop(columns=["Recommendation"], errors="ignore").to_csv(index=False).encode()
            st.download_button(
                "⬇️ Download At-Risk Students List (CSV)",
                data=at_risk_csv,
                file_name="at_risk_students.csv",
                mime="text/csv",
                use_container_width=True,
            )

    # ═══════════════════════════════════════════════════════════
    with tab3:
        result_df = st.session_state.get("teacher_df")
        if result_df is None:
            st.info("📤 Please upload data in the first tab to see individual analysis.")
            return

        st.markdown("### 👤 Individual Student Deep Dive")
        st.markdown("<div style='color:#64748B;font-size:0.82rem;margin-bottom:12px;'>Search or browse individual students to see their full profile and personalised recommendations.</div>", unsafe_allow_html=True)

        col_search, col_sort = st.columns([2, 1])
        with col_search:
            search = st.text_input("🔍 Search student name / ID", key="student_search", placeholder="Type name or roll number...")
        with col_sort:
            sort_by = st.selectbox("Sort by", ["overall_health ↑ (needs help first)", "stress_pct ↓", "motivation_score ↑"],
                                   key="sort_students")

        # Filter and sort
        filtered = result_df.copy()
        if search:
            filtered = filtered[filtered["Student"].str.contains(search, case=False, na=False)]

        if "health ↑" in sort_by:
            filtered = filtered.sort_values("overall_health", ascending=True)
        elif "stress" in sort_by:
            filtered = filtered.sort_values("stress_pct", ascending=False)
        elif "motivation" in sort_by:
            filtered = filtered.sort_values("motivation_score", ascending=True)

        st.markdown(f"<div style='color:#64748B;font-size:0.8rem;margin-bottom:8px;'>Showing {len(filtered)} students</div>", unsafe_allow_html=True)

        # Paginate
        PAGE_SIZE = 10
        total_pages = max(1, (len(filtered) + PAGE_SIZE - 1) // PAGE_SIZE)
        page_num = st.number_input("Page", min_value=1, max_value=total_pages, value=1, key="student_page")
        page_df = filtered.iloc[(page_num-1)*PAGE_SIZE : page_num*PAGE_SIZE]

        for _, row in page_df.iterrows():
            health = row["overall_health"]
            stress = row["stress_pct"]
            at_risk = row["at_risk"]
            health_color = "#10B981" if health >= 65 else "#F59E0B" if health >= 45 else "#F43F5E"
            stress_color = "#10B981" if stress < 35 else "#F59E0B" if stress < 60 else "#F43F5E"
            risk_badge = "🔴 At-Risk" if at_risk else "🟢 OK"

            with st.expander(f"**{row['Student']}** — Health: {health:.0f}/100 | Stress: {stress:.0f}% | {risk_badge}"):
                cols = st.columns([1, 1, 1, 1, 2])
                mini_metrics = [
                    ("Health", f"{health:.0f}/100", health_color),
                    ("Stress", f"{stress:.0f}%", stress_color),
                    ("Anxiety", f"{row['anxiety_level']:.0f}/100", "#F59E0B"),
                    ("Motivation", f"{row['motivation_score']:.0f}/100", "#4F46E5"),
                ]
                for col, (label, val, color) in zip(cols[:4], mini_metrics):
                    with col:
                        st.markdown(f"""
                        <div style="text-align:center;padding:8px;background:rgba(255,255,255,0.03);
                                    border-radius:8px;border:1px solid {color}30;">
                            <div style="font-size:1rem;font-weight:700;color:{color};">{val}</div>
                            <div style="font-size:0.7rem;color:#64748B;">{label}</div>
                        </div>
                        """, unsafe_allow_html=True)

                with cols[4]:
                    st.markdown(f"""
                    <div style="background:rgba(255,255,255,0.03);border-radius:8px;
                                border:1px solid rgba(255,255,255,0.08);padding:10px 14px;">
                        <div style="font-size:0.75rem;font-weight:700;color:#818CF8;margin-bottom:4px;">
                            RECOMMENDATION
                        </div>
                        <div style="font-size:0.78rem;color:#CBD5E1;line-height:1.6;white-space:pre-line;">
                            {row.get('Recommendation','No recommendation.')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Full table export
        st.markdown("### 📥 Export Full Report with Recommendations")
        full_csv = result_df.to_csv(index=False).encode()
        st.download_button(
            "⬇️ Download Full Individual Report CSV",
            data=full_csv,
            file_name="individual_student_recommendations.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.info("🔒 Reminder: No data is uploaded to any server. All analysis is done locally in your browser session.")

"""
app.py – MindMap: Student Psychological Health Assessment
Single-page Streamlit app with multi-language sidebar navigation.
Supports: English | मराठी | हिंदी
Pages stored in /page_modules/ (NOT /pages/) to avoid Streamlit auto-nav conflicts.
"""
import streamlit as st
import os
import sys
import importlib

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from utils.translations import t, LANGUAGE_OPTIONS

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="MindMap – Student Psychological Health",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "MindMap – AI-Powered Student Psychological Assessment | Pune, Maharashtra"
    }
)

# ── Load CSS ──────────────────────────────────────────────────
def load_css():
    css_path = os.path.join(ROOT, "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ── Session state defaults ────────────────────────────────────
defaults = {
    "answers": {}, "scores": {}, "predictions": {}, "recs": {},
    "submitted": False, "current_section": 0, "nav_page": "Home",
    "teacher_df": None,
    "lang": "en",   # active language code
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

lang = st.session_state.lang   # short alias used throughout

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    # ── Brand ─────────────────────────────────────────────────
    st.markdown(f"""
    <div style="text-align:center; padding: 16px 0 14px;">
        <div style="font-size:2.5rem; filter: drop-shadow(0 0 12px rgba(99,102,241,0.3));
                    margin-bottom:4px;">🧠</div>
        <div style="font-family:'Space Grotesk',sans-serif; font-weight:700;
                    font-size:1.3rem; margin-top:6px;
                    background: linear-gradient(135deg, #C7D2FE, #A5B4FC, #818CF8);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">MindMap</div>
        <div style="font-size:0.7rem; color:#475569; margin-top:4px; letter-spacing:0.5px;">
            {t("app_tagline", lang)}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Language Selector ──────────────────────────────────────
    lang_label = t("select_language", lang)
    lang_names = list(LANGUAGE_OPTIONS.keys())   # ["English", "मराठी", "हिंदी"]
    lang_codes = list(LANGUAGE_OPTIONS.values())
    current_idx = lang_codes.index(lang) if lang in lang_codes else 0

    selected_lang_name = st.selectbox(
        lang_label,
        options=lang_names,
        index=current_idx,
        key="lang_selector",
        label_visibility="collapsed",
    )
    selected_code = LANGUAGE_OPTIONS[selected_lang_name]
    if selected_code != st.session_state.lang:
        st.session_state.lang = selected_code
        lang = selected_code
        st.rerun()

    # ── Inline flag+name display ───────────────────────────────
    flags = {"en": "🇬🇧 English", "mr": "🇮🇳 मराठी", "hi": "🇮🇳 हिंदी"}
    st.markdown(
        f"<div style='text-align:center;font-size:0.75rem;color:#6366F1;margin-bottom:6px;'>"
        f"{flags.get(lang,'🌐')}</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ── Nav buttons ────────────────────────────────────────────
    NAV_PAGES = [
        ("nav_home",       "Home"),
        ("nav_global",     "Global"),
        ("nav_assessment", "Assessment"),
        ("nav_results",    "Results"),
        ("nav_report",     "Report"),
        ("nav_parent",     "Parent"),
        ("nav_teacher",    "Teacher"),
    ]

    for key_str, page_key in NAV_PAGES:
        is_active = st.session_state.nav_page == page_key
        label = t(key_str, lang)
        if st.button(label, key=f"nav_{page_key}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.nav_page = page_key
            st.rerun()

    st.markdown("---")

    # ── Student status ─────────────────────────────────────────
    if st.session_state.submitted:
        name = st.session_state.answers.get("name", "Student")
        st.success(f"✅ {name}")
        if st.session_state.scores:
            health = st.session_state.scores.get("overall_health", 0)
            color = "#10B981" if health >= 70 else "#F59E0B" if health >= 45 else "#F43F5E"
            st.markdown(
                f"<div style='color:{color};font-weight:700;font-size:1rem;'>"
                f"💚 {t('score',lang)}: {health}/100</div>",
                unsafe_allow_html=True
            )
    else:
        st.caption(t("take_assessment_hint", lang))

    st.markdown("---")
    footer_lines = t("not_clinical", lang).replace("\n", "<br>")
    st.markdown(
        f"<div style='font-size:0.65rem;color:#475569;text-align:center;'>{footer_lines}</div>",
        unsafe_allow_html=True
    )

# ── Page loader ───────────────────────────────────────────────
def _load_page(module_name: str):
    full_name = f"page_modules.{module_name}"
    if full_name in sys.modules:
        mod = importlib.reload(sys.modules[full_name])
    else:
        mod = importlib.import_module(full_name)
    return mod

def _require_assessment():
    st.warning(t("complete_assessment_first", lang))
    st.info(t("click_assessment_hint", lang))

# ── Routing ───────────────────────────────────────────────────
page = st.session_state.get("nav_page", "Home")

try:
    if page == "Home":
        _load_page("page_01_information").show(lang=lang)
    elif page == "Global":
        _load_page("page_02_global_context").show(lang=lang)
    elif page == "Assessment":
        _load_page("page_03_assessment").show(lang=lang)
    elif page == "Results":
        if not st.session_state.submitted:
            _require_assessment()
        else:
            _load_page("page_04_results").show(lang=lang)
    elif page == "Report":
        if not st.session_state.submitted:
            _require_assessment()
        else:
            _load_page("page_05_report").show(lang=lang)
    elif page == "Parent":
        _load_page("page_06_parent_view").show(lang=lang)
    elif page == "Teacher":
        _load_page("page_07_teacher_view").show(lang=lang)
    else:
        st.error(f"Unknown page: {page}")
except Exception as e:
    st.error(f"❌ Page load error on '{page}': {e}")
    import traceback
    st.code(traceback.format_exc(), language="python")

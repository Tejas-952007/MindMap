"""Page 1 – Information Hub: Online vs. Offline Learning (Enhanced UI)"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.translations import t


def show(lang: str = "en"):
    # determine translated subtitle lines
    _sub_lines = t("home_subtitle", lang).split("\n")
    _sub_html = "<br>".join(
        f'<strong style="color:#A5B4FC;">{l[2:-2]}</strong>' if l.startswith("**") and l.endswith("**") else l
        for l in _sub_lines
    )
    _stats = {
        "en": ["📊 800+ Student Profiles Analysed", "🤖 ML-Powered Insights", "🔒 Privacy-First Design", "🌐 Multilingual Support"],
        "mr": ["📊 ८००+ विद्यार्थी प्रोफाइल", "🤖 ML-चालित अंतर्दृष्टी", "🔒 गोपनीयता-प्रथम", "🌐 बहुभाषिक समर्थन"],
        "hi": ["📊 ८००+ छात्र प्रोफाइल", "🤖 ML-संचालित अंतर्दृष्टि", "🔒 गोपनीयता-प्रथम", "🌐 बहुभाषिक समर्थन"],
    }
    _stat_html = " ".join(f'<span class="mm-stat">{s}</span>' for s in _stats.get(lang, _stats["en"]))

    # ── Enhanced Hero Section ──────────────────────────────────
    st.markdown(f"""
    <div class="mm-hero" style="position:relative;">
        <div style="font-size:4rem; margin-bottom:12px; position:relative; z-index:1;
                    filter: drop-shadow(0 0 20px rgba(99,102,241,0.3));">🧠</div>
        <h1>{t('home_title', lang)}</h1>
        <p class="subtitle">{_sub_html}</p>
        <div style="display:flex; flex-wrap:wrap; justify-content:center; gap:8px; position:relative; z-index:1;">
            {_stat_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Multilingual tagline cards ─────────────────────────────
    col1, col2, col3 = st.columns(3)

    lang_cards = [
        ("🇮🇳", "मराठी:", "विद्यार्थ्यांसाठी मनोवैज्ञानिक विश्लेषण", "#F59E0B"),
        ("📖", "English:", "AI Psychological Health Assessment", "#818CF8"),
        ("🌐", "हिन्दी:", "ऑनलाइन बनाम ऑफलाइन शिक्षा विश्लेषण", "#06B6D4"),
    ]
    for col, (emoji, label, desc, accent) in zip([col1, col2, col3], lang_cards):
        with col:
            st.markdown(f"""
            <div class="mm-card" style="text-align:center; padding:24px 18px;">
                <div style="font-size:2rem; margin-bottom:8px;
                            filter: drop-shadow(0 0 8px rgba(99,102,241,0.2));">{emoji}</div>
                <div style="font-size:0.88rem; color:#CBD5E1; margin-top:8px;">
                    <strong style="color:{accent}; font-size:0.95rem;">{label}</strong><br>
                    <span style="color:#94A3B8; font-size:0.85rem; line-height:1.5;">{desc}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── What is MindMap ────────────────────────────────────────
    st.markdown(f'<div class="mm-section-title">🎯 {t("what_is_mindmap", lang)}</div>', unsafe_allow_html=True)
    _desc = t("mindmap_desc", lang)
    import re
    _desc_html = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color:#A5B4FC;">\1</strong>', _desc)
    _desc_html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', _desc_html)
    st.markdown(f"""
    <div class="mm-card" style="border-left: 3px solid #4F46E5;">
        <p style="font-size:1.02rem; line-height:1.85; color:#CBD5E1; margin:0;">{_desc_html}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Comparison cards ───────────────────────────────────────
    _ovoff = {
        "en": "📚 Online vs. Offline Learning",
        "mr": "📚 ऑनलाइन वि. ऑफलाइन शिक्षण",
        "hi": "📚 ऑनलाइन बनाम ऑफलाइन शिक्षण"
    }
    st.markdown(f'<div class="mm-section-title">{_ovoff.get(lang, _ovoff["en"])}</div>', unsafe_allow_html=True)

    col_on, col_off = st.columns(2)

    with col_on:
        st.markdown("""
        <div class="compare-card compare-online">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
                <div style="font-size:2.2rem; filter: drop-shadow(0 0 8px rgba(79,70,229,0.3));">💻</div>
                <div style="font-size:1.2rem; font-weight:700; color:#A5B4FC;
                            font-family:'Space Grotesk',sans-serif;">Online Learning</div>
            </div>
            <div style="margin-bottom:18px;">
                <div style="font-weight:700; color:#818CF8; margin-bottom:10px; font-size:0.9rem;
                            display:flex; align-items:center; gap:6px;">
                    <span style="background:#818CF820; padding:2px 8px; border-radius:6px;">✅ Advantages</span>
                </div>
                <ul style="color:#CBD5E1; line-height:2; padding-left:18px; margin:0; font-size:0.9rem;">
                    <li>Flexible scheduling — study at your own pace</li>
                    <li>Access to global resources (Coursera, YouTube, MIT OCW)</li>
                    <li>Cost-effective — save on commute and materials</li>
                    <li>Recordings available for revision anytime</li>
                    <li>Suits introverts and self-motivated learners</li>
                </ul>
            </div>
            <div>
                <div style="font-weight:700; color:#F87171; margin-bottom:10px; font-size:0.9rem;
                            display:flex; align-items:center; gap:6px;">
                    <span style="background:#F8717120; padding:2px 8px; border-radius:6px;">⚠️ Challenges</span>
                </div>
                <ul style="color:#CBD5E1; line-height:2; padding-left:18px; margin:0; font-size:0.9rem;">
                    <li>Isolation and reduced peer interaction</li>
                    <li>Screen fatigue and eye strain</li>
                    <li>Requires high self-discipline</li>
                    <li>Technical issues disrupting learning</li>
                    <li>Prone to distraction at home</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_off:
        st.markdown("""
        <div class="compare-card compare-offline">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
                <div style="font-size:2.2rem; filter: drop-shadow(0 0 8px rgba(16,185,129,0.3));">🏫</div>
                <div style="font-size:1.2rem; font-weight:700; color:#34D399;
                            font-family:'Space Grotesk',sans-serif;">Offline Learning</div>
            </div>
            <div style="margin-bottom:18px;">
                <div style="font-weight:700; color:#34D399; margin-bottom:10px; font-size:0.9rem;
                            display:flex; align-items:center; gap:6px;">
                    <span style="background:#34D39920; padding:2px 8px; border-radius:6px;">✅ Advantages</span>
                </div>
                <ul style="color:#CBD5E1; line-height:2; padding-left:18px; margin:0; font-size:0.9rem;">
                    <li>Face-to-face interaction with teachers</li>
                    <li>Structured environment with timetable</li>
                    <li>Peer learning and social development</li>
                    <li>Immediate doubt clarification</li>
                    <li>Better for hands-on subjects (Engineering labs, Medical)</li>
                </ul>
            </div>
            <div>
                <div style="font-weight:700; color:#F87171; margin-bottom:10px; font-size:0.9rem;
                            display:flex; align-items:center; gap:6px;">
                    <span style="background:#F8717120; padding:2px 8px; border-radius:6px;">⚠️ Challenges</span>
                </div>
                <ul style="color:#CBD5E1; line-height:2; padding-left:18px; margin:0; font-size:0.9rem;">
                    <li>Commute stress and time loss</li>
                    <li>Fixed schedule — less flexibility</li>
                    <li>One-size-fits-all teaching pace</li>
                    <li>Peer pressure and comparison anxiety</li>
                    <li>Higher financial cost (hostel, transport, materials)</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Research insights ──────────────────────────────────────
    _res = {
        "en": "📈 India-Specific Research Insights",
        "mr": "📈 भारत-विशिष्ट संशोधन अंतर्दृष्टी",
        "hi": "📈 भारत-विशिष्ट शोध अंतर्दृष्टि"
    }
    st.markdown(f'<div class="mm-section-title">{_res.get(lang, _res["en"])}</div>', unsafe_allow_html=True)

    metrics_cols = st.columns(4)
    _stat_data = {
        "en": [("67%", "Pune engineering students prefer\nHybrid post-COVID", "#4F46E5", "📊"),
               ("1 in 3", "Indian students report academic\nstress weekly", "#F43F5E", "⚡"),
               ("₹12,000", "Average annual savings with\nonline learning (India)", "#10B981", "💰"),
               ("48%", "Students perform better with\npersonalised learning plans", "#F59E0B", "🎯")],
        "mr": [("67%", "पुण्यातील इंजिनियरिंग विद्यार्थी\nHybrid पसंत करतात", "#4F46E5", "📊"),
               ("३ पैकी १", "भारतीय विद्यार्थ्यांना साप्ताहिक\nशैक्षणिक ताण जाणवतो", "#F43F5E", "⚡"),
               ("₹१२,०००", "ऑनलाइन शिक्षणाने वार्षिक\nबचत (भारत)", "#10B981", "💰"),
               ("48%", "वैयक्तिक शिक्षण योजनांमुळे\nचांगली कामगिरी", "#F59E0B", "🎯")],
        "hi": [("67%", "पुणे के इंजीनियरिंग छात्र\nHybrid पसंद करते हैं", "#4F46E5", "📊"),
               ("3 में से 1", "भारतीय छात्रों को साप्ताहिक\nशैक्षणिक तनाव होता है", "#F43F5E", "⚡"),
               ("₹12,000", "ऑनलाइन सीखने से वार्षिक\nबचत (भारत)", "#10B981", "💰"),
               ("48%", "व्यक्तिगत योजनाओं से\nबेहतर प्रदर्शन", "#F59E0B", "🎯")],
    }
    stats = _stat_data.get(lang, _stat_data["en"])
    for col, (val, label, color, icon) in zip(metrics_cols, stats):
        with col:
            label_br = label.replace("\n", "<br>")
            st.markdown(f"""
            <div class="mm-card" style="text-align:center; border-color: {color}25; padding:24px 16px;">
                <div style="font-size:1.5rem; margin-bottom:10px;
                            filter: drop-shadow(0 0 6px {color}40);">{icon}</div>
                <div style="font-size:1.8rem; font-weight:800; color:{color};
                            font-family:'Space Grotesk',sans-serif; line-height:1.2;">{val}</div>
                <div style="font-size:0.8rem; color:#94A3B8; margin-top:8px;
                            line-height:1.5;">{label_br}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Animated quote ─────────────────────────────────────────
    st.markdown("""
    <div class="mm-quote" style="text-align:center; font-size:1.1rem; padding:24px 28px;">
        <em>"The best learning method is the one that fits <strong>your mind</strong>, not the trend."</em>
        <br><span style="font-size:0.82rem; color:#64748B; margin-top:10px; display:block; font-style:normal;">
        — MindMap Principle
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── How it works ───────────────────────────────────────────
    _how = {
        "en": "🔬 How MindMap Works",
        "mr": "🔬 MindMap कसे काम करते",
        "hi": "🔬 MindMap कैसे काम करता है"
    }
    st.markdown(f'<div class="mm-section-title">{_how.get(lang, _how["en"])}</div>', unsafe_allow_html=True)

    steps_cols = st.columns(4)
    _steps_data = {
        "en": [("1", "📝", "Take Assessment", "Answer 33 indirect questions about your lifestyle and habits", "#4F46E5"),
               ("2", "🤖", "AI Analysis", "Our ML model analyses your responses across 7 psychological dimensions", "#7C3AED"),
               ("3", "👤", "Personal Profile", "Receive your learning mode recommendation + student archetype", "#06B6D4"),
               ("4", "🗺️", "Action Plan", "Get a 90-day personalised roadmap to unlock your full potential", "#10B981")],
        "mr": [("1", "📝", "मूल्यांकन करा", "तुमच्या जीवनशैलीबद्दल ३३ अप्रत्यक्ष प्रश्नांची उत्तरे द्या", "#4F46E5"),
               ("2", "🤖", "AI विश्लेषण", "आमचे ML मॉडेल ७ मनोवैज्ञानिक आयामांवर तुमचे उत्तर विश्लेषण करते", "#7C3AED"),
               ("3", "👤", "वैयक्तिक प्रोफाइल", "तुमची शिकण्याची पद्धत शिफारस + विद्यार्थी आर्किटाइप मिळवा", "#06B6D4"),
               ("4", "🗺️", "कृती योजना", "तुमची क्षमता अनलॉक करण्यासाठी ९०-दिवसांचा रोडमॅप मिळवा", "#10B981")],
        "hi": [("1", "📝", "मूल्यांकन करें", "अपनी जीवनशैली के बारे में 33 अप्रत्यक्ष प्रश्नों के उत्तर दें", "#4F46E5"),
               ("2", "🤖", "AI विश्लेषण", "हमारा ML मॉडेल 7 मनोवैज्ञानिक आयामों में आपके उत्तरों का विश्लेषण करता है", "#7C3AED"),
               ("3", "👤", "व्यक्तिगत प्रोफाइल", "अपनी शिक्षण मोड सिफारिश + छात्र आर्किटाइप प्राप्त करें", "#06B6D4"),
               ("4", "🗺️", "कार्य योजना", "अपनी पूरी क्षमता को अनलॉक करने के लिए 90-दिवसीय रोडमैप पाएं", "#10B981")],
    }
    steps = _steps_data.get(lang, _steps_data["en"])
    for col, (num, icon, title, desc, color) in zip(steps_cols, steps):
        with col:
            st.markdown(f"""
            <div class="mm-step-card" style="border-color:{color}20;">
                <div style="width:36px; height:36px; border-radius:50%; margin:0 auto 12px;
                            background: linear-gradient(135deg, {color}, {color}CC);
                            display:flex; align-items:center; justify-content:center;
                            font-weight:800; font-size:0.9rem; color:white;
                            box-shadow: 0 4px 12px {color}40;">{num}</div>
                <div style="font-size:1.6rem; margin-bottom:8px;">{icon}</div>
                <div style="font-weight:700; color:{color}; margin-bottom:8px;
                            font-family:'Space Grotesk',sans-serif; font-size:0.95rem;">{title}</div>
                <div style="font-size:0.82rem; color:#94A3B8; line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Disclaimer ─────────────────────────────────────────────
    _disc = {
        "en": "⚠️ <strong>Disclaimer:</strong> This is not a clinical psychological test. All results are intended for self-reflection and educational guidance only. Please consult a qualified mental health professional.",
        "mr": "⚠️ <strong>अस्वीकरण:</strong> ही वैद्यकीय मनोवैज्ञानिक चाचणी नाही. सर्व निकाल केवळ स्व-विचार आणि शैक्षणिक मार्गदर्शनासाठी आहेत. कृपया पात्र मानसिक आरोग्य व्यावसायिकाचा सल्ला घ्या.",
        "hi": "⚠️ <strong>अस्वीकरण:</strong> यह नैदानिक मनोवैज्ञानिक परीक्षण नहीं है। सभी परिणाम केवल आत्म-चिंतन और शैक्षणिक मार्गदर्शन के लिए हैं। कृपया योग्य मानसिक स्वास्थ्य पेशेवर से परामर्श लें।",
    }
    st.markdown(f"""
    <div style="background: rgba(245,158,11,0.06); border: 1px solid rgba(245,158,11,0.2);
                border-left: 3px solid #F59E0B;
                border-radius:12px; padding:16px 20px; font-size:0.85rem; color:#FCD34D;">
        {_disc.get(lang, _disc['en'])}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CTA Button ─────────────────────────────────────────────
    col_btn = st.columns([1, 2, 1])
    with col_btn[1]:
        _cta = {
            "en": "🚀 Find My Learning Style →",
            "mr": "🚀 माझी शिकण्याची पद्धत शोधा →",
            "hi": "🚀 मेरी शिक्षण शैली खोजें →"
        }
        if st.button(_cta.get(lang, _cta["en"]), key="cta_btn", use_container_width=True):
            st.session_state.nav_page = "Assessment"
            st.rerun()

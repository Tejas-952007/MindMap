"""Page 3 – Student Assessment Questionnaire (33 questions across 5 sections)"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.translations import t


def show(lang: str = "en"):
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:24px;">
        <h2 style="font-family:'Space Grotesk',sans-serif; color:#A5B4FC; margin:0;">
            {t('assessment_title', lang)}
        </h2>
        <p style="color:#64748B; font-size:0.9rem; margin-top:6px;">
            {t('assessment_subtitle', lang)}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Disclaimer
    st.markdown(f"""
    <div style="background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.3);
                border-radius:10px;padding:10px 16px;font-size:0.83rem;color:#FCD34D;margin-bottom:20px;">
    {t('privacy_note', lang)}
    </div>
    """, unsafe_allow_html=True)

    # Progress tracker
    tabs = st.tabs([t("tab_about", lang), t("tab_study", lang), t("tab_daily", lang),
                    t("tab_activity", lang), t("tab_future", lang)])

    # ── Section A: About You ──────────────────────────────────
    with tabs[0]:
        st.markdown(f"#### {t('about_you_header', lang)}")
        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input(f"1. {t('q_name', lang)}", value=st.session_state.answers.get("name", ""),
                                 placeholder=t('q_name_ph', lang), key="q_name")
        with c2:
            _g_opts = [t("opt_male",lang), t("opt_female",lang), t("opt_other",lang), t("opt_prefer_not",lang)]
            _g_orig = ["Male", "Female", "Other", "Prefer not to say"]
            _g_stored = st.session_state.answers.get("gender", "Male")
            _g_idx = _g_orig.index(_g_stored) if _g_stored in _g_orig else 0
            gender_label = st.radio(f"2. {t('q_gender', lang)}", _g_opts,
                              index=_g_idx, horizontal=True, key="q_gender")
            gender = _g_orig[_g_opts.index(gender_label)]

        c3, c4 = st.columns(2)
        with c3:
            edu_opts = ["School (9th-10th)", "School (11th-12th)", "UG Engineering/Technology",
                        "UG Arts/Commerce/Science", "Postgraduate (MBA/MSc/MA)", "Working Professional"]
            edu_level = st.selectbox(f"3. {t('q_education', lang)}",
                                     edu_opts,
                                     index=edu_opts.index(st.session_state.answers.get("education_level", edu_opts[2])),
                                     key="q_edu")
        with c4:
            branch = st.text_input(f"4. {t('q_branch', lang)}",
                                   value=st.session_state.answers.get("branch", ""),
                                   placeholder=t('q_branch_ph', lang),
                                   key="q_branch")

        c5, c6 = st.columns(2)
        with c5:
            living_opts = ["Home", "Hostel", "PG (Paying Guest)", "Relatives"]
            living = st.selectbox(f"16. {t('q_living', lang)}", living_opts,
                                  index=living_opts.index(st.session_state.answers.get("living_situation","Home")),
                                  key="q_living")
        with c6:
            fin_opts = ["Very Comfortable", "Comfortable", "Moderate", "Tight", "Financially Struggling"]
            financial = st.select_slider(f"17. {t('q_financial', lang)}",
                                         options=fin_opts,
                                         value=st.session_state.answers.get("financial_stress","Moderate"),
                                         key="q_fin")

        st.markdown(f'<div style="color:#64748B;font-size:0.8rem;margin-top:12px;">{t("privacy_small", lang)}</div>',
        unsafe_allow_html=True)

    # ── Section B: Study Habits ───────────────────────────────
    with tabs[1]:
        st.markdown(f"#### {t('study_header', lang)}")
        st.markdown("<br>", unsafe_allow_html=True)

        study_hours = st.slider(f"5. {t('q_study_hours', lang)}",
                                0, 12, st.session_state.answers.get("study_hours", 4),
                                step=1, format="%d hrs", key="q_study_hrs")

        attend_hours = st.number_input(f"6. {t('q_attend', lang)}",
                                       min_value=0, max_value=60,
                                       value=st.session_state.answers.get("attend_hours", 18),
                                       step=1, key="q_attend")

        st.markdown("**7. When you study, which method works best for you?** *(Select all that apply)*")
        methods_all = ["Notes (handwritten)", "PDF / Digital Notes", "Textbooks", "Recorded Lectures",
                       "Online Videos (YouTube etc.)", "Peer Teaching", "Flashcards / Revision Cards"]
        saved_methods = st.session_state.answers.get("study_methods", [])
        study_methods = []
        method_cols = st.columns(4)
        for i, m in enumerate(methods_all):
            with method_cols[i % 4]:
                if st.checkbox(m, value=(m in saved_methods), key=f"method_{i}"):
                    study_methods.append(m)

        c7, c8 = st.columns(2)
        with c7:
            sgpa = st.number_input("14. Your recent SGPA / Percentage",
                                   min_value=0.0, max_value=10.0,
                                   value=float(st.session_state.answers.get("sgpa", 7.0)),
                                   step=0.1, format="%.1f", key="q_sgpa")
        with c8:
            atkt = st.radio("14b. Do you have any ATKT / backlog?", ["No", "Yes"],
                            index=0 if not st.session_state.answers.get("atkt", 0) else 1,
                            horizontal=True, key="q_atkt")

        friends_count = st.number_input("15. How many close friends do you have in your class?",
                                        min_value=0, max_value=30,
                                        value=int(st.session_state.answers.get("friends_count", 5)),
                                        step=1, key="q_friends")

        st.markdown("**8. When you explain a topic to a friend, how comfortable do you feel?**")
        conf_emojis = ["😰 Very nervous", "😟 A bit unsure", "😐 Neutral", "🙂 Comfortable", "😄 Very confident"]
        confidence = st.select_slider("", options=conf_emojis,
                                      value=st.session_state.answers.get("confidence_label",
                                                                          conf_emojis[2]),
                                      key="q_conf")
        conf_val = conf_emojis.index(confidence) + 1

        c9, c10 = st.columns(2)
        with c9:
            note_style = st.radio("9. Do you prefer making your own notes or reading readymade notes?",
                                  ["Making my own notes", "Readymade/printed notes", "Both equally"],
                                  index=["Making my own notes","Readymade/printed notes","Both equally"].index(
                                      st.session_state.answers.get("note_style","Both equally")),
                                  key="q_note_style")
        with c10:
            st.markdown("**9b. When you hear a lecture, how engaged do you feel?**")
            engage_emojis = ["😴 Very distracted", "😑 Mostly distracted", "😐 Sometimes focused",
                             "🙂 Usually engaged", "🤩 Fully engaged"]
            engagement = st.select_slider("", options=engage_emojis,
                                          value=st.session_state.answers.get("engagement_label",
                                                                              engage_emojis[2]),
                                          key="q_engage")
            engage_val = engage_emojis.index(engagement) + 1

        st.markdown("**10. What makes you sit and study even when you don't feel like it?**")
        motivation_opts = ["Exam pressure / deadlines", "Career goals", "Parental expectations",
                           "Competitive spirit", "Genuine curiosity / love for subject",
                           "Fear of failure", "Friends studying around me", "Nothing really motivates me"]
        saved_motiv = st.session_state.answers.get("motivators", [])
        motivators = []
        motiv_cols = st.columns(4)
        for i, opt in enumerate(motivation_opts):
            with motiv_cols[i % 4]:
                if st.checkbox(opt, value=(opt in saved_motiv), key=f"motiv_{i}"):
                    motivators.append(opt)

        c11, c12 = st.columns(2)
        with c11:
            goal_freq_opts = ["Never", "Rarely", "Sometimes", "Often", "Always"]
            goal_freq = st.select_slider("10b. How often do you set weekly study goals?",
                                         options=goal_freq_opts,
                                         value=st.session_state.answers.get("goal_setting_freq","Sometimes"),
                                         key="q_goal_freq")
        with c12:
            env_opts = ["School/College Classroom", "Coaching Institute",
                        "Self-study at Home", "Library", "Cafe / Co-working Space"]
            study_env = st.selectbox("18. In which environment did your studies go best?",
                                     env_opts,
                                     index=env_opts.index(st.session_state.answers.get("study_env",
                                                                                        env_opts[2])),
                                     key="q_env")

    # ── Section C+D: Daily Life ───────────────────────────────
    with tabs[2]:
        st.markdown(f"#### {t('daily_header', lang)}")
        st.markdown("""<div style="color:#64748B;font-size:0.83rem;margin-bottom:16px;">
        💡 These questions help us understand your energy levels and daily patterns.</div>""",
        unsafe_allow_html=True)

        sleep_hours = st.slider("29. On average, how many hours of sleep do you get per night?",
                                2, 12, st.session_state.answers.get("sleep_hours", 7),
                                format="%d hrs", key="q_sleep")

        phone_hours = st.slider("27. How many hours per day do you spend on your phone (for non-study activities)?",
                                0, 12, st.session_state.answers.get("phone_hours", 3),
                                format="%d hrs", key="q_phone")

        st.markdown("**11. How often do you have difficulty falling asleep because your mind is too active?**")
        sleep_race_opts = ["Never", "Sometimes", "Often", "Always"]
        sleep_race_emojis = ["😴 Never", "🤔 Sometimes", "😟 Often", "😰 Always"]
        sleep_race = st.select_slider("",
                                      options=sleep_race_emojis,
                                      value=st.session_state.answers.get("sleep_racing_label","🤔 Sometimes"),
                                      key="q_sleep_race")
        sleep_race_val = sleep_race_emojis.index(sleep_race)
        sleep_race_text = sleep_race_opts[sleep_race_val]

        c13, c14 = st.columns(2)
        with c13:
            exam_feel = st.radio("11b. On exam days, you usually feel...",
                                 ["🧠 Sharp and ready", "😶 Blank and scattered"],
                                 index=st.session_state.answers.get("exam_blank", 0),
                                 key="q_exam_feel")
        with c14:
            friday_opts = ["Energised", "Relieved", "Neutral", "Tired but okay", "Exhausted and drained"]
            friday_emojis = ["⚡ Energised", "😊 Relieved", "😐 Neutral",
                             "😩 Tired but okay", "😵 Exhausted and drained"]
            friday_mood = st.selectbox("13. After a full week of college, how do you feel on Friday evening?",
                                       friday_emojis,
                                       index=friday_emojis.index(
                                           st.session_state.answers.get("friday_label", friday_emojis[2])),
                                       key="q_friday")
            friday_idx = friday_emojis.index(friday_mood)

        st.markdown("**12b. When you have many tasks at once, how do you typically feel?**")
        overwhelm_emojis = ["😌 Calm & organised", "🙂 Slightly pressured",
                            "😤 Quite stressed", "😰 Very overwhelmed", "🤯 Completely overwhelmed"]
        overwhelm = st.select_slider("",
                                     options=overwhelm_emojis,
                                     value=st.session_state.answers.get("overwhelm_label",
                                                                         overwhelm_emojis[1]),
                                     key="q_overwhelm")
        overwhelm_val = overwhelm_emojis.index(overwhelm) + 1

        c15, c16 = st.columns(2)
        with c15:
            self_doubt_opts = ["No, I believe them", "Sometimes", "Yes, I doubt them"]
            self_doubt_emojis = ["✅ No, I believe them", "🤔 Sometimes", "😟 Yes, I doubt them"]
            self_doubt = st.radio("20. When someone praises your work, do you believe them?",
                                  self_doubt_emojis,
                                  index=self_doubt_emojis.index(
                                      st.session_state.answers.get("self_doubt_label",
                                                                    self_doubt_emojis[0])),
                                  key="q_self_doubt")
            self_doubt_idx = self_doubt_emojis.index(self_doubt)

        with c16:
            workload_freq_opts = ["Rarely", "Sometimes", "Often", "Almost always"]
            workload_emojis = ["😌 Rarely", "🤔 Sometimes", "😔 Often", "😰 Almost always"]
            workload_freq = st.radio("21. How often do you feel your workload is too much to handle alone?",
                                     workload_emojis,
                                     index=workload_emojis.index(
                                         st.session_state.answers.get("workload_label",
                                                                       workload_emojis[1])),
                                     key="q_workload")
            workload_idx = workload_emojis.index(workload_freq) + 1

        c17, c18 = st.columns(2)
        with c17:
            st.markdown("**13b. Do you feel you have enough time in a day to do what you want?**")
            time_emojis = ["😩 Never enough", "😟 Rarely", "😐 Sometimes", "🙂 Usually", "😄 Always enough"]
            time_enough = st.select_slider("",
                                           options=time_emojis,
                                           value=st.session_state.answers.get("time_enough_label",
                                                                               time_emojis[2]),
                                           key="q_time")
            time_val = time_emojis.index(time_enough) + 1

        with c18:
            social_freq_opts = ["Rarely (monthly or less)", "Occasionally (a few times/month)",
                                "Regularly (weekly)", "Daily"]
            social_freq = st.selectbox("28. How often do you hang out with friends/family outside academics?",
                                       social_freq_opts,
                                       index=social_freq_opts.index(
                                           st.session_state.answers.get("social_freq",
                                                                         social_freq_opts[1])),
                                       key="q_social_freq")
            social_freq_val = social_freq_opts.index(social_freq) + 1

    # ── Section E: Activities ─────────────────────────────────
    with tabs[3]:
        st.markdown(f"#### {t('activity_header', lang)}")
        st.markdown("<br>", unsafe_allow_html=True)

        c19, c20 = st.columns(2)
        with c19:
            internship = st.radio("23. Do you currently have an internship?", ["No", "Yes"],
                                  index=0 if not st.session_state.answers.get("has_internship", 0) else 1,
                                  horizontal=True, key="q_intern")
        with c20:
            part_job = st.radio("25. Do you have a part-time job?", ["No", "Yes"],
                                index=0 if not st.session_state.answers.get("has_job", 0) else 1,
                                horizontal=True, key="q_job")

        c21, c22 = st.columns(2)
        with c21:
            club = st.radio("30. Are you part of any sports team or academic club?", ["No", "Yes"],
                            index=0 if not st.session_state.answers.get("in_club", 0) else 1,
                            horizontal=True, key="q_club")
        with c22:
            st.markdown("**31. How much do you enjoy solving puzzles or brain games?**")
            puzzle_emojis = ["😑 Not at all", "🙁 Not much", "😐 Neutral", "🙂 Enjoy it", "🤩 Love it!"]
            puzzle = st.select_slider("",
                                      options=puzzle_emojis,
                                      value=st.session_state.answers.get("puzzle_label",
                                                                          puzzle_emojis[2]),
                                      key="q_puzzle")
            puzzle_val = puzzle_emojis.index(puzzle) + 1

        st.markdown("**24. Which EdTech platforms do you use?** *(Select all that apply)*")
        edtech_all = ["YouTube Educational", "Coursera", "Unacademy", "NPTEL",
                      "Khan Academy", "Udemy", "Byju's", "Vedantu", "None"]
        saved_et = st.session_state.answers.get("edtech_list", [])
        edtech_selected = []
        et_cols = st.columns(5)
        for i, et in enumerate(edtech_all):
            with et_cols[i % 5]:
                if st.checkbox(et, value=(et in saved_et), key=f"et_{i}"):
                    edtech_selected.append(et)

        st.markdown("**26. Hobbies** *(Select all that apply)*")
        hobby_all = ["Reading", "Gaming", "Music", "Sports / Fitness", "Cooking", "Painting / Art",
                     "Coding / Tech", "Yoga / Meditation", "Dancing", "Photography",
                     "Gardening", "Writing / Blogging"]
        saved_hob = st.session_state.answers.get("hobbies", [])
        hobbies_selected = []
        hob_cols = st.columns(4)
        for i, h in enumerate(hobby_all):
            with hob_cols[i % 4]:
                if st.checkbox(h, value=(h in saved_hob), key=f"hob_{i}"):
                    hobbies_selected.append(h)

        st.markdown("**22. Apart from academics, what activities are you regularly expected to do?**")
        extra_all = ["Household responsibilities", "Part-time job / internship",
                     "Sibling care / family duties", "Sports practice", "Cultural activities",
                     "Religious / community obligations", "Nothing significant"]
        saved_extra = st.session_state.answers.get("extra_activities", [])
        extra_selected = []
        ext_cols = st.columns(4)
        for i, ex in enumerate(extra_all):
            with ext_cols[i % 4]:
                if st.checkbox(ex, value=(ex in saved_extra), key=f"ext_{i}"):
                    extra_selected.append(ex)

    # ── Section F: Future ─────────────────────────────────────
    with tabs[4]:
        st.markdown(f"#### {t('future_header', lang)}")
        st.markdown("<br>", unsafe_allow_html=True)

        fav_subject = st.text_input("19. What is your favourite subject?",
                                    value=st.session_state.answers.get("fav_subject", ""),
                                    placeholder="e.g. Data Structures, Psychology, Economics...",
                                    key="q_fav_sub")

        goal_5yr = st.text_area("32. Where do you see yourself 5 years from now? Describe briefly.",
                                value=st.session_state.answers.get("goal_5yr", ""),
                                placeholder="e.g. I want to work as a software engineer at a startup, or pursue a PhD...",
                                height=120, key="q_goal_5yr")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:rgba(79,70,229,0.10);border:1px solid rgba(99,102,241,0.3);
                    border-radius:12px;padding:16px 20px;font-size:0.9rem;color:#CBD5E1;">
        🔬 <strong style="color:#A5B4FC;">What happens next?</strong><br><br>
        After you submit, our AI will:<br>
        &nbsp;&nbsp;✅ Compute your 7 psychological health scores<br>
        &nbsp;&nbsp;✅ Predict your ideal learning mode (Online / Offline / Hybrid)<br>
        &nbsp;&nbsp;✅ Identify your student archetype from 6 personality types<br>
        &nbsp;&nbsp;✅ Generate a personalised 90-day study roadmap<br>
        &nbsp;&nbsp;✅ Create a full psychological report for you, your parents, and teachers
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(t("submit_btn", lang), key="submit_btn", use_container_width=True):
            # Validate
            if not name.strip():
                _err = {"en": "Please enter your name before submitting.",
                        "mr": "कृपया सबमिट करण्यापूर्वी तुमचे नाव टाका.",
                        "hi": "कृपया सबमिट करने से पहले अपना नाम दर्ज करें."}
                st.error(_err.get(lang, _err["en"]))
                return

            # Assemble answers
            raw = {
                "name": name.strip(),
                "gender": gender,
                "student_type": _edu_to_type(edu_level),
                "education_level": edu_level,
                "branch": branch or "General",
                "study_hours": study_hours,
                "attend_hours": attend_hours,
                "study_methods": study_methods,
                "prefers_online_video": "Online Videos (YouTube etc.)" in study_methods,
                "active_learner": any(m in study_methods for m in
                                      ["Notes (handwritten)", "Flashcards / Revision Cards"]),
                "sgpa": float(sgpa),
                "atkt": 1 if atkt == "Yes" else 0,
                "friends_count": int(friends_count),
                "confidence": conf_val,
                "confidence_label": confidence,
                "engagement": engage_val,
                "engagement_label": engagement,
                "note_style": note_style,
                "motivators": motivators,
                "goal_setting_freq": goal_freq,
                "study_env": study_env,
                "sleep_hours": sleep_hours,
                "phone_hours": phone_hours,
                "sleep_racing": sleep_race_text,
                "sleep_racing_label": sleep_race,
                "exam_blank": 1 if "Blank" in exam_feel else 0,
                "friday_mood": friday_opts[friday_idx],
                "friday_label": friday_mood,
                "overwhelm": overwhelm_val,
                "overwhelm_label": overwhelm,
                "self_doubt": self_doubt_opts[self_doubt_idx],
                "self_doubt_label": self_doubt,
                "workload_freq": workload_idx,
                "workload_label": workload_freq,
                "time_enough": time_val,
                "time_enough_label": time_enough,
                "social_interaction_freq": social_freq_val,
                "social_freq": social_freq,
                "living_situation": living.replace(" (Paying Guest)", "").replace("PG (Paying Guest)", "PG"),
                "financial_stress": financial,
                "has_internship": 1 if internship == "Yes" else 0,
                "has_job": 1 if part_job == "Yes" else 0,
                "in_club": 1 if club == "Yes" else 0,
                "puzzle_score": puzzle_val,
                "puzzle_label": puzzle,
                "edtech_list": edtech_selected,
                "edtech_platforms": max(1, len([e for e in edtech_selected if e != "None"])),
                "hobbies": hobbies_selected,
                "hobbies_count": len(hobbies_selected),
                "extra_activities": extra_selected,
                "fav_subject": fav_subject,
                "goal_5yr": goal_5yr,
            }

            # ML inference
            with st.spinner("🤖 Analysing your profile..."):
                try:
                    from utils.preprocessor import encode_input, compute_psychological_scores, get_student_archetype
                    import joblib, os as _os

                    scores = compute_psychological_scores(raw)
                    fv = encode_input(raw)

                    MODEL_DIR = _os.path.join(_os.path.dirname(_os.path.dirname(__file__)), "models")
                    rf = joblib.load(_os.path.join(MODEL_DIR, "model_learning_mode.pkl"))
                    xgb = joblib.load(_os.path.join(MODEL_DIR, "model_stress.pkl"))
                    lr = joblib.load(_os.path.join(MODEL_DIR, "model_risk.pkl"))
                    le_mode = joblib.load(_os.path.join(MODEL_DIR, "le_mode.pkl"))
                    le_stress = joblib.load(_os.path.join(MODEL_DIR, "le_stress.pkl"))

                    lm_pred = le_mode.inverse_transform(rf.predict(fv))[0]
                    lm_proba = rf.predict_proba(fv)[0]
                    lm_conf = round(float(max(lm_proba)) * 100, 0)

                    stress_pred = le_stress.inverse_transform(xgb.predict(fv))[0]
                    risk_pred = int(lr.predict(fv)[0])
                    archetype_id = get_student_archetype(fv)

                    predictions = {
                        "learning_mode": lm_pred,
                        "learning_mode_confidence": lm_conf,
                        "stress_level": stress_pred,
                        "at_risk_flag": risk_pred,
                        "archetype_id": archetype_id,
                    }
                except Exception as e:
                    # Fallback: rule-based
                    stress_idx = raw.get("overwhelm", 3) / 5.0
                    lm_pred = "Hybrid"
                    stress_pred = "High" if stress_idx > 0.65 else "Medium"
                    risk_pred = 1 if raw.get("atkt", 0) else 0
                    archetype_id = 0
                    lm_conf = 72.0
                    predictions = {
                        "learning_mode": lm_pred,
                        "learning_mode_confidence": lm_conf,
                        "stress_level": stress_pred,
                        "at_risk_flag": risk_pred,
                        "archetype_id": archetype_id,
                    }
                    scores = {
                        "stress_index": stress_idx,
                        "anxiety_level": stress_idx * 80,
                        "motivation_score": 55.0,
                        "social_isolation": 4.5,
                        "digital_comfort": 6.0,
                        "academic_risk_flag": risk_pred,
                        "overall_health": round((1 - stress_idx) * 70 + 20, 1),
                    }

                from utils.recommender import generate_recommendations
                recs = generate_recommendations(scores, predictions, raw)

            st.session_state.answers = raw
            st.session_state.scores = scores
            st.session_state.predictions = predictions
            st.session_state.recs = recs
            st.session_state.submitted = True

            st.success({"en": "✅ Analysis complete! Redirecting to your results...",
                        "mr": "✅ विश्लेषण पूर्ण! तुमच्या निकालांकडे जात आहे...",
                        "hi": "✅ विश्लेषण पूर्ण! आपके परिणामों पर जा रहे हैं..."}[lang if lang in ["en","mr","hi"] else "en"])
            st.session_state.nav_page = "Results"
            st.rerun()


def _edu_to_type(edu_level: str) -> str:
    mapping = {
        "School (9th-10th)": "School",
        "School (11th-12th)": "School",
        "UG Engineering/Technology": "Engineering",
        "UG Arts/Commerce/Science": "Arts_Commerce",
        "Postgraduate (MBA/MSc/MA)": "Postgraduate",
        "Working Professional": "Working_Professional",
    }
    return mapping.get(edu_level, "Engineering")

"""
utils/recommender.py
Generates personalised recommendations based on ML predictions + psychological scores.
"""
import json
import os

RULES_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                           "models", "recommendation_rules.json")

def _rules():
    with open(RULES_PATH) as f:
        return json.load(f)


def generate_recommendations(scores: dict, predictions: dict, raw: dict = None) -> dict:
    """
    Returns a complete recommendation dict.
    scores: output of compute_psychological_scores()
    predictions: {learning_mode, stress_level, at_risk_flag, archetype_id}
    raw: original questionnaire dict (optional enrichment)
    """
    rules = _rules()
    raw = raw or {}

    archetype_id = str(predictions.get("archetype_id", 0))
    arch_data = rules["archetypes"].get(archetype_id, rules["archetypes"]["5"])

    lm = predictions.get("learning_mode", "Hybrid")
    lm_data = rules["learning_mode_desc"].get(lm, rules["learning_mode_desc"]["Hybrid"])

    stress_level = predictions.get("stress_level", "Medium")
    stress_index = scores.get("stress_index", 0.5)
    anxiety = scores.get("anxiety_level", 50)
    motivation = scores.get("motivation_score", 50)
    social_iso = scores.get("social_isolation", 5)

    # Personalised study tips
    study_hours = raw.get("study_hours", 4)
    sleep_hours = raw.get("sleep_hours", 7)

    study_strategy = []
    if study_hours < 3:
        study_strategy.append("📚 Increase your daily study time gradually — start with adding just 30 minutes each day.")
    elif study_hours >= 7:
        study_strategy.append("⏸️ You study a lot! Make sure to include proper breaks using the Pomodoro method (25 min study + 5 min break).")
    else:
        study_strategy.append("✅ Your study hours are in a healthy range. Add one focused review session each evening.")

    if sleep_hours < 6:
        study_strategy.append("😴 Prioritise sleep — aim for 7-8 hours. Sleep deprivation directly reduces memory consolidation.")
    elif sleep_hours >= 8:
        study_strategy.append("🌙 Great sleep routine! Maintain it and consider 20-min power naps if needed.")

    if anxiety > 65:
        study_strategy.append("🧘 Practice box breathing (4-4-4-4 counts) before exams to calm your nervous system.")
    if motivation < 40:
        study_strategy.append("🎯 Set one small, achievable goal each morning. Small wins build momentum.")
    if social_iso > 6:
        study_strategy.append("🤝 Connect with at least one classmate daily — social support is a buffer against stress.")

    # 30/60/90 day roadmap
    branch = raw.get("branch", "your field")
    roadmap = {
        "30_days": [
            f"Establish a consistent daily routine aligned with your {lm.lower()} learning style",
            f"Start with {arch_data['books'][0]} – spend 20 min/day",
            "Track your sleep and screen time for the first 2 weeks",
            "Join one club, team, or online community in your interest area",
        ],
        "60_days": [
            f"Complete one online certificate course related to {branch}",
            "Practice your weakest subject for 30 min daily using spaced repetition",
            "Apply one stress management technique consistently for 30 days",
            "Have one meaningful academic conversation with a teacher/mentor",
        ],
        "90_days": [
            f"Complete a mini-project or assignment that showcases a new skill in {branch}",
            "Reassess your psychological health score — aim for 10+ point improvement",
            "Build a 6-month academic plan leveraging your identified strengths",
            "Share your study system with a peer — teaching deepens your own learning",
        ]
    }

    return {
        "learning_mode": lm,
        "learning_mode_desc": lm_data["desc"],
        "learning_mode_icon": lm_data["icon"],
        "learning_mode_tips": lm_data["tips"],
        "archetype_name": arch_data["name"],
        "archetype_emoji": arch_data["emoji"],
        "archetype_desc": arch_data["description"],
        "archetype_color": arch_data["color"],
        "strengths": arch_data["strengths"],
        "areas_to_improve": arch_data["areas"],
        "daily_routine": arch_data["daily_routine"],
        "stress_tips": arch_data["stress_tips"],
        "books": arch_data["books"],
        "games": arch_data["games"],
        "edtech": arch_data["edtech"],
        "study_strategy": study_strategy,
        "roadmap": roadmap,
        "stress_level": stress_level,
        "stress_index": stress_index,
        "anxiety_level": anxiety,
        "motivation_score": motivation,
    }


def generate_student_report(answers: dict, scores: dict, recs: dict) -> str:
    name = answers.get("name", "Student")
    today = "24 February 2026"
    lm = recs.get("learning_mode", "Hybrid")
    arch = recs.get("archetype_name", "Balanced Learner")
    stress_pct = round(scores.get("stress_index", 0.5) * 100, 1)

    return f"""
PSYCHOLOGICAL ASSESSMENT REPORT
Student: {name}
Date: {today}
Overall Psychological Health Score: {scores.get('overall_health', 70)}/100

─────────────────────────────────────────
EXECUTIVE SUMMARY
─────────────────────────────────────────
{name} demonstrates a {recs.get('stress_level','Medium')} stress profile with an overall
psychological health score of {scores.get('overall_health',70)}/100.

─────────────────────────────────────────
LEARNING MODE ASSESSMENT
─────────────────────────────────────────
Recommended Mode: {lm}
{recs.get('learning_mode_desc','')}

─────────────────────────────────────────
STRESS & ANXIETY ANALYSIS
─────────────────────────────────────────
Stress Index: {stress_pct}%
Anxiety Level: {scores.get('anxiety_level', 50)}/100
Sleep Quality: {answers.get('sleep_hours', 7)} hours/night

─────────────────────────────────────────
MOTIVATION & SELF-EFFICACY PROFILE
─────────────────────────────────────────
Motivation Score: {scores.get('motivation_score', 50)}/100
Confidence Level: {answers.get('confidence', 3)}/5

─────────────────────────────────────────
SOCIAL & ENVIRONMENTAL FACTORS
─────────────────────────────────────────
Social Isolation Index: {scores.get('social_isolation', 5)}/10
Living Situation: {answers.get('living_situation', 'Home')}
Financial Situation: {answers.get('financial_stress', 'Moderate')}

─────────────────────────────────────────
ACADEMIC RISK ASSESSMENT
─────────────────────────────────────────
Risk Flag: {'⚠️ AT RISK – Please consult college counsellor' if scores.get('academic_risk_flag') else '✅ LOW RISK'}
SGPA: {answers.get('sgpa', 7.0)}
ATKT Status: {'Yes' if answers.get('atkt') else 'No'}

─────────────────────────────────────────
STUDENT ARCHETYPE
─────────────────────────────────────────
Archetype: {arch}
{recs.get('archetype_desc','')}

Identified Strengths: {', '.join(recs.get('strengths', []))}
Areas for Growth: {', '.join(recs.get('areas_to_improve', []))}

─────────────────────────────────────────
30/60/90 DAY ACTION PLAN
─────────────────────────────────────────
First 30 Days:
{chr(10).join('• ' + s for s in recs.get('roadmap', {}).get('30_days', []))}

Next 30 Days (Days 31–60):
{chr(10).join('• ' + s for s in recs.get('roadmap', {}).get('60_days', []))}

Final Phase (Days 61–90):
{chr(10).join('• ' + s for s in recs.get('roadmap', {}).get('90_days', []))}

─────────────────────────────────────────
DISCLAIMER
─────────────────────────────────────────
This report is generated by an AI-powered assessment tool and is intended
for self-reflection and educational guidance only. It does not constitute
a clinical diagnosis. Please consult a qualified mental health professional
for personalised clinical assessment.
    """.strip()


def generate_parent_report(answers: dict, scores: dict) -> str:
    name = answers.get("name", "your child")
    stress_level = "high" if scores.get("stress_index", 0.5) > 0.6 else \
                   "moderate" if scores.get("stress_index", 0.5) > 0.35 else "low"

    warning_signs = []
    if scores.get("stress_index", 0) > 0.65:
        warning_signs.append("Frequently appearing tired, withdrawn, or irritable")
    if scores.get("anxiety_level", 0) > 65:
        warning_signs.append("Difficulty sleeping or waking up with worries")
    if scores.get("social_isolation", 0) > 6:
        warning_signs.append("Spending increasing time alone, avoiding social interaction")
    if scores.get("motivation_score", 50) < 35:
        warning_signs.append("Losing interest in subjects or activities they previously enjoyed")
    if not warning_signs:
        warning_signs.append("No major warning signs detected at this time")

    return f"""
PARENT GUIDE – UNDERSTANDING YOUR CHILD
Student: {name}
Date: 24 February 2026

─────────────────────────────────────────
HOW YOUR CHILD IS DOING
─────────────────────────────────────────
Based on the assessment, {name} is currently experiencing {stress_level} stress levels.
Their overall wellbeing score is {scores.get('overall_health', 70)}/100.

─────────────────────────────────────────
WHAT THIS MEANS BEHAVIOURALLY
─────────────────────────────────────────
{"Your child may need additional emotional support right now. Increased academic pressure and lifestyle factors are contributing to stress." if stress_level == "high" else "Your child is managing reasonably well but could benefit from your encouragement and a supportive home environment." if stress_level == "moderate" else "Your child appears to be in a good psychological state. Continue the supportive environment!"}

─────────────────────────────────────────
WHAT YOU CAN DO – Practical Guidance
─────────────────────────────────────────
✅ WHAT TO SAY:
• "I'm proud of your effort, not just your grades."
• "Is there anything I can do to make things easier for you?"
• "It's okay to take breaks – rest is part of success."
• "I trust you to make good decisions about your studies."

❌ WHAT NOT TO SAY:
• Do not compare them to siblings, cousins, or classmates.
• Avoid asking about exam results immediately after they come home.
• Do not make study the only topic of dinner conversation.
• Avoid expressions of disappointment about grades in front of others.

🏠 HOW TO CREATE A SUPPORTIVE ENVIRONMENT:
• Set a family rule: no academic discussion in the first 30 minutes after they return home.
• Encourage at least one shared family meal per day without phones.
• Celebrate non-academic achievements (sports, creativity, helping others).
• Be available but not intrusive – let them come to you.

─────────────────────────────────────────
WARNING SIGNS TO WATCH FOR
─────────────────────────────────────────
{chr(10).join('⚠️ ' + w for w in warning_signs)}

─────────────────────────────────────────
WHEN TO SEEK PROFESSIONAL HELP
─────────────────────────────────────────
If you notice your child:
• Refusing to attend college/school for more than 3 consecutive days
• Expressing feelings of hopelessness or worthlessness
• Showing significant changes in eating or sleeping patterns
• Withdrawing completely from friends and family

Please reach out to:
• College counsellor or student welfare officer
• A licensed child/adolescent psychologist
• iCall (TISS Pune): 9152987821 | Vandrevala Foundation: 1860-2662-345 (24/7)
    """.strip()

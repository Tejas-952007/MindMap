"""
One-shot script: Generates synthetic Pune student data and trains all ML models.
Run: python generate_data_and_train.py
"""

import pandas as pd
import numpy as np
import json
import joblib
import os
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from xgboost import XGBClassifier

random.seed(42)
np.random.seed(42)

os.makedirs("models", exist_ok=True)
os.makedirs("data", exist_ok=True)

# ─────────────────────────────────────────────────────────────
# 1. Synthetic data generation
# ─────────────────────────────────────────────────────────────
PUNE_COLLEGES = [
    "COEP Technological University",
    "Symbiosis Institute of Technology",
    "MIT-WPU",
    "VIT Pune",
    "Bharati Vidyapeeth",
    "Savitribai Phule Pune University Affiliated College",
    "Pune Institute of Computer Technology",
    "Modern College of Arts, Science and Commerce",
    "Fergusson College",
    "BMCC Pune",
]
BRANCHES = ["Computer Engineering", "Mechanical Engineering", "Civil Engineering",
            "Electronics & TC", "MBA", "MSc Data Science", "BCA", "BCom",
            "BA Psychology", "MBBS", "B.Sc Nursing", "BA English Literature"]
HOBBIES = ["Reading", "Gaming", "Music", "Sports", "Cooking", "Painting",
           "Coding", "Yoga", "Dancing", "Photography", "Gardening", "Writing"]
EDTECH = ["YouTube", "Coursera", "Unacademy", "NPTEL", "Khan Academy",
          "Udemy", "Byju's", "Vedantu"]

STUDENT_TYPES = [
    ("Engineering", 200, 0.70, 0.55, 0.45),
    ("School", 150, 0.45, 0.40, 0.60),
    ("Postgraduate", 100, 0.55, 0.65, 0.35),
    ("Arts_Commerce", 100, 0.35, 0.50, 0.50),
    ("Working_Professional", 50, 0.75, 0.80, 0.20),
]

first_names_m = ["Aarav", "Arjun", "Rohan", "Vedant", "Yash", "Siddharth",
                 "Karan", "Nikhil", "Pranav", "Akash", "Gaurav", "Harsh",
                 "Ishaan", "Jay", "Kunal", "Manish", "Omkar", "Parth",
                 "Rahul", "Sachin", "Tanmay", "Uday", "Vivek", "Waqar",
                 "Aniket", "Bhushan", "Chinmay", "Devesh", "Eshan", "Farhan"]
first_names_f = ["Aditi", "Ananya", "Bhakti", "Chaitali", "Divya", "Ekta",
                 "Gauri", "Harshada", "Ishita", "Jyoti", "Kajal", "Lavanya",
                 "Madhuri", "Neha", "Pooja", "Priya", "Riya", "Sneha",
                 "Swati", "Tanvi", "Uma", "Vidya", "Yogita", "Zara",
                 "Aishwarya", "Bhavna", "Deepali", "Geeta", "Kirti", "Meera"]
last_names = ["Patil", "Jadhav", "Kulkarni", "Shinde", "Deshmukh", "More",
              "Pawar", "Bhosale", "Mane", "Salunkhe", "Gaikwad", "Kale",
              "Sawant", "Mohite", "Deshpande", "Joshi", "Nair", "Shah",
              "Mehta", "Sharma", "Verma", "Singh", "Kumar", "Patel"]


def random_name(gender):
    if gender == "Male":
        return f"{random.choice(first_names_m)} {random.choice(last_names)}"
    elif gender == "Female":
        return f"{random.choice(first_names_f)} {random.choice(last_names)}"
    else:
        return f"{random.choice(first_names_m + first_names_f)} {random.choice(last_names)}"


records = []

for student_type, count, stress_prob, online_pref, offline_pref in STUDENT_TYPES:
    for _ in range(count):
        gender = random.choices(["Male", "Female", "Other"],
                                weights=[0.52, 0.45, 0.03])[0]
        name = random_name(gender)

        is_stressed = random.random() < stress_prob
        is_online_pref = random.random() < online_pref

        # Derive base scores that will be used to answer questions coherently
        stress_base = np.clip(np.random.normal(0.65 if is_stressed else 0.30, 0.15), 0, 1)
        motivation_base = np.clip(np.random.normal(0.4 if is_stressed else 0.7, 0.15), 0, 1)
        social_base = np.clip(np.random.normal(0.35 if is_online_pref else 0.65, 0.15), 0, 1)
        digital_base = np.clip(np.random.normal(0.75 if is_online_pref else 0.35, 0.15), 0, 1)

        # Questionnaire responses
        study_hours = max(0, round(np.random.normal(4 if is_stressed else 5, 1.5)))
        attend_hours = max(0, round(np.random.normal(15 if not is_stressed else 10, 4)))
        confidence = max(1, min(5, round(np.random.normal(2.5 if is_stressed else 3.8, 0.8))))
        sleep_hours = max(2, min(12, round(np.random.normal(5.5 if is_stressed else 7, 1))))
        social_interaction_freq = random.choices(
            [1, 2, 3, 4], weights=[
                0.4 if is_stressed else 0.1,
                0.3, 0.2,
                0.1 if is_stressed else 0.4
            ]
        )[0]  # 1=rarely, 4=daily
        phone_hours = max(0, min(12, round(np.random.normal(5 if is_stressed else 3, 1.5))))
        friends_count = max(0, round(np.random.normal(2 if social_base < 0.4 else 7, 2)))
        sgpa = max(4.0, min(10.0, round(np.random.normal(5.5 if is_stressed else 7.5, 1), 1)))
        atkt = 1 if sgpa < 5.5 and random.random() < 0.4 else 0

        sleep_race = random.choices(["Never", "Sometimes", "Often", "Always"],
                                    weights=[0.1, 0.2, 0.35, 0.35] if stress_base > 0.5
                                    else [0.4, 0.35, 0.15, 0.1])[0]
        exam_feeling = 1 if stress_base > 0.55 else 0  # 0=sharp, 1=blank scattered
        overwhelm_scale = max(1, min(5, round(5 * stress_base + np.random.normal(0, 0.5))))
        friday_feeling = random.choices(
            ["Exhausted and drained", "Tired but okay", "Neutral", "Relieved", "Energised"],
            weights=[0.35, 0.30, 0.15, 0.12, 0.08] if is_stressed
            else [0.05, 0.20, 0.25, 0.30, 0.20]
        )[0]
        self_doubt = random.choices(["Yes, I doubt them", "Sometimes", "No, I believe them"],
                                    weights=[0.45, 0.35, 0.20] if stress_base > 0.55
                                    else [0.10, 0.30, 0.60])[0]
        workload_overload_freq = random.choices([1, 2, 3, 4],
                                               weights=[0.05, 0.15, 0.35, 0.45] if is_stressed
                                               else [0.35, 0.35, 0.20, 0.10])[0]
        goal_freq = random.choices(["Never", "Rarely", "Sometimes", "Often", "Always"],
                                   weights=[0.3, 0.25, 0.25, 0.15, 0.05] if stress_base > 0.5
                                   else [0.05, 0.10, 0.25, 0.35, 0.25])[0]
        time_enough = max(1, min(5, round(5 * (1 - stress_base) + np.random.normal(0, 0.5))))
        puzzle_enjoyment = max(1, min(5, round(np.random.normal(3, 1))))
        engagement_scale = max(1, min(5, round(np.random.normal(2.5 if stress_base > 0.5 else 3.8, 0.8))))

        financial = random.choices(
            ["Very Comfortable", "Comfortable", "Moderate", "Tight", "Financially Struggling"],
            weights=[0.10, 0.25, 0.35, 0.20, 0.10]
        )[0]

        living = random.choices(
            ["Home", "Hostel", "PG", "Relatives"],
            weights=[0.45, 0.30, 0.15, 0.10]
        )[0]

        has_internship = random.random() < (0.5 if student_type == "Engineering" else 0.2)
        has_job = random.random() < (0.9 if student_type == "Working_Professional" else 0.1)
        in_club = random.random() < 0.3
        edtech_count = random.randint(1, 4)
        hobbies_count = random.randint(1, 4)

        num_methods = random.choices([1, 2, 3, 4], weights=[0.1, 0.3, 0.4, 0.2])[0]
        all_methods = ["Notes", "PDF", "Books", "Lectures", "Online Videos", "Peer Teaching", "Flashcards"]
        methods = random.sample(all_methods, num_methods)
        prefers_online_video = "Online Videos" in methods

        # Determine label
        if stress_base > 0.75:
            stress_level = "Critical"
        elif stress_base > 0.55:
            stress_level = "High"
        elif stress_base > 0.35:
            stress_level = "Medium"
        else:
            stress_level = "Low"

        # Learning mode
        if digital_base > 0.65 and social_base < 0.45:
            learning_mode = "Online"
        elif social_base > 0.6 and digital_base < 0.5:
            learning_mode = "Offline"
        else:
            learning_mode = "Hybrid"

        at_risk = 1 if (atkt == 1 or (sgpa < 5.0 and stress_base > 0.6) or
                        (motivation_base < 0.3 and stress_base > 0.65)) else 0

        rec = {
            "name": name,
            "gender": gender,
            "student_type": student_type,
            "education_level": student_type.replace("_", " "),
            "branch": random.choice(BRANCHES),
            "study_hours": study_hours,
            "attend_hours": attend_hours,
            "confidence": confidence,
            "prefers_online_video": int(prefers_online_video),
            "active_learner": int("Notes" in methods or "Flashcards" in methods),
            "sleep_hours": sleep_hours,
            "sleep_racing": sleep_race,
            "exam_blank": exam_feeling,
            "overwhelm": overwhelm_scale,
            "friday_mood": friday_feeling,
            "self_doubt": self_doubt,
            "workload_freq": workload_overload_freq,
            "goal_setting_freq": goal_freq,
            "time_enough": time_enough,
            "puzzle_score": puzzle_enjoyment,
            "engagement": engagement_scale,
            "financial_stress": financial,
            "living_situation": living,
            "phone_hours": phone_hours,
            "friends_count": friends_count,
            "sgpa": sgpa,
            "atkt": atkt,
            "has_internship": int(has_internship),
            "has_job": int(has_job),
            "in_club": int(in_club),
            "edtech_platforms": edtech_count,
            "hobbies_count": hobbies_count,
            "social_interaction_freq": social_interaction_freq,
            # Computed scores
            "stress_base": round(stress_base, 3),
            "motivation_base": round(motivation_base, 3),
            "social_base": round(social_base, 3),
            "digital_base": round(digital_base, 3),
            # Targets
            "stress_level": stress_level,
            "learning_mode": learning_mode,
            "at_risk_flag": at_risk,
        }
        records.append(rec)

df = pd.DataFrame(records)
df.to_csv("data/student_data.csv", index=False)
print(f"✅ Generated {len(df)} student records → data/student_data.csv")
print(df["stress_level"].value_counts())
print(df["learning_mode"].value_counts())


# ─────────────────────────────────────────────────────────────
# 2. Feature engineering & preprocessing
# ─────────────────────────────────────────────────────────────

CAT_COLS = ["gender", "student_type", "education_level", "branch",
            "sleep_racing", "friday_mood", "self_doubt", "goal_setting_freq",
            "financial_stress", "living_situation"]
NUM_COLS = ["study_hours", "attend_hours", "confidence", "prefers_online_video",
            "active_learner", "sleep_hours", "exam_blank", "overwhelm",
            "workload_freq", "time_enough", "puzzle_score", "engagement",
            "phone_hours", "friends_count", "sgpa", "atkt", "has_internship",
            "has_job", "in_club", "edtech_platforms", "hobbies_count",
            "social_interaction_freq"]

# Label encode categoricals
le_dict = {}
df_enc = df.copy()
for col in CAT_COLS:
    le = LabelEncoder()
    df_enc[col + "_enc"] = le.fit_transform(df_enc[col].astype(str))
    le_dict[col] = le

# Map ordinal
sleep_racing_map = {"Never": 0, "Sometimes": 1, "Often": 2, "Always": 3}
goal_map = {"Never": 0, "Rarely": 1, "Sometimes": 2, "Often": 3, "Always": 4}
df_enc["sleep_racing_num"] = df_enc["sleep_racing"].map(sleep_racing_map)
df_enc["goal_freq_num"] = df_enc["goal_setting_freq"].map(goal_map)

FEATURE_COLS = NUM_COLS + [c + "_enc" for c in CAT_COLS] + ["sleep_racing_num", "goal_freq_num"]
X = df_enc[FEATURE_COLS].fillna(0)

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Encode targets
le_mode = LabelEncoder()
le_stress = LabelEncoder()
y_mode = le_mode.fit_transform(df["learning_mode"])
y_stress = le_stress.fit_transform(df["stress_level"])
y_risk = df["at_risk_flag"].values

df_enc.to_csv("data/processed_data.csv", index=False)
print("✅ Preprocessed data saved → data/processed_data.csv")


# ─────────────────────────────────────────────────────────────
# 3. Model training
# ─────────────────────────────────────────────────────────────

X_tr_m, X_te_m, y_tr_m, y_te_m = train_test_split(X_scaled, y_mode, test_size=0.2, random_state=42)
X_tr_s, X_te_s, y_tr_s, y_te_s = train_test_split(X_scaled, y_stress, test_size=0.2, random_state=42)
X_tr_r, X_te_r, y_tr_r, y_te_r = train_test_split(X_scaled, y_risk, test_size=0.2, random_state=42)

# Learning mode – Random Forest
rf_mode = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, class_weight="balanced")
rf_mode.fit(X_tr_m, y_tr_m)
acc_mode = rf_mode.score(X_te_m, y_te_m)
print(f"✅ Learning mode RF accuracy: {acc_mode:.3f}")

# Stress level – XGBoost
xgb_stress = XGBClassifier(n_estimators=150, max_depth=6, learning_rate=0.1,
                            use_label_encoder=False, eval_metric="mlogloss", random_state=42)
xgb_stress.fit(X_tr_s, y_tr_s)
acc_stress = xgb_stress.score(X_te_s, y_te_s)
print(f"✅ Stress XGBoost accuracy: {acc_stress:.3f}")

# At-risk – Logistic Regression
lr_risk = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
lr_risk.fit(X_tr_r, y_tr_r)
acc_risk = lr_risk.score(X_te_r, y_te_r)
print(f"✅ At-risk LR accuracy: {acc_risk:.3f}")

# K-Means clustering (archetypes)
km = KMeans(n_clusters=6, random_state=42, n_init=10)
km.fit(X_scaled)
print(f"✅ K-Means trained (6 clusters)")

# ─────────────────────────────────────────────────────────────
# 4. Save models
# ─────────────────────────────────────────────────────────────
joblib.dump(rf_mode, "models/model_learning_mode.pkl")
joblib.dump(xgb_stress, "models/model_stress.pkl")
joblib.dump(lr_risk, "models/model_risk.pkl")
joblib.dump(km, "models/kmeans_archetype.pkl")
joblib.dump(scaler, "models/scaler.pkl")
joblib.dump(le_dict, "models/label_encoders.pkl")
joblib.dump(le_mode, "models/le_mode.pkl")
joblib.dump(le_stress, "models/le_stress.pkl")
joblib.dump(FEATURE_COLS, "models/feature_cols.pkl")

# ─────────────────────────────────────────────────────────────
# 5. Recommendation rules
# ─────────────────────────────────────────────────────────────
recs_json = {
    "archetypes": {
        "0": {
            "name": "The Overloaded Achiever",
            "emoji": "🏆",
            "description": "High grades, high stress, perfectionist tendencies. You push yourself harder than anyone but often forget to recharge.",
            "color": "#F59E0B",
            "strengths": ["High dedication", "Academic excellence", "Self-discipline"],
            "areas": ["Work-life balance", "Stress regulation", "Rest & recovery"],
            "daily_routine": "6:00 AM Wake + 10 min stretch | 6:30-8:00 AM Focused study | 8:30 AM Breakfast + walk | 9:00-12:00 PM Classes | 1:00 PM Lunch break (screen-free) | 2:00-4:00 PM Short study bursts (Pomodoro) | 4:30-5:30 PM Outdoor activity | 6:00-8:00 PM Light revision | 9:00 PM Wind-down | 10:30 PM Sleep",
            "stress_tips": ["Evening walks in Vetal Tekdi, Pune", "5-minute breathing exercise before exams", "Journaling daily wins"],
            "books": ["Atomic Habits – James Clear", "The Achievement Habit – Bernard Roth", "Why Zebras Don't Get Ulcers – Robert Sapolsky"],
            "games": ["Chess (strategy + focus)", "Sudoku puzzles"],
            "edtech": ["Coursera – Deep specialisation courses", "NPTEL – Structured academic content"]
        },
        "1": {
            "name": "The Disengaged Drifter",
            "emoji": "🌊",
            "description": "Low attendance, low motivation, high screen time. You have potential locked inside, just needing the right trigger.",
            "color": "#3B82F6",
            "strengths": ["Creative thinking", "Adaptability", "Out-of-box ideas"],
            "areas": ["Consistency", "Goal clarity", "Reducing passive screen time"],
            "daily_routine": "7:00 AM Wake | 7:30-8:30 AM Light reading (topic of interest) | 9:00 AM Attend all classes | 1:00-2:00 PM Lunch + social break | 2:00-4:00 PM Self-study (gamified – YouTube + quiz) | 4:30-5:30 PM Sport/group activity | 7:00-8:00 PM Revisit one topic | 10:30 PM Sleep",
            "stress_tips": ["Join a tech club or society at college", "Set tiny 15-min study goals", "Reward yourself after completing tasks"],
            "books": ["Start with Why – Simon Sinek", "The 5 AM Club – Robin Sharma", "Drive – Daniel Pink"],
            "games": ["Duolingo (habit building)", "CodeWars (programming puzzles)"],
            "edtech": ["YouTube channels relevant to branch", "Unacademy – Short, engaging lessons"]
        },
        "2": {
            "name": "The Silent Struggler",
            "emoji": "🌸",
            "description": "Appears fine externally but carries high internal anxiety and self-doubt. Your resilience is a superpower you haven't discovered yet.",
            "color": "#EC4899",
            "strengths": ["Empathy", "Attention to detail", "Quiet observation"],
            "areas": ["Self-confidence", "Expressing needs", "Building support network"],
            "daily_routine": "7:00 AM Wake + 5 min gratitude journaling | 8:00 AM Study (with calming background music) | 10:00 AM Connect with one friend/classmate | 1:00 PM Lunch (eat with others, not alone) | 2:00-4:00 PM Study group or library | 5:00 PM Hobby time | 8:00 PM Gentle yoga or stretching | 10:30 PM Sleep",
            "stress_tips": ["Talk to your college counsellor once a week", "Join Toastmasters or any speaking club", "Keep a confidence journal – 3 wins per day"],
            "books": ["The Confidence Code – Katty Kay", "Feel the Fear and Do It Anyway – Susan Jeffers", "The Gifts of Imperfection – Brené Brown"],
            "games": ["Mindfulness colouring apps", "Story-based puzzle games"],
            "edtech": ["Coursera – Personality and soft skills courses", "Khan Academy – Build confidence in weak subjects"]
        },
        "3": {
            "name": "The Social Learner",
            "emoji": "🤝",
            "description": "Thrives in group environments, loves peer interaction, and performs best in collaborative settings.",
            "color": "#10B981",
            "strengths": ["Team player", "Communication skills", "Motivating others"],
            "areas": ["Solo focus time", "Reducing social dependency for studying", "Online learning comfort"],
            "daily_routine": "7:00 AM Wake | 8:00-9:00 AM Solo prep | 9:00 AM Classes | 1:00-1:30 PM Group lunch discussion | 2:00-4:00 PM Study circle with friends | 5:00-6:00 PM Sport or cultural activity | 7:00-8:00 PM Solo revision | 10:30 PM Sleep",
            "stress_tips": ["Join Pune's student study groups (Viman Nagar, FC Road area)", "Teach a classmate – it reinforces your own learning", "Participate in hackathons or group projects"],
            "books": ["How to Win Friends and Influence People – Dale Carnegie", "The Culture Code – Daniel Coyle", "Quiet – Susan Cain (understanding introverts helps you lead better)"],
            "games": ["Multiplayer strategy games", "Group quiz challenges"],
            "edtech": ["Byju's Live Classes", "Vedantu – Interactive live sessions"]
        },
        "4": {
            "name": "The Digital Native",
            "emoji": "💻",
            "description": "High digital comfort, thrives with self-paced online learning. You are ahead of the curve in adaptability.",
            "color": "#8B5CF6",
            "strengths": ["Tech savviness", "Self-discipline for online learning", "Research skills"],
            "areas": ["Physical activity", "Screen time regulation", "Offline social connections"],
            "daily_routine": "7:00 AM Wake | 8:00 AM Study online (focused block) | 10:00 AM 20-min screen break + walk | 11:00 AM Continue or attend online class | 1:30 PM Lunch + offline activity | 3:00-5:00 PM Project/coding/research | 6:00 PM Physical activity (gym, walk, sport) | 8:00 PM Revision | 10:30 PM Sleep (phone off 1 hr before)",
            "stress_tips": ["20-20-20 rule for screen break", "Blue light glasses in the evening", "Pune's tech meetups and hackathons for in-person connection"],
            "books": ["Deep Work – Cal Newport", "The Shallows – Nicholas Carr", "Range – David Epstein"],
            "games": ["Duolingo", "Lumosity – Brain training"],
            "edtech": ["Coursera – Professional certificates", "MIT OpenCourseWare", "GitHub Learning Lab"]
        },
        "5": {
            "name": "The Resilient Balanced",
            "emoji": "⚖️",
            "description": "Moderate stress, good sleep, balanced life. You are the most psychologically stable archetype. Keep growing.",
            "color": "#06B6D4",
            "strengths": ["Emotional balance", "Consistency", "Adaptability"],
            "areas": ["Pushing beyond comfort zone", "Advanced skill development", "Leadership"],
            "daily_routine": "6:30 AM Wake | 7:00 AM Exercise or yoga | 8:00-9:00 AM Study | 9:30 AM Classes | 1:30 PM Lunch | 2:30-4:30 PM Study or project | 5:00-6:00 PM Hobby/club activity | 7:00-8:00 PM Reading/revision | 9:30 PM Relaxation | 10:30 PM Sleep",
            "stress_tips": ["Practice mindfulness to deepen emotional intelligence", "Mentor a struggling peer", "Take on leadership in academic clubs"],
            "books": ["Thinking, Fast and Slow – Daniel Kahneman", "Mindset – Carol Dweck", "Leaders Eat Last – Simon Sinek"],
            "games": ["Strategy board games", "Creative writing challenges"],
            "edtech": ["Coursera – Leadership and advanced specialisations", "LinkedIn Learning – Professional growth"]
        }
    },
    "learning_mode_desc": {
        "Online": {
            "icon": "🌐",
            "desc": "You thrive with self-paced, digital learning. Online learning suits your independent nature and digital comfort.",
            "tips": ["Use Pomodoro technique", "Block distracting websites", "Join online study groups"]
        },
        "Offline": {
            "icon": "🏫",
            "desc": "You learn best in structured, face-to-face environments. Offline learning supports your social and hands-on style.",
            "tips": ["Attend all classes", "Form study groups", "Use library and lab resources"]
        },
        "Hybrid": {
            "icon": "🔀",
            "desc": "You benefit from a mix of both worlds – online flexibility and offline engagement. A hybrid approach is your sweet spot.",
            "tips": ["Blend EdTech with classroom learning", "Reserve complex topics for in-person help", "Use weekends for online exploration"]
        }
    }
}

with open("models/recommendation_rules.json", "w") as f:
    json.dump(recs_json, f, indent=2)

print("✅ Recommendation rules saved → models/recommendation_rules.json")
print("\n🎉 All models trained and saved to /models/ directory")
print("   Run: streamlit run app.py")

"""
Improved Script: Loads Pune student data and trains all ML models.
Changes:
  - Navin engineered features add kele (digital_score, engagement_score, etc.)
  - Learning Mode: RF → XGBoost + GridSearchCV
  - Stress Level: XGBoost tuned
  - At-Risk: Logistic Regression (already good, minor tuning)
  - Cross-validation added
Run: python generate_data_and_train.py
"""

import pandas as pd
import numpy as np
import json
import joblib
import os
import random
import warnings
warnings.filterwarnings("ignore")  # XGBoost warnings band karto
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.cluster import KMeans
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from datetime import datetime
from xgboost import XGBClassifier

random.seed(42)
np.random.seed(42)

os.makedirs("models", exist_ok=True)
os.makedirs("data", exist_ok=True)

# ─────────────────────────────────────────────────────────────
# 1. Data Load
# ─────────────────────────────────────────────────────────────

if os.path.exists("data/student_data.csv"):
    df = pd.read_csv("data/student_data.csv")
    print(f"✅ Loaded {len(df)} student records from data/student_data.csv")
else:
    print("❌ data/student_data.csv not found!")
    exit(1)


# ─────────────────────────────────────────────────────────────
# 2. Feature Engineering & Preprocessing
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

# Ordinal mapping
sleep_racing_map = {"Never": 0, "Sometimes": 1, "Often": 2, "Always": 3}
goal_map = {"Never": 0, "Rarely": 1, "Sometimes": 2, "Often": 3, "Always": 4}
df_enc["sleep_racing_num"] = df_enc["sleep_racing"].map(sleep_racing_map)
df_enc["goal_freq_num"]    = df_enc["goal_setting_freq"].map(goal_map)

# ─────────────────────────────────────────────────────────────
# NAVIN ENGINEERED FEATURES
# ─────────────────────────────────────────────────────────────

# 1. Digital Score — student kitna online-oriented ahe
#    High digital score → Online learning suit hoil
df_enc["digital_score"] = (
    df_enc["prefers_online_video"] * 2 +
    df_enc["phone_hours"] +
    df_enc["edtech_platforms"]
)

# 2. Engagement Score — student class madhe kitna active ahe
#    High engagement → Offline learning suit hoil
df_enc["engagement_score"] = (
    df_enc["engagement"] +
    df_enc["active_learner"] +
    df_enc["attend_hours"]
)

# 3. Academic Pressure Score — stress + workload combine
df_enc["academic_pressure"] = (
    df_enc["overwhelm"] +
    df_enc["workload_freq"] +
    df_enc["atkt"] +
    (10 - df_enc["sgpa"])   # low sgpa = jast pressure
)

# 4. Social Score — student kitna social ahe
df_enc["social_score"] = (
    df_enc["friends_count"] +
    df_enc["social_interaction_freq"] +
    df_enc["in_club"]
)

# 5. Study Efficiency — study hours vs attend hours ratio
df_enc["study_efficiency"] = (
    df_enc["study_hours"] / (df_enc["attend_hours"] + 1)
)

# 6. Wellbeing Score — sleep + confidence + hobbies
df_enc["wellbeing_score"] = (
    df_enc["sleep_hours"] +
    df_enc["confidence"] +
    df_enc["hobbies_count"]
)

print("✅ Navin 6 engineered features banvle!")

# ─────────────────────────────────────────────────────────────
# Feature columns — Navin features include kele
# ─────────────────────────────────────────────────────────────

ENGINEERED_COLS = [
    "digital_score", "engagement_score", "academic_pressure",
    "social_score", "study_efficiency", "wellbeing_score"
]

FEATURE_COLS = (
    NUM_COLS +
    [c + "_enc" for c in CAT_COLS] +
    ["sleep_racing_num", "goal_freq_num"] +
    ENGINEERED_COLS
)

print(f"✅ Total features: {len(FEATURE_COLS)}")

X = df_enc[FEATURE_COLS].fillna(0)

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Encode targets
le_mode   = LabelEncoder()
le_stress = LabelEncoder()
y_mode   = le_mode.fit_transform(df["learning_mode"])
y_stress = le_stress.fit_transform(df["stress_level"])
y_risk   = df["at_risk_flag"].values

df_enc.to_csv("data/processed_data.csv", index=False)
print("✅ Preprocessed data saved → data/processed_data.csv")


# ─────────────────────────────────────────────────────────────
# 3. Train/Test Split
# ─────────────────────────────────────────────────────────────

X_tr_m, X_te_m, y_tr_m, y_te_m = train_test_split(X_scaled, y_mode,   test_size=0.2, random_state=42, stratify=y_mode)
X_tr_s, X_te_s, y_tr_s, y_te_s = train_test_split(X_scaled, y_stress, test_size=0.2, random_state=42, stratify=y_stress)
X_tr_r, X_te_r, y_tr_r, y_te_r = train_test_split(X_scaled, y_risk,   test_size=0.2, random_state=42, stratify=y_risk)

experiment_log = {
    "timestamp": datetime.now().isoformat(),
    "dataset_summary": {
        "total_records": len(df),
        "stress_level_counts":  df["stress_level"].value_counts().to_dict(),
        "learning_mode_counts": df["learning_mode"].value_counts().to_dict(),
        "at_risk_counts":       df["at_risk_flag"].value_counts().to_dict()
    },
    "models": {}
}


# ─────────────────────────────────────────────────────────────
# 4A. Learning Mode — XGBoost + GridSearchCV
#     (RF hota aadhi — XGBoost + tuning ne improve kela)
# ─────────────────────────────────────────────────────────────


param_grid_mode = {
    "n_estimators":  [100, 200, 300],
    "max_depth":     [4, 6, 8],
    "learning_rate": [0.05, 0.1, 0.2],
    "subsample":     [0.8, 1.0]
}

xgb_mode_base = XGBClassifier(
    eval_metric="mlogloss",
    random_state=42
)

grid_mode = GridSearchCV(
    xgb_mode_base,
    param_grid_mode,
    cv=5,
    scoring="accuracy",
    n_jobs=-1,
    verbose=0
)
grid_mode.fit(X_tr_m, y_tr_m)

best_mode_model = grid_mode.best_estimator_
y_pred_m        = best_mode_model.predict(X_te_m)
acc_mode        = best_mode_model.score(X_te_m, y_te_m)

# Cross-validation score pan baghuy
cv_scores_mode = cross_val_score(best_mode_model, X_scaled, y_mode, cv=5, scoring="accuracy")

print(f"✅ Best Params (Learning Mode): {grid_mode.best_params_}")
print(f"✅ Learning Mode NEW accuracy:  {acc_mode:.3f}")
print(f"✅ Cross-Val Accuracy (5-fold): {cv_scores_mode.mean():.3f} ± {cv_scores_mode.std():.3f}")
print("\nLearning Mode Classification Report:")
print(classification_report(y_te_m, y_pred_m, target_names=le_mode.classes_))

experiment_log["models"]["learning_mode_xgb"] = {
    "best_params":             grid_mode.best_params_,
    "accuracy":                acc_mode,
    "cv_mean":                 cv_scores_mode.mean(),
    "cv_std":                  cv_scores_mode.std(),
    "classification_report":   classification_report(y_te_m, y_pred_m, output_dict=True),
    "confusion_matrix":        confusion_matrix(y_te_m, y_pred_m).tolist()
}


# ─────────────────────────────────────────────────────────────
# 4B. Stress Level — XGBoost + GridSearchCV
#     (Already 77% hota — tuning ne improve karnyacha try)
# ─────────────────────────────────────────────────────────────


param_grid_stress = {
    "n_estimators":  [150, 200, 300],
    "max_depth":     [4, 6, 8],
    "learning_rate": [0.05, 0.1, 0.15],
    "subsample":     [0.8, 1.0],
    "colsample_bytree": [0.8, 1.0]
}

xgb_stress_base = XGBClassifier(
    eval_metric="mlogloss",
    random_state=42
)

grid_stress = GridSearchCV(
    xgb_stress_base,
    param_grid_stress,
    cv=5,
    scoring="accuracy",
    n_jobs=-1,
    verbose=0
)
grid_stress.fit(X_tr_s, y_tr_s)

best_stress_model = grid_stress.best_estimator_
y_pred_s          = best_stress_model.predict(X_te_s)
acc_stress        = best_stress_model.score(X_te_s, y_te_s)

cv_scores_stress = cross_val_score(best_stress_model, X_scaled, y_stress, cv=5, scoring="accuracy")

print(f"✅ Best Params (Stress): {grid_stress.best_params_}")
print(f"✅ Stress NEW accuracy:  {acc_stress:.3f}")
print(f"✅ Cross-Val Accuracy (5-fold): {cv_scores_stress.mean():.3f} ± {cv_scores_stress.std():.3f}")
print("\nStress Level Classification Report:")
print(classification_report(y_te_s, y_pred_s, target_names=le_stress.classes_))

experiment_log["models"]["stress_level_xgb"] = {
    "best_params":           grid_stress.best_params_,
    "accuracy":              acc_stress,
    "cv_mean":               cv_scores_stress.mean(),
    "cv_std":                cv_scores_stress.std(),
    "classification_report": classification_report(y_te_s, y_pred_s, output_dict=True),
    "confusion_matrix":      confusion_matrix(y_te_s, y_pred_s).tolist()
}


# ─────────────────────────────────────────────────────────────
# 4C. At-Risk — Logistic Regression (already 91% AUC — minor tuning)
# ─────────────────────────────────────────────────────────────

print("\n⏳ At-Risk: Training...")

param_grid_risk = {
    "C":       [0.01, 0.1, 1, 10],
    "penalty": ["l1", "l2"],
    "solver":  ["liblinear"]
}

lr_base = LogisticRegression(
    class_weight="balanced",
    random_state=42,
    max_iter=1000
)

grid_risk = GridSearchCV(
    lr_base,
    param_grid_risk,
    cv=5,
    scoring="roc_auc",
    n_jobs=-1,
    verbose=0
)
grid_risk.fit(X_tr_r, y_tr_r)

best_risk_model = grid_risk.best_estimator_
y_pred_r        = best_risk_model.predict(X_te_r)
y_prob_r        = best_risk_model.predict_proba(X_te_r)[:, 1]
acc_risk        = best_risk_model.score(X_te_r, y_te_r)
roc_auc         = roc_auc_score(y_te_r, y_prob_r)

cv_scores_risk = cross_val_score(best_risk_model, X_scaled, y_risk, cv=5, scoring="roc_auc")

print(f"✅ Best Params (At-Risk): {grid_risk.best_params_}")
print(f"✅ At-Risk accuracy: {acc_risk:.3f}  |  ROC-AUC: {roc_auc:.3f}")
print(f"✅ Cross-Val AUC (5-fold): {cv_scores_risk.mean():.3f} ± {cv_scores_risk.std():.3f}")
print("\nAt-Risk Classification Report:")
print(classification_report(y_te_r, y_pred_r))

experiment_log["models"]["at_risk_lr"] = {
    "best_params":           grid_risk.best_params_,
    "accuracy":              acc_risk,
    "roc_auc":               roc_auc,
    "cv_auc_mean":           cv_scores_risk.mean(),
    "cv_auc_std":            cv_scores_risk.std(),
    "classification_report": classification_report(y_te_r, y_pred_r, output_dict=True),
    "confusion_matrix":      confusion_matrix(y_te_r, y_pred_r).tolist()
}


# ─────────────────────────────────────────────────────────────
# 4D. K-Means Clustering (Archetypes) — Same as before
# ─────────────────────────────────────────────────────────────

km_params = {"n_clusters": 6, "random_state": 42, "n_init": 10}
km = KMeans(**km_params)
km.fit(X_scaled)
print(f"\n✅ K-Means trained (6 clusters) | Inertia: {km.inertia_:.2f}")

experiment_log["models"]["kmeans_archetypes"] = {
    "params":  km_params,
    "inertia": km.inertia_
}


# ─────────────────────────────────────────────────────────────
# 5. Save Experiment Log
# ─────────────────────────────────────────────────────────────

with open("models/experiment_log.json", "w") as f:
    json.dump(experiment_log, f, indent=2)
print("✅ Experiment log saved → models/experiment_log.json")


# ─────────────────────────────────────────────────────────────
# 6. Save All Models
# ─────────────────────────────────────────────────────────────

joblib.dump(best_mode_model,   "models/model_learning_mode.pkl")
joblib.dump(best_stress_model, "models/model_stress.pkl")
joblib.dump(best_risk_model,   "models/model_risk.pkl")
joblib.dump(km,                "models/kmeans_archetype.pkl")
joblib.dump(scaler,            "models/scaler.pkl")
joblib.dump(le_dict,           "models/label_encoders.pkl")
joblib.dump(le_mode,           "models/le_mode.pkl")
joblib.dump(le_stress,         "models/le_stress.pkl")
joblib.dump(FEATURE_COLS,      "models/feature_cols.pkl")

print("✅ all models saved → models/ directory")


# ─────────────────────────────────────────────────────────────
# 7. Recommendation Rules (same as before)
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


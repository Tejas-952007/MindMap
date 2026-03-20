"""
utils/preprocessor.py
Encodes raw questionnaire answers into feature vectors for ML model inference.
"""
import numpy as np
import joblib
import os

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")

_CACHE = {}

def _load():
    if "data" not in _CACHE:
        _CACHE["data"] = (
            joblib.load(os.path.join(MODEL_DIR, "scaler.pkl")),
            joblib.load(os.path.join(MODEL_DIR, "label_encoders.pkl")),
            joblib.load(os.path.join(MODEL_DIR, "feature_cols.pkl")),
        )
    return _CACHE["data"]


SLEEP_RACE_MAP = {"Never": 0, "Sometimes": 1, "Often": 2, "Always": 3}
GOAL_MAP = {"Never": 0, "Rarely": 1, "Sometimes": 2, "Often": 3, "Always": 4}
SELF_DOUBT_MAP = {"No, I believe them": 0, "Sometimes": 1, "Yes, I doubt them": 2}
FRIDAY_MAP = {
    "Energised": 4,
    "Relieved": 3,
    "Neutral": 2,
    "Tired but okay": 1,
    "Exhausted and drained": 0,
}


def compute_psychological_scores(raw: dict) -> dict:
    """
    Computes 7 derived psychological scores from raw questionnaire answers.
    Returns dict with keys:
      stress_index (0–1), anxiety_level (0–100), motivation_score (0–100),
      social_isolation (0–10), digital_comfort (0–10),
      academic_risk_flag (0/1), overall_health (0–100)
    """
    # --- Stress Index (0–1) ---
    stress_components = []
    sleep_race_val = SLEEP_RACE_MAP.get(raw.get("sleep_racing", "Sometimes"), 1)
    stress_components.append(sleep_race_val / 3.0)

    overwhelm = raw.get("overwhelm", 3)
    stress_components.append((overwhelm - 1) / 4.0)

    workload = raw.get("workload_freq", 2)
    stress_components.append((workload - 1) / 3.0)

    sleep_h = raw.get("sleep_hours", 7)
    sleep_stress = max(0, (7 - sleep_h) / 5.0)
    stress_components.append(min(1, sleep_stress))

    friday = FRIDAY_MAP.get(raw.get("friday_mood", "Neutral"), 2)
    stress_components.append((4 - friday) / 4.0)

    phone_h = raw.get("phone_hours", 3)
    stress_components.append(min(1, phone_h / 8.0))

    fin_stress_map = {"Very Comfortable": 0, "Comfortable": 0.25,
                      "Moderate": 0.5, "Tight": 0.75, "Financially Struggling": 1.0}
    stress_components.append(fin_stress_map.get(raw.get("financial_stress", "Moderate"), 0.5))

    stress_index = float(np.clip(np.mean(stress_components), 0, 1))

    # --- Anxiety Level (0–100) ---
    anxiety_parts = []
    anxiety_parts.append(sleep_race_val / 3.0)
    exam_blank = raw.get("exam_blank", 0)
    anxiety_parts.append(int(exam_blank))
    self_doubt_val = SELF_DOUBT_MAP.get(str(raw.get("self_doubt", "Sometimes")), 1) / 2.0
    anxiety_parts.append(self_doubt_val)
    confidence = raw.get("confidence", 3)
    anxiety_parts.append((5 - confidence) / 4.0)
    anxiety_level = round(float(np.clip(np.mean(anxiety_parts) * 100, 0, 100)), 1)

    # --- Motivation Score (0–100) ---
    goal_val = GOAL_MAP.get(raw.get("goal_setting_freq", "Sometimes"), 2) / 4.0
    motivation_parts = [
        goal_val,
        (raw.get("puzzle_score", 3) - 1) / 4.0,
        raw.get("confidence", 3) / 5.0,
        1 - self_doubt_val,
        min(1, raw.get("edtech_platforms", 2) / 5.0),
    ]
    motivation_score = round(float(np.clip(np.mean(motivation_parts) * 100, 0, 100)), 1)

    # --- Social Isolation Index (0–10, higher = more isolated) ---
    friends_score = max(0, 1 - raw.get("friends_count", 5) / 15.0)
    living_isolation = {"Home": 0.2, "Hostel": 0.4, "PG": 0.6, "Relatives": 0.5}
    liv = living_isolation.get(raw.get("living_situation", "Home"), 0.3)
    social_interact = 1 - (raw.get("social_interaction_freq", 2) - 1) / 3.0
    club = 0.0 if raw.get("in_club", 0) else 0.4
    social_isolation = round(float(np.clip((friends_score + liv + social_interact + club) / 4.0 * 10, 0, 10)), 1)

    # --- Digital Comfort Score (0–10) ---
    edtech = raw.get("edtech_platforms", 2)
    online_vid = int(raw.get("prefers_online_video", 0))
    engagement = raw.get("engagement", 3)
    digital_comfort = round(float(np.clip((edtech / 5 + online_vid + engagement / 5) / 3 * 10, 0, 10)), 1)

    # --- Academic Risk Flag (0/1) ---
    sgpa = raw.get("sgpa", 7.0)
    atkt = raw.get("atkt", 0)
    academic_risk_flag = 1 if (
        atkt == 1 or
        (sgpa < 5.5 and stress_index > 0.6) or
        (motivation_score < 35 and stress_index > 0.65)
    ) else 0

    # --- Overall Psychological Health Score (0–100) ---
    overall_health = round(float(np.clip(
        (1 - stress_index) * 40 +
        (1 - anxiety_level / 100) * 25 +
        motivation_score / 100 * 25 +
        (1 - social_isolation / 10) * 10,
        0, 100
    )), 1)

    return {
        "stress_index": round(stress_index, 3),
        "anxiety_level": anxiety_level,
        "motivation_score": motivation_score,
        "social_isolation": social_isolation,
        "digital_comfort": digital_comfort,
        "academic_risk_flag": academic_risk_flag,
        "overall_health": overall_health,
    }


def encode_input(raw: dict) -> np.ndarray:
    """
    Encodes raw questionnaire dict → scaled feature vector for ML inference.
    """
    scaler, le_dict, feature_cols = _load()

    num_vals = {
        "study_hours": raw.get("study_hours", 4),
        "attend_hours": raw.get("attend_hours", 15),
        "confidence": raw.get("confidence", 3),
        "prefers_online_video": int(raw.get("prefers_online_video", False)),
        "active_learner": int(raw.get("active_learner", False)),
        "sleep_hours": raw.get("sleep_hours", 7),
        "exam_blank": int(raw.get("exam_blank", 0)),
        "overwhelm": raw.get("overwhelm", 3),
        "workload_freq": raw.get("workload_freq", 2),
        "time_enough": raw.get("time_enough", 3),
        "puzzle_score": raw.get("puzzle_score", 3),
        "engagement": raw.get("engagement", 3),
        "phone_hours": raw.get("phone_hours", 3),
        "friends_count": raw.get("friends_count", 5),
        "sgpa": raw.get("sgpa", 7.0),
        "atkt": int(raw.get("atkt", 0)),
        "has_internship": int(raw.get("has_internship", False)),
        "has_job": int(raw.get("has_job", False)),
        "in_club": int(raw.get("in_club", False)),
        "edtech_platforms": raw.get("edtech_platforms", 2),
        "hobbies_count": raw.get("hobbies_count", 2),
        "social_interaction_freq": raw.get("social_interaction_freq", 2),
    }

    cat_vals = {}
    for col in ["gender", "student_type", "education_level", "branch",
                "sleep_racing", "friday_mood", "self_doubt", "goal_setting_freq",
                "financial_stress", "living_situation"]:
        le = le_dict[col]
        raw_val = str(raw.get(col, le.classes_[0]))
        try:
            cat_vals[col + "_enc"] = int(le.transform([raw_val])[0])
        except ValueError:
            # Explicit unknown handling strategy: map to the most frequent/baseline class (index 0)
            # Log this in a production system. For now, assign to the explicit baseline format.
            cat_vals[col + "_enc"] = 0 

    sleep_race_val = SLEEP_RACE_MAP.get(raw.get("sleep_racing", "Sometimes"), 1)
    goal_val = GOAL_MAP.get(raw.get("goal_setting_freq", "Sometimes"), 2)

    row = {**num_vals, **cat_vals,
           "sleep_racing_num": sleep_race_val,
           "goal_freq_num": goal_val}

    vec = [row.get(col, 0) for col in feature_cols]
    return scaler.transform([vec])


def get_student_archetype(feature_vector: np.ndarray) -> int:
    if "kmeans" not in _CACHE:
        _CACHE["kmeans"] = joblib.load(os.path.join(MODEL_DIR, "kmeans_archetype.pkl"))
    km = _CACHE["kmeans"]
    return int(km.predict(feature_vector)[0])

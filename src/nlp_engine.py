import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# ============================================================
# 1. LOAD DATA
# ============================================================

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "safety_reports.xlsx"


def load_data():
    df = pd.read_excel(DATA_PATH)

    # Combine important text fields
    text_columns = [
        "title",
        "brief_incident",
        "observations",
        "root_cause",
        "recommendations"
    ]

    for col in text_columns:
        if col not in df.columns:
            df[col] = ""

    df["combined_text"] = (
        df[text_columns]
        .fillna("")
        .astype(str)
        .agg(" ".join, axis=1)
    )

    return df


# ============================================================
# 2. TEXT CLEANING
# ============================================================

def clean_text(text):

    text = str(text).lower()

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Remove special characters
    text = re.sub(r"[^a-zA-Z0-9\s/-]", " ", text)

    return text.strip()


# ============================================================
# 3. SIF CLASSIFIER
# ============================================================

def train_sif_model(df):

    df["clean_text"] = df["combined_text"].apply(clean_text)

    # Prototype labels
    y = (
        df["sif_potential"]
        .astype(str)
        .str.upper()
        .map({
            "YES": 1,
            "NO": 0
        })
    )

    # Remove rows without labels
    valid = y.notna()

    X_text = df.loc[valid, "clean_text"]
    y = y[valid]

    # TF-IDF
    vectorizer = TfidfVectorizer(
        max_features=3000,
        ngram_range=(1, 2),
        stop_words="english"
    )

    X = vectorizer.fit_transform(X_text)

    # Model
    model = LogisticRegression(
        max_iter=1000
    )

    model.fit(X, y)

    return model, vectorizer


# ============================================================
# 4. HAZARD DETECTION
# ============================================================

HAZARD_KEYWORDS = {

    "Energy Release": [
        "energy release",
        "unexpected energy",
        "electrical energy",
        "stored energy"
    ],

    "Fire / Explosion": [
        "fire",
        "explosion",
        "flammable",
        "ignition"
    ],

    "Toxic Gas": [
        "toxic gas",
        "gas exposure",
        "gas leak",
        "hazardous gas"
    ],

    "Oxygen Deficiency": [
        "oxygen deficiency",
        "low oxygen",
        "oxygen level"
    ],

    "Suspended Load": [
        "suspended load",
        "crane",
        "lifting",
        "lifted load"
    ],

    "Struck-by": [
        "struck-by",
        "struck by",
        "impact"
    ],

    "Dropped Object": [
        "dropped object",
        "dropped cylinder",
        "falling object"
    ],

    "Slip / Trip": [
        "slip",
        "trip",
        "walkway"
    ]
}


def detect_hazards(text):

    text = clean_text(text)

    detected = []

    for hazard, keywords in HAZARD_KEYWORDS.items():

        for keyword in keywords:

            if keyword in text:
                detected.append(hazard)
                break

    return list(set(detected))


# ============================================================
# 5. BARRIER DETECTION
# ============================================================

BARRIER_KEYWORDS = {

    "LOTO / Electrical Isolation": [
        "loto",
        "electrical isolation",
        "test for dead"
    ],

    "Gas Testing": [
        "gas testing",
        "gas test"
    ],

    "Work Authorization": [
        "work authorization",
        "permit"
    ],

    "Fire Watch": [
        "fire watch"
    ],

    "Exclusion Zone": [
        "exclusion zone",
        "segregation"
    ],

    "Lift Plan": [
        "lift plan",
        "lifting plan"
    ],

    "Certified Lifting Gear": [
        "certified lifting gear",
        "lifting gear"
    ],

    "PPE": [
        "ppe",
        "personal protective equipment"
    ],

    "Standby / Rescue": [
        "standby",
        "rescue"
    ]
}


def detect_barriers(text):

    text = clean_text(text)

    detected = []

    for barrier, keywords in BARRIER_KEYWORDS.items():

        for keyword in keywords:

            if keyword in text:
                detected.append(barrier)
                break

    return list(set(detected))


# ============================================================
# 6. IOGP LIFE-SAVING RULE
# ============================================================

IOGP_RULES = {

    "Energy Isolation": [
        "loto",
        "isolation",
        "electrical maintenance",
        "stored energy"
    ],

    "Line of Fire": [
        "dropped",
        "impact",
        "struck",
        "suspended load",
        "cylinder"
    ],

    "Hot Work": [
        "hot work",
        "fire",
        "explosion",
        "ignition"
    ],

    "Confined Space": [
        "confined space",
        "vessel entry",
        "tank entry",
        "oxygen deficiency"
    ],

    "Safe Mechanical Lifting": [
        "crane",
        "lifting",
        "lift plan",
        "suspended load"
    ],

    "Work Authorization": [
        "permit",
        "work authorization"
    ]
}


def detect_iogp_rules(text):

    text = clean_text(text)

    rules = []

    for rule, keywords in IOGP_RULES.items():

        for keyword in keywords:

            if keyword in text:
                rules.append(rule)
                break

    return list(set(rules))


# ============================================================
# 7. RISK SCORE
# ============================================================

def calculate_risk_score(row):

    score = 0

    # SIF
    if str(row.get("sif_potential", "")).upper() == "YES":
        score += 50

    # Barrier
    barrier_status = str(
        row.get("barrier_status", "")
    ).lower()

    if "failed" in barrier_status:
        score += 25

    elif "missing" in barrier_status:
        score += 25

    elif "ineffective" in barrier_status:
        score += 20

    # Serious injury
    outcome = str(
        row.get("loss_outcome", "")
    ).lower()

    if "serious injury" in outcome:
        score += 25

    return min(score, 100)


# ============================================================
# 8. RECOMMENDATION ENGINE
# ============================================================

def generate_recommendations(row):

    hazard = str(row.get("hazard", "")).lower()
    barrier = str(row.get("barrier", "")).lower()
    status = str(row.get("barrier_status", "")).lower()

    short_term = []
    long_term = []
    next_cycle = []

    # -------------------------
    # SHORT TERM
    # -------------------------

    short_term.append(
        "Stop or control the activity until the critical hazard is controlled."
    )

    if "failed" in status or "missing" in status:

        short_term.append(
            f"Verify and restore the failed/missing barrier: {barrier}."
        )

    if "gas" in hazard:

        short_term.append(
            "Conduct atmospheric testing before restarting the activity."
        )

    if "electrical" in hazard or "energy" in hazard:

        short_term.append(
            "Verify isolation, LOTO and test-for-dead before work resumes."
        )

    if "fire" in hazard or "explosion" in hazard:

        short_term.append(
            "Verify hot-work controls, gas testing and fire-watch requirements."
        )

    # -------------------------
    # LONG TERM
    # -------------------------

    long_term.extend([
        "Review the applicable SOP and permit requirements.",
        "Conduct task-specific safety training.",
        "Strengthen supervisory verification.",
        "Share the learning across relevant operating areas."
    ])

    # -------------------------
    # NEXT CYCLE
    # -------------------------

    next_cycle.extend([
        "Verify corrective-action completion.",
        "Confirm competency/training completion.",
        "Audit the effectiveness of the corrective barrier.",
        "Record closure evidence before the next work cycle."
    ])

    return {
        "short_term": short_term,
        "long_term": long_term,
        "next_cycle": next_cycle
    }


# ============================================================
# 9. COMPLETE NLP PIPELINE
# ============================================================

def run_nlp_pipeline():

    df = load_data()

    # Clean text
    df["clean_text"] = df["combined_text"].apply(clean_text)

    # NLP extraction
    df["detected_hazards"] = df["combined_text"].apply(
        detect_hazards
    )

    df["detected_barriers"] = df["combined_text"].apply(
        detect_barriers
    )

    df["detected_iogp_rules"] = df["combined_text"].apply(
        detect_iogp_rules
    )

    # Risk
    df["risk_score"] = df.apply(
        calculate_risk_score,
        axis=1
    )

    # Risk category
    df["risk_level"] = pd.cut(
        df["risk_score"],
        bins=[-1, 30, 60, 80, 100],
        labels=[
            "Low",
            "Medium",
            "High",
            "Critical"
        ]
    )

    # Recommendations
    recommendations = df.apply(
        generate_recommendations,
        axis=1
    )

    df["short_term_action"] = [
        x["short_term"] for x in recommendations
    ]

    df["long_term_action"] = [
        x["long_term"] for x in recommendations
    ]

    df["next_cycle_action"] = [
        x["next_cycle"] for x in recommendations
    ]

    return df


if __name__ == "__main__":

    df = run_nlp_pipeline()

    print("\n========== OIL SAFETY NLP PROTOTYPE ==========\n")

    print(
        df[
            [
                "report_id",
                "sif_potential",
                "detected_hazards",
                "detected_iogp_rules",
                "risk_score",
                "risk_level"
            ]
        ].to_string(index=False)
    )
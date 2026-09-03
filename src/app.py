import streamlit as st
import pandas as pd
import plotly.express as px
import sys

sys.path.append("src")

from nlp_engine import run_nlp_pipeline


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="OIL Safety Intelligence",
    page_icon="🛡️",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_pipeline():

    return run_nlp_pipeline()


df = load_pipeline()


# ============================================================
# HEADER
# ============================================================

st.title("🛡️ OIL Safety Intelligence")

st.markdown(
    """
    ### AI/NLP Engine for SIF Precursor Detection

    Prototype dashboard for identifying:
    - SIF-potential events
    - Hazards
    - Barrier failures
    - IOGP Life-Saving Rules
    - Risk levels
    - Corrective actions
    """
)


st.divider()


# ============================================================
# SIDEBAR FILTER
# ============================================================

st.sidebar.header("Filters")

risk_filter = st.sidebar.multiselect(
    "Risk Level",
    options=df["risk_level"].dropna().unique(),
    default=df["risk_level"].dropna().unique()
)

sif_filter = st.sidebar.multiselect(
    "SIF Potential",
    options=["YES", "NO"],
    default=["YES", "NO"]
)


filtered_df = df[
    (df["risk_level"].isin(risk_filter)) &
    (df["sif_potential"].str.upper().isin(sif_filter))
]


# ============================================================
# KPI SECTION
# ============================================================

total_reports = len(filtered_df)

sif_reports = (
    filtered_df["sif_potential"]
    .str.upper()
    .eq("YES")
    .sum()
)

non_sif = total_reports - sif_reports

sif_percentage = (
    sif_reports / total_reports * 100
    if total_reports > 0
    else 0
)


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Total Reports",
    total_reports
)

col2.metric(
    "SIF Potential",
    sif_reports
)

col3.metric(
    "Non-SIF",
    non_sif
)

col4.metric(
    "SIF %",
    f"{sif_percentage:.1f}%"
)


st.divider()


# ============================================================
# CHARTS
# ============================================================

col1, col2 = st.columns(2)


# SIF distribution
with col1:

    sif_counts = (
        filtered_df["sif_potential"]
        .str.upper()
        .value_counts()
        .reset_index()
    )

    sif_counts.columns = [
        "SIF Potential",
        "Count"
    ]

    fig = px.pie(
        sif_counts,
        names="SIF Potential",
        values="Count",
        title="SIF Potential Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# Risk distribution
with col2:

    risk_counts = (
        filtered_df["risk_level"]
        .value_counts()
        .reset_index()
    )

    risk_counts.columns = [
        "Risk Level",
        "Count"
    ]

    fig = px.bar(
        risk_counts,
        x="Risk Level",
        y="Count",
        title="Risk Level Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# IOGP RULE
# ============================================================

st.subheader("IOGP Life-Saving Rule Analysis")


rule_data = []

for _, row in filtered_df.iterrows():

    rules = row["detected_iogp_rules"]

    for rule in rules:

        rule_data.append({
            "IOGP Rule": rule
        })


if rule_data:

    rule_df = pd.DataFrame(rule_data)

    rule_counts = (
        rule_df["IOGP Rule"]
        .value_counts()
        .reset_index()
    )

    rule_counts.columns = [
        "IOGP Rule",
        "Count"
    ]

    fig = px.bar(
        rule_counts,
        x="IOGP Rule",
        y="Count",
        title="Reports by Life-Saving Rule"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info("No IOGP rules detected.")


# ============================================================
# HAZARDS
# ============================================================

st.subheader("Top Detected Hazards")


hazard_data = []

for _, row in filtered_df.iterrows():

    for hazard in row["detected_hazards"]:

        hazard_data.append({
            "Hazard": hazard
        })


if hazard_data:

    hazard_df = pd.DataFrame(hazard_data)

    hazard_counts = (
        hazard_df["Hazard"]
        .value_counts()
        .reset_index()
    )

    hazard_counts.columns = [
        "Hazard",
        "Count"
    ]

    fig = px.bar(
        hazard_counts,
        x="Hazard",
        y="Count",
        title="Detected Safety Hazards"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# REPORT TABLE
# ============================================================

st.subheader("Safety Report Intelligence")


display_df = filtered_df[
    [
        "report_id",
        "date",
        "title",
        "sif_potential",
        "hazard",
        "barrier_status",
        "risk_score",
        "risk_level"
    ]
].copy()


st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# INDIVIDUAL REPORT ANALYSIS
# ============================================================

st.divider()

st.subheader("🔎 AI Safety Report Analysis")


selected_report = st.selectbox(
    "Select Report",
    filtered_df["report_id"].tolist()
)


selected = filtered_df[
    filtered_df["report_id"] == selected_report
].iloc[0]


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Risk Score",
        f"{selected['risk_score']}/100"
    )


with col2:

    st.metric(
        "SIF Potential",
        selected["sif_potential"]
    )


with col3:

    st.metric(
        "Risk Level",
        str(selected["risk_level"])
    )


# ------------------------------------------------------------
# Incident
# ------------------------------------------------------------

st.markdown("### Incident")

st.write(
    selected["brief_incident"]
)


# ------------------------------------------------------------
# NLP findings
# ------------------------------------------------------------

st.markdown("### NLP Findings")

st.write(
    "**Detected Hazards:**",
    ", ".join(selected["detected_hazards"])
)

st.write(
    "**Detected Barriers:**",
    ", ".join(selected["detected_barriers"])
)

st.write(
    "**IOGP Rules:**",
    ", ".join(selected["detected_iogp_rules"])
)


# ============================================================
# ACTION PLAN
# ============================================================

st.divider()

st.subheader("🚨 Recommended Action Plan")


tab1, tab2, tab3 = st.tabs(
    [
        "Short-Term",
        "Long-Term",
        "Next Cycle Mandatory"
    ]
)


with tab1:

    for action in selected["short_term_action"]:
        st.checkbox(
            action,
            key=f"short_{hash(action)}"
        )


with tab2:

    for action in selected["long_term_action"]:
        st.checkbox(
            action,
            key=f"long_{hash(action)}"
        )


with tab3:

    for action in selected["next_cycle_action"]:
        st.checkbox(
            action,
            key=f"next_{hash(action)}"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Prototype — Safety data shown here is based on the synthetic "
    "SIH/OIL prototype dataset and should not be interpreted as "
    "actual OIL operational data."
)


st.sidebar.header("Submit Safety Observation")

with st.sidebar.form("safety_report_form"):

    report_text = st.text_area(
        "Enter Safety Observation / Near Miss",
        placeholder="Example: Electrical maintenance was carried out without proper LOTO..."
    )

    activity = st.text_input(
        "Activity",
        placeholder="Electrical Maintenance"
    )

    location = st.text_input(
        "Location",
        placeholder="Processing Plant - Unit 2"
    )

    submitted = st.form_submit_button("Analyze Report")

if submitted:

    if report_text.strip() == "":
        st.warning("Please enter a safety observation.")
    else:

        st.subheader("AI Safety Analysis")

        hazards = detect_hazards(report_text)
        barriers = detect_barriers(report_text)
        rules = detect_iogp_rules(report_text)

        st.write("### Detected Hazards")
        st.write(hazards if hazards else "No major hazard detected")

        st.write("### Barrier Findings")
        st.write(barriers if barriers else "No barrier identified")

        st.write("### IOGP Life-Saving Rules")
        st.write(rules if rules else "No rule identified")
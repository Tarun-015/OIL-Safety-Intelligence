# OIL Safety Intelligence Engine

### AI/NLP Engine for Detecting Serious Injury & Fatality (SIF) Precursors

An AI/NLP-based safety intelligence prototype designed for **Oil India Limited (OIL)** to analyze unstructured Unsafe Act (UA), Unsafe Condition (UC), Near-Miss and Incident reports.

The system converts free-text safety observations into structured safety intelligence by identifying **SIF potential, hazards, safety barriers, IOGP Life-Saving Rules, risk levels and recommended corrective actions**.

> **Note:** The current prototype uses synthetic data for demonstration purposes and does not represent actual OIL operational data.

---

## Problem Statement

Safety observations and near-miss reports often contain critical information in unstructured text.

Important indicators such as:

* Serious Injury & Fatality (SIF) potential
* Hazard types
* Failed or missing barriers
* High-risk activities
* Applicable Life-Saving Rules
* Corrective actions

can be difficult to identify consistently when reports are analyzed manually.

The objective of this project is to build an AI/NLP engine that can analyze these reports and help safety teams identify **high-risk precursor patterns before they result in serious incidents**.

---

# Current Prototype

The current version focuses on the **NLP Safety Intelligence layer**.

### Workflow

```text
Safety Report
      ↓
Text Preprocessing
      ↓
NLP Analysis
      ↓
┌─────────────────────────────┐
│ SIF Potential               │
│ Hazard Detection            │
│ Barrier Identification      │
│ IOGP Rule Mapping           │
└──────────────┬──────────────┘
               ↓
         Risk Scoring
               ↓
      Action Recommendations
               ↓
        Safety Dashboard
```

---

# Key Features

### 1. Safety Report Analysis

The system processes information such as:

* Report title
* Incident description
* Observations
* Root cause
* Recommendations

The fields are combined and processed as a unified safety narrative.

### 2. SIF Potential Identification

Reports are categorized based on whether they indicate potential for:

* Serious Injury
* Fatality
* Non-SIF events

The current prototype uses available labelled data and rule-based safety intelligence to demonstrate the workflow.

### 3. Hazard Detection

The NLP engine identifies hazards such as:

* Energy Release
* Fire / Explosion
* Toxic Gas
* Oxygen Deficiency
* Suspended Load
* Struck-by
* Dropped Object
* Slip / Trip

### 4. Safety Barrier Detection

The system identifies safety barriers and controls including:

* LOTO / Electrical Isolation
* Gas Testing
* Work Authorization
* Fire Watch
* Exclusion Zone
* Lift Plan
* Certified Lifting Gear
* PPE
* Standby / Rescue

### 5. IOGP Life-Saving Rule Mapping

Safety observations are mapped to relevant Life-Saving Rules such as:

* Energy Isolation
* Line of Fire
* Hot Work
* Confined Space
* Safe Mechanical Lifting
* Work Authorization

### 6. Risk Scoring

A prototype risk score is generated using factors such as:

* SIF potential
* Barrier failure
* Missing or ineffective controls
* Serious injury outcome

The resulting score is classified into:

```text
Low
Medium
High
Critical
```

### 7. Action Recommendation Engine

Recommendations are divided into three levels:

**Short-Term**

Immediate controls required to make the situation safe.

**Long-Term**

Actions such as SOP review, safety training and stronger supervisory verification.

**Next-Cycle Mandatory**

Actions that should be verified before the next work cycle, including corrective-action closure, competency verification and barrier effectiveness.

---

# Interactive Dashboard

The application is built using Streamlit.

The dashboard provides:

* Total safety reports
* SIF vs Non-SIF distribution
* Risk-level distribution
* IOGP Life-Saving Rule analysis
* Hazard analysis
* Individual report analysis
* Risk score
* Recommended actions

Users can select an individual safety report and view its complete NLP analysis.

---

# Technology Stack

### Programming

* Python

### Data Processing

* Pandas
* NumPy

### NLP / Machine Learning

* Scikit-learn
* TF-IDF
* Logistic Regression
* Rule-based NLP / keyword extraction

### Visualization & Application

* Streamlit
* Plotly

### Data Sources

* CSV safety-report dataset for the current NLP prototype
* Synthetic Excel datasets planned for Asset and Workforce Readiness modules

---

# Project Structure

```text
OIL_Safety_AI/
│
├── data/
│   ├── safety_reports.csv
│   ├── asset_data/
│   └── workforce_data/
│
├── src/
│   ├── nlp_engine.py
│   ├── asset_engine.py
│   ├── workforce_engine.py
│   └── safety_engine.py
│
├── pages/
│   ├── 1_NLP_Safety_Intelligence.py
│   ├── 2_Asset_Readiness.py
│   ├── 3_Workforce_Readiness.py
│   └── 4_Safety_Assessment.py
│
├── requirements.txt
└── README.md
```

---

# Future Scope

The current NLP dashboard is the first layer of a larger **Safety Readiness Intelligence Platform**.

## 1. Asset / Factory Readiness Dashboard

The next phase will integrate equipment and factory information from Excel datasets.

The system will analyze:

* Sites
* Units
* Areas
* Equipment
* Components
* Maintenance plans
* Maintenance history
* Lubrication records
* Inspection records
* Failure records
* Equipment risk
* Employee-equipment authorization

The objective is to answer:

> **Is the equipment ready for the planned activity?**

Example:

```text
Equipment: Pump P-204

Maintenance       ✓
Inspection        ✓
Failure Risk      LOW
Critical Controls ✓

Asset Readiness: 92%
```

---

## 2. Workforce Readiness Dashboard

The next layer will evaluate whether the employee assigned to a task is ready and authorized to perform it.

The system will consider:

* Employee skills
* Job role
* Training records
* Certifications
* Deployments
* Equipment authorization

The objective is to answer:

> **Is the assigned person qualified, trained and authorized for this activity?**

Example:

```text
Employee: EMP-1045

Required Skill          ✓
Training                ✓
Certification           ✓
Equipment Authorization ✗

Workforce Readiness: 78%

Decision:
Authorization required
before task execution.
```

---

# 3. Integrated Safety Readiness Engine

The most important future component is to connect all three layers:

```text
              SAFETY REPORT
                    ↓
              NLP ENGINE
                    ↓
        SIF / Hazard / Barrier
                    ↓
          IOGP Life-Saving Rule
                    ↓
          ┌─────────┴─────────┐
          ↓                   ↓
   ASSET READINESS      WORKFORCE READINESS
          ↓                   ↓
 Maintenance              Skills
 Inspection               Training
 Failure Risk             Certification
 Authorization            Authorization
          └─────────┬─────────┘
                    ↓
             SAFETY READINESS
                    ↓
        ┌───────────┼───────────┐
        ↓           ↓           ↓
       GO      CONDITIONAL     NO-GO
```

This will transform the system from a **report-analysis tool** into a **safety decision-support system**.

---

# 4. User-Driven Safety Assessment

Instead of only analyzing historical reports, users will be able to enter a new safety observation.

Example:

```text
Safety Observation:
"Technician is performing electrical maintenance
without proper LOTO."

Activity:
Electrical Maintenance

Site:
Site-04

Equipment:
P-204

Employee:
EMP-1045
```

The system can then evaluate:

```text
SIF Potential       → HIGH
Hazard              → Energy Release
IOGP Rule           → Energy Isolation

Asset Readiness     → 92%
Employee Readiness  → 78%

Final Decision      → CONDITIONAL / NO-GO

Required Action:
Complete authorization and verify LOTO
before work begins.
```

---

# 5. Advanced Machine Learning

As more labelled safety reports become available, the prototype can move beyond keyword-based rules toward advanced ML/NLP models.

Potential improvements include:

* Transformer-based text classification
* Sentence embeddings
* Semantic similarity
* Multi-label classification
* Automatic precursor clustering
* Root-cause classification
* Barrier-failure prediction
* SIF probability estimation

---

# 6. Generative AI / LLM Integration

A future GenAI layer can allow safety professionals to interact with the system using natural language.

For example:

> "Show me the most common SIF precursors in electrical maintenance."

or:

> "Find previous incidents similar to this observation."

or:

> "Why is this activity classified as high risk?"

The LLM can explain the model's findings using retrieved safety reports and structured operational data.

---

# 7. Similar Incident Retrieval

Using embeddings and vector search, the system can retrieve historically similar incidents.

```text
New Observation
      ↓
Embedding
      ↓
Vector Search
      ↓
Similar Historical Events
      ↓
Common Hazards
      ↓
Common Barrier Failures
      ↓
Recommended Controls
```

This can help safety teams learn from previous events instead of treating every observation independently.

---

# 8. Predictive Safety Intelligence

With sufficient historical data, the platform could identify recurring patterns such as:

```text
Activity
    ↓
Location
    ↓
Equipment
    ↓
Barrier Failure
    ↓
Repeated Near Misses
    ↓
Increasing SIF Risk
```

This could enable proactive identification of activities, locations or assets with increasing precursor density.

---

# 9. Real-Time Asset and Sensor Integration

In a production implementation, the system could eventually integrate with operational systems and equipment-health data.

Potential inputs include:

* Equipment condition
* Maintenance status
* Inspection status
* Failure history
* Sensor/IoT signals
* Work permits
* Isolation status

This would allow safety readiness to be evaluated using both **reported safety information and real operational conditions**.

---

# 10. Management Safety Dashboard

A management-level dashboard can provide:

* SIF precursor density by site
* High-risk activities
* Repeated barrier failures
* Top Life-Saving Rule violations
* Asset readiness
* Workforce readiness
* Corrective-action closure
* Emerging risk trends

This would provide leadership with a high-level view while allowing safety teams to drill down into individual observations.

---

# Long-Term Vision

The ultimate goal is to move from:

```text
Reactive Safety Reporting
          ↓
Incident Analysis
          ↓
Risk Identification
```

to:

```text
          PROACTIVE SAFETY INTELLIGENCE

Safety Reports
      +
Asset Condition
      +
Employee Competency
      +
Historical Incidents
      +
Operational Data
      ↓
AI Safety Intelligence
      ↓
Risk Prediction
      ↓
Preventive Action
      ↓
Safer Operations
```

---

## Disclaimer

This project is an academic/SIH prototype. The current demonstration uses synthetic data and should not be interpreted as representing actual OIL personnel, equipment, operational records or safety performance.

The system is intended as a **decision-support prototype**, not as a replacement for qualified safety professionals, permit-to-work processes, engineering controls or organizational safety procedures.

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ==========================================
# RISK WEIGHTS
# ==========================================

RISK_WEIGHTS = {

    "Unlimited Liability": 20,

    "Broad Indemnity": 15,

    "One Sided Termination": 15,

    "Auto Renewal": 10,

    "Confidentiality Forever": 10,

    "No Audit Rights": 10,

    "No Data Protection": 15,

    "Weak Security Controls": 15
}

# ==========================================
# COMPLIANCE WEIGHTS
# ==========================================

COMPLIANCE_WEIGHTS = {

    "Consent": 10,

    "Data Retention": 15,

    "Right To Deletion": 15,

    "Data Processing": 10,

    "Data Security": 20,

    "Data Transfer": 10
}

# ==========================================
# MAIN FUNCTION
# ==========================================

def calculate_score(
    risk_df,
    compliance_df
):

    # ======================================
    # RISK PENALTY
    # ======================================

    risk_penalty = 0

    if (
        risk_df is not None
        and not risk_df.empty
        and "risk_type" in risk_df.columns
    ):

        unique_risks = (

            risk_df["risk_type"]
            .dropna()
            .unique()

        )

        for risk_type in unique_risks:

            risk_penalty += (

                RISK_WEIGHTS.get(
                    risk_type,
                    10
                )

            )

    else:

        unique_risks = []

    # ======================================
    # COMPLIANCE PENALTY
    # ======================================

    missing_requirements = compliance_df[

        compliance_df["status"]
        == "MISSING"

    ]

    compliance_penalty = 0

    for _, row in (
        missing_requirements.iterrows()
    ):

        compliance_penalty += (

            COMPLIANCE_WEIGHTS.get(
                row["requirement"],
                10
            )

        )

    # ======================================
    # WEIGHTED PENALTY
    # ======================================

    weighted_penalty = (

        (risk_penalty * 0.60)

        +

        (compliance_penalty * 0.40)

    )

    weighted_penalty = min(
        weighted_penalty,
        100
    )

    # ======================================
    # FINAL SCORE
    # ======================================

    final_score = (
        100 - weighted_penalty
    )

    final_score = max(
        final_score,
        0
    )

    # ======================================
    # RISK LEVEL
    # ======================================

    if final_score >= 80:

        risk_level = "LOW"

    elif final_score >= 50:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"

    # ======================================
    # REPORT
    # ======================================

    report = {

        "risk_score":
            round(
                final_score,
                2
            ),

        "risk_level":
            risk_level,

        "safety_score":
            round(
                final_score,
                2
            ),

        "unique_risk_types":
            len(
                unique_risks
            ),

        "missing_compliance_items":
            len(
                missing_requirements
            ),

        "risk_penalty":
            risk_penalty,

        "compliance_penalty":
            compliance_penalty,

        "weighted_penalty":
            round(
                weighted_penalty,
                2
            )
    }

    return report


# ==========================================
# TEST MODE
# ==========================================

if __name__ == "__main__":

    risk_file = (

        PROJECT_ROOT
        /
        "data"
        /
        "processed"
        /
        "risk_results.csv"

    )

    compliance_file = (

        PROJECT_ROOT
        /
        "data"
        /
        "processed"
        /
        "compliance_report_v2.csv"

    )

    risk_df = pd.read_csv(
        risk_file
    )

    compliance_df = pd.read_csv(
        compliance_file
    )

    report = calculate_score(

        risk_df,
        compliance_df

    )

    print("\n")
    print("=" * 70)
    print("FINAL CONTRACT REPORT")
    print("=" * 70)

    for key, value in report.items():

        print(
            f"{key}: {value}"
        )

    report_df = pd.DataFrame(
        [report]
    )

    output_file = (

        PROJECT_ROOT
        /
        "data"
        /
        "processed"
        /
        "final_contract_report.csv"

    )

    report_df.to_csv(

        output_file,
        index=False

    )

    print("\nSaved:")
    print(output_file)
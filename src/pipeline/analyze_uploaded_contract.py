from pathlib import Path
import pandas as pd

from src.extraction.pdf_extractor import extract_pdf_text

from src.segmentation.clause_segmenter import (
    segment_clauses
)

from src.risk_detection.risk_detector_v2 import (
    detect_risks
)

from src.compliance.compliance_detector_v2 import (
    detect_compliance
)

from src.scoring.risk_scoring import (
    calculate_score
)

from src.classification.contract_classifier import (
    classify_contract
)


# =====================================
# SUMMARY GENERATOR
# =====================================

def generate_summary(
    contract_type,
    risk_level,
    risk_count,
    missing_count
):

    risk_word = (
    "risk finding"
    if risk_count == 1
    else "risk findings"
)
    summary = (
        f"This {contract_type} contains "
        f"{risk_count} risk findings and "
        f"{missing_count} missing compliance items. "
        f"Overall risk level is {risk_level}."
    )

    return summary


# =====================================
# MAIN ANALYSIS FUNCTION
# =====================================

def analyze_contract(pdf_path):

    print("\n")
    print("=" * 80)
    print("CONTRACT ANALYSIS STARTED")
    print("=" * 80)

    # =====================================
    # EXTRACT PDF TEXT
    # =====================================

    print("\nExtracting Text...")

    text = extract_pdf_text(
        pdf_path
    )

    print(
        f"Characters Extracted: {len(text)}"
    )

    # =====================================
    # SEGMENT CLAUSES
    # =====================================

    print("\nSegmenting Clauses...")

    clauses_df = segment_clauses(
        text
    )

    print(
        f"Clauses Found: {len(clauses_df)}"
    )

    # =====================================
    # CONTRACT TYPE
    # =====================================

    # temporary
    contract_type = classify_contract(
    text
    )

    print(
        f"\nContract Type: {contract_type}"
    )

    # =====================================
    # RISK DETECTION
    # =====================================

    print(
        "\nRunning Risk Detection..."
    )

    risk_df = detect_risks(
        clauses_df
    )

    print(
        f"Risks Found: {len(risk_df)}"
    )

    # =====================================
    # COMPLIANCE DETECTION
    # =====================================

    print(
        "\nRunning Compliance Check..."
    )

    compliance_df = detect_compliance(
    clauses_df,
    contract_type
    )

    missing_count = len(

        compliance_df[
            compliance_df["status"]
            == "MISSING"
        ]

    )

    print(
        f"Missing Compliance Items: "
        f"{missing_count}"
    )

    # =====================================
    # SCORING
    # =====================================

    print(
        "\nCalculating Score..."
    )

    report = calculate_score(
        risk_df,
        compliance_df
    )


    summary = generate_summary(
    contract_type,
    report["risk_level"],
    len(risk_df),
    missing_count
    )

    # =====================================
    # FINAL RESULT
    # =====================================

    result = {

        "contract_type":
            contract_type,

        "risk_score":
            report["risk_score"],

        "risk_level":
            report["risk_level"],

        "summary":
            summary,

        "unique_risk_types":
            report["unique_risk_types"],

        "missing_compliance_items":
            report[
                "missing_compliance_items"
            ],

        "risk_penalty":
            report["risk_penalty"],

        "compliance_penalty":
            report[
                "compliance_penalty"
            ],

        # "risk_findings":
        #     risk_df[
        #         "risk_type"
        #     ].dropna()
        #      .unique()
        #      .tolist(),

        "risks": risk_df.to_dict(
            orient="records"
            ),

        "missing_requirements":
            compliance_df[
                compliance_df["status"]
                == "MISSING"
            ]["requirement"]
             .tolist(),
            
        "compliance_details":
            compliance_df.to_dict(
            orient="records"
            )

    }

    print("\n")
    print("=" * 80)
    print("FINAL RESULT")
    print("=" * 80)

    for key, value in result.items():

        print(
            f"{key}: {value}"
        )

    return result


if __name__ == "__main__":

    pdf_file = (
        Path("data/contracts")
        /
        "NondisclosureAgreement.pdf"
    )

    analyze_contract(
        pdf_file
    )
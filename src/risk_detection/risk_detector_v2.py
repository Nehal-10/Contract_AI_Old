from pathlib import Path
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

from src.models.embedding_model import model

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RISK_FILE = (
    PROJECT_ROOT /
    "data" /
    "risk_library" /
    "high_risk_clauses.csv"
)

SIMILARITY_THRESHOLD = 0.68


def detect_risks(clauses_df):

    risk_df = pd.read_csv(
        RISK_FILE
    )

    print(
        f"Total Clauses: {len(clauses_df)}"
    )

    print(
        f"Risk Library Size: {len(risk_df)}"
    )

    contract_embeddings = model.encode(
        clauses_df["text"]
        .fillna("")
        .tolist(),
        show_progress_bar=True
    )

    risk_embeddings = model.encode(
        risk_df["clause"]
        .fillna("")
        .tolist(),
        show_progress_bar=True
    )

    results = []

    for clause_idx, clause_embedding in enumerate(
        contract_embeddings
    ):

        similarities = cosine_similarity(
            [clause_embedding],
            risk_embeddings
        )[0]

        best_match_idx = similarities.argmax()

        best_score = similarities[
            best_match_idx
        ]

        if best_score >= SIMILARITY_THRESHOLD:

            contract_clause = (
                clauses_df.iloc[
                    clause_idx
                ]["text"]
            )

            title = (
                clauses_df.iloc[
                    clause_idx
                ]["title"]
            )

            matched_row = risk_df.iloc[
                best_match_idx
            ]

            results.append({

                "title":
                    title,

                "risk_type":
                    matched_row["risk_type"],

                "severity":
                    matched_row["severity"],

                "similarity":
                    round(
                        float(best_score),
                        3
                    ),

                "matched_clause":
                    matched_row["clause"],

                "recommendation":
                    matched_row[
                        "recommendation"
                    ],

                "contract_clause":
                    contract_clause[:500]

            })

    results_df = pd.DataFrame(
        results
    )

    output_file = (
        PROJECT_ROOT /
        "data" /
        "processed" /
        "risk_results.csv"
    )

    results_df.to_csv(
        output_file,
        index=False
    )

    return results_df
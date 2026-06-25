from pathlib import Path
import sqlite3
import json



PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = (
    PROJECT_ROOT
    / "data"
    / "database"
    / "contract_ai.db"
)


def get_connection():

    return sqlite3.connect(
        DB_PATH
    )


def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS analyses (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            filename TEXT,

            contract_type TEXT,

            risk_score REAL,

            risk_level TEXT,

            summary TEXT,

            analysis_json TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":

    create_tables()

    print(
        "Database Initialized"
    )


def save_analysis(
    filename,
    contract_type,
    risk_score,
    risk_level,
    summary,
    analysis_json
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO analyses (

            filename,
            contract_type,
            risk_score,
            risk_level,
            summary,
            analysis_json

        )

        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            filename,
            contract_type,
            risk_score,
            risk_level,
            summary,
            json.dumps(analysis_json)
        )
    )

    conn.commit()
    conn.close()

def get_all_analyses():

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM analyses
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return [

        dict(row)

        for row in rows

    ]

def get_analysis_by_id(
    analysis_id
):

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM analyses
        WHERE id = ?
        """,
        (analysis_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if not row:
        return None

    result = dict(row)

    if result["analysis_json"]:

        result["analysis_json"] = json.loads(
            result["analysis_json"]
        )

    return result

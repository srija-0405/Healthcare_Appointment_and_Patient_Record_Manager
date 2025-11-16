import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from datetime import datetime

# Import the constant from app
from app import MEDICAL_CSV, load_medical_records

# Convert MEDICAL_CSV to absolute path
MEDICAL_CSV = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", MEDICAL_CSV))



def test_csv_created_if_missing():
    # Ensure CSV does not exist
    if os.path.exists(MEDICAL_CSV):
        os.remove(MEDICAL_CSV)

    # Calling loader should auto-create CSV
    _ = load_medical_records()
    assert os.path.exists(MEDICAL_CSV)


def test_add_medical_record():
    df = pd.read_csv(MEDICAL_CSV)
    initial_count = len(df)

    new_row = {
        "record_id": datetime.now().timestamp(),
        "patient": "Test Patient",
        "notes": "Test diagnosis",
        "treatment": "Test treatment",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(MEDICAL_CSV, index=False)

    updated = pd.read_csv(MEDICAL_CSV)
    assert len(updated) == initial_count + 1


def test_view_history():
    df = load_medical_records()
    subset = df[df["patient"] == "Test Patient"]

    # Should always return a DataFrame
    assert isinstance(subset, pd.DataFrame)

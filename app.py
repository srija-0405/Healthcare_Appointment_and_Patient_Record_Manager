import streamlit as st
import pandas as pd
from datetime import datetime
from utils.helpers import validate_phone, generate_patient_id, format_date

# Future extension: Patient Health Management dashboard
# - vitals, medications, history, chronic condition flags

st.set_page_config(page_title="Healthcare Appointment & Record Manager", layout="wide")

# ======================
# Load Data
# ======================
@st.cache_data
def load_patients():
    # Loads patient records from CSV file.
    # Returns a DataFrame with columns: patient_id, name, dob, age, contact, emergency_contact
    try:
        return pd.read_csv("data/demo_data.csv")
    except Exception:
        return pd.DataFrame(columns=["patient_id","name","dob","age","contact","emergency_contact"])

@st.cache_data
def load_users():
    try:
        return pd.read_csv("data/users.csv")
    except Exception:
        return pd.DataFrame(columns=["username","password","role"])

patients = load_patients()
users = load_users()

# ======================
# Helper Functions
# ======================
def login(username, password):
    """Validate username and password"""
    match = users[(users['username'] == username) & (users['password'] == password)]
    if not match.empty:
        return match.iloc[0]['role']
    else:
        return None

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.success("You have been logged out.")

# ======================
# Authentication
# ======================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.title("🏥 Healthcare Appointment & Patient Record Manager")
    st.subheader("🔐 Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        role = login(username, password)
        if role:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role
            st.success(f"Welcome {username}! You are logged in as {role}.")
            st.rerun()

        else:
            st.error("Invalid credentials! Please try again.")

else:
    # ======================
    # Sidebar + Logout
    # ======================
    st.sidebar.title(f"Welcome, {st.session_state.username} 👋")
    st.sidebar.write(f"Role: {st.session_state.role}")

    if st.sidebar.button("Logout"):
        logout()
        st.rerun()

    # ======================
    # Role-Based Menu
    # ======================
    role = st.session_state.role

    if role == "Patient":
        pages = ["Home", "Appointments", "EMR"]
    elif role == "Medical Staff":
        pages = ["Home", "Patient Management", "EMR", "Reports"]
    elif role == "Admin":
        pages = ["Home", "Patient Management", "Appointments", "EMR", "Billing", "Reports"]
    else:
        pages = ["Home"]

    menu = st.sidebar.radio("Navigate", pages)

    # ======================
    # PAGE CONTENTS
    # ======================
    if menu == "Home":
        st.header("🏠 Home")
        st.write("Use the sidebar to navigate. This system adjusts based on your role.")

    elif menu == "Patient Management" and role in ["Medical Staff", "Admin"]:
        st.header("👩‍⚕️ Patient Management")
        action = st.radio("Action", ["Register New Patient", "View Patients"])
        if action == "Register New Patient":
            name = st.text_input("Full Name")
            dob = st.date_input("Date of Birth", value=datetime(1990,1,1))
            age = st.number_input("Age", min_value=0, max_value=150, value=30)
            contact = st.text_input("Contact Number")
            emergency = st.text_input("Emergency Contact")
            if st.button("Register"):
                if not name.strip():
                    st.error("Name is required.")
                elif not validate_phone(contact):
                    st.error("Invalid contact number. Enter a 10-digit Indian mobile starting with 6-9.")
                else:
                    new_id = generate_patient_id()
                    new_row = {
                        "patient_id": new_id,
                        "name": name,
                        "dob": format_date(dob),
                        "age": age,
                        "contact": contact,
                        "emergency_contact": emergency
                    }
                    patients = pd.concat([patients, pd.DataFrame([new_row])], ignore_index=True)
                    patients.to_csv("data/demo_data.csv", index=False)
                    st.success(f"Patient {name} registered with ID {new_id}")
        else:
            st.dataframe(patients)

    elif menu == "Appointments" and role in ["Patient", "Admin"]:
        st.header("📅 Appointments")
        pnames = patients["name"].tolist()
        if not pnames:
            st.info("No patients available. Register a patient first.")
        else:
            patient = st.selectbox("Patient", pnames)
            doctor = st.text_input("Doctor Name", value="Dr. Example")
            date = st.date_input("Appointment Date", value=datetime.today())
            time = st.time_input("Time", value=datetime.now().time())
            if st.button("Book Appointment"):
                st.success(f"Appointment booked for {patient} with {doctor} on {date} at {time}")

    elif menu == "EMR" and role in ["Patient", "Medical Staff", "Admin"]:
        st.header("🧾 Electronic Medical Records (EMR)")
        pnames = patients["name"].tolist()
        if not pnames:
            st.info("No patients available. Register a patient first.")
        else:
            patient = st.selectbox("Select Patient", pnames)
            notes = st.text_area("Visit Notes / Diagnosis")
            plan = st.text_area("Treatment Plan")
            if st.button("Save EMR"):
                st.success(f"EMR saved for {patient} (demo mode)")

    elif menu == "Billing" and role == "Admin":
        st.header("💳 Billing")
        pnames = patients["name"].tolist()
        if not pnames:
            st.info("No patients available.")
        else:
            patient = st.selectbox("Patient", pnames)
            service = st.text_input("Service")
            amount = st.number_input("Amount", min_value=0)
            status = st.selectbox("Payment Status", ["Pending", "Paid"])
            if st.button("Generate Invoice"):
                st.success(f"Invoice for {patient}: ₹{amount} ({status})")

    elif menu == "Reports" and role in ["Medical Staff", "Admin"]:
        st.header("📊 Reports Dashboard")
        st.metric("Total Patients", len(patients))
        st.write("Charts & detailed data will appear here later.")

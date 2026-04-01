import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Equipment Dashboard", layout="wide")

st.title("Equipment Dashboard")

# --- TABS ---
tab1, tab2 = st.tabs(["Equipment Master List", "History Cards & Breakdown Log"])

# ===================== TAB 1 =====================
with tab1:
    st.header("Equipment Master List")
    st.markdown("""
    Every plant asset displayed with its classification (A/B/C), PM coverage status, and discipline — giving any user an instant snapshot of the full asset population.
    """)

    num_equipment = 50

    sample_data = {
        "Equipment": [f"EQ-{i+1}" for i in range(num_equipment)],
        "Class (A/B/C)": [random.choice(['A','B','C']) for _ in range(num_equipment)],
        "PM Coverage": [random.choice(['Covered','Not Covered']) for _ in range(num_equipment)],
        "Discipline": [random.choice(['Mechanical','Electrical','Instrumentation']) for _ in range(num_equipment)]
    }

    sample_df = pd.DataFrame(sample_data)

    st.subheader("50 Equipment Snapshot")
    st.dataframe(sample_df, use_container_width=True)

    # Metrics
    total = len(sample_df)
    covered = sample_df['PM Coverage'].str.contains('cover', case=False).sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Equipment", total)
    col2.metric("PM Covered", covered)
    col3.metric("PM Not Covered", total - covered)

# ===================== TAB 2 =====================
with tab2:
    st.header("History Cards & Breakdown Log")
    st.markdown("""
    Each asset carries a linked history card showing past failures, unplanned downtime events, and repair records — enabling trend analysis and repeat-failure identification.
    """)

    # Select equipment
    equipment_list = [f"EQ-{i+1}" for i in range(50)]
    selected_eq = st.selectbox("Select Equipment", equipment_list)

    # Generate mock history data
    history_data = []

    for i in range(random.randint(3, 8)):
        history_data.append({
            "Date": f"2026-03-{random.randint(1,28)}",
            "Failure Type": random.choice(["Seal Leak", "Bearing Failure", "Overheating", "Vibration"]),
            "Downtime (hrs)": round(random.uniform(1, 10), 1),
            "Action Taken": random.choice(["Replaced Part", "Lubrication", "Alignment Fix", "Inspection"])
        })

    history_df = pd.DataFrame(history_data)

    st.subheader(f"History Card for {selected_eq}")
    st.dataframe(history_df, use_container_width=True)

    # KPIs
    total_failures = len(history_df)
    total_downtime = history_df["Downtime (hrs)"].sum()

    col1, col2 = st.columns(2)
    col1.metric("Total Failures", total_failures)
    col2.metric("Total Downtime (hrs)", round(total_downtime, 1))

    # Trend hint
    st.info("Use this log to identify recurring failures and plan preventive maintenance.")
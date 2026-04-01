import streamlit as st
import pandas as pd
import random
# Removed matplotlib dependency for Streamlit Cloud compatibility

st.set_page_config(page_title="Equipment Dashboard", layout="wide")

st.title("Equipment Dashboard")

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "Equipment Master List", 
    "History Cards & Breakdown Log",
    "PM Routes & Maintenance Schedules",
    "KPI & Downtime Tracking"
])

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

    equipment_list = [f"EQ-{i+1}" for i in range(50)]
    selected_eq = st.selectbox("Select Equipment", equipment_list)

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

    total_failures = len(history_df)
    total_downtime = history_df["Downtime (hrs)"].sum()

    col1, col2 = st.columns(2)
    col1.metric("Total Failures", total_failures)
    col2.metric("Total Downtime (hrs)", round(total_downtime, 1))

    st.info("Use this log to identify recurring failures and plan preventive maintenance.")

# ===================== TAB 3 =====================
with tab3:
    st.header("PM Routes & Maintenance Schedules")
    st.markdown("""
    Revised, OEM-aligned maintenance routes are embedded per asset — with task lists, frequencies, and responsible parties visible to planners and technicians in real time.
    """)

    equipment_list = [f"EQ-{i+1}" for i in range(50)]
    selected_eq = st.selectbox("Select Equipment for PM Plan", equipment_list)

    tasks = []

    for i in range(random.randint(4, 8)):
        tasks.append({
            "Task": random.choice([
                "Check lubrication",
                "Inspect seals",
                "Vibration analysis",
                "Temperature check",
                "Alignment check",
                "Tighten bolts"
            ]),
            "Frequency": random.choice(["Daily", "Weekly", "Monthly", "Quarterly"]),
            "Responsible": random.choice(["Operator", "Maintenance Tech", "Supervisor"])
        })

    pm_df = pd.DataFrame(tasks)

    st.subheader(f"PM Route for {selected_eq}")
    st.dataframe(pm_df, use_container_width=True)

    col1, col2 = st.columns(2)
    col1.metric("Total Tasks", len(pm_df))
    col2.metric("Most Common Frequency", pm_df['Frequency'].mode()[0])

# ===================== TAB 4 =====================
with tab4:
    st.header("KPI & Downtime Tracking")
    st.markdown("""
    Live metrics including MTBF, MTTR, PM compliance rate, and unplanned downtime hours give management and maintenance teams the data needed to measure progress and drive decisions.
    """)

    # --- KPI VALUES ---
    mtbf = round(random.uniform(50, 200), 1)
    mttr = round(random.uniform(2, 10), 1)
    pm_compliance = round(random.uniform(70, 100), 1)
    downtime = round(random.uniform(20, 100), 1)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("MTBF (hrs)", mtbf)
    col2.metric("MTTR (hrs)", mttr)
    col3.metric("PM Compliance (%)", pm_compliance)
    col4.metric("Downtime (hrs)", downtime)

    # --- TREND DATA ---
    days = list(range(1, 11))
    downtime_trend = [round(random.uniform(1, 10), 1) for _ in days]

        # --- PLOT 1: DOWNTIME TREND ---
    downtime_df = pd.DataFrame({"Day": days, "Downtime": downtime_trend})
    st.line_chart(downtime_df.set_index("Day"))

        # --- PLOT 2: PM COMPLIANCE TREND ---
    compliance_trend = [round(random.uniform(70, 100), 1) for _ in days]
    compliance_df = pd.DataFrame({"Day": days, "PM Compliance": compliance_trend})
    st.line_chart(compliance_df.set_index("Day"))

    # --- INSIGHT ---
    st.success("Track KPIs to improve reliability, reduce downtime, and optimize maintenance strategy.")

import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Equipment Master List", layout="wide")

st.title("Equipment Master List")
st.markdown("""
Every plant asset displayed with its classification (A/B/C), PM coverage status, and discipline — giving any user an instant snapshot of the full asset population.
""")

# --- GENERATE 50 SAMPLE EQUIPMENT (NO EXCEL NEEDED) ---
num_equipment = 50

sample_data = {
    "Equipment": [f"EQ-{i+1}" for i in range(num_equipment)],
    "Class (A/B/C)": [random.choice(['A','B','C']) for _ in range(num_equipment)],
    "PM Coverage": [random.choice(['Covered','Not Covered']) for _ in range(num_equipment)],
    "Discipline": [random.choice(['Mechanical','Electrical','Instrumentation']) for _ in range(num_equipment)]
}

sample_df = pd.DataFrame(sample_data)

# --- DISPLAY TABLE ---
st.subheader("50 Equipment Snapshot")
st.dataframe(sample_df, use_container_width=True)

# --- SNAPSHOT METRICS ---
st.subheader("Quick Snapshot")

total = len(sample_df)
covered = sample_df['PM Coverage'].str.contains('cover', case=False).sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Equipment", total)
col2.metric("PM Covered", covered)
col3.metric("PM Not Covered", total - covered)

# --- OPTIONAL FILTERS ---
st.subheader("Filters")

col1, col2 = st.columns(2)

with col1:
    class_filter = st.multiselect("Select Class", options=sample_df['Class (A/B/C)'].unique())

with col2:
    discipline_filter = st.multiselect("Select Discipline", options=sample_df['Discipline'].unique())

filtered_df = sample_df.copy()

if class_filter:
    filtered_df = filtered_df[filtered_df['Class (A/B/C)'].isin(class_filter)]

if discipline_filter:
    filtered_df = filtered_df[filtered_df['Discipline'].isin(discipline_filter)]

st.subheader("Filtered View")
st.dataframe(filtered_df, use_container_width=True)
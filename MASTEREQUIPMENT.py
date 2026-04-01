import streamlit as st
import pandas as pd

st.set_page_config(page_title="Equipment Master List", layout="wide")

st.title("Equipment Master List")
st.markdown("""
Every plant asset displayed with its classification (A/B/C), PM coverage status, and discipline — giving any user an instant snapshot of the full asset population.
""")

# Upload Excel file
uploaded_file = st.file_uploader("Upload Equipment Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Ensure required columns exist
    required_cols = ['Equipment ID', 'Equipment Name', 'Class', 'PM Status', 'Discipline']
    for col in required_cols:
        if col not in df.columns:
            st.error(f"Missing column: {col}")
            st.stop()

    # Filter only critical equipment (Class A)
    critical_df = df[df['Class'] == 'A'].head(50)

    st.subheader("Top 50 Critical Equipment (Class A)")

    # Filters
    col1, col2 = st.columns(2)

    with col1:
        discipline_filter = st.multiselect("Select Discipline", options=critical_df['Discipline'].unique())

    with col2:
        pm_filter = st.multiselect("Select PM Status", options=critical_df['PM Status'].unique())

    filtered_df = critical_df.copy()

    if discipline_filter:
        filtered_df = filtered_df[filtered_df['Discipline'].isin(discipline_filter)]

    if pm_filter:
        filtered_df = filtered_df[filtered_df['PM Status'].isin(pm_filter)]

    # Display table
    st.dataframe(filtered_df, use_container_width=True)

    # Summary metrics
    st.subheader("Summary")

    total = len(filtered_df)
    pm_done = len(filtered_df[filtered_df['PM Status'] == 'Covered'])
    pm_pending = len(filtered_df[filtered_df['PM Status'] != 'Covered'])

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Equipment", total)
    col2.metric("PM Covered", pm_done)
    col3.metric("PM Pending", pm_pending)

else:
    st.info("Please upload an Excel file to proceed.")

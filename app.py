import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Annual Mock Drill Tracker",
    page_icon="📅",
    layout="wide"
)

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>

.main{
    padding-top:20px;
}

.title{
    font-size:34px;
    font-weight:700;
    color:#1F2937;
}

.legend{
    display:flex;
    gap:20px;
    margin-bottom:25px;
}

.legend-item{
    display:flex;
    align-items:center;
    gap:8px;
    font-size:15px;
    font-weight:600;
}

.box{
    width:18px;
    height:18px;
    border-radius:4px;
}

table{
    width:100%;
    border-collapse:collapse;
    table-layout:fixed;
}

th{
    background:#f4f4f4;
    text-align:center;
    padding:10px;
    font-size:15px;
    position:sticky;
    top:0;
}

td{
    border:1px solid #ececec;
    height:36px;
    text-align:center;
}

.training{
    text-align:left;
    font-weight:600;
    padding-left:10px;
    width:320px;
}

.cell{
    width:100%;
    height:28px;
    border-radius:6px;
}

.planned{
    background:#FFC107;
}

.executed{
    background:#4CAF50;
}

.delayed{
    background:#E53935;
}

.empty{
    background:transparent;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------

st.markdown(
    "<div class='title'>Annual Mock Drill Tracker - 2026</div>",
    unsafe_allow_html=True
)

st.markdown("""
<div class='legend'>
<div class='legend-item'><div class='box planned'></div>Planned</div>
<div class='legend-item'><div class='box executed'></div>Executed</div>
<div class='legend-item'><div class='box delayed'></div>Delayed</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Load Data
# -----------------------------

df = pd.read_excel("C:\Users\sivas\Downloads\tracker_data.xlsx")

months = [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
]

trainings = df["Training"].unique()

# -----------------------------
# HTML Table
# -----------------------------

html = "<table>"

# Header

html += "<tr>"
html += "<th style='text-align:left;width:320px'>Training</th>"

for m in months:
    html += f"<th>{m}</th>"

html += "</tr>"

# Rows

for training in trainings:

    html += "<tr>"

    html += f"<td class='training'>{training}</td>"

    for month in months:

        rows = df[
            (df["Training"] == training) &
            (df["Month"] == month)
        ]

        if rows.empty:

            html += "<td></td>"

        else:

            cell_html = ""

            for _, r in rows.iterrows():

                status = r["Status"]

                if status == "Planned":
                    css = "planned"

                elif status == "Executed":
                    css = "executed"

                else:
                    css = "delayed"

                cell_html += f"<div class='cell {css}'></div>"

            html += f"<td>{cell_html}</td>"

    html += "</tr>"

html += "</table>"

st.markdown(html, unsafe_allow_html=True)

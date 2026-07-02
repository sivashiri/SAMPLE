import streamlit as st
import pandas as pd
from pathlib import Path

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Annual Mock Drill Tracker",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "tracker_data.xlsx"

df = pd.read_excel(DATA_FILE)

months = [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
]

# ---------------------------------------------------
# CSS
# ---------------------------------------------------

st.markdown("""
<style>

html, body, [class*="css"]{
    font-family:'Segoe UI',sans-serif;
}

/* Remove Streamlit menu */

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

/* Main */

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
    max-width:98%;
}

/* Header */

.title{

    font-size:42px;
    font-weight:700;

    color:#0F172A;

}

.subtitle{

    color:#64748B;

    font-size:17px;

    margin-top:-10px;

}

/* Toolbar */

.toolbar{

display:flex;

justify-content:space-between;

align-items:center;

margin-top:30px;

margin-bottom:25px;

}

/* Search */

.search{

padding:12px;

border-radius:10px;

border:1px solid #E5E7EB;

width:350px;

font-size:15px;

}

/* Legend */

.legend{

display:flex;

gap:20px;

margin-top:15px;

margin-bottom:25px;

}

.legend-item{

display:flex;

align-items:center;

gap:10px;

font-weight:600;

font-size:15px;

}

.legend-box{

width:18px;

height:18px;

border-radius:6px;

}

/* Table */

table{

width:100%;

border-collapse:separate;

border-spacing:0;

background:white;

border-radius:12px;

overflow:hidden;

box-shadow:0 4px 20px rgba(0,0,0,.05);

}

th{

background:#0F172A;

color:white;

padding:14px;

font-size:15px;

position:sticky;

top:0;

z-index:100;

}

th:first-child{

text-align:left;

padding-left:20px;

}

td{

border-bottom:1px solid #F1F5F9;

height:60px;

text-align:center;

}

.training{

text-align:left;

padding-left:20px;

font-weight:600;

font-size:16px;

width:350px;

background:white;

position:sticky;

left:0;

z-index:50;

}

/* Status Blocks */

.status{

height:34px;

border-radius:8px;

margin:auto;

width:42px;

transition:.25s;

}

.status:hover{

transform:scale(1.08);

}

.planned{

background:#3B82F6;

}

.executed{

background:#10B981;

}

.delayed{

background:#F97316;

}

.empty{

background:transparent;

}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

left, right = st.columns([8,2])

with left:

    st.markdown(
        "<div class='title'>Annual Mock Drill Calendar</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitle'>Annual Safety Mock Drill Schedule</div>",
        unsafe_allow_html=True
    )

with right:

    year = st.selectbox(
        "",
        [2026]
    )

# ---------------------------------------------------
# LEGEND
# ---------------------------------------------------

st.markdown("""

<div class="legend">

<div class="legend-item">
<div class="legend-box planned"></div>
Planned
</div>

<div class="legend-item">
<div class="legend-box executed"></div>
Executed
</div>

<div class="legend-item">
<div class="legend-box delayed"></div>
Delayed
</div>

</div>

""", unsafe_allow_html=True)

# ---------------------------------------------------
# SEARCH
# ---------------------------------------------------

search = st.text_input(
    "Search Training",
    placeholder="Type training name..."
)

if search:

    df = df[
        df["Training"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

# ---------------------------------------------------
# SORT
# ---------------------------------------------------

df = df.sort_values(
    ["Training","Month No"]
)

trainings = df["Training"].unique()

# ---------------------------------------------------
# START HTML TABLE
# ---------------------------------------------------

html = """

<table>

<tr>

<th style='width:350px'>Training</th>

"""

for month in months:

    html += f"<th>{month}</th>"

html += "</tr>"
# ---------------------------------------------------
# BUILD TABLE
# ---------------------------------------------------

for training in trainings:

    html += "<tr>"

    html += f"<td class='training'>{training}</td>"

    for month in months:

        month_data = df[
            (df["Training"] == training) &
            (df["Month"] == month)
        ]

        html += "<td>"

        if not month_data.empty:

            # Display all events for this month
            for _, row in month_data.iterrows():

                status = str(row["Status"]).strip().lower()

                if status == "planned":
                    css = "planned"

                elif status == "executed":
                    css = "executed"

                elif status == "delayed":
                    css = "delayed"

                else:
                    css = "empty"

                tooltip = (
                    f"{training}<br>"
                    f"Status : {row['Status']}<br>"
                    f"Type : {row['Type']}<br>"
                    f"Month : {month}"
                )

                html += f"""
                <div
                    class="status {css}"
                    title="{tooltip}"
                    style="margin-bottom:4px;">
                </div>
                """

        html += "</td>"

    html += "</tr>"

html += "</table>"

# ---------------------------------------------------
# DISPLAY
# ---------------------------------------------------

st.markdown(
    html,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

planned = (df["Status"] == "Planned").sum()
executed = (df["Status"] == "Executed").sum()
delayed = (df["Status"] == "Delayed").sum()

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Planned", planned)

with c2:
    st.metric("Executed", executed)

with c3:
    st.metric("Delayed", delayed)

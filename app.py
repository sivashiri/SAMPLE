import streamlit as st
import pandas as pd
from pathlib import Path

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="Annual Mock Drill Tracker",
    page_icon="🛡️",
    layout="wide"
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "tracker_data.xlsx"

df = pd.read_excel(DATA_FILE)

months = [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
]

# -------------------------------------------------
# PAGE CSS
# -------------------------------------------------

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.block-container{
    max-width:98%;
    padding-top:1rem;
}

body{
    background:#F6F8FC;
}

/* ---------- TITLE ---------- */

.title{
    font-size:40px;
    font-weight:700;
    color:#1F2937;
}

.subtitle{
    color:#6B7280;
    margin-bottom:20px;
}

/* ---------- LEGEND ---------- */

.legend{
    display:flex;
    gap:20px;
    margin-top:10px;
    margin-bottom:25px;
}

.item{
    display:flex;
    align-items:center;
    gap:8px;
    font-weight:600;
}

.box{
    width:18px;
    height:18px;
    border-radius:5px;
}

/* ---------- STATUS ---------- */

.status{
    width:42px;
    height:18px;
    border-radius:30px;
    margin:auto;
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

.monthHeader{

    text-align:center;

    font-weight:700;

    color:#374151;

}

.training{

    font-weight:600;

    color:#111827;

}

.row{

    background:white;

    border-radius:12px;

    padding:8px;

    margin-bottom:6px;

    box-shadow:0 1px 3px rgba(0,0,0,.08);

}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HEADER
# -------------------------------------------------

left,right = st.columns([8,2])

with left:

    st.markdown(
        "<div class='title'>Annual Mock Drill Tracker</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitle'>2026 Annual Safety Mock Drill Calendar</div>",
        unsafe_allow_html=True
    )

with right:

    year = st.selectbox(
        "Year",
        [2026]
    )

# -------------------------------------------------
# LEGEND
# -------------------------------------------------

st.markdown("""

<div class='legend'>

<div class='item'>
<div class='box planned'></div>
Planned
</div>

<div class='item'>
<div class='box executed'></div>
Executed
</div>

<div class='item'>
<div class='box delayed'></div>
Delayed
</div>

</div>

""", unsafe_allow_html=True)

# -------------------------------------------------
# SEARCH
# -------------------------------------------------

search = st.text_input(
    "",
    placeholder="🔍 Search training..."
)

if search:

    df = df[
        df["Training"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

trainings = sorted(df["Training"].unique())

# -------------------------------------------------
# MONTH HEADER
# -------------------------------------------------

header = st.columns([4] + [1]*12)

header[0].markdown("### Training")

for i,m in enumerate(months):

    header[i+1].markdown(
        f"<div class='monthHeader'>{m}</div>",
        unsafe_allow_html=True
    )
    # -------------------------------------------------
# CALENDAR GRID
# -------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

for training in trainings:

    row = st.columns([4] + [1]*12)

    # Training Name
    row[0].markdown(
        f"""
        <div class='training'>
            {training}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Months
    for i, month in enumerate(months):

        month_df = df[
            (df["Training"] == training) &
            (df["Month"] == month)
        ]

        with row[i+1]:

            if month_df.empty:

                st.markdown(
                    """
                    <div style="
                        height:18px;
                        width:42px;
                        margin:auto;
                    ">
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                for _, r in month_df.iterrows():

                    status = str(r["Status"]).lower()

                    if status == "planned":
   
                        color = "#FACC15"

                    elif status == "executed":

                        color = "#22C55E"

                    else:

                        color = "#EF4444"

                    st.markdown(
                        f"""
                        <div
                        title="{training} | {r['Status']}"
                        style="
                        background:{color};
                        height:18px;
                        width:42px;
                        border-radius:20px;
                        margin:auto;
                        margin-bottom:4px;
                        box-shadow:0px 2px 4px rgba(0,0,0,.15);
                        ">
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    st.markdown("<hr style='margin:4px 0;border:none;border-top:1px solid #F1F5F9;'>",
                unsafe_allow_html=True)
    # -------------------------------------------------
# SUMMARY
# -------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

planned = (df["Status"] == "Planned").sum()
executed = (df["Status"] == "Executed").sum()
delayed = (df["Status"] == "Delayed").sum()

total = len(df)

compliance = round(executed / total * 100)

st.markdown("## Dashboard Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Planned",
        planned
    )

with c2:
    st.metric(
        "Executed",
        executed
    )

with c3:
    st.metric(
        "Delayed",
        delayed
    )

with c4:
    st.metric(
        "Compliance",
        f"{compliance}%"
    )

st.markdown("---")

# -------------------------------------------------
# DOWNLOAD
# -------------------------------------------------

with open(DATA_FILE, "rb") as file:

    st.download_button(
        label="⬇ Download Schedule",
        data=file,
        file_name="tracker_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.markdown("<br>", unsafe_allow_html=True)

st.caption(
    "Annual Safety Mock Drill Calendar | © 2026"
)

import streamlit as st
import pandas as pd
import plotly.express as px
import os
# =================================
# LOAD DATA
# =================================
DATA_PATH = "Data"
def get_excel_file(keyword):
    
    for file in os.listdir(DATA_PATH):

        if file.endswith(".xlsx") and keyword.lower() in file.lower():
            return os.path.join(DATA_PATH, file)

    raise FileNotFoundError(
        f"No Excel file found containing '{keyword}'"
    )
store_df = pd.read_excel(
    get_excel_file("Store Build")
)
major_df = pd.read_excel(
    get_excel_file("Major Deployments")
)
minor_df = pd.read_excel(
    get_excel_file("Minor Deployments")
)
coo_df = pd.read_excel(
    get_excel_file("COO")
)
helpdesk_df = pd.read_excel(
    get_excel_file("Help Desk")
)
pta_df = pd.read_excel(
    get_excel_file("PTA")
)
hmtoy_df = pd.read_excel(
    get_excel_file("HM Toy")
)
market_df = pd.read_excel(
    get_excel_file("Market Request")
)
automation_df = pd.read_excel(
    get_excel_file("Automation")
)
validation_df = pd.read_excel(
    get_excel_file("Validation")
)
urgent_df = pd.read_excel(
    get_excel_file("Urgent Store Build")
)

##Months
# Minor Deployments
minor_df["Month"] = (
minor_df["Month"]
.astype(str)
.str.strip()
.str[:3]
.str.title()
)

# Urgent Store Build
urgent_df["Month"] = (
    urgent_df["Month"]
    .astype(str)
    .str.strip()
    .str[:3]
    .str.title()
)
# Store Build
store_df["Month"] = pd.to_datetime(
    store_df["Go Live Date"],
    errors="coerce"
).dt.strftime("%b")

# COO
coo_df["Month"] = pd.to_datetime(
    coo_df["Effective Date"],
    errors="coerce"
).dt.strftime("%b")

# Help Desk
helpdesk_df["Month"] = pd.to_datetime(
    helpdesk_df["Came to PCS Queue"],
    errors="coerce"
).dt.strftime("%b")

# HM Toy
hmtoy_df["Month"] = pd.to_datetime(
    hmtoy_df["GL Date"],
    errors="coerce"
).dt.strftime("%b")

# PTA
pta_df["Month"] = pd.to_datetime(
    pta_df["Date Indexed"],
    errors="coerce"
).dt.strftime("%b")

# Market Request
market_df["Month"] = pd.to_datetime(
    market_df["Delivery Date"],
    errors="coerce"
).dt.strftime("%b")
st.sidebar.header("Filters")


##Month Slicer
month_order = [
    "Jan","Feb","Mar","Apr",
    "May","Jun","Jul","Aug",
    "Sep","Oct","Nov","Dec"
]

selected_months = st.sidebar.multiselect(
    "Select Month(s)",
    month_order,
    default=month_order
)

def filter_month(df):

    if "Month" not in df.columns:
        return df

    if len(selected_months) == 0:
        return df

    return df[
        df["Month"].isin(selected_months)
    ]

major_df = filter_month(major_df)
minor_df = filter_month(minor_df)
store_df = filter_month(store_df)
coo_df = filter_month(coo_df)
helpdesk_df = filter_month(helpdesk_df)
pta_df = filter_month(pta_df)
hmtoy_df = filter_month(hmtoy_df)
market_df = filter_month(market_df)
urgent_df = filter_month(urgent_df)

# =================================
# KPI CALCULATIONS
# =================================

major_count = len(major_df)

minor_count = len(minor_df)

store_count = len(store_df)

urgent_count = len(urgent_df)

coo_count = coo_df["Restaurant Count"].fillna(0).sum()

helpdesk_count = len(helpdesk_df)

pta_count = (
    pta_df["Menu Items Count"]
    .fillna(0)
    .sum()
)


hmtoy_count = len(hmtoy_df)

market_count = len(market_df)

automation_count = (
    automation_df["Improvement Category"]
    .count()
)

validation_count = validation_df.count().sum()

total_deployments = minor_count

# =================================
# HEADER
# =================================

# =================================
# PAGE CONFIG
# =================================

st.set_page_config(
    page_title="2026 Executive Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =================================
# GLOBAL CSS
# =================================

st.markdown("""
<style>

.stApp{
    background-color:#efefef;
}

.top-header{
    background:#d9d9d9;
    border-radius:12px;
    padding:15px;
    border:1px solid #c0c0c0;
    margin-bottom:20px;
}

.metric-box{
    background:white;
    border-radius:8px;
    padding:12px;
    text-align:center;
    box-shadow:0px 4px 12px rgba(0,0,0,0.20);
}

.metric-value{
    font-size:38px;
    font-weight:bold;
    color:black;
}

.metric-label{
    font-size:14px;
    color:#222;
}

</style>
""", unsafe_allow_html=True)

# =================================
# HEADER SECTION
# =================================

header_col1,header_col2,header_col3,header_col4,header_col5 = st.columns(
    [2,1,2,2,2]
)

# --------------------------
# LOGOS
# --------------------------

with header_col1:

    logo1,logo2 = st.columns([1,1])

    with logo1:
        st.image(
            r"C:\Users\aisdhana\Documents\Metrics\Images\Capgemini-Logo.wine.png",
            width=130
        )

    with logo2:
        st.image(
            r"C:\Users\aisdhana\Documents\Metrics\Images\mcdonalds-logo-mcdonald-icon-free-free-vector.jpg",
            width=90
        )

    st.markdown(
        """
        <div style='text-align:center'>
        <b>2026</b><br>
        Key Highlights
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------
# DEPLOYMENTS
# --------------------------

with header_col3:

    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-value'>
        {total_deployments}
        </div>
        <div class='metric-label'>
        RFM Deployments (Till Date)
        </div>
    </div>
    """,
    unsafe_allow_html=True)

# --------------------------
# SUCCESS RATE
# --------------------------

with header_col4:

    st.markdown("""
    <div class='metric-box'>
        <div class='metric-value'>
        100%
        </div>
        <div class='metric-label'>
        Success Rate, Zero Rollbacks
        </div>
    </div>
    """,
    unsafe_allow_html=True)

# --------------------------
# MARKET REQUESTS
# --------------------------

with header_col5:

    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-value'>
        {market_count}
        </div>
        <div class='metric-label'>
        Market Requests Supported
        </div>
    </div>
    """,
    unsafe_allow_html=True)

st.markdown("---")

# =================================
# SECOND ROW
# =================================

c1,c2,c3,c4,c5 = st.columns(5)

c1.metric(
    "Urgent Builds",
    urgent_count
)

c2.metric(
    "PTA Uploads",
    int(pta_count)
)

c3.metric(
    "HM Toy Campaigns",
    hmtoy_count
)

c4.metric(
    "Market Requests",
    market_count
)

c5.metric(
    "Automation Ideas",
    automation_count
)

st.divider()

# =================================
# KEY INITIATIVES PANEL
# =================================

st.markdown("""
<style>

.yellow-panel{
    background:#FFC000;
    padding:15px;
    border-radius:12px;
}

.white-card{
    background:white;
    border-radius:20px;
    padding:20px;
    text-align:center;
    margin-bottom:20px;
}

.title-panel{
    color:white;
    font-size:32px;
    font-weight:bold;
    text-align:center;
    margin-bottom:20px;
}

.green{
    color:#1F7A1F;
    font-weight:bold;
}

.red{
    color:#C00000;
    font-weight:bold;
}

.blue{
    color:#0B5E8E;
    font-weight:bold;
}

.light-text{
    color:gray;
    font-style:italic;
}

</style>
""", unsafe_allow_html=True)

# =================================
# CHARTS
# =================================

left,middle,right = st.columns([1,2,2])
st.markdown("""
<style>

[data-testid="stVerticalBlockBorderWrapper"]{
    background:white;
    border-radius:20px;
    padding:10px;
    margin-bottom:12px;
    box-shadow:0px 3px 8px rgba(0,0,0,0.15);
}

</style>
""", unsafe_allow_html=True)

with left:

    st.markdown("""
    <div style="
        background:#FFC000;
        color:white;
        text-align:center;
        padding:15px;
        border-radius:12px;
        font-size:22px;
        font-weight:bold;
        margin-bottom:10px;
    ">
        2026 Key Initiatives
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(
            "<h4 style='color:#228B22;text-align:center'>New Store Builds</h4>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<h2 style='text-align:center'>{store_count}</h2>",
            unsafe_allow_html=True,
        )
        st.caption("Stores")

    with st.container(border=True):
        st.markdown(
            "<h4 style='color:red;text-align:center'>COO</h4>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<h2 style='text-align:center'>{int(coo_count)}</h2>",
            unsafe_allow_html=True,
        )
        st.caption("Surveys")

    with st.container(border=True):
        st.markdown(
            "<h4 style='color:#005B96;text-align:center'>Helpdesk</h4>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<h2 style='text-align:center'>{helpdesk_count}</h2>",
            unsafe_allow_html=True,
        )
        st.caption("Tickets")

    with st.container(border=True):
        st.markdown(
            "<h4 style='color:#0096FF;text-align:center'>RFM Deployments</h4>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<h2 style='text-align:center'>{total_deployments}</h2>",
            unsafe_allow_html=True,
        )
        st.caption("Zero Noise")


with middle:

    st.subheader("Major Deployments")

    month_order = [
    "Jan","Feb","Mar","Apr",
    "May","Jun","Jul","Aug",
    "Sep","Oct","Nov","Dec"
]

    chart = (
        major_df.groupby("Month")
        .size()
        .reset_index(name="Count")
    )

    chart["Month"] = pd.Categorical(
        chart["Month"],
        categories=month_order,
        ordered=True
    )

    chart = chart.sort_values("Month")


    fig = px.bar(
    chart,
    x="Month",
    y="Count",
    text="Count",
    color_discrete_sequence=["#0070C0"]
)

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        title="Major Deployments by Month",
        title_x=0.5,
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False,
        height=450
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

# Minor Deployment Trend

with right:

    st.subheader("Minor Deployments")

    if "Month" in minor_df.columns:

        chart = (
            minor_df
            .groupby("Month")
            .size()
            .reset_index(name="Count")
        )

        fig = px.bar(
            chart,
            x="Month",
            y="Count",
            color="Count",
            title="Minor Deployments by Month"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

# =================================
# FOCUS AREAS
# =================================

st.divider()

st.subheader("Key Highlights")

col1,col2,col3 = st.columns(3)

with col1:

    st.success(
        f"Total Deployments : {total_deployments}"
    )

    st.success(
        f"Store Builds : {store_count}"
    )

    st.success(
        f"Urgent Store Builds : {urgent_count}"
    )

with col2:

    st.info(
        f"Help Desk Tickets : {helpdesk_count}"
    )

    st.info(
        f"PTA Uploads : {pta_count}"
    )

    st.info(
        f"Market Requests : {market_count}"
    )

with col3:

    st.warning(
        f"HM Toy Campaigns : {hmtoy_count}"
    )

    st.warning(
        f"Automation Ideas : {automation_count}"
    )

    st.warning(
        f"Validation Entries : {validation_count}"
    )

# =================================
# RAW DATA SECTION
# =================================

with st.expander("View Source Data"):

    dataset = st.selectbox(
        "Choose Dataset",
        [
            "Major Deployments",
            "Minor Deployments",
            "Store Builds",
            "COO",
            "Help Desk",
            "PTA",
            "HM Toy",
            "Market Requests",
            "Automation"
        ]
    )

    mapping = {
        "Major Deployments": major_df,
        "Minor Deployments": minor_df,
        "Store Builds": store_df,
        "COO": coo_df,
        "Help Desk": helpdesk_df,
        "PTA": pta_df,
        "HM Toy": hmtoy_df,
        "Market Requests": market_df,
        "Automation": automation_df
    }

    st.dataframe(
        mapping[dataset],
        width="stretch"
    )
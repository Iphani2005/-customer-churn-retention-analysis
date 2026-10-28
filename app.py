import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Customer Churn & Revenue Retention",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .main {
        background-color: #f7f9fc;
    }

    /* Header */
    .header {
        background: linear-gradient(135deg, #172554, #2563eb);
        padding: 35px;
        border-radius: 15px;
        margin-bottom: 25px;
        color: white !important;
    }

    .header h1 {
        font-size: 38px;
        margin-bottom: 10px;
        font-weight: 700;
        color: white !important;
    }

    .header p {
        font-size: 18px;
        margin: 0;
        opacity: 0.9;
        color: white !important;
    }

    /* KPI Cards */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        text-align: center;
        color: #111827 !important;
    }

    .metric-title {
        font-size: 14px;
        color: #6b7280 !important;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #111827 !important;
    }

    /* Section titles */
    .section-title {
        font-size: 24px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
        color: #111827 !important;
    }

    /* ========================================================
       RETENTION STRATEGY CARDS
       ======================================================== */

    .risk-card {
        padding: 18px;
        border-radius: 12px;
        background: white !important;
        border: 1px solid #e5e7eb;
        margin-bottom: 10px;
        color: #111827 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .risk-card * {
        color: #111827 !important;
    }

    .risk-card h3 {
        color: #111827 !important;
        font-size: 22px;
        margin-bottom: 10px;
    }

    .risk-card p {
        color: #374151 !important;
        font-size: 16px;
        line-height: 1.5;
        margin-bottom: 0;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #6b7280 !important;
        padding: 30px;
        margin-top: 30px;
    }

</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================

RISK_FILE = "outputs/customer_churn_risk_scores.csv"
CLEAN_FILE = "outputs/telco_customer_churn_cleaned.csv"

try:
    df = pd.read_csv(RISK_FILE)
    clean_df = pd.read_csv(CLEAN_FILE)

except FileNotFoundError:
    st.error(
        "CSV files were not found. Make sure the app is running "
        "from the main project folder."
    )
    st.stop()

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="header">
    <h1>Customer Churn & Revenue Retention Analysis</h1>
    <p>
        Machine Learning powered customer churn prediction,
        risk segmentation and revenue retention intelligence
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Dashboard Filters")

risk_options = ["All"] + sorted(
    df["ChurnRiskBand"].dropna().unique().tolist()
)

selected_risk = st.sidebar.selectbox(
    "Select Risk Level",
    risk_options
)

filtered_df = df.copy()

if selected_risk != "All":
    filtered_df = filtered_df[
        filtered_df["ChurnRiskBand"] == selected_risk
    ]

st.sidebar.markdown("---")

st.sidebar.info(
    "Use the filters to analyze customers based on their predicted "
    "churn risk and revenue exposure."
)

# ============================================================
# KPI CALCULATIONS
# ============================================================

total_customers = len(filtered_df)

if total_customers > 0:

    churn_rate = filtered_df["ChurnFlag"].mean() * 100

    churned_customers = filtered_df["ChurnFlag"].sum()

    annual_revenue_risk = filtered_df.loc[
        filtered_df["ChurnFlag"] == 1,
        "EstimatedAnnualRevenue"
    ].sum()

else:

    churn_rate = 0
    churned_customers = 0
    annual_revenue_risk = 0

# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Total Customers</div>
            <div class="metric-value">{total_customers:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Churn Rate</div>
            <div class="metric-value">{churn_rate:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Churned Customers</div>
            <div class="metric-value">{int(churned_customers):,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Annual Revenue at Risk</div>
            <div class="metric-value">£{annual_revenue_risk:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "⚠️ Risk Analysis",
    "💰 Revenue Analysis",
    "👤 Customer Details"
])

# ============================================================
# TAB 1 — OVERVIEW
# ============================================================

with tab1:

    st.markdown(
        '<div class="section-title">Customer Churn Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        churn_counts = (
            filtered_df["Churn"]
            .value_counts()
            .reset_index()
        )

        churn_counts.columns = ["Churn", "Count"]

        fig = px.pie(
            churn_counts,
            names="Churn",
            values="Count",
            title="Customer Churn Distribution",
            hole=0.45
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        contract_churn = (
            filtered_df
            .groupby("Contract")["ChurnFlag"]
            .mean()
            .reset_index()
        )

        contract_churn["ChurnRate"] = (
            contract_churn["ChurnFlag"] * 100
        )

        fig = px.bar(
            contract_churn,
            x="Contract",
            y="ChurnRate",
            title="Churn Rate by Contract Type",
            labels={
                "ChurnRate": "Churn Rate (%)",
                "Contract": "Contract"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.histogram(
            filtered_df,
            x="MonthlyCharges",
            color="Churn",
            title="Monthly Charges Distribution",
            nbins=30
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        internet_churn = (
            filtered_df
            .groupby("InternetService")["ChurnFlag"]
            .mean()
            .reset_index()
        )

        internet_churn["ChurnRate"] = (
            internet_churn["ChurnFlag"] * 100
        )

        fig = px.bar(
            internet_churn,
            x="InternetService",
            y="ChurnRate",
            title="Churn Rate by Internet Service",
            labels={
                "ChurnRate": "Churn Rate (%)"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ============================================================
# TAB 2 — RISK ANALYSIS
# ============================================================

with tab2:

    st.markdown(
        '<div class="section-title">Customer Risk Analysis</div>',
        unsafe_allow_html=True
    )

    risk_summary = (
        df.groupby("ChurnRiskBand")
        .agg(
            Customers=("customerID", "count"),
            ChurnRate=("ChurnFlag", "mean"),
            RevenueRisk=("EstimatedAnnualRevenue", "sum")
        )
        .reset_index()
    )

    risk_summary["ChurnRate"] *= 100

    risk_order = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    risk_summary["ChurnRiskBand"] = pd.Categorical(
        risk_summary["ChurnRiskBand"],
        categories=risk_order,
        ordered=True
    )

    risk_summary = risk_summary.sort_values(
        "ChurnRiskBand"
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            risk_summary,
            x="ChurnRiskBand",
            y="Customers",
            title="Customers by Risk Level",
            text="Customers"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.bar(
            risk_summary,
            x="ChurnRiskBand",
            y="ChurnRate",
            title="Actual Churn Rate by Risk Level",
            text="ChurnRate",
            labels={
                "ChurnRate": "Churn Rate (%)"
            }
        )

        fig.update_traces(
            texttemplate="%{text:.1f}%"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("### Risk Summary")

    display_risk = risk_summary.copy()

    display_risk["ChurnRate"] = (
        display_risk["ChurnRate"]
        .map(lambda x: f"{x:.1f}%")
    )

    display_risk["RevenueRisk"] = (
        display_risk["RevenueRisk"]
        .map(lambda x: f"£{x:,.0f}")
    )

    st.dataframe(
        display_risk,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# TAB 3 — REVENUE ANALYSIS
# ============================================================

with tab3:

    st.markdown(
        '<div class="section-title">Revenue Risk Analysis</div>',
        unsafe_allow_html=True
    )

    revenue_by_churn = (
        filtered_df
        .groupby("Churn")[
            "EstimatedAnnualRevenue"
        ]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        revenue_by_churn,
        x="Churn",
        y="EstimatedAnnualRevenue",
        title="Annual Revenue by Churn Status",
        labels={
            "EstimatedAnnualRevenue": "Annual Revenue (£)"
        },
        text_auto=".2s"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    contract_revenue = (
        filtered_df
        .groupby("Contract")[
            "EstimatedAnnualRevenue"
        ]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        contract_revenue,
        x="Contract",
        y="EstimatedAnnualRevenue",
        title="Annual Revenue by Contract Type",
        labels={
            "EstimatedAnnualRevenue": "Annual Revenue (£)"
        },
        text_auto=".2s"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("### Revenue Insights")

    churned_revenue = filtered_df.loc[
        filtered_df["ChurnFlag"] == 1,
        "EstimatedAnnualRevenue"
    ].sum()

    st.info(
        f"Current filtered segment represents approximately "
        f"£{churned_revenue:,.0f} in annual revenue associated "
        f"with churned customers."
    )

# ============================================================
# TAB 4 — CUSTOMER DETAILS
# ============================================================

with tab4:

    st.markdown(
        '<div class="section-title">Customer Risk Details</div>',
        unsafe_allow_html=True
    )

    customer_search = st.text_input(
        "Search Customer ID",
        placeholder="Example: 7590-VHVEG"
    )

    details_df = filtered_df.copy()

    if customer_search:

        details_df = details_df[
            details_df["customerID"]
            .astype(str)
            .str.contains(
                customer_search,
                case=False,
                na=False
            )
        ]

    columns_to_show = [
        "customerID",
        "Contract",
        "tenure",
        "MonthlyCharges",
        "Churn",
        "PredictedChurnProbability",
        "ChurnRiskBand",
        "EstimatedAnnualRevenue",
        "RecommendedRetentionAction"
    ]

    available_columns = [
        col
        for col in columns_to_show
        if col in details_df.columns
    ]

    display_df = details_df[
        available_columns
    ].copy()

    if "PredictedChurnProbability" in display_df.columns:

        display_df["PredictedChurnProbability"] = (
            display_df["PredictedChurnProbability"]
            .map(lambda x: f"{x:.1%}")
        )

    if "EstimatedAnnualRevenue" in display_df.columns:

        display_df["EstimatedAnnualRevenue"] = (
            display_df["EstimatedAnnualRevenue"]
            .map(lambda x: f"£{x:,.2f}")
        )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# RETENTION STRATEGY
# ============================================================

st.markdown(
    '<div class="section-title">Retention Strategy</div>',
    unsafe_allow_html=True
)

strategy_col1, strategy_col2 = st.columns(2)

# -------------------- LEFT COLUMN ----------------------------

with strategy_col1:

    st.markdown("""
    <div class="risk-card">
        <h3>🔴 Critical Risk</h3>
        <p>
        Immediate intervention. Review service quality,
        identify customer complaints and provide personalized
        retention offers.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="risk-card">
        <h3>🟠 High Risk</h3>
        <p>
        Run proactive retention campaigns and encourage
        customers to move from month-to-month contracts
        to longer-term plans.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -------------------- RIGHT COLUMN ---------------------------

with strategy_col2:

    st.markdown("""
    <div class="risk-card">
        <h3>🟡 Medium Risk</h3>
        <p>
        Improve onboarding, customer support and payment
        experience before customers become high risk.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="risk-card">
        <h3>🟢 Low Risk</h3>
        <p>
        Maintain normal service levels and avoid unnecessary
        promotional spending.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# ABOUT PROJECT
# ============================================================

with st.expander("About This Project"):

    st.write("""
    This project combines Machine Learning, SQL, Business Analysis
    and Power BI concepts to analyze customer churn and revenue risk.

    The Machine Learning pipeline compares Logistic Regression,
    Random Forest and a tuned Random Forest model.

    The tuned Random Forest prioritizes recall because identifying
    customers who are likely to churn is more important than simply
    maximizing overall accuracy.

    The final output provides customer-level churn probability,
    risk segmentation and recommended retention actions.
    """)

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    Customer Churn & Revenue Retention Analysis |
    Machine Learning + Business Analytics
</div>
""", unsafe_allow_html=True)
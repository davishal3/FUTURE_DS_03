import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Marketing Funnel Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# CUSTOM CSS (PREMIUM UI)
# ==============================
st.markdown("""
<style>
.metric-card {
    background-color: #111827;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
}
.title {
    font-size: 28px;
    font-weight: bold;
}
.subtitle {
    color: gray;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">📊 Marketing Funnel Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Conversion & Campaign Performance Analysis</div>', unsafe_allow_html=True)

# ==============================
# LOAD DATA
# ==============================
@st.cache_data
def load_data():
    return pd.read_csv('data/processed/cleaned_bank_data.csv')

df = load_data()

# ==============================
# SIDEBAR
# ==============================
st.sidebar.header("🔍 Filters")

job = st.sidebar.multiselect("Job", df['job'].dropna().unique(), default=df['job'].dropna().unique())
month = st.sidebar.multiselect("Month", df['month'].dropna().unique(), default=df['month'].dropna().unique())
contact = st.sidebar.multiselect("Contact", df['contact'].dropna().unique(), default=df['contact'].dropna().unique())

filtered_df = df[
    (df['job'].isin(job)) &
    (df['month'].isin(month)) &
    (df['contact'].isin(contact))
]

# ==============================
# KPI SECTION (PREMIUM CARDS)
# ==============================
total = len(filtered_df)
converted = filtered_df['converted'].sum()
conversion_rate = (converted / total) * 100 if total else 0
engaged = filtered_df['engaged'].sum()

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f'<div class="metric-card"><h3>Total Users</h3><h2>{total}</h2></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="metric-card"><h3>Converted</h3><h2>{int(converted)}</h2></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="metric-card"><h3>Conversion Rate</h3><h2>{conversion_rate:.2f}%</h2></div>', unsafe_allow_html=True)
col4.markdown(f'<div class="metric-card"><h3>Engaged Users</h3><h2>{engaged}</h2></div>', unsafe_allow_html=True)

st.markdown("---")

# ==============================
# ADVANCED FUNNEL (WITH %)
# ==============================
st.subheader("📉 Funnel Analysis (Advanced)")

total_users = len(filtered_df)
contacted_users = filtered_df['contacted'].sum()
engaged_users = filtered_df['engaged'].sum()
converted_users = filtered_df['converted'].sum()

funnel_df = pd.DataFrame({
    "Stage": ["Total", "Contacted", "Engaged", "Converted"],
    "Users": [total_users, contacted_users, engaged_users, converted_users]
})

# Conversion %
funnel_df["Conversion %"] = funnel_df["Users"] / total_users * 100

fig_funnel = px.funnel(
    funnel_df,
    x="Users",
    y="Stage",
    text="Conversion %",
    color="Stage",
    title="User Funnel with Conversion %"
)

fig_funnel.update_traces(texttemplate="%{text:.2f}%")
fig_funnel.update_layout(transition_duration=800)

st.plotly_chart(fig_funnel, use_container_width=True)

# ==============================
# CHARTS (ANIMATED + CLEAN)
# ==============================
st.subheader("📊 Conversion Insights")

col1, col2 = st.columns(2)

# Job
job_conv = filtered_df.groupby('job')['converted'].mean().reset_index()

fig_job = px.bar(
    job_conv,
    x='job',
    y='converted',
    color='converted',
    title="Conversion by Job",
    animation_frame=None
)

fig_job.update_layout(transition_duration=800)
col1.plotly_chart(fig_job, use_container_width=True)

# Age
age_conv = filtered_df.groupby('age_group')['converted'].mean().reset_index()

fig_age = px.bar(
    age_conv,
    x='age_group',
    y='converted',
    color='converted',
    title="Conversion by Age Group"
)

fig_age.update_layout(transition_duration=800)
col2.plotly_chart(fig_age, use_container_width=True)

# ==============================
# MONTH + CONTACT
# ==============================
col3, col4 = st.columns(2)

month_conv = filtered_df.groupby('month')['converted'].mean().reset_index()

fig_month = px.line(
    month_conv,
    x='month',
    y='converted',
    markers=True,
    title="Monthly Conversion Trend"
)

fig_month.update_layout(transition_duration=800)
col3.plotly_chart(fig_month, use_container_width=True)

contact_conv = filtered_df.groupby('contact')['converted'].mean().reset_index()

fig_contact = px.pie(
    contact_conv,
    names='contact',
    values='converted',
    title="Contact Type Performance"
)

col4.plotly_chart(fig_contact, use_container_width=True)

# ==============================
# CAMPAIGN ANALYSIS
# ==============================
st.subheader("📈 Campaign Performance")

campaign_conv = filtered_df.groupby('campaign')['converted'].mean().reset_index()

fig_campaign = px.scatter(
    campaign_conv.head(100),
    x='campaign',
    y='converted',
    size='converted',
    title="Campaign vs Conversion (Bubble View)"
)

fig_campaign.update_layout(transition_duration=800)
st.plotly_chart(fig_campaign, use_container_width=True)

# ==============================
# INSIGHTS SECTION
# ==============================
st.subheader("💡 Business Insights")

st.markdown("""
- 🔻 Biggest drop happens before **engagement stage**
- 📞 Contact type strongly affects conversion
- 💼 Some job roles show significantly higher conversion
- 📅 Seasonal trends visible in monthly performance
- 🔁 Increasing campaign calls does not guarantee success

### 🚀 Recommendations:
- Improve **call quality & engagement strategy**
- Focus on **high-converting segments**
- Optimize campaigns for **best-performing months**
- Use **effective contact methods**
""")
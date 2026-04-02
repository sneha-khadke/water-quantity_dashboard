import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Water Quality Dashboard", layout="wide")

# Title
st.title("💧 Water Quality Analysis Dashboard")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("water_dataX.csv", encoding='latin1')
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")

state = st.sidebar.selectbox("Select State", df["STATE"].unique())
year = st.sidebar.selectbox("Select Year", df["year"].unique())

filtered_df = df[(df["STATE"] == state) & (df["year"] == year)]

# Show data
st.subheader("📊 Filtered Data")
st.dataframe(filtered_df)

# KPI Metrics
st.subheader("📈 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Avg Temp", round(filtered_df["Temp"].mean(), 2))
col2.metric("Avg pH", round(filtered_df["PH"].mean(), 2))
col3.metric("Avg DO", round(filtered_df["D.O. (mg/l)"].mean(), 2))

# Charts
st.subheader("📉 Visualizations")

# Temperature vs pH
fig1, ax1 = plt.subplots()
sns.scatterplot(data=filtered_df, x="Temp", y="PH", ax=ax1)
ax1.set_title("Temperature vs pH")
st.pyplot(fig1)

# BOD distribution
fig2, ax2 = plt.subplots()
sns.histplot(filtered_df["B.O.D. (mg/l)"], kde=True, ax=ax2)
ax2.set_title("BOD Distribution")
st.pyplot(fig2)

# DO trend
fig3, ax3 = plt.subplots()
sns.lineplot(data=filtered_df, x="LOCATIONS", y="D.O. (mg/l)", ax=ax3)
ax3.set_title("Dissolved Oxygen by Location")
plt.xticks(rotation=90)
st.pyplot(fig3)

# Correlation Heatmap
st.subheader("🔥 Correlation Heatmap")

numeric_df = filtered_df.select_dtypes(include=['float64', 'int64'])

fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax4)
st.pyplot(fig4)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")

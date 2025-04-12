import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Team Dismissal Sensitivity", layout="wide")
st.title("🧨 Team Sensitivity to Dismissal Types")
st.markdown("See which teams are more prone to specific types of dismissals.")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("data/mw_overall.csv")

df = load_data()

# Dismissal columns (you can adjust based on what matters most)
dismissal_cols = ["bowled", "caught", "caught and bowled", "lbw", "run out"]

# Group by team and sum dismissals
dismissal_summary = df.groupby("batting_team")[dismissal_cols].sum()

# Option to normalize (convert counts to % of total dismissals for each team)
normalize = st.checkbox("Normalize (Show % of each dismissal type)", value=True)

if normalize:
    dismissal_summary = dismissal_summary.div(dismissal_summary.sum(axis=1), axis=0) * 100

# Reset index for Plotly
dismissal_summary = dismissal_summary.reset_index()
dismissal_melted = dismissal_summary.melt(id_vars="batting_team", var_name="Dismissal Type", value_name="Count")

# Plot
fig = px.imshow(
    dismissal_summary.set_index("batting_team")[dismissal_cols],
    labels=dict(x="Dismissal Type", y="Team", color="Dismissal Count" if not normalize else "Percentage"),
    x=dismissal_cols,
    y=dismissal_summary["batting_team"],
    color_continuous_scale="Reds"
)

st.plotly_chart(fig, use_container_width=True)

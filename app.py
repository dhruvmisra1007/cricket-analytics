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

# Common dismissal types to analyze
dismissal_cols = ["bowled", "caught", "caught and bowled", "lbw", "run out"]

# Group by batting team and sum dismissals
dismissal_summary = df.groupby("batting_team")[dismissal_cols].sum()

# Option to normalize values
normalize = st.checkbox("Normalize (Show % of each dismissal type)", value=True)

if normalize:
    dismissal_summary = dismissal_summary.div(dismissal_summary.sum(axis=1), axis=0) * 100

# Melt data for long-form format required by density_heatmap
dismissal_long = dismissal_summary.reset_index().melt(
    id_vars="batting_team",
    var_name="Dismissal Type",
    value_name="Value"
)

# Sort to prioritize higher values in visualization
dismissal_long = dismissal_long.sort_values(by="Value", ascending=False)

# Plot heatmap
fig = px.density_heatmap(
    dismissal_long,
    x="Dismissal Type",
    y="batting_team",
    z="Value",
    color_continuous_scale="Reds",
    labels={
        "batting_team": "Team",
        "Value": "Dismissal Count" if not normalize else "Percentage"
    },
    height=800
)

fig.update_layout(
    xaxis=dict(tickangle=45),
    yaxis=dict(autorange="reversed"),
    margin=dict(l=100, r=20, t=40, b=40)
)

st.plotly_chart(fig, use_container_width=True)

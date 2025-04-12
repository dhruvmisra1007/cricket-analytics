import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Team Dismissal Analysis", layout="wide")
st.title("🎯 Team Dismissal Breakdown")
st.markdown("Select a team and season to view dismissal type distribution.")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("data/mw_overall.csv")

df = load_data()

# Ensure expected columns are present
dismissal_cols = ["bowled", "caught", "caught and bowled", "lbw", "run out"]
required_cols = dismissal_cols + ["batting_team", "season"]
missing_cols = [col for col in required_cols if col not in df.columns]

if missing_cols:
    st.error(f"The following required columns are missing from the dataset: {missing_cols}")
else:
    # Choose season
    available_seasons = sorted(df["season"].dropna().unique())
    selected_season = st.radio("📅 Select Season", available_seasons, horizontal=True)

    # Filter data by selected season
    season_df = df[df["season"] == selected_season]

    # Choose team
    teams = sorted(season_df["batting_team"].dropna().unique())
    selected_team = st.selectbox("🏏 Select Team", teams)

    # Aggregate dismissal counts for selected team
    team_dismissals = (
        season_df[season_df["batting_team"] == selected_team][dismissal_cols]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    team_dismissals.columns = ["Dismissal Type", "Count"]

    # Remove dismissal types with zero counts (optional)
    team_dismissals = team_dismissals[team_dismissals["Count"] > 0]

    # Plot Pie Chart
    fig = px.pie(
        team_dismissals,
        names="Dismissal Type",
        values="Count",
        title=f"{selected_team} Dismissal Breakdown - {selected_season}",
        color_discrete_sequence=px.colors.sequential.Reds
    )

    st.plotly_chart(fig, use_container_width=True)

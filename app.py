import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cricket Analytics Dashboard", layout="wide")

st.title("🏏 Cricket Analytics Dashboard")
st.markdown("Explore batsman performance against different bowlers")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("data/mw_overall.csv")

df = load_data()

# Basic cleanup (ensure column names exist and are consistent)
if 'batsman' not in df.columns or 'bowler' not in df.columns or 'runs' not in df.columns:
    st.error("Missing essential columns like 'batsman', 'bowler', or 'runs' in the dataset.")
else:
    # Player Selection
    selected_player = st.selectbox("Select a Player", sorted(df['batsman'].dropna().unique()))

    # Filter data for the selected player
    player_df = df[df['batsman'] == selected_player]

    if player_df.empty:
        st.warning(f"No data available for {selected_player}")
    else:
        # Group by bowler to get runs scored against each
        bowler_summary = (
            player_df.groupby('bowler')['runs']
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
        )

        st.subheader(f"Top 5 Bowlers Against Whom {selected_player} Scored the Most Runs")
        fig = px.bar(bowler_summary, x='bowler', y='runs',
                     labels={'runs': 'Total Runs', 'bowler': 'Bowler'},
                     color='runs',
                     color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)

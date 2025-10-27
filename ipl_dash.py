# ipl_dashboard.py
import os
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# ---------------------------
# Page Setup
# ---------------------------
st.set_page_config(page_title="🏏 IPL Dashboard", layout="wide", page_icon="🏏")
st.title("🏏 IPL Data Analysis Dashboard")

# ---------------------------
# Load Data
# ---------------------------
def load_data(file_path="matches.csv"):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        st.sidebar.success("Data loaded successfully from matches.csv")
    else:
        uploaded = st.sidebar.file_uploader("Upload IPL Dataset (CSV)", type="csv")
        if uploaded is not None:
            df = pd.read_csv(uploaded)
            st.sidebar.success("File uploaded successfully!")
        else:
            st.warning("Please upload matches.csv to continue.")
            st.stop()
    return df

df = load_data()

# ---------------------------
# Basic Info
# ---------------------------
st.sidebar.header("Filter Options")
seasons = sorted(df["season"].unique())
selected_season = st.sidebar.selectbox("Select Season", options=["All"] + list(seasons))

if selected_season != "All":
    df = df[df["season"] == selected_season]

# ---------------------------
# Key Metrics
# ---------------------------
total_matches = len(df)
total_teams = len(pd.unique(df[["team1", "team2"]].values.ravel("K")))
top_team = df["winner"].value_counts().idxmax()
top_venue = df["venue"].value_counts().idxmax()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Matches", total_matches)
col2.metric("Total Teams", total_teams)
col3.metric("Most Winning Team", top_team)
col4.metric("Most Played Venue", top_venue)

# ---------------------------
# Plot 1: Most Winning Teams (Plotly)
# ---------------------------
st.subheader("🏆 Most Winning Teams")
win_counts = df["winner"].value_counts().reset_index()
win_counts.columns = ["Team", "Wins"]
fig = px.bar(win_counts, x="Team", y="Wins", color="Wins",
             color_continuous_scale="Blues", title="Most Winning Teams in IPL")
st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Plot 2: Matches per Season (Seaborn + Matplotlib)
# ---------------------------
st.subheader("📅 Matches Played per Season")
season_counts = df["season"].value_counts().sort_index()
fig2, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x=season_counts.index, y=season_counts.values, palette="viridis", ax=ax)
ax.set_xlabel("Season")
ax.set_ylabel("Number of Matches")
ax.set_title("Matches Played per Season")
st.pyplot(fig2)

# ---------------------------
# Plot 3: Top Venues (Plotly)
# ---------------------------
st.subheader("🏟️ Top Stadiums by Matches")
venue_counts = df["venue"].value_counts().reset_index().head(10)
venue_counts.columns = ["Venue", "Matches"]
fig3 = px.bar(venue_counts, x="Venue", y="Matches", color="Matches",
              color_continuous_scale="sunset", title="Top 10 Venues by Matches")
st.plotly_chart(fig3, use_container_width=True)

# ---------------------------
# Plot 4: Toss Decision Impact (Seaborn)
# ---------------------------
if "toss_decision" in df.columns:
    st.subheader("🎲 Toss Decision Impact")
    toss = df["toss_decision"].value_counts()
    fig4, ax4 = plt.subplots()
    sns.barplot(x=toss.index, y=toss.values, palette="Set2", ax=ax4)
    ax4.set_title("Toss Decision Distribution")
    st.pyplot(fig4)

# ---------------------------
# Plot 5: Team vs Season (Matplotlib)
# ---------------------------
st.subheader("📊 Top 5 Teams Wins Across Seasons")
top5_teams = df["winner"].value_counts().nlargest(5).index
team_wins_by_season = df[df["winner"].isin(top5_teams)].groupby(["season", "winner"]).size().unstack().fillna(0)
fig5, ax5 = plt.subplots(figsize=(10, 5))
team_wins_by_season.plot(kind="bar", ax=ax5)
plt.title("Top 5 Teams Wins per Season")
plt.xlabel("Season")
plt.ylabel("Wins")
st.pyplot(fig5)

# ---------------------------
# Table
# ---------------------------
st.subheader("📋 Dataset Preview")
st.dataframe(df.head(10))

st.markdown("---")
st.caption("Made with ❤️ using Streamlit, pandas, plotly, seaborn, matplotlib, and os.")

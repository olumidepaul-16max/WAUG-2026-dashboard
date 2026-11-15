import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE SETUP
# ============================================================
st.set_page_config(
    page_title="WAUG 2026 OAU Dashboard",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# COMPATIBILITY HELPER - BadgeColumn only exists in Streamlit >= 1.44
# ============================================================
def badge_col(label, options=None):
    """Returns BadgeColumn if available, else falls back to TextColumn."""
    if hasattr(st.column_config, "BadgeColumn"):
        return st.column_config.BadgeColumn(label, options=options, format="%s")
    return st.column_config.TextColumn(label)

# ============================================================
# CSS
# ============================================================
st.markdown("""
<style>
.hero {
    background: linear-gradient(135deg, #7A0016 0%, #50000E 55%, #0B1220 100%);
    border-left: 6px solid #FACC15;
    border-radius: 14px;
    padding: 30px 36px;
    margin-bottom: 28px;
    box-shadow: 0 8px 24px rgba(0,0,0,.35);
}
.hero-badge {
    display: inline-block;
    background: #FACC15;
    color: #0B1220;
    font-weight: 800;
    font-size: .72rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 999px;
    margin-bottom: 12px;
}
.hero h1 {
    color: #FFFFFF;
    font-size: 2.3rem;
    font-weight: 800;
    letter-spacing: -.5px;
    margin: 0 0 8px 0;
    line-height: 1.15;
}
.hero p { color: #FACC15; font-size: 1rem; font-weight: 500; margin: 0; }
.hero .hero-sub { color: #CBD5E1; font-size: .9rem; font-weight: 400; margin-top: 10px; }
.card-label {
    font-size: .78rem;
    font-weight: 800;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    color: #FACC15;
    margin-bottom: 12px;
}
.stTabs [data-baseweb="tab-list"] { gap: 8px; border-bottom: 2px solid #243049; padding-bottom: 8px; }
.stTabs [data-baseweb="tab"] {
    background-color: #16213A;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 700;
    font-size: .92rem;
}
.stTabs [data-baseweb="tab"]:hover { background-color: #1F2D4A; }
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background-color: #FACC15 !important;
    color: #0B1220 !important;
}
[data-testid="stMetricValue"] { color: #FACC15 !important; font-weight: 800 !important; }
[data-testid="stMetricLabel"] { color: #94A3B8 !important; font-weight: 700 !important; }
[data-testid="stMetricDelta"] { color: #4ADE80 !important; font-weight: 600 !important; }
[data-testid="stDataFrame"] { border-radius: 10px; }
[data-testid="stSidebar"] { border-right: 2px solid #243049; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# CHART HELPER
# ============================================================
def style_chart(fig, title=None, height=380, y_title=None):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#CBD5E1",
        title_font_color="#FACC15",
        title_font_size=16,
        margin=dict(t=60 if title else 30, b=40, l=50, r=20),
        height=height,
        hoverlabel=dict(bgcolor="#16213A", font_color="#FFFFFF", bordercolor="#FACC15"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font_color="#CBD5E1"),
        xaxis=dict(gridcolor="#243049", zerolinecolor="#243049", linecolor="#334155"),
        yaxis=dict(gridcolor="#243049", zerolinecolor="#243049", linecolor="#334155", title=y_title),
        bargap=0.35
    )
    if title:
        fig.update_layout(title=dict(text=title, x=0.5, xanchor="center"))
    return fig

GOLD = "#FACC15"
CRIMSON = "#E11D48"
NAVY = "#38BDF8"
GREEN = "#4ADE80"
GREY = "#94A3B8"

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.image("https://img.icons8.com/color/96/trophy.png", width=68)
st.sidebar.markdown("### 🏆 WAUG 2026")
st.sidebar.markdown("*West African Universities Games*")

sport = st.sidebar.selectbox(
    "Select Sport",
    ["Football", "Basketball", "Volleyball", "Table Tennis", "Lawn Tennis", "Swimming", "Handball"]
)

st.sidebar.markdown("---")
with st.sidebar.expander("🏅 Overall Medal Standings", expanded=False):
    medal_df = pd.DataFrame([
        {"University": "OAU", "Gold": 38, "Silver": 24, "Bronze": 18, "Total": 80},
        {"University": "UNILAG", "Gold": 31, "Silver": 27, "Bronze": 20, "Total": 78},
        {"University": "UG Legon", "Gold": 22, "Silver": 21, "Bronze": 26, "Total": 69},
        {"University": "UI", "Gold": 17, "Silver": 20, "Bronze": 23, "Total": 60},
        {"University": "KNUST", "Gold": 14, "Silver": 16, "Bronze": 21, "Total": 51},
    ])
    st.dataframe(
        medal_df, use_container_width=True, hide_index=True,
        column_config={
            "Gold": st.column_config.NumberColumn("🥇", format="%d"),
            "Silver": st.column_config.NumberColumn("🥈", format="%d"),
            "Bronze": st.column_config.NumberColumn("🥉", format="%d"),
        }
    )

st.sidebar.markdown("---")
st.sidebar.caption("📍 OAU, Ile-Ife, Nigeria")
st.sidebar.caption("📅 2026 Games")

# ============================================================
# DATA
# ============================================================
@st.cache_data
def get_football():
    matches = pd.DataFrame([
        {"Match": "OAU Giants vs UNILAG Marines", "Stage": "Final", "Score": "2 - 1", "Venue": "OAU Main Bowl", "Status": "Completed"},
        {"Match": "UG Legon vs UI Pioneers", "Stage": "Semi-Final", "Score": "1 (4) - 1 (3)", "Venue": "OAU Mini Stadium", "Status": "Penalty"},
        {"Match": "OAU Giants vs KNUST Titans", "Stage": "Semi-Final", "Score": "3 - 0", "Venue": "OAU Main Bowl", "Status": "Completed"},
        {"Match": "UNILAG Marines vs ABU Zaria", "Stage": "Quarter-Final", "Score": "1 - 0", "Venue": "OAU Mini Stadium", "Status": "Completed"},
    ])
    standings = pd.DataFrame([
        {"Team": "OAU Giants", "P": 5, "W": 4, "D": 1, "L": 0, "GF": 12, "GA": 3, "Pts": 13},
        {"Team": "UG Legon", "P": 5, "W": 3, "D": 2, "L": 0, "GF": 9, "GA": 4, "Pts": 11},
        {"Team": "UNILAG Marines", "P": 5, "W": 3, "D": 0, "L": 2, "GF": 8, "GA": 6, "Pts": 9},
        {"Team": "UI Pioneers", "P": 5, "W": 2, "D": 1, "L": 2, "GF": 6, "GA": 5, "Pts": 7},
    ])
    goals = pd.DataFrame({"Stage": ["Group Stage", "Quarter-Final", "Semi-Final", "Final"], "Goals": [24, 12, 6, 3]})
    teams_goals = pd.DataFrame({"Team": ["OAU Giants", "UG Legon", "UNILAG Marines", "UI Pioneers"], "Goals For": [12, 9, 8, 6]})
    return matches, standings, goals, teams_goals

@st.cache_data
def get_basketball():
    teams = pd.DataFrame([
        {"Team": "OAU Titans", "PPG": 88.5, "OPPG": 71.2, "Wins": 6},
        {"Team": "UNILAG Waves", "PPG": 84.2, "OPPG": 73.8, "Wins": 5},
        {"Team": "KNUST Kings", "PPG": 79.0, "OPPG": 75.4, "Wins": 4},
        {"Team": "UI Warriors", "PPG": 76.4, "OPPG": 74.9, "Wins": 3},
        {"Team": "UNN Sparks", "PPG": 71.1, "OPPG": 77.6, "Wins": 2},
    ])
    results = pd.DataFrame([
        {"Match": "OAU Titans vs KNUST Kings", "Score": "92 - 81", "Winner": "OAU Titans", "Stage": "Final"},
        {"Match": "UNILAG Waves vs UI Warriors", "Score": "85 - 78", "Winner": "UNILAG Waves", "Stage": "Semi-Final"},
        {"Match": "OAU Titans vs UNN Sparks", "Score": "88 - 74", "Winner": "OAU Titans", "Stage": "Semi-Final"},
        {"Match": "UNILAG Waves vs KNUST Kings", "Score": "79 - 82", "Winner": "KNUST Kings", "Stage": "Quarter-Final"},
    ])
    return teams, results

@st.cache_data
def get_volleyball():
    table = pd.DataFrame([
        {"University": "OAU Spikers", "Played": 6, "Wins": 6, "Losses": 0, "Sets Ratio": "18:2", "Points": 18, "Standing": "1st (Pool A)"},
        {"University": "University of Benin", "Played": 6, "Wins": 5, "Losses": 1, "Sets Ratio": "15:6", "Points": 15, "Standing": "2nd (Pool A)"},
        {"University": "University of Ghana", "Played": 6, "Wins": 4, "Losses": 2, "Sets Ratio": "13:8", "Points": 13, "Standing": "1st (Pool B)"},
        {"University": "ABU Zaria", "Played": 6, "Wins": 3, "Losses": 3, "Sets Ratio": "10:10", "Points": 10, "Standing": "2nd (Pool B)"},
    ])
    sets = pd.DataFrame({"University": ["OAU Spikers", "Uniben Smashers", "UG Legon Volley", "ABU Zaria", "UI Nets"], "Sets Won": [18, 15, 13, 10, 8]})
    return table, sets

@st.cache_data
def get_table_tennis():
    matches = pd.DataFrame([
        {"Category": "Men's Singles Final", "Player 1": "Adebayo T. (OAU)", "Player 2": "Mensah K. (UG Legon)", "Score": "4 - 2", "Winner": "Adebayo T. (OAU)"},
        {"Category": "Women's Singles Final", "Player 1": "Olatunji R. (UNILAG)", "Player 2": "Chukwu E. (UNN)", "Score": "4 - 1", "Winner": "Olatunji R. (UNILAG)"},
        {"Category": "Mixed Doubles Final", "Player 1": "OAU Duo", "Player 2": "UNILAG Duo", "Score": "3 - 0", "Winner": "OAU Duo"},
    ])
    cats = pd.DataFrame({"Category": ["Men's Singles", "Women's Singles", "Men's Doubles", "Women's Doubles", "Mixed Doubles"], "Matches": [7, 6, 5, 5, 6]})
    return matches, cats

@st.cache_data
def get_lawn_tennis():
    matches = pd.DataFrame([
        {"Round": "Final", "Player A": "Ibrahim S. (OAU)", "Player B": "Adekunle D. (UNILAG)", "Score": "6-4, 6-3", "Status": "Completed"},
        {"Round": "Semi-Final", "Player A": "Ibrahim S. (OAU)", "Player B": "Boateng A. (UG)", "Score": "7-5, 6-3", "Status": "Completed"},
        {"Round": "Quarter-Final", "Player A": "Ibrahim S. (OAU)", "Player B": "Okafor C. (UI)", "Score": "6-4, 6-2", "Status": "Completed"},
    ])
    rounds = pd.DataFrame({"Round": ["Round of 16", "Quarter-Final", "Semi-Final", "Final"], "Matches": [8, 4, 2, 1]})
    return matches, rounds

@st.cache_data
def get_swimming():
    table = pd.DataFrame([
        {"Event": "100m Freestyle (Men)", "Athlete": "David E. (OAU)", "Time (s)": 52.41, "Time": "52.41s", "Medal": "Gold"},
        {"Event": "100m Freestyle (Women)", "Athlete": "Folake B. (UNILAG)", "Time (s)": 58.12, "Time": "58.12s", "Medal": "Gold"},
        {"Event": "200m Medley Relay", "Athlete": "University of Ghana Team", "Time (s)": 108.30, "Time": "1m 48.3s", "Medal": "Gold"},
        {"Event": "50m Butterfly (Men)", "Athlete": "Kofi A. (KNUST)", "Time (s)": 24.89, "Time": "24.89s", "Medal": "Gold"},
        {"Event": "50m Butterfly (Women)", "Athlete": "Amina S. (OAU)", "Time (s)": 27.31, "Time": "27.31s", "Medal": "Gold"},
    ])
    times = pd.DataFrame({
        "Event": ["100m Free (M)", "100m Free (W)", "200m Medley", "50m Fly (M)", "50m Fly (W)"],
        "Time (s)": [52.41, 58.12, 108.30, 24.89, 27.31]
    })
    return table, times

@st.cache_data
def get_handball():
    matches = pd.DataFrame([
        {"Match": "OAU Panthers vs UNILAG Hammers", "Stage": "Final", "Score": "32 - 28", "Venue": "OAU Sports Hall", "Status": "Completed"},
        {"Match": "UG Legon vs UI Strikers", "Stage": "Semi-Final", "Score": "27 - 25", "Venue": "OAU Sports Hall", "Status": "Completed"},
        {"Match": "OAU Panthers vs KNUST Titans", "Stage": "Semi-Final", "Score": "35 - 29", "Venue": "OAU Sports Hall", "Status": "Completed"},
    ])
    goals = pd.DataFrame({"Stage": ["Group Stage", "Quarter-Final", "Semi-Final", "Final"], "Goals": [48, 32, 24, 16]})
    return matches, goals

# ============================================================
# HERO HEADER
# ============================================================
SPORT_EMOJI = {
    "Football": "⚽", "Basketball": "🏀", "Volleyball": "🏐",
    "Table Tennis": "🏓", "Lawn Tennis": "🎾", "Swimming": "🏊", "Handball": "🤾‍♂️"
}
SPORT_DESC = {
    "Football": "Premier Division — Group Stage to Final",
    "Basketball": "Men's Championship — Preliminaries to Final",
    "Volleyball": "Men's Pool Championship — Groups A & B",
    "Table Tennis": "Singles & Doubles — Individual Categories",
    "Lawn Tennis": "Men's Singles — Knockout Bracket",
    "Swimming": "Aquatics — Freestyle, Butterfly & Medley Relay",
    "Handball": "Men's Championship — Group Stage to Final"
}

st.markdown(f"""
<div class="hero">
    <span class="hero-badge">{SPORT_EMOJI[sport]} {sport} Division</span>
    <h1>{SPORT_DESC[sport]}</h1>
    <p>West African Universities Games 2026 · Obafemi Awolowo University, Ile-Ife</p>
    <p class="hero-sub">Official live results, standings and performance statistics</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# PAGES
# ============================================================
if sport == "Football":
    matches, standings, goals, teams_goals = get_football()
    tab1, tab2, tab3 = st.tabs(["📋 Match Results", "📊 Statistics", "🏅 Standings"])

    with tab1:
        with st.container(border=True):
            st.markdown('<div class="card-label">Match Results</div>', unsafe_allow_html=True)
            st.dataframe(
                matches, use_container_width=True, hide_index=True,
                column_config={
                    "Status": badge_col("Status", ["Completed", "Penalty"]),
                    "Score": st.column_config.TextColumn("Score"),
                }
            )

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown('<div class="card-label">Goals by Stage</div>', unsafe_allow_html=True)
                fig = px.bar(goals, x="Stage", y="Goals", color_discrete_sequence=[GOLD])
                st.plotly_chart(style_chart(fig, "Goals per Tournament Stage", y_title="Goals"), use_container_width=True)
        with c2:
            with st.container(border=True):
                st.markdown('<div class="card-label">Goals Scored by Team</div>', unsafe_allow_html=True)
                fig = px.bar(teams_goals, x="Team", y="Goals For", color_discrete_sequence=[CRIMSON])
                st.plotly_chart(style_chart(fig, "Top Scorers", y_title="Goals"), use_container_width=True)

    with tab3:
        with st.container(border=True):
            st.markdown('<div class="card-label">Group Standings</div>', unsafe_allow_html=True)
            st.dataframe(
                standings, use_container_width=True, hide_index=True,
                column_config={
                    "Pts": st.column_config.ProgressColumn("Points", min_value=0, max_value=15, format="%d"),
                    "GF": st.column_config.NumberColumn("Goals For", format="%d"),
                    "GA": st.column_config.NumberColumn("Goals Against", format="%d"),
                }
            )

elif sport == "Basketball":
    teams, results = get_basketball()
    tab1, tab2, tab3 = st.tabs(["📋 Game Results", "📊 Team Performance", "🏆 Leaders"])

    with tab1:
        with st.container(border=True):
            st.markdown('<div class="card-label">Game Results</div>', unsafe_allow_html=True)
            st.dataframe(
                results, use_container_width=True, hide_index=True,
                column_config={
                    "Winner": badge_col("Winner", ["OAU Titans", "UNILAG Waves", "KNUST Kings", "UI Warriors", "UNN Sparks"]),
                }
            )

    with tab2:
        with st.container(border=True):
            st.markdown('<div class="card-label">Scoring Comparison</div>', unsafe_allow_html=True)
            fig = px.bar(teams, x="Team", y=["PPG", "OPPG"], barmode="group",
                         color_discrete_map={"PPG": GOLD, "OPPG": GREY})
            st.plotly_chart(style_chart(fig, "Points Scored vs Conceded per Game", y_title="Points"), use_container_width=True)

    with tab3:
        with st.container(border=True):
            st.markdown('<div class="card-label">Team Standings</div>', unsafe_allow_html=True)
            st.dataframe(
                teams, use_container_width=True, hide_index=True,
                column_config={
                    "PPG": st.column_config.ProgressColumn("Points / Game", min_value=60, max_value=95, format="%.1f"),
                    "Wins": st.column_config.ProgressColumn("Wins", min_value=0, max_value=6, format="%d"),
                }
            )

elif sport == "Volleyball":
    table, sets = get_volleyball()
    tab1, tab2 = st.tabs(["🏐 Pool Standings", "📊 Sets Analysis"])

    with tab1:
        with st.container(border=True):
            st.markdown('<div class="card-label">Pool Standings</div>', unsafe_allow_html=True)
            st.dataframe(
                table, use_container_width=True, hide_index=True,
                column_config={
                    "Points": st.column_config.ProgressColumn("Set Points", min_value=0, max_value=18, format="%d"),
                    "Standing": badge_col("Standing"),
                }
            )

    with tab2:
        with st.container(border=True):
            st.markdown('<div class="card-label">Sets Won by Team</div>', unsafe_allow_html=True)
            fig = px.bar(sets, x="University", y="Sets Won", color_discrete_sequence=[NAVY])
            st.plotly_chart(style_chart(fig, "Sets Won Across Pools", y_title="Sets"), use_container_width=True)

elif sport == "Table Tennis":
    matches, cats = get_table_tennis()
    tab1, tab2 = st.tabs(["🏓 Finals Results", "📊 Category Breakdown"])

    with tab1:
        with st.container(border=True):
            st.markdown('<div class="card-label">Championship Finals</div>', unsafe_allow_html=True)
            st.dataframe(
                matches, use_container_width=True, hide_index=True,
                column_config={"Winner": badge_col("Champion")},
            )

    with tab2:
        with st.container(border=True):
            st.markdown('<div class="card-label">Matches by Category</div>', unsafe_allow_html=True)
            fig = px.bar(cats, x="Category", y="Matches", color_discrete_sequence=[GOLD])
            st.plotly_chart(style_chart(fig, "Matches Played per Category", y_title="Matches"), use_container_width=True)

elif sport == "Lawn Tennis":
    matches, rounds = get_lawn_tennis()
    tab1, tab2 = st.tabs(["🎾 Knockout Results", "📊 Bracket Progression"])

    with tab1:
        with st.container(border=True):
            st.markdown('<div class="card-label">Knockout Results</div>', unsafe_allow_html=True)
            st.dataframe(
                matches, use_container_width=True, hide_index=True,
                column_config={"Status": badge_col("Status", ["Completed", "Pending"])},
            )

    with tab2:
        with st.container(border=True):
            st.markdown('<div class="card-label">Matches by Round</div>', unsafe_allow_html=True)
            fig = px.bar(rounds, x="Round", y="Matches", color_discrete_sequence=[CRIMSON])
            st.plotly_chart(style_chart(fig, "Knockout Bracket Size", y_title="Matches"), use_container_width=True)

elif sport == "Swimming":
    table, times = get_swimming()
    tab1, tab2 = st.tabs(["🏊 Event Results", "📊 Timing Analysis"])

    with tab1:
        with st.container(border=True):
            st.markdown('<div class="card-label">Aquatics Results</div>', unsafe_allow_html=True)
            st.dataframe(
                table, use_container_width=True, hide_index=True,
                column_config={
                    "Medal": badge_col("Medal", ["Gold", "Silver", "Bronze"]),
                    "Time (s)": st.column_config.ProgressColumn("Time (s)", min_value=20, max_value=110, format="%.2f"),
                }
            )

    with tab2:
        with st.container(border=True):
            st.markdown('<div class="card-label">Winning Times</div>', unsafe_allow_html=True)
            fig = px.bar(times, x="Event", y="Time (s)", color_discrete_sequence=[NAVY])
            st.plotly_chart(style_chart(fig, "Performance Times (Lower is Better)", y_title="Seconds"), use_container_width=True)

elif sport == "Handball":
    matches, goals = get_handball()
    tab1, tab2 = st.tabs(["🤾 Match Results", "📊 Goals Analysis"])

    with tab1:
        with st.container(border=True):
            st.markdown('<div class="card-label">Match Results</div>', unsafe_allow_html=True)
            st.dataframe(
                matches, use_container_width=True, hide_index=True,
                column_config={"Status": badge_col("Status", ["Completed", "Scheduled"])},
            )

    with tab2:
        with st.container(border=True):
            st.markdown('<div class="card-label">Goals by Stage</div>', unsafe_allow_html=True)
            fig = px.bar(goals, x="Stage", y="Goals", color_discrete_sequence=[GOLD])
            st.plotly_chart(style_chart(fig, "Handball Goals per Stage", y_title="Goals"), use_container_width=True)

st.markdown("---")
st.caption("📌 **WAUG 2026 Official Analytics** · Obafemi Awolowo University Sports Directorate")
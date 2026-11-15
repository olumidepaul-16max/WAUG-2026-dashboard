# WAUG 2026 OAU Sports Dashboard

A **Streamlit** dashboard for the **West African Universities Games (WAUG) 2026**, hosted at
**Obafemi Awolowo University (OAU), Ile-Ife, Nigeria**.

## Sports Covered

| Sport | Division |
|-------|----------|
| ⚽ Football | Premier Division — Group Stage to Final |
| 🏀 Basketball | Men's Championship — Preliminaries to Final |
| 🏐 Volleyball | Men's Pool Championship — Groups A & B |
| 🏓 Table Tennis | Singles & Doubles — Individual Categories |
| 🎾 Lawn Tennis | Men's Singles — Knockout Bracket |
| 🏊 Swimming | Aquatics — Freestyle, Butterfly & Medley Relay |
| 🤾‍♂️ Handball | Men's Championship — Group Stage to Final |

## Features

- **Hero header banner** with sport-specific branding
- **Deep navy + gold (OAU crimson/amber) custom theme** via `.streamlit/config.toml`
- **Tabbed layout** per sport — Results, Statistics and Standings
- **Clean bordered cards** for every metric, chart and table block
- **Transparent Plotly charts** that blend seamlessly with the theme
- **Progress bars** (`ProgressColumn`) for points, PPG, wins and swim times
- **Badge pills** (`BadgeColumn`) for status, winners, standings and medals
- **Collapsible overall medal table** in the sidebar

## Project Structure

```
waug-streamlit/
├── .streamlit/
│   └── config.toml     # Custom colour theme
├── app.py              # Dashboard application
├── requirements.txt    # Dependencies
└── README.md           # Documentation
```

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

## Deploy to Streamlit Cloud

1. Push this repository to GitHub (make sure it is **Public**).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **Create app** → select this repository, branch `main`, main file path `app.py`.
4. Click **Deploy**.

Streamlit Cloud will build the app and generate a public link.

## Requirements

```
streamlit>=1.32
pandas
plotly
```

## Credits

WAUG 2026 Official Analytics · Obafemi Awolowo University Sports Directorate

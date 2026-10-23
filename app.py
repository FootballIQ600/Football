
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Football IQ | Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- COLOURS AND STYLING ----------

st.markdown(
    """
    <style>
    :root {
        --navy: #0b1220;
        --panel: #141f30;
        --green: #65e6a1;
        --muted: #94a3b8;
    }

    .stApp {
        background: var(--navy);
        color: #f1f5f9;
    }

    [data-testid="stHeader"] {
        background: rgba(11, 18, 32, 0.95);
    }

    [data-testid="stSidebar"] {
        background: #101a2a;
        border-right: 1px solid #253247;
    }

    [data-testid="stSidebar"] * {
        color: #e2e8f0;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    h1, h2, h3 {
        color: #f8fafc !important;
        letter-spacing: -0.5px;
    }

    p, label {
        color: #cbd5e1;
    }

    .brand {
        font-size: 1.7rem;
        font-weight: 800;
        color: #f8fafc;
        letter-spacing: 1px;
    }

    .brand span {
        color: var(--green);
    }

    .subtitle {
        color: var(--muted);
        font-size: 0.9rem;
        margin-top: -8px;
        margin-bottom: 24px;
    }

    .section-label {
        color: var(--muted);
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .metric-card {
        background: linear-gradient(
            145deg, #172438, #111c2c
        );
        border: 1px solid #29374b;
        border-radius: 15px;
        padding: 20px;
        min-height: 145px;
    }

    .metric-label {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-bottom: 12px;
    }

    .metric-value {
        color: #f8fafc;
        font-size: 1.8rem;
        font-weight: 750;
        margin-bottom: 8px;
    }

    .metric-note {
        color: #65e6a1;
        font-size: 0.8rem;
    }

    .panel {
        background: #141f30;
        border: 1px solid #29374b;
        border-radius: 15px;
        padding: 22px;
        margin-top: 8px;
        margin-bottom: 12px;
    }

    .panel-description {
        color: #94a3b8;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    .status-pill {
        display: inline-block;
        background: #173e2b;
        color: #65e6a1;
        padding: 6px 11px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
    }

div.stButton > button {
    background: #65e6a1 !important;
    color: #0b1220 !important;
    border: 1px solid #65e6a1 !important;
    border-radius: 9px;
    font-weight: 700;
    min-height: 42px;
}

div.stButton > button p,
div.stButton > button span {
    color: #0b1220 !important;
}

div.stButton > button:hover {
    background: #8af0b8 !important;
    color: #0b1220 !important;
    border-color: #8af0b8 !important;
}

    div[data-testid="stMetric"] {
        background: #141f30;
        border: 1px solid #29374b;
        border-radius: 12px;
        padding: 16px;
    }

    div[data-testid="stMetricLabel"] {
        color: #94a3b8;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc;
    }

    hr {
        border-color: #29374b;
    }

    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- SIDEBAR ----------

with st.sidebar:
    st.markdown(
        '<div class="brand">⚽ FOOTBALL <span>IQ</span></div>',
        unsafe_allow_html=True,
    )
    st.caption("MATCH ANALYTICS & PERFORMANCE")
    st.divider()
    
    pages = [
        "Dashboard",
        "Historical Data",
        "Upcoming Fixtures",
        "Match Predictions",
        "Bankroll Tracker",
    ]

    if "selected_page" not in st.session_state:
        st.session_state["selected_page"] = "Dashboard"

    page = st.radio(
        "NAVIGATION",
        pages,
        key="selected_page",
        label_visibility="visible",
    )


    st.divider()
    st.markdown("**YOUR ANALYTICS HUB**")
    st.caption(
        "Fixtures, statistical probabilities "
        "and bankroll management."
    )
    st.markdown(
        '<span class="status-pill">● APP READY</span>',
        unsafe_allow_html=True,
    )

# ---------- DASHBOARD ----------

if page == "Dashboard":
    st.markdown(
        '<div class="brand">Your Football <span>Dashboard</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="subtitle">'
        'Your central hub for fixtures, match analysis '
        'and bankroll performance.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-label">YOUR OVERVIEW</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">📅 Upcoming fixtures</div>
                <div class="metric-value">—</div>
                <div class="metric-note">Awaiting fixture data</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">📊 Predictions recorded</div>
                <div class="metric-value">0</div>
                <div class="metric-note">No predictions recorded yet</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">💷 Current bankroll</div>
                <div class="metric-value">Not set</div>
                <div class="metric-note">Configure your starting balance</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    left, right = st.columns([1.4, 1])

    with left:
        st.markdown(
            """
            <div class="panel">
                <h3>⚽ Match Centre</h3>
                <p class="panel-description">
                    Your upcoming football fixtures will appear here.
                    We'll connect the app to a football data provider
                    so matches, competitions and kickoff times can
                    be loaded automatically.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Explore Upcoming Fixtures",
            use_container_width=True,
        ):
            st.session_state["selected_page"] = "Upcoming Fixtures"
            st.rerun()

    with right:
        st.markdown(
            """
            <div class="panel">
                <h3>🎯 Prediction Lab</h3>
                <p class="panel-description">
                    Analyse both teams to score (BTTS), over 2.5 goals
                    and other match markets using historical results
                    and team performance.
                </p>
                <hr>
                <p class="panel-description">
                    <strong>Model status:</strong>
                    Awaiting historical data
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Explore Match Predictions",
            use_container_width=True,
        ):
            st.session_state["selected_page"] = "Match Predictions"
            st.rerun()

    st.markdown(
        """
        <div class="panel">
            <h3>💷 Bankroll Management</h3>
            <p class="panel-description">
                Track your starting balance, stakes, settled bets,
                profit and loss. Your actual results will be kept
                separate from model predictions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Open Bankroll Tracker"):
        st.session_state["selected_page"] = "Bankroll Tracker"
        st.rerun()

    st.caption(
        "Analysis and record-keeping only. Probabilities are estimates, "
        "and no prediction guarantees a result."
    )

# ---------- OTHER PAGES: PLACEHOLDERS ----------

# ---------- HISTORICAL DATA ----------

elif page == "Historical Data":
    st.title("📊 Historical Data")
    st.caption("Explore your historical football results")

    csv_file = Path(__file__).resolve().parent / "historical_results.csv"

    if not csv_file.exists():
        st.error(
            "Could not find historical_results.csv. "
            "Please check that it is in your Football_App folder."
        )
    else:
        try:
            results = pd.read_csv(csv_file)

            if "Date" in results.columns:
                results["Date"] = pd.to_datetime(
                    results["Date"], errors="coerce"
                )

            for column in ["FTHG", "FTAG"]:
                if column in results.columns:
                    results[column] = pd.to_numeric(
                        results[column], errors="coerce"
                    )

            st.success("Historical results loaded successfully!")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Matches loaded", f"{len(results):,}")

            with col2:
                if "Competition" in results.columns:
                    st.metric(
                        "Competitions",
                        results["Competition"].nunique()
                    )

            st.subheader("Match Results")

            if "Competition" in results.columns:
                competitions = sorted(
                    results["Competition"].dropna().unique().tolist()
                )
                selected_competitions = st.multiselect(
                    "Filter by competition",
                    competitions,
                    default=competitions,
                )
                results = results[
                    results["Competition"].isin(selected_competitions)
                ]

            st.dataframe(
                results,
                use_container_width=True,
                hide_index=True,
            )

            st.caption(
                "Showing the results stored in your local CSV file."
            )

        except (OSError, ValueError, pd.errors.ParserError) as error:
            st.error(f"Could not read the CSV file: {error}")

elif page == "Upcoming Fixtures":
    st.title("📅 Upcoming Fixtures")
    st.caption("Your football match centre")
    st.info(
        "Fixture data has not been connected yet. "
        "No live fixtures are being displayed."
    )
    st.write(
        "Planned competitions: Premier League, Championship, "
        "League One and League Two."
    )

elif page == "Match Predictions":
    st.title("🎯 Match Predictions")
    st.caption("Statistical match analysis")
    st.info(
        "The prediction model is not connected yet. "
        "No match probabilities have been generated."
    )
    st.write(
        "Planned markets: BTTS, over 2.5 goals and "
        "estimated probabilities based on historical results."
    )

elif page == "Bankroll Tracker":
    st.title("💷 Bankroll Tracker")
    st.caption("Manage and review your betting records")
    st.info(
        "Bankroll tracking has not been configured yet. "
        "No balance or betting results have been assumed."
    )
    st.write(
        "Next we'll add your starting balance, bet records, "
        "stakes, odds, settled results and profit/loss."
    )

st.divider()
st.caption("FOOTBALL IQ  •  ANALYTICS & PERFORMANCE")

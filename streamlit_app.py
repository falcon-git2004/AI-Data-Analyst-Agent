import matplotlib

matplotlib.use("Agg")  # no GUI windows: safe inside server threads

import os
import shutil
import tempfile
import threading
import time

import pandas as pd
import streamlit as st

from agent.planner import DataAnalysisAgent
from agent.executor import AgentExecutor

from tools.quick_analyzer import quick_analyze
from tools.visual_explorer import build_visuals
from tools.llm_assistant import (
    DEFAULT_MODEL,
    LLMError,
    answer_question,
    build_context,
    explain_results
)


# ==========================
# Page Config
# ==========================

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="🤖",
    layout="wide"
)


# ==========================
# Emerald + Gold Theme
# ==========================

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Manrope:wght@400;500;600;700&display=swap');

:root {
    --bg: #07181a;
    --panel: #0d2326;
    --panel2: #122c30;
    --line: #1f3d41;
    --text: #e4f3ef;
    --mute: #85a8a3;
    --gold: #e2c27c;
    --gold2: #f3dca6;
    --emerald: #4fd1a5;
    --glow: rgba(79, 209, 165, 0.13);
}

/* ---------- Base ---------- */
.stApp {
    background:
        radial-gradient(900px 500px at 85% -10%, rgba(79, 209, 165, 0.10), transparent 60%),
        radial-gradient(700px 400px at 0% 100%, rgba(226, 194, 124, 0.06), transparent 60%),
        var(--bg);
    font-family: 'Manrope', system-ui, sans-serif;
}

.stApp, .stApp p, .stApp label, .stApp li {
    color: var(--text);
    font-family: 'Manrope', system-ui, sans-serif;
}

.block-container {
    padding-top: 2rem;
    max-width: 1600px;
}

/* ---------- Headings ---------- */
h1 {
    font-family: 'Fraunces', serif !important;
    font-weight: 600 !important;
    color: var(--gold2) !important;
    letter-spacing: 0.3px;
}

h2, h3 {
    font-family: 'Fraunces', serif !important;
    font-weight: 600 !important;
    color: var(--text) !important;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: var(--panel);
    border-right: 1px solid var(--line);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2 {
    color: var(--gold2) !important;
}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
    color: var(--text);
}

[data-testid="stFileUploaderDropzone"] {
    background: var(--panel2);
    border: 1px dashed var(--gold);
    border-radius: 14px;
}

/* ---------- Metric cards ---------- */
[data-testid="stMetric"],
div[data-testid="metric-container"] {
    background: linear-gradient(160deg, var(--panel2), var(--panel));
    border: 1px solid var(--line);
    border-top: 2px solid var(--gold);
    border-radius: 18px;
    padding: 18px 20px;
    box-shadow: 0 0 40px var(--glow);
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: var(--mute) !important;
    font-weight: 500;
}

[data-testid="stMetricValue"] {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 2.2rem;
    color: var(--text);
}

/* ---------- Buttons ---------- */
.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(135deg, var(--gold2), var(--gold));
    color: #07181a;
    border: 0;
    border-radius: 12px;
    font-weight: 700;
    padding: 0.55rem 1.2rem;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    color: #07181a;
    transform: translateY(-1px);
    box-shadow: 0 6px 22px rgba(226, 194, 124, 0.25);
}

.stButton > button:focus-visible,
.stDownloadButton > button:focus-visible {
    outline: 2px solid var(--emerald);
    outline-offset: 2px;
}

/* ---------- Tabs ---------- */
button[data-baseweb="tab"] {
    color: var(--mute);
    font-weight: 600;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--gold2);
}

div[data-baseweb="tab-highlight"] {
    background-color: var(--gold);
}

div[data-baseweb="tab-border"] {
    background-color: var(--line);
}

/* ---------- Alerts (success / info / warning) ---------- */
div[data-testid="stAlert"] {
    background: var(--panel2);
    border: 1px solid var(--line);
    border-left: 4px solid var(--gold);
    border-radius: 14px;
}

div[data-testid="stAlert"] > div {
    background: transparent;
}

div[data-testid="stAlert"] p,
div[data-testid="stAlert"] h3 {
    color: var(--text) !important;
}

/* ---------- Expander & tables ---------- */
[data-testid="stExpander"] details {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 14px;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 14px;
    overflow: hidden;
}

[data-testid="stImage"] img {
    border-radius: 16px;
    border: 1px solid var(--line);
}

hr {
    border-color: var(--line);
}

@media (prefers-reduced-motion: reduce) {
    * { transition: none !important; }
}
</style>
"""

st.markdown(THEME_CSS, unsafe_allow_html=True)


# ==========================
# Chart helpers
# ==========================

def show_figure(fig, key, height=None):
    """Show a Plotly figure full-width (works across Streamlit versions)."""

    if height:
        fig.update_layout(height=height)

    try:
        st.plotly_chart(fig, width="stretch", key=key)
    except Exception:
        st.plotly_chart(fig, use_container_width=True, key=key)


def show_image(path):
    try:
        st.image(path, width="stretch")
    except Exception:
        st.image(path, use_container_width=True)


def show_grid(figures, prefix, columns=3, height=300):
    """Lay charts out in a grid of equal columns."""

    for start in range(0, len(figures), columns):

        row = st.columns(columns)

        for offset, fig in enumerate(figures[start:start + columns]):
            with row[offset]:
                show_figure(
                    fig,
                    key=f"{prefix}_{start + offset}",
                    height=height
                )


# ==========================
# Dashboard helpers
# ==========================

INSIGHT_ICONS = {
    "quality": "✅",
    "outlier": "🚨",
    "distribution": "📊",
    "relationship": "🔗"
}


def render_kpis(kpis):

    columns = st.columns(len(kpis))

    for column, (label, value) in zip(columns, kpis.items()):
        column.metric(label, value)


def insight_card(item):

    icon = INSIGHT_ICONS.get(item.get("type"), "💡")

    with st.container(border=True):
        st.markdown(f"**{icon} {item.get('title', '')}**")
        st.write(item.get("finding", ""))
        st.caption("Recommendation: " + item.get("recommendation", ""))


def render_insights(insights, columns=3, limit=6):

    if not insights:
        st.warning("No AI insights generated.")
        return

    def grid(items):
        for start in range(0, len(items), columns):
            row = st.columns(columns)
            for offset, item in enumerate(items[start:start + columns]):
                with row[offset]:
                    insight_card(item)

    grid(insights[:limit])

    if len(insights) > limit:
        with st.expander(f"More insights ({len(insights) - limit})"):
            grid(insights[limit:])


def render_ai_assistant(results, settings):

    st.subheader("🤖 AI Assistant")

    if not settings["api_key"]:
        st.info(
            "Add a Gemini API key in the sidebar (AI Assistant) to get a "
            "plain-language summary and ask questions about your data. "
            "The rest of the dashboard works without it."
        )
        return

    st.caption(
        "Only a statistical summary of your data (no raw rows) "
        "is sent to Google Gemini."
    )

    if st.button("✨ Explain results with AI"):

        try:
            with st.spinner("Gemini is writing the summary..."):
                reply = explain_results(
                    results["context"],
                    settings["api_key"],
                    settings["model"],
                    settings["language"]
                )

            results["ai_summary"] = reply["text"]

            st.session_state["tokens_used"] = (
                st.session_state.get("tokens_used", 0) + reply["tokens"]
            )

        except LLMError as error:
            st.error(str(error))

    if results.get("ai_summary"):
        with st.container(border=True):
            st.markdown(results["ai_summary"])

    st.markdown("**Ask a question about your data**")

    if "chat" not in st.session_state:
        st.session_state["chat"] = []

    history = st.session_state["chat"]

    with st.container():

        for message in history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        question = st.chat_input("e.g. Which columns matter most?")

        if question:

            with st.chat_message("user"):
                st.markdown(question)

            try:
                with st.spinner("Thinking..."):
                    reply = answer_question(
                        question,
                        results["context"],
                        settings["api_key"],
                        history=history,
                        model=settings["model"],
                        language=settings["language"]
                    )

                history.append({"role": "user", "content": question})
                history.append({"role": "assistant", "content": reply["text"]})

                st.session_state["tokens_used"] = (
                    st.session_state.get("tokens_used", 0) + reply["tokens"]
                )

                with st.chat_message("assistant"):
                    st.markdown(reply["text"])

            except LLMError as error:
                st.error(str(error))

    tokens = st.session_state.get("tokens_used", 0)

    if tokens:
        st.caption(f"Tokens used this session: {tokens:,}")


def render_quick_dashboard(results):

    result = results["result"]

    render_kpis(results["kpis"])

    st.subheader("💡 Quick Findings")

    findings = result.get("quick_findings", [])

    if not findings:
        st.info("No findings from the quick analysis.")

    for finding in findings:
        st.info(finding.get("message", ""))


def render_full_dashboard(results):

    render_kpis(results["kpis"])

    # ---------- Insights ----------
    st.subheader("🧠 Key insights")

    render_insights(results["insights"])

    render_ai_assistant(results, ai_settings)

    # ---------- Key charts ----------
    st.subheader("📈 Key charts")

    visuals = results["visuals"]

    corr = visuals["correlations"]["figures"]

    relationship_images = [
        path for path in results["chart_paths"]
        if os.path.exists(path)
    ]

    if corr and relationship_images:

        left, right = st.columns([3, 2])

        with left:
            show_figure(corr[0], key="main_corr", height=420)

        with right:
            show_image(relationship_images[0])

    elif corr:
        show_figure(corr[0], key="main_corr", height=420)

    elif relationship_images:
        show_image(relationship_images[0])

    dist = visuals["distributions"]["figures"]
    cats = visuals["categories"]["figures"]
    quality = visuals["quality"]["figures"]
    outs = visuals["outliers"]["figures"]

    featured = dist[:2] + cats[:2] + quality[:1] + outs[:1]
    extra = dist[2:] + cats[2:] + outs[1:]

    if featured:
        show_grid(featured, "feat")

    elif not (corr or relationship_images):
        st.info("No charts could be generated for this dataset.")

    if extra or relationship_images[1:]:

        with st.expander(
            f"Show all charts ({len(extra) + len(relationship_images[1:])} more)"
        ):

            for path in relationship_images[1:]:
                show_image(path)

            show_grid(extra, "extra")

    # ---------- Report + pipeline ----------
    st.subheader("📄 Report")

    if results["report"]:

        st.download_button(
            label="📄 Download AI Report",
            data=results["report"],
            file_name="AI_Analysis_Report.pdf",
            mime="application/pdf"
        )

    else:
        st.warning("Report not found.")

    with st.expander("🤖 Agent pipeline"):

        for step in results["plan"]:
            st.success("✅ " + step)


# ==========================
# Header
# ==========================

st.title("🤖 AI Data Analyst Dashboard")

st.write("Intelligent dataset analysis powered by AI Agent.")


# ==========================
# Per-session workspace
# ==========================

WORKSPACE_ROOT = os.path.join(tempfile.gettempdir(), "ai_data_analyst")

WORKSPACE_MAX_AGE_HOURS = 6


def cleanup_old_workspaces():
    """Delete session folders that have not been used for a few hours."""

    cutoff = time.time() - WORKSPACE_MAX_AGE_HOURS * 3600

    for name in os.listdir(WORKSPACE_ROOT):

        path = os.path.join(WORKSPACE_ROOT, name)

        try:
            if os.path.isdir(path) and os.path.getmtime(path) < cutoff:
                shutil.rmtree(path, ignore_errors=True)
        except OSError:
            pass


def get_workspace():
    """Private temporary folder for this browser session."""

    os.makedirs(WORKSPACE_ROOT, exist_ok=True)

    workspace = st.session_state.get("workspace")

    if not workspace:
        cleanup_old_workspaces()
        workspace = tempfile.mkdtemp(prefix="session_", dir=WORKSPACE_ROOT)
        st.session_state["workspace"] = workspace

    os.makedirs(workspace, exist_ok=True)
    os.utime(workspace)  # mark as recently used

    return workspace


@st.cache_resource
def get_analysis_lock():
    """One lock shared by all sessions: matplotlib is not thread-safe,
    so analyses run one at a time."""
    return threading.Lock()


# ==========================
# Sidebar
# ==========================

st.sidebar.title("⚙️ Control Panel")

uploaded_file = st.sidebar.file_uploader(
    "📂 Upload CSV Dataset",
    type=["csv"]
)

st.sidebar.caption(
    "🔒 Files are kept in a private temporary folder and deleted "
    "automatically. Avoid uploading sensitive data to a public deployment."
)

mode = st.sidebar.radio(
    "Analysis Mode",
    [
        "⚡ Quick Analysis",
        "🧠 Full AI Analysis"
    ]
)

run_analysis = st.sidebar.button("🚀 Run Analysis")


def find_api_key(typed_key):
    """Key priority: sidebar > environment > Streamlit secrets."""

    if typed_key.strip():
        return typed_key.strip()

    for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        if os.environ.get(name):
            return os.environ[name]

    try:
        return st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        return ""


with st.sidebar.expander("🤖 AI Assistant (Gemini)"):

    typed_key = st.text_input(
        "Gemini API key",
        type="password",
        placeholder="Optional - kept in memory only"
    )

    ai_model = st.text_input("Model", value=DEFAULT_MODEL)

    ai_language = st.selectbox(
        "Answer language",
        ["Auto", "English", "العربية"]
    )

ai_settings = {
    "api_key": find_api_key(typed_key),
    "model": ai_model.strip() or DEFAULT_MODEL,
    "language": "Arabic" if ai_language == "العربية" else ai_language
}


# ==========================
# Dataset Loading
# ==========================

if not uploaded_file:

    st.info("Upload a CSV file from the sidebar to start.")

else:

    workspace = get_workspace()

    file_path = os.path.join(workspace, "uploaded_data.csv")

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    try:
        data = pd.read_csv(file_path)
    except Exception as error:
        st.error(f"Could not read this file as a CSV: {error}")
        st.stop()

    if data.empty:
        st.error("The uploaded CSV has no rows. Upload a file with data.")
        st.stop()

    # A new file means the old results no longer apply
    source_key = (uploaded_file.name, uploaded_file.size)

    if st.session_state.get("source_key") != source_key:
        st.session_state["source_key"] = source_key
        st.session_state.pop("results", None)
        st.session_state.pop("chat", None)
        st.session_state.pop("tokens_used", None)

    # ==========================
    # Run Analysis
    # ==========================

    if run_analysis:

        base_kpis = {
            "Rows": f"{data.shape[0]:,}",
            "Columns": data.shape[1],
            "Missing Values": int(data.isnull().sum().sum()),
            "Duplicate Rows": int(data.duplicated().sum())
        }

        # ----- QUICK ANALYSIS -----

        if mode == "⚡ Quick Analysis":

            with st.spinner("⚡ Running Quick Analysis..."):
                result = quick_analyze(data)

            st.session_state["results"] = {
                "mode": "quick",
                "result": result,
                "kpis": base_kpis
            }

        # ----- FULL AI ANALYSIS -----

        else:

            agent = DataAnalysisAgent()

            plan = agent.plan("Analyze my dataset")

            executor = AgentExecutor(
                plan,
                output_dir=os.path.join(workspace, "reports")
            )

            try:
                with st.spinner("🤖 AI Agent analyzing..."):
                    with get_analysis_lock():
                        executor.execute(file_path)
            except Exception as error:
                st.error(f"Analysis failed: {error}")
                st.stop()

            report_bytes = None

            report_path = executor.report_path

            if os.path.exists(report_path):
                with open(report_path, "rb") as report:
                    report_bytes = report.read()

            st.session_state["results"] = {
                "mode": "full",
                "plan": plan,
                "insights": executor.ai_insights,
                "chart_paths": list(executor.chart_paths),
                "visuals": build_visuals(
                    executor.data,
                    executor.profile,
                    executor.outliers
                ),
                "report": report_bytes,
                "context": build_context(
                    executor.data,
                    executor.profile,
                    executor.ai_insights,
                    executor.relationships,
                    executor.outliers
                ),
                "kpis": {
                    **base_kpis,
                    "Columns with Outliers": len(executor.outliers)
                }
            }

    # ==========================
    # Dashboard
    # ==========================

    results = st.session_state.get("results")

    if results is None:

        st.success("✅ Dataset Loaded Successfully")

        st.subheader("📊 Dataset Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Rows", data.shape[0])

        with col2:
            st.metric("Columns", data.shape[1])

        with col3:
            st.metric("Missing Values", int(data.isnull().sum().sum()))

        st.info(
            "Choose an analysis mode in the sidebar, "
            "then click Run Analysis."
        )

    elif results["mode"] == "quick":
        render_quick_dashboard(results)

    else:
        render_full_dashboard(results)

    with st.expander("👀 Preview Dataset"):
        st.dataframe(data.head())
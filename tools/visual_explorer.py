"""
Interactive Plotly charts for the dashboard.
 
build_visuals() returns one section per chart family. Each section is
{"figures": [...], "total": N} so the UI can tell when charts were capped.
"""
 
import pandas as pd
import plotly.express as px
 
EMERALD = "#4fd1a5"
GOLD = "#e2c27c"
ROSE = "#e88a8a"
TEXT = "#e4f3ef"
GRID = "#1f3d41"
 
MAX_CHARTS = 12
MAX_CORR_COLUMNS = 15
MAX_CATEGORY_VALUES = 10
MAX_CATEGORY_UNIQUE = 50
 
 
# ==========================
# Styling
# ==========================
 
def style_figure(fig, height=340):
    """Apply the Emerald + Gold look to a Plotly figure."""
 
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT),
        margin=dict(l=10, r=10, t=50, b=10),
        height=height,
        colorway=[EMERALD, GOLD, "#8fd3c4", "#f3dca6", ROSE],
    )
 
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID)
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID)
 
    return fig
 
 
# ==========================
# Column selection
# ==========================
 
def _is_numeric(series):
    return (
        pd.api.types.is_numeric_dtype(series)
        and not pd.api.types.is_bool_dtype(series)
    )
 
 
def get_numeric_columns(data, profile):
    """Numeric columns that are not IDs and not binary (0/1)."""
 
    excluded = set(profile.get("id_columns", [])) | set(
        profile.get("binary_columns", [])
    )
 
    return [
        column for column in data.columns
        if column not in excluded and _is_numeric(data[column])
    ]
 
 
def get_category_columns(data, profile):
    """Text, category and binary columns with a readable number of values."""
 
    ids = set(profile.get("id_columns", []))
    binary = set(profile.get("binary_columns", []))
 
    columns = []
 
    for column in data.columns:
 
        if column in ids:
            continue
 
        series = data[column]
 
        if pd.api.types.is_datetime64_any_dtype(series):
            continue
 
        is_text = not _is_numeric(series)
 
        if not (is_text or column in binary):
            continue
 
        if 1 <= series.nunique() <= MAX_CATEGORY_UNIQUE:
            columns.append(column)
 
    return columns
 
 
# ==========================
# Chart builders
# ==========================
 
def distribution_charts(data, profile):
 
    columns = get_numeric_columns(data, profile)
    figures = []
 
    for column in columns[:MAX_CHARTS]:
 
        try:
            fig = px.histogram(
                data,
                x=column,
                nbins=30,
                marginal="box",
                title=f"Distribution of {column}",
                color_discrete_sequence=[EMERALD],
            )
            figures.append(style_figure(fig, height=380))
        except Exception:
            continue
 
    return {"figures": figures, "total": len(columns)}
 
 
def category_charts(data, profile):
 
    columns = get_category_columns(data, profile)
    figures = []
 
    for column in columns[:MAX_CHARTS]:
 
        try:
            counts = (
                data[column]
                .astype(str)
                .value_counts()
                .head(MAX_CATEGORY_VALUES)
                .rename_axis("value")
                .reset_index(name="count")
            )
 
            fig = px.bar(
                counts,
                x="value",
                y="count",
                title=f"Most common values in {column}",
                color_discrete_sequence=[GOLD],
            )
            fig.update_xaxes(title_text="")
            figures.append(style_figure(fig))
        except Exception:
            continue
 
    return {"figures": figures, "total": len(columns)}
 
 
def correlation_chart(data, profile):
 
    ids = set(profile.get("id_columns", []))
 
    columns = [
        column for column in data.columns
        if column not in ids and _is_numeric(data[column])
    ]
 
    total = len(columns)
    columns = columns[:MAX_CORR_COLUMNS]
 
    if len(columns) < 2:
        return {"figures": [], "total": total}
 
    try:
        corr = data[columns].corr().round(2)
 
        fig = px.imshow(
            corr,
            text_auto=True,
            zmin=-1,
            zmax=1,
            aspect="auto",
            color_continuous_scale=[
                [0.0, ROSE],
                [0.5, "#0d2326"],
                [1.0, EMERALD],
            ],
            title="Correlation between numeric columns",
        )
 
        height = max(380, min(720, 140 + 45 * len(columns)))
 
        return {"figures": [style_figure(fig, height=height)], "total": total}
 
    except Exception:
        return {"figures": [], "total": total}
 
 
def quality_charts(profile):
    """Missing values per column, counted BEFORE cleaning."""
 
    missing = {
        column: int(count)
        for column, count in profile.get("missing_values", {}).items()
        if count and count > 0
    }
 
    if not missing:
        return {"figures": [], "total": 0}
 
    try:
        frame = (
            pd.DataFrame(
                {"column": list(missing), "missing": list(missing.values())}
            )
            .sort_values("missing")
        )
 
        fig = px.bar(
            frame,
            x="missing",
            y="column",
            orientation="h",
            title="Missing values per column (original data)",
            color_discrete_sequence=[ROSE],
        )
 
        height = max(300, 80 + 36 * len(frame))
 
        return {"figures": [style_figure(fig, height=height)], "total": 1}
 
    except Exception:
        return {"figures": [], "total": 0}
 
 
def outlier_charts(data, outliers):
 
    figures = []
 
    for item in outliers[:MAX_CHARTS]:
 
        column = item.get("column")
 
        if column not in data.columns:
            continue
 
        try:
            fig = px.box(
                data,
                y=column,
                points="outliers",
                title=(
                    f"Outliers in {column} "
                    f"({item.get('outlier_count', 0)} values)"
                ),
                color_discrete_sequence=[GOLD],
            )
            figures.append(style_figure(fig))
        except Exception:
            continue
 
    return {"figures": figures, "total": len(outliers)}
 
 
# ==========================
# Public entry point
# ==========================
 
def build_visuals(data, profile, outliers):
 
    profile = profile or {}
    outliers = outliers or []
 
    if data is None or data.empty:
 
        empty = {"figures": [], "total": 0}
 
        return {
            "distributions": empty,
            "categories": empty,
            "correlations": empty,
            "quality": empty,
            "outliers": empty,
        }
 
    return {
        "distributions": distribution_charts(data, profile),
        "categories": category_charts(data, profile),
        "correlations": correlation_chart(data, profile),
        "quality": quality_charts(profile),
        "outliers": outlier_charts(data, outliers),
    }
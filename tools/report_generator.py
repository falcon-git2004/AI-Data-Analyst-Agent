import os
from html import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image as ReportImage,
    PageBreak
)


def format_name(name):
    """
    Convert keys like total_rows into Total Rows.
    """

    return str(name).replace("_", " ").title()


def safe_text(value):
    """
    Make text safe for ReportLab Paragraph.
    """

    return escape(str(value))


def create_table(data, column_widths=None):

    table = Table(
        data,
        colWidths=column_widths,
        repeatRows=1
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1F4E78")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.HexColor("#F5F7FA")
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#D9E2F3")
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ]
        )
    )

    return table


def add_chart(content, chart_path, title, styles):

    if not chart_path:
        return

    if not os.path.exists(chart_path):
        return

    content.append(
        Paragraph(
            safe_text(title),
            styles["SectionHeading"]
        )
    )

    content.append(
        Spacer(1, 8)
    )

    image = ReportImage(chart_path)

    max_width = 6.3 * inch
    max_height = 4.3 * inch

    scale = min(
        max_width / image.imageWidth,
        max_height / image.imageHeight,
        1
    )

    image.drawWidth = image.imageWidth * scale
    image.drawHeight = image.imageHeight * scale

    content.append(image)

    content.append(
        Spacer(1, 18)
    )


def generate_report(
    insights,
    output_path,
    chart_info=None
):
    """
    Generate a professional PDF report containing:
    - Dataset overview
    - Numeric analysis
    - Categorical analysis
    - Important relationships
    - Business insights when available
    - Automatically generated charts
    """

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    base_styles = getSampleStyleSheet()

    styles = {
        "Title": ParagraphStyle(
            "ReportTitle",
            parent=base_styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=28,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#17365D"),
            spaceAfter=10
        ),

        "Subtitle": ParagraphStyle(
            "Subtitle",
            parent=base_styles["Normal"],
            fontSize=10,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#666666"),
            spaceAfter=24
        ),

        "SectionHeading": ParagraphStyle(
            "SectionHeading",
            parent=base_styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=18,
            textColor=colors.HexColor("#1F4E78"),
            spaceBefore=12,
            spaceAfter=10
        ),

        "Normal": ParagraphStyle(
            "ReportNormal",
            parent=base_styles["Normal"],
            fontSize=10,
            leading=15,
            textColor=colors.HexColor("#333333")
        ),

        "Finding": ParagraphStyle(
            "Finding",
            parent=base_styles["Normal"],
            fontSize=10,
            leading=15,
            leftIndent=10,
            spaceAfter=8,
            textColor=colors.HexColor("#333333")
        ),

        "Note": ParagraphStyle(
            "Note",
            parent=base_styles["Normal"],
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#777777"),
            spaceBefore=6,
            spaceAfter=12
        )
    }

    content = []


    # ==================================
    # Title
    # ==================================

    content.append(
        Paragraph(
            "AI Data Analysis Report",
            styles["Title"]
        )
    )

    content.append(
        Paragraph(
            "Generated automatically by AI Data Analyst Agent",
            styles["Subtitle"]
        )
    )


    # ==================================
    # Dataset Overview
    # ==================================

    overview = insights.get(
        "dataset_overview",
        {}
    )

    if overview:

        content.append(
            Paragraph(
                "1. Dataset Overview",
                styles["SectionHeading"]
            )
        )

        overview_data = [
            [
                "Metric",
                "Value"
            ]
        ]

        for key, value in overview.items():

            overview_data.append(
                [
                    format_name(key),
                    safe_text(value)
                ]
            )

        content.append(
            create_table(
                overview_data,
                [
                    3.2 * inch,
                    2.8 * inch
                ]
            )
        )

        content.append(
            Spacer(1, 18)
        )


    # ==================================
    # Numeric Analysis
    # ==================================

    numeric_analysis = insights.get(
        "numeric_analysis",
        {}
    )

    if numeric_analysis:

        content.append(
            Paragraph(
                "2. Numeric Analysis",
                styles["SectionHeading"]
            )
        )

        numeric_data = [
            [
                "Column",
                "Average",
                "Minimum",
                "Maximum"
            ]
        ]

        for column, values in numeric_analysis.items():

            numeric_data.append(
                [
                    safe_text(column),
                    safe_text(
                        values.get(
                            "average",
                            "-"
                        )
                    ),
                    safe_text(
                        values.get(
                            "minimum",
                            "-"
                        )
                    ),
                    safe_text(
                        values.get(
                            "maximum",
                            "-"
                        )
                    )
                ]
            )

        content.append(
            create_table(
                numeric_data,
                [
                    2.4 * inch,
                    1.2 * inch,
                    1.2 * inch,
                    1.2 * inch
                ]
            )
        )

        content.append(
            Spacer(1, 18)
        )


    # ==================================
    # Categorical Analysis
    # ==================================

    categorical_analysis = insights.get(
        "categorical_analysis",
        {}
    )

    if categorical_analysis:

        content.append(
            Paragraph(
                "3. Categorical Analysis",
                styles["SectionHeading"]
            )
        )

        categorical_data = [
            [
                "Column",
                "Unique Values",
                "Most Common",
                "Count"
            ]
        ]

        for column, values in categorical_analysis.items():

            categorical_data.append(
                [
                    safe_text(column),
                    safe_text(
                        values.get(
                            "unique_values",
                            "-"
                        )
                    ),
                    safe_text(
                        values.get(
                            "most_common",
                            "-"
                        )
                    ),
                    safe_text(
                        values.get(
                            "count",
                            "-"
                        )
                    )
                ]
            )

        content.append(
            create_table(
                categorical_data,
                [
                    2.0 * inch,
                    1.3 * inch,
                    1.7 * inch,
                    1.0 * inch
                ]
            )
        )

        content.append(
            Spacer(1, 18)
        )


    # ==================================
    # Important Relationships
    # ==================================

    relationships = insights.get(
        "important_relationships",
        []
    )

    if relationships:

        content.append(
            Paragraph(
                "4. Important Relationships",
                styles["SectionHeading"]
            )
        )

        for index, relationship in enumerate(
            relationships,
            start=1
        ):

            features = relationship.get(
                "features",
                ()
            )

            if len(features) >= 2:

                feature_1 = features[0]
                feature_2 = features[1]

            else:

                feature_1 = "Unknown"
                feature_2 = "Unknown"

            relationship_type = relationship.get(
                "relationship_type",
                "unknown"
            )

            strength = relationship.get(
                "strength",
                "-"
            )

            chart = relationship.get(
                "recommended_chart",
                "-"
            )

            if relationship_type == "numeric_numeric":

                description = (
                    f"{feature_1} and {feature_2} "
                    f"show a numeric relationship."
                )

            elif relationship_type == "numeric_target":

                description = (
                    f"{feature_1} shows a measurable "
                    f"relationship with {feature_2}."
                )

            elif relationship_type == "categorical_target":

                description = (
                    f"An association was detected between "
                    f"{feature_1} and {feature_2}."
                )

            elif relationship_type == "categorical_categorical":

                description = (
                    f"An association was detected between "
                    f"{feature_1} and {feature_2}."
                )

            else:

                description = (
                    f"A relationship was detected between "
                    f"{feature_1} and {feature_2}."
                )

            finding_text = (
                f"<b>{index}. "
                f"{safe_text(feature_1)} vs "
                f"{safe_text(feature_2)}</b><br/>"
                f"{safe_text(description)}<br/>"
                f"Relationship score: "
                f"<b>{safe_text(strength)}</b><br/>"
                f"Recommended visualization: "
                f"{safe_text(chart)}"
            )

            content.append(
                Paragraph(
                    finding_text,
                    styles["Finding"]
                )
            )

        content.append(
            Paragraph(
                "Note: relationship scores are generated by "
                "different statistical methods depending on the "
                "data types. They should not be interpreted as "
                "percentages.",
                styles["Note"]
            )
        )


    # ==================================
    # Business Insights
    # ==================================

    business_insights = insights.get(
        "business_insights",
        {}
    )

    if business_insights:

        content.append(
            Paragraph(
                "5. Business Insights",
                styles["SectionHeading"]
            )
        )

        business_data = [
            [
                "Metric",
                "Result"
            ]
        ]

        for key, value in business_insights.items():

            business_data.append(
                [
                    format_name(key),
                    safe_text(value)
                ]
            )

        content.append(
            create_table(
                business_data,
                [
                    3.2 * inch,
                    2.8 * inch
                ]
            )
        )

        content.append(
            Spacer(1, 20)
        )


    # ==================================
    # Visualizations
    # ==================================

    valid_charts = []

    if chart_info:

        for chart in chart_info:

            if not chart:
                continue

            chart_path = chart.get(
                "output_path"
            )

            if (
                chart_path
                and os.path.exists(chart_path)
            ):
                valid_charts.append(chart)


    if valid_charts:

        content.append(
            PageBreak()
        )

        content.append(
            Paragraph(
                "6. Visualizations",
                styles["SectionHeading"]
            )
        )

        for index, chart in enumerate(
            valid_charts,
            start=1
        ):

            chart_type = chart.get(
                "chart_type",
                "Chart"
            )

            chart_path = chart.get(
                "output_path"
            )

            add_chart(
                content,
                chart_path,
                (
                    f"Visualization {index}: "
                    f"{format_name(chart_type)}"
                ),
                styles
            )


    # ==================================
    # Final Note
    # ==================================

    content.append(
        Spacer(1, 10)
    )

    content.append(
        Paragraph(
            "This report was generated automatically from "
            "the uploaded dataset using the AI Data Analyst Agent.",
            styles["Note"]
        )
    )


    doc.build(content)

    print(
        f"📄 Professional report generated: {output_path}"
    )
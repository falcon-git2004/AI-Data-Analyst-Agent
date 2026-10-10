import streamlit as st
import os
import pandas as pd


from agent.planner import DataAnalysisAgent
from agent.executor import AgentExecutor

from tools.quick_analyzer import quick_analyze


st.set_page_config(
    page_title="AI Data Analyst Agent",
    page_icon="🤖",
    layout="wide"
)


st.title(
    "🤖 AI Data Analyst Agent"
)


st.write(
    "Upload your dataset and choose the analysis mode."
)


uploaded_file = st.file_uploader(
    "📂 Upload CSV file",
    type=["csv"]
)



if uploaded_file:


    file_path = "data/uploaded_data.csv"


    with open(
        file_path,
        "wb"
    ) as file:

        file.write(
            uploaded_file.getbuffer()
        )


    st.success(
        "✅ File uploaded successfully!"
    )


    data = pd.read_csv(
        file_path
    )


    # ==========================
    # Dataset Preview
    # ==========================

    st.subheader(
        "📊 Dataset Preview"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Rows",
            data.shape[0]
        )


    with col2:

        st.metric(
            "Columns",
            data.shape[1]
        )


    st.write(
        "Column Names:"
    )


    st.write(
        list(data.columns)
    )


    st.dataframe(
        data.head()
    )


    # ==========================
    # Analysis Mode
    # ==========================


    st.subheader(
        "Choose Analysis Mode"
    )


    mode = st.radio(
        "",
        [
            "⚡ Quick Analysis",
            "🧠 Full AI Analysis"
        ]
    )



    # ==========================
    # QUICK MODE
    # ==========================


    if mode == "⚡ Quick Analysis":


        if st.button(
            "⚡ Run Quick Analysis"
        ):


            with st.spinner(
                "Analyzing dataset quickly..."
            ):


                result = quick_analyze(
                    data
                )


            st.success(
                "Quick Analysis Completed!"
            )


            st.subheader(
                "📌 Overview"
            )


            st.write(
                result["overview"]
            )


            st.subheader(
                "✅ Data Quality"
            )


            st.write(
                result["data_quality"]
            )


            st.subheader(
                "💡 Quick Findings"
            )


            for finding in result[
                "quick_findings"
            ]:

                st.info(
                    finding["message"]
                )



    # ==========================
    # FULL MODE
    # ==========================


    else:


        if st.button(
            "🚀 Run Full AI Analysis"
        ):


            agent = DataAnalysisAgent()


            plan = agent.plan(
                "Analyze my dataset"
            )


            st.subheader(
                "🤖 Agent Plan"
            )


            for step in plan:

                st.write(
                    f"✅ {step}"
                )



            executor = AgentExecutor(
                plan
            )


            with st.spinner(
                "AI Agent analyzing dataset..."
            ):

                executor.execute(
                    file_path
                )


            st.success(
                "🎉 Full Analysis Completed!"
            )



            # ==========================
            # Charts
            # ==========================


            chart_files = []


            for file in os.listdir(
                "reports"
            ):

                if (
                    file.endswith(".png")
                ):

                    chart_files.append(
                        "reports/" + file
                    )


            if chart_files:


                st.subheader(
                    "📈 AI Generated Visualizations"
                )


                for chart in chart_files:

                    st.image(
                        chart
                    )



            # ==========================
            # Report Download
            # ==========================


            report_path = (
                "reports/AI_Analysis_Report.pdf"
            )


            if os.path.exists(
                report_path
            ):


                with open(
                    report_path,
                    "rb"
                ) as report:


                    st.download_button(

                        label=
                        "📄 Download AI Report",

                        data=report,

                        file_name=
                        "AI_Analysis_Report.pdf",

                        mime=
                        "application/pdf"
                    )
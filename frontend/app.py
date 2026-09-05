import streamlit as st
import requests
import pandas as pd
import os

st.set_page_config(page_title="Blood Report Simplifier", page_icon="🩸", layout="wide")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def render_report(report_data):
    st.subheader(f"Report: {report_data.get('filename', 'Unknown')}")
    if 'upload_date' in report_data:
        # Format the date slightly better
        date_str = report_data.get('upload_date', '').split('T')[0]
        st.caption(f"Uploaded: {date_str}")
    
    t1, t2, t3 = st.tabs(["English", "हिंदी (Hindi)", "ਪੰਜਾਬੀ (Punjabi)"])
    with t1:
        st.info(report_data.get("summary_english", report_data.get("summary", "No summary provided.")))
    with t2:
        st.info(report_data.get("summary_hindi", "Hindi summary not available for older reports."))
    with t3:
        st.info(report_data.get("summary_punjabi", "Punjabi summary not available for older reports."))
    
    if "markers" in report_data and report_data["markers"]:
        df = pd.DataFrame(report_data["markers"])
        
        # Style the dataframe (only works for string exact matches)
        def color_status(val):
            color = '#ff4b4b' if str(val).lower() != 'normal' else '#21c354'
            return f'color: {color}; font-weight: bold;'
            
        if 'status' in df.columns:
            st.dataframe(df.style.map(color_status, subset=['status']), use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)

st.title("🩸 AI Blood Report Simplifier")
st.markdown("Upload your blood report (Image or PDF) and let AI simplify the medical jargon for you.")
st.warning("⚠️ **Disclaimer:** This tool is for educational purposes only and should not replace professional medical advice.")

tab1, tab2 = st.tabs(["Upload New Report", "View History"])

with tab1:
    st.header("Upload Report")
    uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png", "pdf"])
    
    if st.button("Analyze Report", type="primary"):
        if uploaded_file is not None:
            with st.spinner("Analyzing your report... (This may take a few seconds)"):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    response = requests.post(f"{BACKEND_URL}/analyze", files=files)
                    
                    if response.status_code == 200:
                        st.success("Analysis Complete!")
                        render_report(response.json())
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown Error')}")
                except Exception as e:
                    st.error(f"Failed to connect to backend: {str(e)}")
        else:
            st.warning("Please upload a file first.")

with tab2:
    st.header("Report History")
    if st.button("Refresh History"):
        try:
            response = requests.get(f"{BACKEND_URL}/history")
            if response.status_code == 200:
                history = response.json().get("reports", [])
                if not history:
                    st.info("No reports found in history.")
                else:
                    for i, report in enumerate(history):
                        with st.expander(f"Report: {report.get('filename')} - {report.get('upload_date', '')[:10]}"):
                            render_report(report)
            else:
                st.error("Failed to fetch history.")
        except Exception as e:
            st.error(f"Failed to connect to backend: {str(e)}")

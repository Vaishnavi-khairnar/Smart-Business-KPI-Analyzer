import streamlit as st
import pandas as pd
from utils import api, session

def show():
    """Display data upload page."""
    st.title("Upload Business Data")

    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file",
        type=["csv", "xlsx"],
        help="Upload business data for KPI analysis"
    )

    if uploaded_file is not None:
        try:
            # Read file
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            else:
                st.error("Unsupported file format.")
                return

            # File info
            st.write(f"**File Name:** {uploaded_file.name}")
            st.write(f"**File Size:** {uploaded_file.size / 1024:.2f} KB")
            st.write(f"**Rows:** {len(df)}")

            # Preview
            if st.checkbox("Preview data"):
                st.dataframe(df.head(10))

            # Upload
            if st.button("Upload to Database", type="primary"):
                if not session.is_logged_in():
                    st.error("Please log in to upload data.")
                    return

                with st.spinner("Uploading data..."):
                    response = api.post(
                        "/data/upload/sales",
                        files={"file": uploaded_file}
                    )

                    if response.get("success"):
                        st.success(f"Uploaded {len(df)} records successfully!")
                        st.rerun()
                    else:
                        st.error(response.get("message", "Upload failed"))

        except Exception as e:
            st.error(f"Error processing file: {e}")

    else:
        st.info("Please upload a file to begin.")

import streamlit as st
import pandas as pd
from utils.api import APIClient
from utils.session import is_authenticated

def show():
    """Display data upload page."""
    if not is_authenticated():
        st.error("🔒 Please login to access the upload page.")
        st.stop()

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
                client = APIClient()
                with st.spinner("Uploading data..."):
                    # ✅ CRITICAL: Reset file pointer after pd.read_csv()
                    uploaded_file.seek(0)
                    
                    # The backend expects a file in the 'file' field
                    # Explicitly provide filename and type for better compatibility
                    files = {
                        "file": (uploaded_file.name, uploaded_file, uploaded_file.type)
                    }
                    
                    response = client.post(
                        "/data/upload/sales",
                        files=files,
                        raise_for_status=False
                    )

                    if response.status_code in (200, 201):
                        res_data = response.json()
                        st.success(res_data.get("message", "Uploaded successfully!"))
                        if res_data.get("errors"):
                            with st.expander("Show processing warnings"):
                                for err in res_data["errors"]:
                                    st.warning(err)
                        st.balloons()
                    else:
                        try:
                            err_detail = response.json().get("detail", "Upload failed")
                        except:
                            err_detail = response.text
                        st.error(f"Upload failed: {err_detail}")

        except Exception as e:
            st.error(f"Error processing file: {e}")

    else:
        st.info("Please upload a file to begin.")

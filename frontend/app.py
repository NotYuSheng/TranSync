import streamlit as st
import requests
import os

st.set_page_config(page_title="XLSX Translate", layout="centered")
st.title("📄 XLSX Translate")

uploaded_files = st.file_uploader("Upload Excel files", type=["xlsx"], accept_multiple_files=True)
st.caption("Upload one or more `.xlsx` files for translation. Only cells with Arabic will be translated.")

if uploaded_files:
    if st.button("Translate Files"):
        with st.spinner("Sending files to backend for translation..."):
            files = [("files", (f.name, f.getvalue())) for f in uploaded_files]
            try:
                response = requests.post("http://xlsx-translate-backend:8000/translate-xlsx/", files=files)
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Failed to contact backend: {e}")
                st.stop()

            if response.status_code == 200:
                results = response.json()["results"]

                if not results:
                    st.warning("⚠️ No files were translated.")
                else:
                    st.success(f"✅ {len(results)} file(s) translated!")

                    for result in results:
                        translated_path = f"./data/output/{result['translated_filename']}"

                        if os.path.exists(translated_path):
                            with open(translated_path, "rb") as f:
                                st.download_button(
                                    label=f"⬇ Download: {result['translated_filename']}",
                                    data=f.read(),
                                    file_name=result['translated_filename'],
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                        else:
                            st.error(f"❌ Could not find translated file: {result['translated_filename']}")
            else:
                st.error(f"❌ Backend returned error: {response.status_code}")

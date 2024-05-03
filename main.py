import streamlit as st
import subprocess
import pandas as pd
import os

st.title('Upload CSV and Execute Script')

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])


session_state = st.session_state

if 'uploaded_file' not in session_state:
    session_state.uploaded_file = None

if uploaded_file is not None:
    session_state.uploaded_file = uploaded_file
    st.write(pd.read_csv(uploaded_file))
ApiKey = st.text_input("Enter the Open-ai API Key",key="ApiKey")
outputfileName = st.text_input("Enter the outputfileName",key="ouputfilename")
selected_script = st.selectbox("Select a script to execute", ["mass_scrape.py", "script2.py"])


if st.button("Execute Script") and session_state.uploaded_file is not None and ApiKey is not None and outputfileName is not None: 

    file_path = f"{session_state.uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    # st.write(pd.read_csv(file_path))
    subprocess.run(["python3", selected_script,file_path,outputfileName,ApiKey])
    st.write(pd.read_csv(f"output/{file_path}/{outputfileName}"))

    os.remove(file_path)

import pandas as pd
import streamlit as st

def upload_file():
    uploaded_file = st.file_uploader("Choose a file showing the stock date and its high value for analysis")
    return uploaded_file

def read_csv(file):
    df = pd.read_csv(file)
    return df

def run():
    uploaded_file = upload_file()
    if uploaded_file:
        df = read_csv(uploaded_file)
        st.line_chart(df, x="Date", y="High", width="stretch")

if __name__ == "__main__":
    run()
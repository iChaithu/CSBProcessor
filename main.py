# main.py
import streamlit as st
import pandas as pd
from backend import *
import io

st.set_page_config(page_title="CSB PROCESSOR",page_icon=":sauropod:",layout="wide")
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.css-1lsmgbg e1fqkh3o2 {display: none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("PDF Data Extractor")

col, col1 = st.columns(2)
with col:
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    
with col1:
    st.write("")
    password = st.text_input("Enter PDF Password", type="password")

if uploaded_file and password:
    try:
        pdf_bytes = io.BytesIO(uploaded_file.getvalue())
        df, summary = extract_data_from_pdf(pdf_bytes, password)
        st.subheader("Extracted Data")
        coll, coll1 = st.columns(2)
        with coll:
            st.subheader("Summary")
            for key, value in summary.items():
                st.write(f"{key}: {value}")
        with coll1:st.dataframe(df)

    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        print("hello")  
else:
    st.info("Please upload a PDF and enter the password.")
 
 # Adding the footer
footer = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: black;
        text-align: center;
        padding: 10px;
        font-size: 12px;
    }
    </style>
    <div class="footer">
        <p>Made by Heisenberg</p>
    </div>
    """

st.markdown(footer, unsafe_allow_html=True)
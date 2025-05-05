def upload_file():
    import streamlit as st
    import pandas as pd

    st.title("Upload Financing Plan")

    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

    if uploaded_file is not None:
        # Read the Excel file
        df = pd.read_excel(uploaded_file)

        # Display the contents of the file
        st.write("File contents:")
        st.dataframe(df)

        # Here you can add additional processing of the dataframe as needed
        return df

    return None
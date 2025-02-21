import streamlit as st
import pandas as pd
import os
from io import BytesIO
 

st.set_page_config(page_title="Data Zen" , layout="wide")
st.title ("Data Zen")
st.write("Transform your files between CSV and Excel formats with built-in cleaning and visualization")


uploaded_files = st.file_uploader("Upload Your files (CSV or Excel):", type=["csv","xlsx"] , accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file format. Please upload either {file_ext}.")
            continue
         


        st.write(f"**File Name: {file.name}")
        st.write(f"**File Size: {file.size/1024}")


        st.write("Preview the head of DataFrame")
        st.dataframe(df.head())

        #Data Filtering Option
        st.subheader("Data Filtering Options")
        filter_column = st.selectbox(f"Select Column to filter {file.name}",df.columns , key=file.name+"filter")
        unique_value = df[filter_column].unique()
        selected_value = st.multiselect(f"Filter Values for {filter_column}" , unique_value , default=unique_value[:2])
        df_filtered = df[df[filter_column].isin(selected_value)]
        st.write("Filtered Data Preview:")
        st.dataframe(df_filtered.head())




        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            

            
                if st.button(f"Remove Data from {file.name}"):
                    df_filtered.drop_duplicates(inplace=True)
                    st.write("Duplicate Removed")

            
                if st.button(f"Fill Missing values for {file.name}"):
                    numeric_cols = df_filtered.select_dtypes(include=['number']).columns
                    df_filtered[numeric_cols] = df_filtered[numeric_cols].fillna(df_filtered[numeric_cols].mean())
                    st.write("Missing Values have been filled")

        st.subheader("Select column to convert")
        columns = st.multiselect(f"Choose Columns for {file.name}",df.columns,default=df.columns)
        df_plot = df[columns]
        df_plot.reset_index(drop=True , inplace=True)


        # visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show Summary Statistics for {file.name}"):
            
            numeric_columns = df_filtered.select_dtypes(include=['number']).columns.tolist()
            if numeric_columns:
                graph_column = st.multiselect(f"Select column for visualization ({file.name})",numeric_columns,key=file.name+"graph")
                if  st.checkbox(f"Show Bar for {file.name}"):
                    st.bar_chart(df_filtered.set_index(df_filtered.columns[0])[graph_column])
                if st.checkbox(f"Show Line fot {file.name}"):
                    st.line_chart(df_filtered.set_index(df_filtered.columns[0])[graph_column])
                if st.checkbox(f"Show Area fot {file.name}"):
                    st.area_chart(df_filtered.set_index(df_filtered.columns[0])[graph_column])
        


        st.subheader("conversion Type")
        conversion_type = st.radio(f"Conversion {file.name} to:" , ["CSV" , "Excel"] , key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext , ".csv")
                mime_type = "type/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext , ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label = f"Download {file_name} as {conversion_type}",
                data = buffer,
                file_name = file_name,
                mime = mime_type
            
            )

st.success("All Files Processed")
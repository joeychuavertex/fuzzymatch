import pandas as pd
from fuzzywuzzy import process
import streamlit as st
from stqdm import stqdm

uploaded_file1 = st.file_uploader("Choose the first CSV file (to match to)")
uploaded_file2 = st.file_uploader("Choose the second CSV file (choices for matching)")

my_bar = st.progress(0)

# Check if the files were uploaded
if uploaded_file1 is not None and uploaded_file2 is not None:

    # Load the contents of the files into dataframes
    df1 = pd.read_csv(uploaded_file1)
    st.write("First CSV file")
    st.write(df1)
    st.write("Second CSV file")
    df2 = pd.read_csv(uploaded_file2)
    st.write(df2)

    # Create dropdown menus for the user to select the columns to use for matching
    column1 = st.selectbox("Select the column in the first dataframe", df1.columns)
    column2 = st.selectbox("Select the column in the second dataframe", df2.columns)
    threshold = st.slider("Select the matching threshold (0-100). Recommended: 90", 0, 100)


    if st.button("Start fuzzy matching"):
        st.text("Note: Fuzzy matching can take a long time.")
        st.button("Stop")
        # Data cleaning for dataframes
        df1.dropna(subset=[column1])
        df1[column1] = df1[column1]
        df1[column1].astype(str)

        df2.dropna(subset=[column2])
        df2[column2] = df2[column2]
        df2[column2].astype(str)

        # Find the closest match for each row in df1 in df2
        best_matches = [process.extractOne(c, df2[column2], score_cutoff=threshold) for c in stqdm(df1[column1])]
        if st.button("Stop"):
            st.stop()
        else:
            best_matches_list = ['NA' if x is None else x[0] for x in best_matches]
            best_score_list = ['NA' if x is None else x[1] for x in best_matches]

            # Merge the dataframes based on the closest match
            df_output = df1.copy()
            df_output["best_match"] = best_matches_list
            df_output["best_score"] = best_score_list

            st.download_button("Download merged dataframe", df_output.to_csv(index=False), "merged_dataframe.csv")

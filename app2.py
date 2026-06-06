import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pickle
from helper import HelperClass

# load the models
model = pickle.load(open('model_dtr.pkl', 'rb'))

# ===========================================================
# python main.........................................
if __name__ == "__main__":
    st.set_page_config(page_title="World GDP Dashboard", layout="wide")
    st.markdown("""
        <style>
            .main { background-color: #f0f2f6; }
            h1 { color: #336699; }
            .stButton>button { background-color: #4CAF50; color: white; }
        </style>
    """, unsafe_allow_html=True)

    st.title("🌍 Countries GDP Analysis & Prediction Dashboard")

    # Predictive System
    st.header("📈 Predict GDP Per Capita")
    with st.container():
        features = st.text_input("Enter features (comma-separated):")
        if st.button("Predict GDP"):
            features = np.array([features.split(',')])
            gdp_pred = model.predict(features).reshape(1, -1)[0][0]
            st.metric("Predicted GDP Per Capita", f"${gdp_pred:,.2f}")

            if 'df' in locals():
                df_pred = df.copy()
                df_pred['GDP Difference'] = abs(df_pred['GDP ($ per capita) dollars'] - gdp_pred)
                nearest_countries = df_pred.nsmallest(5, 'GDP Difference')[['Country', 'GDP ($ per capita) dollars']]
                st.subheader("🧭 5 Countries Closest to Predicted GDP")
                st.dataframe(nearest_countries.set_index('Country').style.format({"GDP ($ per capita) dollars": "${:,.2f}"}))
            else:
                st.info("Upload a CSV first to enable nearest country comparison.")

    # Sidebar
    st.sidebar.title("📂 Upload Dataset")
    file = st.sidebar.file_uploader('Upload CSV File', type=['csv'])

    if file is not None:
        df = pd.read_csv(file)
        region, countries, countries_counts = HelperClass.basic_counts(df)
        st.sidebar.success(f"✅ Regions: {region}")
        st.sidebar.success(f"✅ Countries: {countries}")
        st.sidebar.write("📊 Countries Per Region:")
        st.sidebar.write(countries_counts)

        if st.sidebar.button('Show Analysis Dashboard'):
            df = HelperClass.ConvertToFloatAndFillMissValues(df)
            
            st.header("🔎 Data Analysis Dashboard")
            st.subheader("📋 Dataset Preview")
            st.dataframe(df.head())

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📊 Average GDP, Literacy, Agriculture by Region")
                st.dataframe(HelperClass.AverageRegionsGDPLiteracyAgriculture(df))
            with col2:
                st.subheader("📊 Aggregated Region Data")
                st.dataframe(HelperClass.DataAgg(df))

            st.subheader("🏆 Top 15 Countries by GDP Per Capita")
            HelperClass.plot_gdp_bar_chart(df)

            st.subheader("🌏 Top 5 Asian Countries by GDP & Literacy")
            HelperClass.AsiaFiveRegionGDP(df)

            st.subheader("📍 Top 5 Countries by GDP in Each Region")
            HelperClass.EachReginGDP(df)

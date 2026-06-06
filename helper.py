import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class HelperClass:

    @staticmethod
    def basic_counts(df):
        region = df['Region'].nunique()
        countries = df['Country'].nunique()
        countries_counts = df['Region'].value_counts()
        return region, countries, countries_counts

    @staticmethod
    def ConvertToFloatAndFillMissValues(df):
        for col in df.columns:
            if col in ['Country', 'Region']:
                continue

            if df[col].dtype == object:
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace(',', '.', regex=False)
                )
                df[col] = pd.to_numeric(df[col], errors='coerce')

        return df

    @staticmethod
    def AverageRegionsGDPLiteracyAgriculture(df):
        cols = [
            'GDP ($ per capita)',
            'Literacy (%)',
            'Agriculture'
        ]

        for col in cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        result = df.groupby('Region')[cols].mean()

        return result

    @staticmethod
    def join_countries(data):
        return ', '.join(data.astype(str))

    @staticmethod
    def DataAgg(df):
        numeric_cols = [
            'Pop. Density (per sq. mi.)',
            'Coastline (coast/area ratio)',
            'Net migration',
            'Infant mortality (per 1000 births)',
            'GDP ($ per capita)',
            'Literacy (%)',
            'Phones (per 1000)',
            'Arable (%)',
            'Crops (%)',
            'Other (%)',
            'Birthrate',
            'Deathrate',
            'Agriculture',
            'Industry',
            'Service'
        ]

        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        region_data = df.groupby('Region').agg({
            'Country': HelperClass.join_countries,
            'Population': 'sum',
            'Area (sq. mi.)': 'sum',
            'Pop. Density (per sq. mi.)': 'mean',
            'Coastline (coast/area ratio)': 'mean',
            'Net migration': 'mean',
            'Infant mortality (per 1000 births)': 'mean',
            'GDP ($ per capita)': 'mean',
            'Literacy (%)': 'mean',
            'Phones (per 1000)': 'mean',
            'Arable (%)': 'mean',
            'Crops (%)': 'mean',
            'Other (%)': 'mean',
            'Birthrate': 'mean',
            'Deathrate': 'mean',
            'Agriculture': 'mean',
            'Industry': 'mean',
            'Service': 'mean'
        })

        region_data.reset_index(inplace=True)

        return region_data

    @staticmethod
    def plot_gdp_bar_chart(df):
        fig, ax = plt.subplots(figsize=(16, 6))

        top_gdp_countries = (
            df.sort_values(
                'GDP ($ per capita)',
                ascending=False
            )
            .head(15)
        )

        mean = pd.DataFrame({
            'Country': ['World mean'],
            'GDP ($ per capita)': [
                df['GDP ($ per capita)'].mean()
            ]
        })

        gdps = pd.concat(
            [
                top_gdp_countries[['Country', 'GDP ($ per capita)']],
                mean
            ],
            ignore_index=True
        )

        sns.barplot(
            x='Country',
            y='GDP ($ per capita)',
            data=gdps
        )

        ax.set_xlabel(ax.get_xlabel(), labelpad=15)
        ax.set_ylabel(ax.get_ylabel(), labelpad=30)

        plt.xticks(rotation=45)

        st.pyplot(fig)

    @staticmethod
    def AsiaFiveRegionGDP(df):
        asia_df = df[df['Region'].str.strip().str.upper() == 'ASIA (EX. NEAR EAST)'].copy()

        if asia_df.empty:
            st.warning(f"No data found for 'ASIA (EX. NEAR EAST)'. Available regions: {df['Region'].str.strip().unique().tolist()}")
            return

        # Convert to numeric and drop rows with NaN in either column
        asia_df['Literacy (%)'] = pd.to_numeric(asia_df['Literacy (%)'], errors='coerce')
        asia_df['GDP ($ per capita)'] = pd.to_numeric(asia_df['GDP ($ per capita)'], errors='coerce')
        asia_df = asia_df.dropna(subset=['Literacy (%)', 'GDP ($ per capita)'])

        top_five_asia_countries_literacy = asia_df.nlargest(5, 'Literacy (%)')

        top_five_asia_countries_literacy = (
            top_five_asia_countries_literacy[
                ['Country', 'Literacy (%)', 'GDP ($ per capita)']
            ]
        )

        labels = top_five_asia_countries_literacy['Country']
        literacy_rates = top_five_asia_countries_literacy['Literacy (%)']
        gdp_values = top_five_asia_countries_literacy['GDP ($ per capita)']

        fig, axes = plt.subplots(1, 2, figsize=(12, 6))

        axes[0].pie(
            literacy_rates,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90
        )
        axes[0].set_title('Literacy Rates')

        axes[1].pie(
            gdp_values,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90
        )
        axes[1].set_title('GDP Per Capita')

        plt.tight_layout()

        st.pyplot(fig)

    @staticmethod
    def EachReginGDP(df):
        region_gdp = (
            df.groupby('Region')['GDP ($ per capita)']
            .mean()
        )

        regions = region_gdp.index

        num_subplots = len(regions)
        num_cols = 5
        num_rows = (num_subplots - 1) // num_cols + 1

        fig, axes = plt.subplots(
            num_rows,
            num_cols,
            figsize=(20, 4 * num_rows),
            constrained_layout=True
        )

        axes = axes.ravel()

        colors = plt.cm.tab20c(np.arange(20))

        for i in range(num_subplots):
            ax = axes[i]

            countries = df[df['Region'] == regions[i]]

            top_countries = countries.nlargest(
                5,
                'GDP ($ per capita)'
            )

            country_names = top_countries['Country']
            country_gdp = top_countries['GDP ($ per capita)']

            region_colors = colors[:len(country_names)]

            ax.pie(
                country_gdp,
                labels=country_names,
                autopct='%1.1f%%',
                startangle=90,
                colors=region_colors,
                shadow=True
            )

            ax.set_aspect('equal')
            ax.set_title(f'{regions[i]} Region')

        for i in range(num_subplots, num_cols * num_rows):
            fig.delaxes(axes[i])

        plt.suptitle(
            "Top 5 GDP Distribution by Region",
            fontsize=16
        )

        st.pyplot(fig)

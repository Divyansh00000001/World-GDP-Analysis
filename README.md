# 🌍 World GDP Analysis & Prediction System

## Overview

An interactive Streamlit-based dashboard for analyzing global economic indicators and predicting GDP per capita using Machine Learning.

The application enables users to upload country-level datasets, explore regional economic trends, visualize GDP distributions, and generate GDP predictions based on socio-economic indicators.

## Features

* 📈 GDP Per Capita Prediction using Decision Tree Regression
* 🌍 Regional GDP Analysis
* 📊 Top 15 Countries by GDP Visualization
* 📚 Literacy, Agriculture, and GDP Comparison by Region
* 🌏 Top 5 Asian Countries GDP & Literacy Analysis
* 📍 Top 5 GDP-Contributing Countries in Each Region
* 📂 Interactive CSV Upload Support

## Tech Stack

* Python
* Streamlit
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-Learn

## Machine Learning Model

Model: Decision Tree Regressor

Input Features:

* Literacy Rate (%)
* Agriculture Index
* Birth Rate

Output:

* GDP Per Capita Prediction

## Dataset

Countries of the World Dataset

Key Attributes:

* Country
* Region
* Population
* GDP Per Capita
* Literacy Rate
* Agriculture
* Industry
* Service
* Birth Rate
* Death Rate

## How to Run

```bash
pip install -r requirements.txt
streamlit run app2.py
```

## Key Insights

* Compare GDP performance across global regions.
* Identify top-performing economies by GDP per capita.
* Analyze relationships between literacy, agriculture, and GDP.
* Predict GDP per capita using machine learning techniques.

## Repository Structure

World-GDP-Analysis/
│
├── app.py
├── app2.py
├── helper.py
├── train_model.py
├── model_dtr.pkl
├── countries of the world.csv
├── Screenshots/
├── requirements.txt
└── README.md

## Author

Divyansh Chauhan

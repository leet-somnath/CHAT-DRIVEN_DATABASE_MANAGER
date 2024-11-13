import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# Load DataFrame and column names
with open('data.pkl', 'rb') as f:
    df, col_names = pickle.load(f)

st.title("Data Visualization")

# Visualization options
if not df.empty:
    chart_type = st.selectbox("Select Chart Type:", ["Bar Chart", "Pie Chart", "Line Chart", "Scatter Plot", "Histogram"])
    
    x_axis = st.selectbox("Select X-Axis:", col_names)
    y_axis = st.selectbox("Select Y-Axis:", col_names) if chart_type != "Pie Chart" else None
    color = st.color_picker("Pick a color:", "#4CAF50")
    threshold_value = st.number_input("Threshold Value", value=0)
    threshold_color = st.color_picker("Pick a threshold color:", "#FF0000")

    # Generate the chart based on selections
    fig, ax = plt.subplots()
    if chart_type == "Bar Chart" and y_axis:
        ax.bar(df[x_axis], df[y_axis], color=[threshold_color if val > threshold_value else color for val in df[y_axis]])
    elif chart_type == "Pie Chart":
        df[x_axis].value_counts().plot.pie(autopct="%1.1f%%", colors=[color, threshold_color], ax=ax)
    elif chart_type == "Line Chart" and y_axis:
        ax.plot(df[x_axis], df[y_axis], color=color)
    elif chart_type == "Scatter Plot" and y_axis:
        scatter_colors = [threshold_color if val > threshold_value else color for val in df[y_axis]]
        ax.scatter(df[x_axis], df[y_axis], color=scatter_colors)
    elif chart_type == "Histogram":
        sns.histplot(df[x_axis], kde=True, color=color, ax=ax)

    st.pyplot(fig)

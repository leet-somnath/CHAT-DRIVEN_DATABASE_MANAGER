import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_chart(df, chart_type, x_axis, y_axis, color, threshold_value, threshold_color):
    fig, ax = plt.subplots()
    if chart_type == 'Bar Chart':
        ax.bar(df[x_axis], df[y_axis], color=[threshold_color if val > threshold_value else color for val in df[y_axis]])
    elif chart_type == 'Pie Chart':
        df[y_axis].value_counts().plot.pie(autopct='%1.1f%%', colors=[color, threshold_color], ax=ax)
    elif chart_type == 'Line Chart':
        ax.plot(df[x_axis], df[y_axis], color=color)
    elif chart_type == 'Scatter Plot':
        ax.scatter(df[x_axis], df[y_axis], c=[threshold_color if val > threshold_value else color for val in df[y_axis]])
    elif chart_type == 'Histogram':
        sns.histplot(df[y_axis], kde=True, color=color, ax=ax)

    plot_path = 'static/images/plot.png'
    plt.savefig(plot_path)
    plt.close(fig)
    return plot_path

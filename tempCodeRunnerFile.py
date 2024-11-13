from flask import Flask, render_template, request, send_file, redirect, url_for, session
import os
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Set your secret key for session management

# Configure MySQL database connection
def connect_to_mysql():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="school",
        port=3306
    )

# Route to display home page and handle queries
@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    data = None
    col_names = []
    plot_path = None
    tables = []

    # Fetch table names
    db_conn = connect_to_mysql()
    cursor = db_conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    cursor.close()
    db_conn.close()

    if request.method == "POST":
        if "question" in request.form:
            # Handle the SQL query generation
            table = request.form["table"]
            question = request.form["question"]
            
            # Generate SQL query based on question - here, assuming some pre-generated query for testing
            query = f"SELECT * FROM {table} LIMIT 10"  # Example query, replace with actual generated query

            # Execute query and fetch data
            db_conn = connect_to_mysql()
            cursor = db_conn.cursor()
            cursor.execute(query)
            col_names = [i[0] for i in cursor.description]
            data = cursor.fetchall()
            cursor.close()
            db_conn.close()

            # Convert to DataFrame for visualization
            df = pd.DataFrame(data, columns=col_names)
            if not df.empty:
                data_html = df.to_html(classes="table table-striped", index=False)
                session["df"] = df.to_dict(orient="records")  # Store DataFrame as a list of records
                return render_template("index.html", query=query, data=data_html, col_names=col_names, tables=tables)

        elif "chart_type" in request.form:
            # Handle visualization request
            df = pd.DataFrame(session.get("df"))  # Retrieve DataFrame from session
            if df is not None:
                chart_type = request.form["chart_type"]
                x_axis = request.form["x_axis"]
                y_axis = request.form["y_axis"]
                color = request.form["color"]
                threshold_value = int(request.form.get("threshold_value", 0))
                threshold_color = request.form["threshold_color"]

                # Generate the appropriate chart
                fig, ax = plt.subplots()
                if chart_type == "Bar Chart":
                    ax.bar(df[x_axis], df[y_axis], color=[threshold_color if val > threshold_value else color for val in df[y_axis]])
                elif chart_type == "Pie Chart":
                    df[y_axis].value_counts().plot.pie(autopct="%1.1f%%", colors=[color, threshold_color], ax=ax)
                elif chart_type == "Line Chart":
                    ax.plot(df[x_axis], df[y_axis], color=color)
                elif chart_type == "Scatter Plot":
                    scatter_colors = [threshold_color if val > threshold_value else color for val in df[y_axis]]
                    ax.scatter(df[x_axis], df[y_axis], color=scatter_colors)
                elif chart_type == "Histogram":
                    sns.histplot(df[y_axis], kde=True, color=color, ax=ax)

                # Save the plot as an image in memory
                img = BytesIO()
                fig.savefig(img, format="png")
                img.seek(0)
                session["plot"] = img.getvalue()  # Store the image in session

                # Re-render the page with results and plot information
                data_html = df.to_html(classes="table table-striped", index=False)
                return render_template("index.html", query=query, data=data_html, col_names=col_names, tables=tables, plot_path=True)

    return render_template("index.html", query=query, data=data, col_names=col_names, tables=tables)

# Route to download query results as CSV
@app.route("/download_data")
def download_data():
    df = pd.DataFrame(session.get("df"))  # Retrieve DataFrame from session
    if df is not None:
        csv = df.to_csv(index=False)
        return send_file(BytesIO(csv.encode()), download_name="query_results.csv", as_attachment=True, mimetype="text/csv")

# Route to download the generated plot as PNG
@app.route("/download_plot")
def download_plot():
    img_data = session.get("plot")
    if img_data:
        return send_file(BytesIO(img_data), download_name="visualization.png", as_attachment=True, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, session, redirect, url_for, send_file
import os
import uuid
import mysql.connector
import pandas as pd
from io import BytesIO
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Initial AI prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION. \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    WHERE CLASS="Data Science"; 
    The SQL code should not have 
at the beginning or end and sql word in output.
    """
]

def connect_to_mysql():
    """Establish a connection to the MySQL database."""
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="school",
        port=3306
    )

def get_gemini_response(question, prompt):
    """Get SQL query response from Gemini AI model."""
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text.strip()

@app.route("/", methods=["GET", "POST"])
def index():
    tables = []
    query = ""
    db_conn = connect_to_mysql()
    cursor = db_conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    cursor.close()
    db_conn.close()

    if request.method == "POST":
        selected_table = request.form.get("table")
        question = request.form.get("question")

        if selected_table:
            query = get_gemini_response(question, prompt)
            query = query.replace("STUDENT", selected_table)

            # Store conversation entry in session
            entry_id = str(uuid.uuid4())
            db_conn = connect_to_mysql()
            cursor = db_conn.cursor()
            try:
                cursor.execute(query)
                col_names = [i[0] for i in cursor.description]
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=col_names)
                
                # HTML formatted table
                data_html = df.to_html(classes="table table-striped", index=False)

                # Initialize conversation list if it doesn't exist
                if "conversation" not in session:
                    session["conversation"] = []

                # Append current entry to conversation
                session["conversation"].append({
                    "id": entry_id,
                    "question": question,
                    "query": query,
                    "data_html": data_html,
                    "data": df.to_dict(orient="records")
                })

                # Ensure session updates correctly
                session.modified = True

            except Exception as e:
                return render_template("index.html", tables=tables, error=str(e))
            finally:
                cursor.close()
                db_conn.close()

    return render_template("index.html", tables=tables, conversation=session.get("conversation", []))

@app.route("/download_data")
def download_data():
    entry_id = request.args.get("entry_id")
    conversation = session.get("conversation", [])
    
    # Find the entry by ID
    entry = next((item for item in conversation if item["id"] == entry_id), None)
    
    if entry:
        df = pd.DataFrame(entry["data"])
        csv = df.to_csv(index=False)
        # Avoid modifying session here
        return send_file(BytesIO(csv.encode()), 
                         download_name="query_results.csv", 
                         as_attachment=True, 
                         mimetype="text/csv")
    
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

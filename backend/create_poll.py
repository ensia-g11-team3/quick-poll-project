from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",           
        password="",           
        database="quick_poll_db"   
    )

# Serve HTML
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Create poll endpoint
@app.route('/create_poll', methods=['POST'])
def create_poll():
    data = request.get_json()
    question = data.get("pollQuestion")

    if not question or len(question) > 200:
        return jsonify({"status":"error","message":"Invalid question"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO polls (pollQuestion) VALUES (%s)", (question,))
        conn.commit()
        poll_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"status":"success","pollid":poll_id,"pollQuestion":question}), 201
    except Exception as e:
        return jsonify({"status":"error","message":str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

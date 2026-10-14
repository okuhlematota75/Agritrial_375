from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db():
    return sqlite3.connect("users.db")

@app.route("/signup", methods = ["POST"])

def signup():
    data =  request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    password_hash = generate_password_hash(password)

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users(username, password_hash) VALUES (?,?)",
            (username, password_hash)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error":"Username already exists"}), 409
    finally:
        conn.close()

    return jsonify({"message":"New user"}), 201

@app.route("/login",methods =["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = ?",(username,))
    row = cursor.fetchone()
    conn.close()

    if row and check_password_hash(row[0],password):
        return jsonify({"message":"Login success"}), 200
    else:
        return jsonify({"error":"Invalid credentials"}), 401


def get_plant_db():
    return sqlite3.connect("plant_data.db")

@app.route("/add_plant_data", methods=["POST"])
def save_plant_data():
    data = request.get_json()

    site = data.get("site")
    crop = data.get("crop") 
    date = data.get("date")
    variety = data.get("variety")
    treatment = data.get("treatment")
    observer = data.get("observer")
    week = data.get("week")
    ph = data.get("ph")
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    notes = data.get("notes")
    plots = data.get("plots")

    if not site or not crop or not treatment or not plots:
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_plant_db()
    cursor = conn.cursor()
    try:
        for plot in plots:
            cursor.execute(
                """INSERT INTO plant_data(
                site, crop, date, variety, treatment, observer, week, plot, height, leaf_count, fresh_weight, dry_weight, root_length, yield_kg, disease_pct, ph, temperature, humidity, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",(site, crop, date, variety, treatment, observer, week, plot.get("plot"),plot.get("height"),plot.get("leaf_count"),plot.get("fresh_weight"),plot.get("dry_weight"),plot.get("root_length"),plot.get("yield_kg"),plot.get("disease_pct"),ph,temperature,humidity,notes)
            )
        conn.commit()
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()    
    return jsonify({"message": "Plant data saved successfully"}), 201

@app.route("/get_plant_data", methods=["GET"])
def get_plant_data():
     conn = get_plant_db()
     conn.row_factory = sqlite3.Row
     cursor = conn.cursor() 
     cursor.execute("SELECT * FROM plant_data")
     rows = cursor.fetchall()   
     conn.close()

     results = [dict(row) for row in rows]
     return jsonify({"plant_data": results}), 200

if __name__ == "__main__":
    app.run(debug=True)




import sqlite3

def plant_db():

 conn = sqlite3.connect("plant_data.db")
 cursor = conn.cursor()

 cursor.execute("""
 CREATE TABLE IF NOT EXISTS plant_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site TEXT NOT NULL,
    crop TEXT NOT NULL,
    date TEXT,
    variety TEXT,
    treatment TEXT,
    observer TEXT,
    week INTEGER,
    plot INTEGER NOT NULL,
    height NUMERIC,
    leaf_count INTEGER,
    fresh_weight NUMERIC,
    dry_weight NUMERIC,
    root_length NUMERIC,
    yield_kg NUMERIC,
    disease_pct NUMERIC,
    ph NUMERIC,
    temperature NUMERIC,
    humidity NUMERIC,
    notes TEXT
 )
""")
 
 conn.commit()
 conn.close()

plant_db()
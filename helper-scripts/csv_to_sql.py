import csv
import sqlite3
from pathlib import Path

# File paths
CSV_FILE = Path("journal.csv")
DB_FILE = Path("journalCSV.db")

# Delete DB if it exists (starting fresh)
if DB_FILE.exists():
    DB_FILE.unlink()

# Connect to SQLite
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# Create schema
cur.executescript("""
CREATE TABLE entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_date TEXT,
    date TEXT,
    weekday TEXT,
    time TEXT,
    mood TEXT,
    note_title TEXT,
    note TEXT
);

CREATE TABLE activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
);

CREATE TABLE entry_activities (
    entry_id INTEGER,
    activity_id INTEGER,
    PRIMARY KEY (entry_id, activity_id),
    FOREIGN KEY (entry_id) REFERENCES entries(id),
    FOREIGN KEY (activity_id) REFERENCES activities(id)
);
""")

# Cache to avoid re-inserting same activities
activity_cache = {}

def get_or_create_activity_id(name):
    name = name.strip()
    if not name:
        return None
    if name in activity_cache:
        return activity_cache[name]

    cur.execute("INSERT OR IGNORE INTO activities (name) VALUES (?)", (name,))
    cur.execute("SELECT id FROM activities WHERE name = ?", (name,))
    result = cur.fetchone()
    if result:
        activity_id = result[0]
        activity_cache[name] = activity_id
        return activity_id
    return None

# Read and import CSV
with open(CSV_FILE, newline='', encoding='utf-8-sig') as csvfile: # utf-8-sig to handle BOM
    reader = csv.DictReader(csvfile)
    for row in reader:
        note_clean = row['note'].replace("<br><br>", "\n\n")

        # Insert into entries table
        cur.execute("""
            INSERT INTO entries (full_date, date, weekday, time, mood, note_title, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            row['full_date'],
            row['date'],
            row['weekday'],
            row['time'],
            row['mood'],
            row['note_title'],
            note_clean
        ))
        entry_id = cur.lastrowid

        # Split and insert activities
        raw_activities = row['activities']
        if raw_activities.strip():
            activities = [a.strip() for a in raw_activities.split('|')]
            for act in activities:
                activity_id = get_or_create_activity_id(act)
                if activity_id:
                    cur.execute("""
                        INSERT INTO entry_activities (entry_id, activity_id)
                        VALUES (?, ?)
                    """, (entry_id, activity_id))

# Commit and close
conn.commit()
conn.close()

print(f"✅ All data imported into '{DB_FILE}' successfully.")

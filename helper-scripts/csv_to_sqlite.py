import csv
import sqlite3
from datetime import datetime

def create_database():
    conn = sqlite3.connect('journalDEEP.db')
    c = conn.cursor()
    
    # Create main entries table
    c.execute('''CREATE TABLE IF NOT EXISTS entries
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  full_date DATE NOT NULL,
                  date TEXT NOT NULL,
                  weekday TEXT NOT NULL,
                  time TIME NOT NULL,
                  mood TEXT NOT NULL,
                  note_title TEXT,
                  note TEXT)''')
    
    # Create activities lookup table
    c.execute('''CREATE TABLE IF NOT EXISTS activities
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT UNIQUE)''')
    
    # Create entry-activity relationship table
    c.execute('''CREATE TABLE IF NOT EXISTS entry_activities
                 (entry_id INTEGER,
                  activity_id INTEGER,
                  FOREIGN KEY(entry_id) REFERENCES entries(id),
                  FOREIGN KEY(activity_id) REFERENCES activities(id))''')
    
    # Predefined activities and moods
    predefined_activities = {
        'work', 'relax', 'friends', 'date', 'sport', 'celebration',
        'watching', 'reading', 'gaming', 'shopping', 'travel',
        'good meal', 'cleaning', 'thinking', 'beaten up', 'art',
        'sleeping', 'adrenaline', 'IDEA'
    }
    
    predefined_moods = {
        'Rad', 'Great', 'meh', 'Bad', 'Pissed',
        'Depressed', 'Terrible', 'Hurt'
    }
    
    # Insert predefined activities
    for activity in predefined_activities:
        c.execute('INSERT OR IGNORE INTO activities (name) VALUES (?)', (activity,))
    
    conn.commit()
    return conn

def process_csv(conn):
    c = conn.cursor()
    
    with open('journal_entries.csv', 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            # Clean note content
            note = row['note'].replace('<br><br>', '\n\n')
            
            # Insert main entry
            c.execute('''INSERT INTO entries
                         (full_date, date, weekday, time, mood, note_title, note)
                         VALUES (?, ?, ?, ?, ?, ?, ?)''',
                     (row['full_date'],
                      row['date'],
                      row['weekday'],
                      row['time'],
                      row['mood'],
                      row['note_title'],
                      note))
            
            entry_id = c.lastrowid
            
            # Process activities
            if row['activities']:
                activities = [a.strip() for a in row['activities'].split(' | ')]
                for activity in activities:
                    # Insert activity relationship
                    c.execute('''INSERT INTO entry_activities (entry_id, activity_id)
                                 SELECT ?, id FROM activities WHERE name = ?''',
                              (entry_id, activity))
    
    conn.commit()

def main():
    conn = create_database()
    try:
        process_csv(conn)
        print("Successfully converted CSV to SQLite database!")
    except Exception as e:
        print(f"Error processing data: {str(e)}")
    finally:
        conn.close()

if __name__ == '__main__':
    main()
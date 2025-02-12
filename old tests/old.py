import streamlit as st
import sqlite3
import datetime

# Helper functions
def get_ordinal_suffix(day):
    if 11 <= (day % 100) <= 13:
        return 'th'
    return {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

def format_full_date(date_obj):
    day_name = date_obj.strftime("%A")
    day = date_obj.day
    suffix = get_ordinal_suffix(day)
    month_year = date_obj.strftime("%B %Y")
    return f"{day_name}, {day}{suffix} {month_year}"

# Database setup
def get_db_connection():
    conn = sqlite3.connect('journal.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_date TEXT NOT NULL,
            entry_date DATE NOT NULL,
            entry_time TEXT NOT NULL,
            mood TEXT NOT NULL,
            activities TEXT,
            entry_title TEXT NOT NULL,
            entry_text TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setting_name TEXT UNIQUE,
            setting_value TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database and settings
init_db()

# Page configuration
st.set_page_config(page_title="Digital Journal", layout="wide")

# Session state initialization
if 'settings' not in st.session_state:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT setting_name, setting_value FROM settings")
    st.session_state.settings = {row['setting_name']: row['setting_value'] for row in cursor.fetchall()}
    conn.close()

# Navigation
page = st.sidebar.radio("Navigation", ["Write", "Read", "Settings"])

# Write Page
if page == "Write":
    st.header("New Journal Entry")
    with st.form("entry_form"):
        entry_date = st.date_input("Entry Date", datetime.date.today())
        entry_time = st.time_input("Entry Time", datetime.datetime.now().time())
        mood = st.selectbox("Mood", ["😊 Happy", "😢 Sad", "😐 Neutral", "🤩 Excited", "😴 Tired", "😠 Angry", "😌 Calm"])
        activities = st.multiselect("Activities", ["💼 Work", "🏋️ Exercise", "📚 Study", "👥 Social", "🎨 Hobby", "✈️ Travel", "🎮 Gaming"])
        entry_title = st.text_input("Entry Title")
        entry_text = st.text_area("Entry Text", height=200)
        submitted = st.form_submit_button("Save Entry")

    if submitted:
        full_date = format_full_date(entry_date)
        time_str = entry_time.strftime("%H:%M")
        activities_str = ", ".join(activities) if activities else "None"
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO journal_entries 
            (full_date, entry_date, entry_time, mood, activities, entry_title, entry_text)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (full_date, entry_date.isoformat(), time_str, mood, activities_str, entry_title, entry_text))
        conn.commit()
        conn.close()
        st.success("Entry saved successfully!")

# Read Page
elif page == "Read":
    st.header("Journal Entries")
    
    # Filters
    st.sidebar.header("Filters")
    date_col1, date_col2 = st.sidebar.columns(2)
    with date_col1:
        start_date = st.date_input("Start date", datetime.date.today() - datetime.timedelta(days=7))
    with date_col2:
        end_date = st.date_input("End date", datetime.date.today())
    
    mood_options = ["😊 Happy", "😢 Sad", "😐 Neutral", "🤩 Excited", "😴 Tired", "😠 Angry", "😌 Calm"]
    selected_moods = st.sidebar.multiselect("Filter by Mood", mood_options)
    
    activity_options = ["💼 Work", "🏋️ Exercise", "📚 Study", "👥 Social", "🎨 Hobby", "✈️ Travel", "🎮 Gaming"]
    selected_activities = st.sidebar.multiselect("Filter by Activities", activity_options)
    
    search_text = st.sidebar.text_input("Search Entries")

    # Build query
    query = '''
        SELECT * FROM journal_entries 
        WHERE entry_date BETWEEN ? AND ?
    '''
    params = [start_date.isoformat(), end_date.isoformat()]

    if selected_moods:
        query += f" AND mood IN ({','.join(['?']*len(selected_moods))}"
        params += selected_moods

    if selected_activities:
        for activity in selected_activities:
            query += " AND activities LIKE ?"
            params.append(f"%{activity}%")

    if search_text:
        query += " AND (entry_title LIKE ? OR entry_text LIKE ?)"
        params += [f"%{search_text}%"] * 2

    # Fetch entries
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    entries = cursor.fetchall()
    conn.close()

    # Display entries
    if not entries:
        st.info("No entries found matching the current filters.")
    else:
        for entry in entries:
            with st.expander(f"{entry['entry_title']} - {entry['full_date']}"):
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.subheader("Details")
                    st.write(f"**Date:** {entry['full_date']}")
                    
                    # Time formatting based on settings
                    time_str = entry['entry_time']
                    if st.session_state.settings.get('time_format') == '12-hour':
                        time_obj = datetime.datetime.strptime(time_str, "%H:%M")
                        display_time = time_obj.strftime("%I:%M %p")
                    else:
                        display_time = time_str
                    st.write(f"**Time:** {display_time}")
                    
                    st.write(f"**Mood:** {entry['mood']}")
                    st.write(f"**Activities:** {entry['activities']}")
                
                with col2:
                    st.subheader("Entry Content")
                    st.write(entry['entry_text'])

# Settings Page
elif page == "Settings":
    st.header("Settings")
    
    # Time format setting
    current_format = st.session_state.settings.get('time_format', '24-hour')
    new_format = st.selectbox(
        "Time Format", 
        options=['24-hour', '12-hour'], 
        index=0 if current_format == '24-hour' else 1
    )
    
    if st.button("Save Settings"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO settings (setting_name, setting_value)
            VALUES ('time_format', ?)
        ''', (new_format,))
        conn.commit()
        conn.close()
        st.session_state.settings = {'time_format': new_format}
        st.success("Settings updated!")
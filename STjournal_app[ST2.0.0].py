import streamlit as st
import sqlite3
import datetime
import pandas as pd

# Helper functions
def format_full_date(date_obj):
    day_name = date_obj.strftime("%A")
    day = date_obj.day
    suffix = get_ordinal_suffix(day)
    month_year = date_obj.strftime("%B %Y")
    return f"{day_name}, {day}{suffix} {month_year}"

def get_ordinal_suffix(day):
    if 11 <= (day % 100) <= 13:
        return 'th'
    return {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

# Database connections
def get_journal_db():
    conn = sqlite3.connect('my_journal.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_settings_db():
    conn = sqlite3.connect('settings.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_dbs():
    # Initialise journal database
    conn_journal = get_journal_db()
    cursor = conn_journal.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_date DATE NOT NULL,
            date TEXT NOT NULL,
            weekday TEXT NOT NULL,
            time TIME NOT NULL,
            mood TEXT NOT NULL,
            note_title TEXT,
            note TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entry_activities (
            entry_id INTEGER,
            activity_id INTEGER,
            FOREIGN KEY(entry_id) REFERENCES entries(id),
            FOREIGN KEY(activity_id) REFERENCES activities(id)
        )
    ''')
    predefined_activities = [
        'work', 'relax', 'friends', 'date', 'sport', 'celebration',
        'watching', 'reading', 'gaming', 'shopping', 'travel',
        'good meal', 'cleaning', 'thinking', 'beaten up', 'art',
        'sleeping', 'adrenaline', 'IDEA'
    ]
    for activity in predefined_activities:
        cursor.execute('INSERT OR IGNORE INTO activities (name) VALUES (?)', (activity,))
    conn_journal.commit()
    conn_journal.close()

    # Initialise settings database
    conn_settings = get_settings_db()
    cursor = conn_settings.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setting_name TEXT UNIQUE,
            setting_value TEXT
        )
    ''')
    conn_settings.commit()
    conn_settings.close()

def delete_entry(entry_id):
    conn = get_journal_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM entries WHERE id = ?', (entry_id,))
    cursor.execute('DELETE FROM entry_activities WHERE entry_id = ?', (entry_id,))
    conn.commit()
    conn.close()

# Initialise databases
init_dbs()

# Page configuration
st.set_page_config(
    page_title="Digital Journal",
    page_icon="📔",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': None,
        'Report a bug': "https://github.com/A-wase/journal-app/pulls",
        'About': "# Your Digital Journal App"
    }
)

# Session state initialisation
if 'settings' not in st.session_state:
    conn = get_settings_db()
    cursor = conn.cursor()
    cursor.execute("SELECT setting_name, setting_value FROM settings")
    st.session_state.settings = {row['setting_name']: row['setting_value'] for row in cursor.fetchall()}
    conn.close()

# Mappings for UI display
MOOD_MAPPING = {
    'Rad': '😊 Rad',
    'Great': '🎉 Great',
    'meh': '😐 meh',
    'Bad': '😞 Bad',
    'Pissed': '😠 Pissed',
    'Depressed': '😔 Depressed',
    'Terrible': '😖 Terrible',
    'Hurt': '💔 Hurt'
}

ACTIVITY_MAPPING = {
    'work': '💼 Work',
    'relax': '🛋️ Relax',
    'friends': '👥 Friends',
    'date': '💑 Date',
    'sport': '🏋️ Sport',
    'celebration': '🎉 Celebration',
    'watching': '📺 Watching',
    'reading': '📚 Reading',
    'gaming': '🎮 Gaming',
    'shopping': '🛍️ Shopping',
    'travel': '✈️ Travel',
    'good meal': '🍲 Good Meal',
    'cleaning': '🧹 Cleaning',
    'thinking': '🤔 Thinking',
    'beaten up': '😵 Beaten Up',
    'art': '🎨 Art',
    'sleeping': '😴 Sleeping',
    'adrenaline': '🎢 Adrenaline',
    'IDEA': '💡 IDEA'
}

# Navigation Sidebar
page = st.sidebar.radio("Navigation", ["Write", "Read", "Analytics", "Settings"])

# Write Page
if page == "Write":
    st.header("New Journal Entry")
    with st.form("entry_form"):
        entry_date = st.date_input("Entry Date", datetime.date.today())
        entry_time = st.time_input("Entry Time", datetime.datetime.now().time())
        mood = st.selectbox("Mood", list(MOOD_MAPPING.values()))
        activities = st.multiselect("Activities", list(ACTIVITY_MAPPING.values()))
        note_title = st.text_input("Entry Title")
        note_text = st.text_area("Entry Text", height=200)
        submitted = st.form_submit_button("Save Entry")

    if submitted:
        full_date = entry_date.isoformat()
        date_str = entry_date.strftime("%B %d").lstrip("0").replace(" 0", " ")
        weekday = entry_date.strftime("%A")
        time_str = entry_time.strftime("%H:%M")
        db_mood = [k for k, v in MOOD_MAPPING.items() if v == mood][0]
        db_activities = [k for k, v in ACTIVITY_MAPPING.items() if v in activities]

        conn = get_journal_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO entries 
            (full_date, date, weekday, time, mood, note_title, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (full_date, date_str, weekday, time_str, db_mood, note_title, note_text))
        entry_id = cursor.lastrowid

        for activity in db_activities:
            cursor.execute('''
                INSERT INTO entry_activities (entry_id, activity_id)
                SELECT ?, id FROM activities WHERE name = ?
            ''', (entry_id, activity))
        
        conn.commit()
        conn.close()
        st.success("Entry saved successfully!")

elif page == "Read":
    st.header("Journal Entries")
    
    # Filters
    st.sidebar.header("Filters")
    date_col1, date_col2 = st.sidebar.columns(2)
    with date_col1:
        start_date = st.date_input("Start date", datetime.date.today() - datetime.timedelta(days=7))
    with date_col2:
        end_date = st.date_input("End date", datetime.date.today())
    
    selected_moods = st.sidebar.multiselect("Filter by Mood", list(MOOD_MAPPING.values()))
    selected_activities = st.sidebar.multiselect("Filter by Activities", list(ACTIVITY_MAPPING.values()))
    search_text = st.sidebar.text_input("Search Entries")

    # Build query
    base_query = '''
        SELECT 
            entries.*, 
            GROUP_CONCAT(activities.name, ' | ') AS activities 
        FROM entries
        LEFT JOIN entry_activities ON entries.id = entry_activities.entry_id
        LEFT JOIN activities ON entry_activities.activity_id = activities.id
        WHERE entries.full_date BETWEEN ? AND ?
    '''
    params = [start_date.isoformat(), end_date.isoformat()]
    query_parts = [base_query]

    if selected_moods:
        db_moods = [k for k, v in MOOD_MAPPING.items() if v in selected_moods]
        placeholders = ','.join(['?'] * len(db_moods))
        query_parts.append(f" AND entries.mood IN ({placeholders})")
        params += db_moods

    if selected_activities:
        db_activities = [k for k, v in ACTIVITY_MAPPING.items() if v in selected_activities]
        for activity in db_activities:
            query_parts.append(" AND activities.name = ?")
            params.append(activity)

    if search_text:
        query_parts.append(" AND (note_title LIKE ? OR note LIKE ?)")
        params += [f"%{search_text}%", f"%{search_text}%"]

    query_parts.append(" GROUP BY entries.id")
    final_query = ' '.join(query_parts)

    # Fetch entries
    conn = get_journal_db()
    cursor = conn.cursor()
    cursor.execute(final_query, params)
    entries = cursor.fetchall()
    conn.close()

    # Display entries
    if not entries:
        st.info("No entries found matching the current filters.")
    else:
        for entry in entries:
            with st.expander(f"{entry['note_title']} - {entry['date']}"):
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.subheader("Details")
                    st.write(f"**Date:** {format_full_date(datetime.date.fromisoformat(entry['full_date']))}")
                    
                    # Time formatting
                    time_str = entry['time']
                    if st.session_state.settings.get('time_format') == '12-hour':
                        time_obj = datetime.datetime.strptime(time_str, "%H:%M")
                        display_time = time_obj.strftime("%I:%M %p")
                    else:
                        display_time = time_str
                    st.write(f"**Time:** {display_time}")
                    
                    st.write(f"**Mood:** {MOOD_MAPPING.get(entry['mood'], entry['mood'])}")
                    activities = [ACTIVITY_MAPPING.get(a, a) for a in entry['activities'].split(' | ')] if entry['activities'] else []
                    st.write(f"**Activities:** {', '.join(activities) if activities else 'None'}")

                    if st.button(
                        "🗑️ Delete Entry",
                        key=f"delete_{entry['id']}",
                        on_click=delete_entry,
                        args=(entry['id'],),
                        help="Permanently delete this entry"
                    ):
                        st.success("Entry deleted successfully!")
                        st.experimental_rerun()

                with col2:
                    st.subheader("Entry Content")
                    st.write(entry['note'])

# Settings Page
elif page == "Settings":
    st.header("Settings")
    
    current_format = st.session_state.settings.get('time_format', '24-hour')
    new_format = st.selectbox(
        "Time Format", 
        options=['24-hour', '12-hour'], 
        index=0 if current_format == '24-hour' else 1
    )
    
    if st.button("Save Settings"):
        conn = get_settings_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO settings (setting_name, setting_value)
            VALUES ('time_format', ?)
        ''', (new_format,))
        conn.commit()
        conn.close()
        st.session_state.settings = {'time_format': new_format}
        st.success("Settings updated!")

elif page == "Analytics":
    st.header("📈 Journal Analytics")
    
    conn = get_journal_db()
    query = '''
        SELECT full_date, mood 
        FROM entries
        ORDER BY full_date
    '''
    mood_df = pd.read_sql(query, conn)
    conn.close()
    
    if not mood_df.empty:
        mood_df['full_date'] = pd.to_datetime(mood_df['full_date'])
        min_date = mood_df['full_date'].min().date()
        max_date = mood_df['full_date'].max().date()
        
        with st.sidebar:
            st.subheader("Date Range")
            start_date, end_date = st.date_input(
                "Select range",
                [min_date, max_date],
                min_value=min_date,
                max_value=max_date
            )
        
        mask = (mood_df['full_date'].dt.date >= start_date) & (mood_df['full_date'].dt.date <= end_date)
        filtered_df = mood_df[mask]
        
        if not filtered_df.empty:
            # Mood Frequency Chart
            st.subheader("Mood Distribution")
            freq_df = filtered_df['mood'].map(MOOD_MAPPING).value_counts().reset_index()
            freq_df.columns = ['Mood', 'Count']
            st.bar_chart(freq_df.set_index('Mood'), use_container_width=True)
            
            # Mood Timeline Chart
            st.subheader("Mood Timeline")
            timeline_df = filtered_df.copy()
            timeline_df['mood'] = timeline_df['mood'].map(MOOD_MAPPING)
            timeline_df = timeline_df.groupby(
                [pd.Grouper(key='full_date', freq='D'), 'mood']
            ).size().unstack(fill_value=0)
            
            date_range = pd.date_range(start=start_date, end=end_date)
            timeline_df = timeline_df.reindex(date_range, fill_value=0)
            
            st.line_chart(timeline_df, height=400)
            
            # Statistics Section
            st.subheader("Key Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Entries", len(filtered_df))
                
            with col2:
                most_common_mood = filtered_df['mood'].map(MOOD_MAPPING).mode()[0]
                st.metric("Most Frequent Mood", most_common_mood)
                
            with col3:
                days_with_entries = filtered_df['full_date'].nunique()
                st.metric("Days with Entries", days_with_entries)
                
        else:
            st.warning("No entries found in the selected date range")
    else:
        st.info("No journal entries available for analysis yet!")
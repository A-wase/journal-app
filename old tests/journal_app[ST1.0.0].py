import streamlit as st # Streamlit made this whole app much easier than my initial Tkinter plan.
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

def delete_entry(entry_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM journal_entries WHERE id = ?', (entry_id,))
    conn.commit()
    conn.close()

# Initialise database and settings
init_db()

# Page configuration
st.set_page_config(page_title="Digital Journal", page_icon="📔", layout="wide", initial_sidebar_state="auto",  menu_items={
        'Get Help': None,
        'Report a bug': "https://github.com/A-wase/journal-app/pulls",
        'About': "# This is a header. This is an *extremely* cool app!"
    })

# Session state initialisation
if 'settings' not in st.session_state:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT setting_name, setting_value FROM settings")
    st.session_state.settings = {row['setting_name']: row['setting_value'] for row in cursor.fetchall()}
    conn.close()

# Navigation Sidebar
page = st.sidebar.radio("Navigation", ["Write", "Read", "Analytics", "Settings"])

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

    # Displaying entries
    if not entries:
        st.info("No entries found matching the current filters.")
    else:
        for entry in entries:
            with st.expander(f"{entry['entry_title']} - {entry['full_date']}"):
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.subheader("Details")
                    st.write(f"**Date:** {entry['full_date']}")
                    
                    # Time formatting from option in the settings page
                    time_str = entry['entry_time']
                    if st.session_state.settings.get('time_format') == '12-hour':
                        time_obj = datetime.datetime.strptime(time_str, "%H:%M")
                        display_time = time_obj.strftime("%I:%M %p")
                    else:
                        display_time = time_str
                    st.write(f"**Time:** {display_time}")
                    
                    st.write(f"**Mood:** {entry['mood']}")
                    st.write(f"**Activities:** {entry['activities']}")

                    # Add delete button
                    if st.button(
                        "🗑️ Delete Entry",
                        key=f"delete_{entry['id']}",  # Unique key per entry
                        on_click=delete_entry,  # Calls delete function
                        args=(entry['id'],),     # Passes entry ID to function
                        help="Permanently delete this entry"
                    ):
                        st.success("Entry deleted successfully!")
                        st.experimental_rerun()  # Refresh the page

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

elif page == "Analytics":
    st.header("📈 Journal Analytics")
    
    # Fetch all mood data
    conn = get_db_connection()
    query = '''
        SELECT entry_date, mood 
        FROM journal_entries
        ORDER BY entry_date
    '''
    mood_df = pd.read_sql(query, conn)
    conn.close()
    
    if not mood_df.empty:
        # Convert to datetime and extract metrics
        mood_df['entry_date'] = pd.to_datetime(mood_df['entry_date'])
        min_date = mood_df['entry_date'].min().date()
        max_date = mood_df['entry_date'].max().date()
        
        # Date filters in sidebar
        with st.sidebar:
            st.subheader("Date Range")
            start_date, end_date = st.date_input(
                "Select range",
                [min_date, max_date],
                min_value=min_date,
                max_value=max_date
            )
        
        # Filter data
        mask = (mood_df['entry_date'].dt.date >= start_date) & (mood_df['entry_date'].dt.date <= end_date)
        filtered_df = mood_df[mask]
        
        if not filtered_df.empty:
            # Mood Frequency Chart
            st.subheader("Mood Distribution")
            freq_df = filtered_df['mood'].value_counts().reset_index()
            freq_df.columns = ['Mood', 'Count']
            st.bar_chart(freq_df.set_index('Mood'), use_container_width=True)
            
            # Mood Timeline Chart
            st.subheader("Mood Timeline")
            
            # Create daily mood counts
            timeline_df = filtered_df.groupby(
                [pd.Grouper(key='entry_date', freq='D'), 'mood']
            ).size().unstack(fill_value=0)
            
            # Resample to include all dates in range
            date_range = pd.date_range(start=start_date, end=end_date)
            timeline_df = timeline_df.reindex(date_range, fill_value=0)
            
            st.line_chart(timeline_df, height=400)
            
            # Statistics Section
            st.subheader("Key Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Entries", len(filtered_df))
                
            with col2:
                most_common_mood = filtered_df['mood'].mode()[0]
                st.metric("Most Frequent Mood", most_common_mood)
                
            with col3:
                days_with_entries = filtered_df['entry_date'].nunique()
                st.metric("Days with Entries", days_with_entries)
                
        else:
            st.warning("No entries found in the selected date range")
    else:
        st.info("No journal entries available for analysis yet!")
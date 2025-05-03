# Digital Journal App

## NOT FINISHED! STILL IN DEVELOPMENT! BUT FEEL FREE TO CHECK WHAT I HAVE MADE! HELP WELCOMED!!!
A Streamlit-based web application for maintaining a personal journal with rich analytics and data persistence.

![App Screenshot](https://via.placeholder.com/800x400.png?text=Digital+Journal+App+Screenshot)

## Why I made this journal app
I created this journal app for personal use and as a way to learn more about the Streamlit library and SQLite. Initially, I planned to build this project using Tkinter and to export the database into Microsoft Excel. However, as I worked on improving my programming skills, I researched better database management solutions beyond simple Excel file exports. That’s when I discovered and decided to use SQLite.

While saving data as an Excel or CSV file might have been a viable alternative, I believe that Excel spreadsheets could become slow when handling large amounts of data and this could negatively impact the app's usage in the future. With CSV, it does not have efficient querying, data integrity, and scalability for a structured journal application, unlike SQL. More importantly, my main goal was to learn, experiment, and grow as a developer. I was particularly excited to discover Streamlit and explore SQL-based data management within my own project.

In the end, I successfully built this simple yet functional journal app, and I’m proud of what I’ve learned along the way. The app itself is nothing fancy, complicated, or groundbreaking, but it serves its purpose well. It provides a simple and intuitive way to jot down thoughts, reflect on past entries, and helped me practice working with databases and web-based Python applications. More than anything, it represents my progress as a developer and my excitement for learning new technologies.

## Features

### 📝 Write Entries
- Date and time tracking with automatic formatting
- Mood selection with emoji visualisation
- Activity tagging system
- Rich text entries with titles
- Automatic SQLite database storage (journal.db)

### 📖 Read & Organise
- Chronological entry display
- Advanced filtering by:
  - Date range
  - Mood
  - Activities
  - Keyword search
- Expandable entry cards
- Delete entries with one click

### 📊 Analytics Dashboard
- Mood frequency distribution charts
- Mood timeline visualisation
- Journaling statistics:
  - Total entries
  - Most frequent mood
  - Days with entries
- Interactive date range filtering

### ⚙️ Settings
- 12/24 hour time format preference


## Installation

1. **Prerequisites**:
   - Python 3.8+
   - pip package manager

2. **Install dependencies**:
   ```bash
   pip install streamlit pandas

## To run

1. **In terminal run**:
   ```bash
   streamlit run journal_app.py

## Usage
**First Run:**
- Automatically creates journal.db database
- Default settings initialised

**Navigation:**
- Use the sidebar to switch between pages

**Four main siderbar sections:**
- **Write:** Create new journal entries
- **Read:** Browse and manage existing entries
- **Analytics:** View journaling statistics
- **Settings:** Configure display preferences

## Data Management:
- Entries automatically saved on submission
- Deleted entries are permanently removed
- Database stored in journal.db file

### 🗃️ Storage Format Comparison

| Feature               | SQLite3        | JSON Files      | CSV Files       | Markdown Files   |
|-----------------------|----------------|------------------|------------------|------------------|
| Structured Data       | ✅ Yes         | ✅ Yes           | ⚠️ Limited       | ⚠️ Limited       |
| Scalability           | ✅ High        | ⚠️ Medium        | ❌ Low           | ❌ Low           |
| Search & Filtering    | ✅ Advanced    | ⚠️ Manual Coding | ❌ Basic Only    | ❌ Manual Only   |
| Tagging Support       | ✅ Native Schema | ⚠️ Manual Logic | ❌ None          | ⚠️ With Frontmatter |
| Stats & Analytics     | ✅ Easy (SQL)  | ⚠️ Manual        | ⚠️ Manual        | ❌ Difficult     |
| Performance (Large Data) | ✅ Fast    | ⚠️ Slower (in-memory) | ⚠️ Slow         | ❌ Very Slow     |
| Portability & Backup  | ✅ Single File | ✅ Folder-based  | ✅ Single File   | ✅ Folder-based  |
| Readability (Raw Data)| ⚠️ Moderate   | ✅ High          | ✅ High          | ✅ Very High     |

> ✅ = Good / Recommended, ⚠️ = Possible but needs effort, ❌ = Poor or impractical


## Acknowledgments
- Built with Streamlit in Python
- Thanks to the [Python documentation page about the SQLite3 module](https://docs.python.org/3/library/sqlite3.html#sqlite3-tutorial) for introducing me to how SQLite3 works, and also, thanks to [this YouTube video](https://www.youtube.com/watch?v=byHcYRpMgI4) by freeCodeCamp.org for ironing out my knowledge on SQLite3.
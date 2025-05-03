Using Streamlit and SQLite in Python, I am making a simple Journal App that is a simple CRUD app with multiple pages (read, write, analytics, settings).

Current App Features:

Write Entries
- Date and time tracking with automatic formatting
- Mood selection with emoji visualisation
- Activity tagging system
- Rich text entries with titles
- Automatic SQLite database storage (journal.db)

Read & Organise
- Chronological entry display
- Advanced filtering by:
  - Date range
  - Mood
  - Activities
  - Keyword search
- Expandable entry cards
- Delete entries with one click

Analytics Dashboard
- Mood frequency distribution charts
- Mood timeline visualisation
- Journaling statistics:
  - Total entries
  - Most frequent mood
  - Days with entries
- Interactive date range filtering

Settings
- 12/24 hour time format preference

Data Managment
- Entries automatically saved on submission
- Deleted entries are permanently removed
- Database stored in journal.db file
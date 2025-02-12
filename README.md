# Digital Journal App

A Streamlit-based web application for maintaining a personal journal with rich analytics and data persistence.

![App Screenshot](https://via.placeholder.com/800x400.png?text=Digital+Journal+App+Screenshot)

## Features

### 📝 Write Entries
- Date and time tracking with automatic formatting
- Mood selection with emoji visualisation
- Activity tagging system
- Rich text entries with titles
- Automatic SQLite database storage

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

2. **In terminal run**:
   ```bash
   streamlit run journal_app.py

## Usage
**First Run:**
- Automatically creates journal.db database
- Default settings initialised

**Navigation:**
- Use the sidebar to switch between pages

**Four main sections:**
- Write: Create new journal entries
- Read: Browse and manage existing entries
- Analytics: View journaling statistics
- Settings: Configure display preferences

## Data Management:
- Entries automatically saved on submission
- Deleted entries are permanently removed
- Database stored in journal.db file

## Acknowledgments
- Built with Streamlit in Python
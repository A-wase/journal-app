# Changelog
All notable changes to this project will be documented in this file. `CHANGELOG.md` is for myself, contributors, or collaborators to track technical updates (features, fixes, versions).

## [2.0.0] 06-MAY-2025
### New Database Schema!
- **Database Separation**: Split into `journal.db` (entries) and `settings.db` (config)
- **Schema Alignment**: Matched database structure with CSV conversion format
- **Normalized Data**: Added activity relationship table for multi-select entries

### Key Improvements
- **UI Mappings**: Added emoji displays for moods/activities while storing raw values
- **Enhanced Queries**: Implemented JOIN operations for activity filtering
- **Deletion Handling**: Added cascading delete for activity relationships
- **Analytics Update**: Migrated stats to work with new schema
- **Time Format**: Moved time display setting to separate settings DB

### Compatibility
- Full backward compatibility with converted CSV data taken from another app I used for 10 years!
- Automatic DB initialisation for new users
- Preserved existing Streamlit UI/UX patterns


## [1.0.0] 12-FEB-2025
### The First Release!
- Create, read, update and delete entries
- Search through entires with an analytics page
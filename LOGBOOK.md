# Logbook
Welcome to my logbook: a personal and reflective journal capturing my thinking process, decisions, and experiments. This space serves as a non-linear record of ideas, insights, and progress, offering a glimpse into the journey behind the work. It is similar to `CHANGELOG.md` but less technical. Logbooks are looser by nature: notes, drafts, brainstorming and many abandoned ideas. Keeping it separate from `CHANGELOG.md` encourages more honest and useful reflection from myself... If only there were some kind of app designed specifically for jotting down thoughts and plans... oh well, guess I’ll just use this file.

## [LOG: 1] 06-MAY-2025
### **App data conversion**
I am in the process of trying to parse my previous journal data from a CSV file and converting it into a SQLite database file. I got the CSV from the current journal app that I use. I wish to use my existing data in my own app. The app also has another export choice: an encrypted custom file with more of my data.

I have good news and bad news.

The good news...
I have succeeded in reverse engineering this application's custom ".REDACTED" app data export file. I have redacted the actual file name to preserve the app's identity.

I have discovered that this is actually just a zip file.

I first renamed the file and replaced ".REDACTED" with ".zip"

Inside the zip file was another REDACTED file. This one was not a zip. It was an encoded file. It was encoded in base64.

I reversed the encoding and a JSON file was output.

I viewed the contents of the JSON code with a online JSON viewer and it contained all my data. It had everything. My thousands of entries, my saved custom-activities, my in-app settings. It literally had everything important for the app.

The bad news is that I cannot use this data. It would take the absolute pain to clean up. It has a lot of unnecessary stuff and I do not have energy for this.

My solution: I will instead choose to use the CSV file and clean that up and then convert it into a SQLite database. It is much easier to go this route because the CSV does not have a lot of bloat into it. The JSON is my full in-app data and written journal data. The CSV is just my written journal data and it is in a more concise format, albeit strange formatting code with "utf-8-sig".

### **Design Decision: Separation of Data into `journal.db` and `settings.db`**

To improve modularity, privacy, and flexibility, I decided to separate user content from app configuration by creating two SQLite databases:

* `journal.db`: Stores user-generated content such as journal entries, moods, activities, and notes.
* `settings.db`: Stores in-app settings like UI themes, preferences, and custom configurations.

This structure allows users to export/share only their journal data without exposing personal settings. It also enables settings sharing between users without affecting journal content. This separation improves maintainability, supports safer imports/exports, and lays the groundwork for potential features like theme sharing or settings versioning.  I will then chnage my old SQL database schema to match the new one.
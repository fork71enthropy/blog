QUIZ_DATA = {
    "post_id": 1,
    "passing_score": 4,
    "questions": [
        {
            "base_question_id": 1,
            "text": "What exactly does the db.sqlite3 file contain in a Django project?",
            "explanation": "It's the entire local database as a single binary file, including every table, row, and user account created during development, such as the superuser made with createsuperuser.",
            "choices": [
                ("The entire local database, including every table, row, and user account", True),
                ("Only the project's static files (CSS, JS, images)", False),
                ("A backup of the settings.py configuration", False),
                ("A log file of past database migrations only", False),
            ],
        },
        {
            "base_question_id": 2,
            "text": "Why didn't Django automatically prevent db.sqlite3 from being committed to GitHub?",
            "explanation": "Django doesn't manage Git configuration, that's the developer's responsibility. Git tracks everything by default unless explicitly told to ignore a file via .gitignore.",
            "choices": [
                ("Because Django doesn't manage Git configuration, that's the developer's responsibility", True),
                ("Because GitHub blocks database files automatically, so this shouldn't have happened", False),
                ("Because SQLite files are encrypted by default", False),
                ("Because .gitignore is created automatically by Django on project start", False),
            ],
        },
        {
            "base_question_id": 3,
            "text": "If db.sqlite3 was already committed before adding it to .gitignore, what's needed to actually stop tracking it?",
            "explanation": "Simply adding the file to .gitignore isn't enough once it's already tracked. You need to explicitly remove it from tracking with 'git rm --cached', then commit that change.",
            "choices": [
                ("Run git rm --cached db.sqlite3, then commit the change", True),
                ("Just add db.sqlite3 to .gitignore, Git handles the rest automatically", False),
                ("Delete the GitHub repository and create a new one", False),
                ("Rename the file so Git no longer recognizes it", False),
            ],
        },
        {
            "base_question_id": 4,
            "text": "Why is exposing the Django SECRET_KEY particularly dangerous?",
            "explanation": "The SECRET_KEY is used to sign cookies and sessions. If someone obtains it, they can forge valid authentication tokens and impersonate users.",
            "choices": [
                ("It's used to sign cookies and sessions, so it can be used to forge authentication tokens", True),
                ("It's used to encrypt the database file itself", False),
                ("It grants direct SSH access to the production server", False),
                ("It's required to run any Django management command", False),
            ],
        },
        {
            "base_question_id": 5,
            "text": "What's the recommended way to handle secrets like SECRET_KEY according to the article?",
            "explanation": "Store secrets in a local .env file (excluded via .gitignore), loaded via a library like python-decouple, and commit a .env.example with placeholder values instead.",
            "choices": [
                ("Store them in a local .env file loaded via python-decouple, and commit a .env.example with placeholders", True),
                ("Hardcode them directly in settings.py since it's simpler to manage", False),
                ("Store them in a public GitHub Gist for easy access", False),
                ("Email them to yourself as a backup", False),
            ],
        },
        {
            "base_question_id": 6,
            "text": "According to the article, what should you do before your very first commit on a new Django project?",
            "explanation": "Add a .gitignore covering db.sqlite3 and .env, move SECRET_KEY to an environment variable, and set DEBUG=False in production settings, security should be set up from the start, not added later.",
            "choices": [
                ("Add a .gitignore for db.sqlite3 and .env, move SECRET_KEY to an env variable, and set DEBUG=False in production", True),
                ("Deploy to production first, then worry about security once there are real users", False),
                ("Only add .gitignore rules once a security incident actually happens", False),
                ("Keep DEBUG=True in production for easier troubleshooting", False),
            ],
        },
    ],
}
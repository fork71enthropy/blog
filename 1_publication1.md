# I Committed My Database to GitHub — Here's What I Learned About Django Security

A few days ago, I pushed my Django blog project to GitHub. The repo was public. The code looked clean. I was proud of it.

Then someone pointed out that `db.sqlite3` was sitting right there in my repository, visible to anyone on the internet.

I didn't think much of it at first. It's just a local database, right? Wrong. Here's what I learned.

---

## What is db.sqlite3 exactly?

When you start a Django project and run `python manage.py migrate`, Django creates a `db.sqlite3` file in your root directory. This is your entire local database — a single binary file that contains every table, every row, every user account you created during development, including the superuser you created with `createsuperuser`.

That means if you commit it to a public GitHub repo, anyone can download it, open it with any SQLite viewer, and read your data directly — no password required.

```bash
# Anyone can do this with your file
sqlite3 db.sqlite3
.tables
SELECT * FROM auth_user;
```

Usernames, email addresses, hashed passwords — all exposed.

---

## Why didn't Django prevent this?

It didn't because Django doesn't manage your Git configuration. That's your responsibility. Django creates `db.sqlite3`, Git tracks everything by default, and if you never told Git to ignore it, it gets committed.

The fix is a single line in your `.gitignore`:

```
db.sqlite3
```

But there's a catch — if the file was already committed before you added it to `.gitignore`, Git will keep tracking it. You have to explicitly remove it from tracking:

```bash
git rm --cached db.sqlite3
echo "db.sqlite3" >> .gitignore
git commit -m "remove db.sqlite3 from tracking"
```

---

## What else should be in your .gitignore?

While I was fixing this, I realized `db.sqlite3` wasn't the only thing that shouldn't be in the repo. The Django `SECRET_KEY` in `settings.py` is equally critical — it's used to sign cookies and sessions. If someone gets it, they can forge authentication tokens.

The proper way to handle secrets is with a `.env` file and a library like `python-decouple`:

```bash
pip install python-decouple
```

```python
# settings.py
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

Your `.env` file stays local and goes in `.gitignore`. You commit a `.env.example` instead, with placeholder values, so other developers know what variables are needed without exposing the actual secrets.

```bash
# .env.example
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=your-database-url
```

---

## What I should have done from the start

Honestly, this should have been set up before the first commit. A proper Django `.gitignore` at project creation would have prevented all of this. GitHub actually offers a Django-specific `.gitignore` template when you create a new repository — use it.

The lesson isn't that I made a mistake. The lesson is that security isn't something you add later. It's something you set up at the beginning, even on a small personal project, precisely because habits built on personal projects carry over to production code.

---

## Takeaway

If you're starting a Django project right now, do these three things before your first commit:

1. Add a `.gitignore` with `db.sqlite3` and `.env`
2. Move your `SECRET_KEY` to an environment variable
3. Set `DEBUG=False` in your production settings

It takes five minutes. The alternative is explaining to users why their data was exposed.

---

*Still learning — this is exactly the kind of mistake I'm documenting so you don't have to make it.*
# Shaadi-style Matrimonial Website

Full-stack matrimonial site built from the existing pink, white, and navy HTML/CSS frontend. The original layout is preserved. Flask now serves the pages, stores members in a database, and makes registration, login, search, profiles, shortlists, and the contact form actually work.

This is an independent study project inspired by a matrimonial layout. It is not affiliated with Shaadi.com.

## What changed

The original ZIP was a static UI prototype (`shaadi_multipage/`). There was no backend, so Flask is a new addition rather than a replacement of an existing API.

Working features:

- Registration with validation, hashed passwords, and duplicate-email checks
- Full matrimonial bio-data: gotra, manglik, family background, father's and mother's name and occupation, number of brothers/sisters, occupation, work, age, family village, district, current address
- One profile photo per user (single URL; multiple values are rejected)
- Session login and logout
- Search against real database profiles (gender, age, religion, gotra, manglik, city, district, education)
- Community member cards and profile detail pages
- Edit Profile (owner only)
- Heart icon shortlists
- Interest / connection requests: send interest from a profile, review received requests, accept or decline, and see sent requests on the Connections page. Mutual interest connects automatically.
- Help/contact messages saved to the database
- Sample success stories stored as labeled sample content

## Project layout

```
app/                 Flask application, models, forms, routes
templates/           Jinja pages that reuse the original design
static/style.css     Original stylesheet plus small extras
instance/            Local SQLite database (created at runtime)
scripts/             Demo seed and reset helpers
tests/               Automated tests
shaadi_multipage/    Original static frontend (kept for reference)
```

## Windows setup

1. Install Python 3.11 or 3.12 from https://www.python.org/downloads/
   During setup, tick **Add python.exe to PATH**.

2. Open Command Prompt in this project folder.

```
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

3. Open `.env` in Notepad and set a long random `SECRET_KEY`.

4. Create tables and optional demo members:

```
flask --app wsgi.py init-db
flask --app wsgi.py seed-demo
```

The first app start also creates tables. If the database is empty it seeds 8 labeled fictional demo accounts.

5. Run the site:

```
flask --app wsgi.py run --host=127.0.0.1 --port=8000
```

6. Open http://127.0.0.1:8000 in your browser.

On macOS or Linux, activate with `source venv/bin/activate` and copy env with `cp .env.example .env`.

## Demo accounts (development only)

All eight demo accounts use the same development password:

`DemoPass123!`

| Name | Email |
| --- | --- |
| Priya Sharma | priya.sharma.demo@example.com |
| Rohit Verma | rohit.verma.demo@example.com |
| Sneha Patel | sneha.patel.demo@example.com |
| Amit Singh | amit.singh.demo@example.com |
| Ananya Gupta | ananya.gupta.demo@example.com |
| Kabir Khan | kabir.khan.demo@example.com |
| Meera Kapoor | meera.kapoor.demo@example.com |
| Arjun Mehta | arjun.mehta.demo@example.com |

Re-run seeding safely:

```
flask --app wsgi.py seed-demo
python scripts\seed_demo.py
```

Remove sample data:

```
flask --app wsgi.py reset-demo
python scripts\reset_demo.py
```

Do not enable these accounts or this password on a public production deployment.

## Tests

```
venv\Scripts\activate
pytest -q
```

Tests cover registration, duplicate emails, login, logout, profile edits, search filters, shortlists, protected pages, and database persistence.

## Database

Local default is SQLite at `instance/shaadi.db`.

Tables:

- `users` — email, password hash, demo flag
- `profiles` — public member details incl. gotra, manglik, family/parent and address fields (no email or password)
- `favourites` — shortlisted profiles, unique per pair
- `interests` — connection requests with pending/accepted/declined status
- `success_stories` — sample story cards
- `contact_messages` — Help form submissions
- `newsletter_subscribers` — footer subscribe form

PostgreSQL for production:

1. Create a database.
2. Set `DATABASE_URL` in `.env`:

```
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/shaadi
```

3. Restart the app. SQLAlchemy creates tables on first boot.

`postgres://` URLs are rewritten to `postgresql://` automatically.

On startup the app also runs a small auto-migration that adds any newly introduced `profiles` columns to an existing database without dropping data. For full schema history, add Alembic.

## Security notes

- Passwords are hashed with Werkzeug (PBKDF2).
- Forms use CSRF tokens.
- Queries use SQLAlchemy, not string-built SQL.
- Search results never include emails or password hashes.
- Login and registration are rate-limited.
- Session cookies are HTTP-only. Set `SESSION_COOKIE_SECURE=true` behind HTTPS.

## Features that need extra services

These are intentionally not faked:

- Email verification / OTP — needs an email provider
- Cloud photo uploads — paste an image URL on Edit Profile, or later add S3/Cloudinary
- Payments / premium plans — UI only
- Google login — needs OAuth credentials
- Newsletter sending — emails are stored only

## Public hosting

1. Set a strong `SECRET_KEY`.
2. Use PostgreSQL via `DATABASE_URL`.
3. Set `SESSION_COOKIE_SECURE=true`.
4. Do not seed demo accounts.
5. Run with gunicorn:

```
gunicorn --bind 0.0.0.0:8000 wsgi:app
```

Place a reverse proxy (nginx, Caddy, or your host's HTTPS router) in front of gunicorn.

Example hosts: Render, Railway, Fly.io, or a Linux VPS.

## Local URL

http://127.0.0.1:8000

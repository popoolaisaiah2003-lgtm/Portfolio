# KayDev Portfolio

A responsive Flask portfolio for Popoola Isaiah, built with an application factory, blueprints, reusable Jinja templates, Flask-WTF validation, and local Bootstrap and Font Awesome assets.

## Local setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m flask --app app run
```

Open `http://127.0.0.1:5000`.

## Contact email

The contact form sends messages to `popoolaisaiah2003@gmail.com` through Gmail SMTP. Google does not accept your normal account password for this connection.

1. Enable two-step verification on the Google account.
2. Create a Google App Password at `https://myaccount.google.com/apppasswords`.
3. Enter that 16-character App Password as `MAIL_PASSWORD` in `.env` locally and in the hosting provider's environment variables for production.

Never commit the populated `.env` file. Visitors' addresses are assigned to `Reply-To`, so replying to a delivered message addresses the visitor directly.

## Tests

```powershell
python -m unittest discover -s tests -v
```

## Production

Set `FLASK_ENV=production` and provide a long random `SECRET_KEY`, `MAIL_USERNAME`, and `MAIL_PASSWORD` through the deployment environment. The included `Procfile` starts the app with Gunicorn on Linux hosting platforms.

Project content is centralized in `portfolio/routes/project_data.py`. Add a new dictionary entry and a matching image under `static/images/` to create another project card and detail URL.
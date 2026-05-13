# Auth0 Login Flow

A simple Flask app that lets users log in with Auth0, view their profile, and log out. Built for MLH Global Hack Week.

## What it does

- Home page with a login button
- Auth0 handles the entire authentication flow
- Protected profile page shows your name, email and avatar
- Logout clears the session and redirects back home

## Setup

Clone the repo and install dependencies:

```bash
uv venv
source .venv/bin/activate
uv add flask python-dotenv authlib requests pyyaml
```

Copy the example env file and fill in your credentials:

```bash
cp .env.example .env
```

Your `.env` should look like this:

```
AUTH0_DOMAIN=your-domain.us.auth0.com
AUTH0_CLIENT_ID=your-client-id
AUTH0_CLIENT_SECRET=your-client-secret
SECRET_KEY=any-random-string
```

## Auth0 Setup

1. Go to [auth0.com](https://auth0.com) and create a **Regular Web Application**
2. Copy your Domain, Client ID and Client Secret into `.env`
3. In your Auth0 app settings, add these URLs:
   - Allowed Callback URLs: `http://localhost:3000/callback`
   - Allowed Logout URLs: `http://localhost:3000`
4. Save changes

## Run

```bash
python app.py
```

Open `http://localhost:3000` in your browser.

## Project Structure

```
auth0-login-flow/
├── app.py
├── configs/
│   └── config.yaml
├── templates/
│   ├── home.html
│   └── profile.html
├── .env.example
└── README.md
```

## Built by

[Muhammad Faizan](https://github.com/mhd-faizzan) during MLH Global Hack Week 2026.
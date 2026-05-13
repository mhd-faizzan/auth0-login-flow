import logging
import os
from functools import wraps

import yaml
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, session, url_for

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

with open("configs/config.yaml") as f:
    config = yaml.safe_load(f)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", config["app"]["secret_key"])
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  # fixes state mismatch on callback
app.config["SESSION_COOKIE_SECURE"] = False

oauth = OAuth(app)

auth0 = oauth.register(
    "auth0",
    client_id=os.getenv("AUTH0_CLIENT_ID"),
    client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f'https://{os.getenv("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)


def require_login(f: callable) -> callable:
    """
    Decorator that blocks access to a route if user is not logged in.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return decorated


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    # send user to Auth0 login page
    return auth0.authorize_redirect(
        redirect_uri=config["auth0"]["callback_url"]
    )


@app.route("/callback")
def callback():
    # Auth0 redirects here after login with a token
    token = auth0.authorize_access_token()
    session["user"] = token["userinfo"]
    logger.info("User logged in: %s", session["user"].get("email"))
    return redirect(url_for("profile"))


@app.route("/profile")
@require_login
def profile():
    return render_template("profile.html", user=session["user"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        f'https://{os.getenv("AUTH0_DOMAIN")}/v2/logout?returnTo={url_for("home", _external=True)}'
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=config["app"]["port"],
        debug=config["app"]["debug"]
    )
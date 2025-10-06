import os
import yaml
import streamlit_authenticator as stauth

def load_credentials(path="credentials.yaml"):
    with open(path, "r") as f:
        cfg = yaml.safe_load(f)
    return cfg.get("credentials", cfg)

def get_secret():
    # same logic you already have (env or docker secret file)
    s = os.environ.get("SECRET_KEY")
    if s:
        return s
    secret_file = os.environ.get("SECRET_KEY_FILE", "/run/secrets/secret_key")
    if os.path.exists(secret_file):
        with open(secret_file, "r") as f:
            return f.read().strip()
    raise RuntimeError("SECRET_KEY not set")

# pick a cookie name from env or default (must be stable across pages/instances)
COOKIE_NAME = os.environ.get("COOKIE_NAME", "my_app_cookie")

# Create a single Authenticate instance (reuse it application-wide)
_credentials = load_credentials(os.environ.get("CREDENTIALS_PATH", "credentials.yaml"))
_AUTH = stauth.Authenticate(_credentials, COOKIE_NAME, get_secret(), cookie_expiry_days=1)

def login_widget():
    """
    Call this on every Streamlit page/script.
    """
    return _AUTH.login(location="main")

def logout_widget(key):
    return _AUTH.logout(location="sidebar", key=key)




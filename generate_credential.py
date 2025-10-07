# generate_credentials.py
import yaml
import getpass
import os
import sys

# try importing streamlit_authenticator but be defensive about API differences
try:
    import streamlit_authenticator as stauth
except Exception as e:
    stauth = None

# fallback bcrypt if stauth not usable
try:
    import bcrypt
except Exception:
    bcrypt = None


def hash_passwords_with_stauth(passwords):
    """
    Try several ways to use streamlit_authenticator.Hasher depending on library version.
    Returns list of hashed password strings.
    """
    Hasher = getattr(stauth, "Hasher", None)
    if Hasher is None:
        raise RuntimeError("streamlit_authenticator.Hasher not found")

    # Try old-style: Hasher(list).generate()
    try:
        hashed = Hasher(passwords).generate()
        return hashed
    except TypeError:
        pass
    except Exception:
        # if it fails for some other reason, try other approaches
        pass

    # Try new-style: Hasher().generate(list)
    try:
        hashed = Hasher().generate(passwords)
        return hashed
    except Exception:
        pass

    # Try classmethod style: Hasher.generate(list)
    try:
        hashed = Hasher.generate(passwords)
        return hashed
    except Exception:
        pass

    raise RuntimeError("Could not generate hashes using streamlit_authenticator.Hasher (unknown API).")


def hash_passwords_with_bcrypt(passwords):
    """
    Produce bcrypt hashes using the bcrypt library as fallback.
    streamlit-authenticator's Hasher by default uses bcrypt-like hashes ($2b$...).
    """
    if bcrypt is None:
        raise RuntimeError("bcrypt is not available; install 'bcrypt' or 'streamlit-authenticator' properly.")
    out = []
    for pw in passwords:
        # bcrypt.gensalt rounds default is 12 which is fine
        h = bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt())
        out.append(h.decode("utf-8"))
    return out


def make_credentials(users):
    """
    users: dict of username -> display name
    Prompts for each user's plain password (hidden), returns config dict ready to dump to YAML.
    """
    passwords = []
    for u in users:
        pw = getpass.getpass(prompt=f"Password for {u}: ")
        if not pw:
            print("Empty password entered — aborting.")
            sys.exit(1)
        passwords.append(pw)

    hashed = None
    if stauth is not None:
        try:
            hashed = hash_passwords_with_stauth(passwords)
        except Exception as e:
            print(f"Warning: streamlit_authenticator Hasher failed: {e}")
            hashed = None

    if hashed is None:
        # fallback to bcrypt if installed
        try:
            hashed = hash_passwords_with_bcrypt(passwords)
            print("Hashed passwords using bcrypt fallback.")
        except Exception as e:
            raise RuntimeError("Could not hash passwords: install streamlit-authenticator or bcrypt.") from e

    credentials = {"usernames": {}}
    for (uname, display), h in zip(users.items(), hashed):
        credentials["usernames"][uname] = {"name": display, "password": h}
    return {"credentials": credentials}


if __name__ == "__main__":
    # EDIT HERE the usernames and display names you want
    users = {
        "giorgio": "Giorgio",
        # add more if needed: "bob": "Bob Example"
    }

    cfg = make_credentials(users)
    out_path = os.environ.get("CREDENTIALS_OUT", "credentials.yaml")
    with open(out_path, "w") as f:
        yaml.safe_dump(cfg, f, sort_keys=False)
    print(f"Wrote credentials to {out_path} (DO NOT COMMIT this file).")

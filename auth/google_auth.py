import os
from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

def verify_google_token(token):

    idinfo = id_token.verify_oauth2_token(
        token,
        requests.Request(),
        GOOGLE_CLIENT_ID
    )

    email = idinfo["email"]

    allowed_test_accounts = [
        "md.mahatabmahimn@gmail.com"
    ]

    if not (
        email.endswith("@burnside.school.nz")
        or email in allowed_test_accounts
    ):
        return None

    return {
        "google_id": idinfo["sub"],
        "email": email,
        "name": idinfo["name"]
    }
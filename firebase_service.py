import os
import json

import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

from dotenv import load_dotenv


load_dotenv()


def initialize_firebase():

    if firebase_admin._apps:
        return

    # -----------------------------------
    # OPTION 1: RENDER ENVIRONMENT
    # -----------------------------------

    credentials_json = os.getenv(
        "FIREBASE_CREDENTIALS_JSON"
    )

    if credentials_json:

        print(
            "Initializing Firebase using "
            "Render environment credentials..."
        )

        credentials_dict = json.loads(
            credentials_json
        )

        firebase_credentials = credentials.Certificate(
            credentials_dict
        )

        firebase_admin.initialize_app(
            firebase_credentials
        )

        return

    # -----------------------------------
    # OPTION 2: LOCAL DEVELOPMENT
    # -----------------------------------

    local_credentials_path = os.getenv(
        "FIREBASE_CREDENTIALS_PATH"
    )

    if local_credentials_path:

        print(
            "Initializing Firebase using "
            "local credentials file..."
        )

        firebase_credentials = credentials.Certificate(
            local_credentials_path
        )

        firebase_admin.initialize_app(
            firebase_credentials
        )

        return

    # -----------------------------------
    # NO CREDENTIALS FOUND
    # -----------------------------------

    raise RuntimeError(
        "Firebase credentials not found. "
        "Set FIREBASE_CREDENTIALS_JSON on Render "
        "or FIREBASE_CREDENTIALS_PATH locally."
    )


initialize_firebase()


db = firestore.client()


def verify_firebase_token(id_token):

    decoded_token = auth.verify_id_token(
        id_token
    )

    return decoded_token
import os

import firebase_admin
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from firebase_admin import auth, credentials
from rest_framework import authentication

from .exceptions import FirebaseError, InvalidAuthToken, NoAuthToken
import logging

logger = logging.getLogger(__name__)

firebase_config = {
    "type": "service_account",
    "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
    "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_CERT_URL"),
}

cred = credentials.Certificate(firebase_config)

default_app = firebase_admin.initialize_app(cred, {'databaseURL': os.environ.get("FIREBASE_DATABASE_URL")})

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            if request.method == "GET":
                return
            raise NoAuthToken("No auth token provided")

        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(str(id_token))
        except Exception:
            raise InvalidAuthToken("Invalid auth token")

        if not id_token or not decoded_token:
            return None

        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise FirebaseError()

        user, created = User.objects.get_or_create(username=uid)
        # user.profile.last_activity = timezone.localtime()

        return (user, None)
import json

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from oauth2client.service_account import ServiceAccountCredentials


def get_credentials(scopes=None):
    try:
        with open(settings.GOOGLE_SERVICE_ACCOUNT_JSON_PATH) as fh:
            json_data = json.load(fh)
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            json_data,
            scopes=scopes or '',
        )
    except Exception as exc:
        raise ImproperlyConfigured(
            'Google Service Account not correctly configured! Error: "{}"'
            .format(exc)
        )
    return credentials

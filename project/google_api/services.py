import httplib2

import googleapiclient.discovery

from . import auth


def get_fusiontable_service():
    credentials = auth.get_credentials(scopes=(
        'https://www.googleapis.com/auth/fusiontables',
    ))
    http = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build(
        'fusiontables',
        'v2',
        http=http,
        cache_discovery=False,
    )
    return service

from django.conf import settings
from social_core.backends.oauth import BaseOAuth2
from urllib.parse import urlencode


class MailcowOAuth2(BaseOAuth2):
    """GitHub OAuth authentication backend"""
    name = 'mailcow'
    AUTHORIZATION_URL = settings.MAILCOW_OAUTH_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = settings.MAILCOW_OAUTH_ACCESS_TOKEN_URL
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ','
    EXTRA_DATA = [
        ('expires_in', 'expires')
    ]
    REDIRECT_STATE = False
    ID_KEY = 'identifier'

    def get_user_details(self, response):
        return {'username': response.get('username'),
                'email': response.get('email'),
                'first_name': response.get('full_name')}

    def user_data(self, access_token, *args, **kwargs):
        url = settings.MAILCOW_OAUTH_PROFILE_URL + '?' + urlencode({
            'access_token': access_token
        })
        return self.get_json(url)

    def get_key_and_secret(self):
        return settings.MAILCOW_OAUTH_CLIENT_ID, settings.MAILCOW_OAUTH_CLIENT_SECRET

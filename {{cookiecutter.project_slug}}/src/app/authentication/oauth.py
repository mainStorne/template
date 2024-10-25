from httpx_oauth.oauth2 import BaseOAuth2

class Yandex(BaseOAuth2):
    def __init__(self, client_id: str, client_secret: str, authorize_endpoint: str, access_token_endpoint: str):
        super().__init__(client_id, client_secret, authorize_endpoint, access_token_endpoint, token_endpoint_auth_method="client_secret_basic", name='yandex')


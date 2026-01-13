from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

# Fix for "OAuth2Client.__init__() got multiple values for argument 'scope_delimiter'"
class CustomOAuth2Client(OAuth2Client):
    def __init__(self, request, consumer_key, consumer_secret, access_token_method, access_token_url, callback_url, scope=None, scope_delimiter=" ", headers=None, basic_auth=False):
        # We intercept the 'scope' argument (which dj-rest-auth sends but allauth doesn't want)
        # and we don't pass it to the super() method.
        super().__init__(
            request=request,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token_method=access_token_method,
            access_token_url=access_token_url,
            callback_url=callback_url,
            scope_delimiter=scope_delimiter,
            headers=headers,
            basic_auth=basic_auth
        )

FRONTEND_REDIRECT_URL = "https://room-chat-frontend-alpha.vercel.app/pages/login.html"

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = FRONTEND_REDIRECT_URL
    client_class = CustomOAuth2Client

class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = FRONTEND_REDIRECT_URL
    client_class = CustomOAuth2Client  
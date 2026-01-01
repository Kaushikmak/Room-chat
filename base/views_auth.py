from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    # Matches your "Authorised redirect URIs" in Google Console
    callback_url = "https://www.room-chat.com/login" 
    client_class = OAuth2Client

class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    # MUST match the "Authorization callback URL" in GitHub Developer Settings
    callback_url = "https://room-chat-api-eudf.onrender.com/accounts/github/login/callback/"
    client_class = OAuth2Client
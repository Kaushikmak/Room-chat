from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    # In production, you might need to specify callback_url here depending on your frontend setup
    # client_class = OAuth2Client 

class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    # GitHub often requires the callback_url to match exactly what is in your GitHub App settings
    # callback_url = "http://localhost:8000/api/auth/github/callback/" 
    # client_class = OAuth2Client
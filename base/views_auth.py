from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

# DEFINE THE EXACT FRONTEND URL HERE
# If testing locally, it might be "http://127.0.0.1:5500/frontend/pages/login.html"
# If on Vercel/Render, it is your actual domain + file path
# FRONTEND_REDIRECT_URL = "https://www.room-chat.com/pages/login.html" 
FRONTEND_REDIRECT_URL = "https://room-chat-frontend.vercel.app/pages/login.html"

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = FRONTEND_REDIRECT_URL 
    client_class = OAuth2Client

class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    # CHANGE THIS: Point to frontend, NOT backend
    callback_url = FRONTEND_REDIRECT_URL 
    client_class = OAuth2Client
from requests_oauthlib import OAuth2Session
import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

REDIRECT_URI = "http://localhost:8000/callback"
AUTHORIZATION_BASE_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"
SCOPE = ["read:user"]

oauth = OAuth2Session(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
)

authorization_url, state = oauth.authorization_url(AUTHORIZATION_BASE_URL)

print("Перейдите по ссылке для авторизации:")
print(authorization_url)

redirect_response = input("\nВставьте полный URL перенаправления: ")

token = oauth.fetch_token(
    TOKEN_URL,
    authorization_response=redirect_response,
    client_secret=CLIENT_SECRET
)

print("\nПолученный токен:")
print(token)

response = oauth.get("https://api.github.com/user")

print("\nДанные пользователя GitHub:")
print(response.json())

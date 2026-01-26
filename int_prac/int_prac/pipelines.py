from rest_framework_simplejwt.tokens import RefreshToken

def generate_jwt_for_user(strategy, details, user=None, *args, **kwargs):
    if user:
        refresh = RefreshToken.for_user(user)

        strategy.session["access_token"] = str(refresh.access_token)
        strategy.session["refresh_token"] = str(refresh)
from datetime import timedelta

from django.conf import settings
from django.core import signing
from django.utils import timezone
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView


OAUTH_STATE_SALT = "auth.oauth.state"


def get_cookie_settings():
    access_lifetime = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
    refresh_lifetime = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())
    cookie_domain = getattr(settings, "AUTH_COOKIE_DOMAIN", None)
    cookie_secure = getattr(settings, "AUTH_COOKIE_SECURE", not settings.DEBUG)
    cookie_samesite = getattr(settings, "AUTH_COOKIE_SAMESITE", "Lax")

    return {
        "access_max_age": access_lifetime,
        "refresh_max_age": refresh_lifetime,
        "domain": cookie_domain,
        "secure": cookie_secure,
        "samesite": cookie_samesite,
        "path": "/",
    }


def set_auth_cookies(response: Response, access_token: str, refresh_token: str):
    cookie_settings = get_cookie_settings()

    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=cookie_settings["access_max_age"],
        httponly=True,
        secure=cookie_settings["secure"],
        samesite=cookie_settings["samesite"],
        domain=cookie_settings["domain"],
        path=cookie_settings["path"],
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=cookie_settings["refresh_max_age"],
        httponly=True,
        secure=cookie_settings["secure"],
        samesite=cookie_settings["samesite"],
        domain=cookie_settings["domain"],
        path=cookie_settings["path"],
    )

    return response


def clear_auth_cookies(response: Response):
    cookie_settings = get_cookie_settings()
    response.delete_cookie(
        key="access_token",
        path=cookie_settings["path"],
        domain=cookie_settings["domain"],
        samesite=cookie_settings["samesite"],
    )
    response.delete_cookie(
        key="refresh_token",
        path=cookie_settings["path"],
        domain=cookie_settings["domain"],
        samesite=cookie_settings["samesite"],
    )
    return response


def auth_response(payload: dict, status_code: int = 200, access_token: str | None = None, refresh_token: str | None = None):
    response = Response(payload, status=status_code)
    if access_token and refresh_token:
        set_auth_cookies(response, access_token, refresh_token)
    return response


def build_oauth_state(flow: str, redirect_uri: str, account_type: str | None = None):
    payload = {
        "flow": flow,
        "redirect_uri": redirect_uri,
        "issued_at": timezone.now().timestamp(),
    }
    if account_type:
        payload["account_type"] = account_type
    return signing.dumps(payload, salt=OAUTH_STATE_SALT)


def verify_oauth_state(state: str, expected_flow: str, redirect_uri: str, max_age_seconds: int | None = None):
    if max_age_seconds is None:
        max_age_seconds = getattr(settings, "OAUTH_STATE_MAX_AGE_SECONDS", 600)
    try:
        payload = signing.loads(state, salt=OAUTH_STATE_SALT, max_age=max_age_seconds)
    except signing.SignatureExpired as exc:
        raise ValueError("Expired OAuth state") from exc
    except signing.BadSignature as exc:
        raise ValueError("Invalid OAuth state") from exc

    if payload.get("flow") != expected_flow:
        raise ValueError("Invalid OAuth state")
    if payload.get("redirect_uri") != redirect_uri:
        raise ValueError("OAuth redirect URI mismatch")

    return payload


class CookieTokenRefreshView(TokenRefreshView):
    """
    Refreshes the JWT pair using the refresh cookie and rotates cookies.
    """

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token") or request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=400)

        if hasattr(request.data, "_mutable"):
            request.data._mutable = True
            request.data["refresh"] = refresh_token
            request.data._mutable = False
        else:
            request._full_data = {"refresh": refresh_token}

        try:
            response = super().post(request, *args, **kwargs)
        except (TokenError, InvalidToken) as exc:
            return clear_auth_cookies(
                Response(
                    {"error": "Invalid or expired refresh token", "detail": str(exc)},
                    status=401,
                )
            )

        if response.status_code != 200:
            return response

        access_token = response.data.get("access")
        new_refresh_token = response.data.get("refresh", refresh_token)
        return auth_response(
            {
                "message": "Token refreshed successfully",
                "access": access_token,
                "refresh": new_refresh_token,
            },
            access_token=access_token,
            refresh_token=new_refresh_token,
        )

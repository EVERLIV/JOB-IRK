from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions


def enforce_csrf(request):
    check = CSRFCheck(lambda _: None)
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        raise exceptions.PermissionDenied(f"CSRF Failed: {reason}")


class CookieJWTAuthentication(JWTAuthentication):
    """
    JWT auth that falls back to the HttpOnly access_token cookie when the
    Authorization header is absent.
    """

    def authenticate(self, request):
        header = self.get_header(request)
        used_cookie = False
        if header is None:
            raw_token = request.COOKIES.get("access_token")
            used_cookie = raw_token is not None
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        if used_cookie and request.method not in ("GET", "HEAD", "OPTIONS", "TRACE"):
            enforce_csrf(request)

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token

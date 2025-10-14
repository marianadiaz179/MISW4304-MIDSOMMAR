import os


def validate_token(auth_header):
    # Validate token is present
    if not auth_header or not auth_header.startswith("Bearer "):
        return False, 403, "Authorization header is required"

    # Validate token is valid
    token = auth_header.split("Bearer ")[1]
    valid_token = os.getenv("SECRET_TOKEN")
    if token != valid_token:
        return False, 401, "Invalid token"

    return True, 200, None
from flask import request, Blueprint

from services.auth_service import validate_token
from services.blacklist_service import (
    add_email_to_blacklist,
    is_email_blacklisted,
)


blacklist_bp = Blueprint("blacklist", __name__)


# 1. Add an email to the blacklist
@blacklist_bp.route("/blacklists", methods=["POST"])
def create():
    data = request.get_json()
    auth_header = request.headers.get("Authorization")
    
    is_valid_token, status_code_token, message_token = validate_token(auth_header)
    if not is_valid_token:
        return {"msg": message_token}, status_code_token
    
    return add_email_to_blacklist(data)


# 2. Check if an email is blacklisted
@blacklist_bp.route("/blacklists/<string:email>", methods=["GET"])
def get(email):
    auth_header = request.headers.get("Authorization")
    
    is_valid_token, status_code_token, message_token = validate_token(auth_header)
    if not is_valid_token:
        return {"msg": message_token}, status_code_token
    return is_email_blacklisted(email)

# 3. Health check
@blacklist_bp.route("/blacklists/ping", methods=["GET"])
def ping():
    return "pong", 200
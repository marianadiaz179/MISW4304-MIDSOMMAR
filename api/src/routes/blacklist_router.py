from flask import request, Blueprint

from api.src.services.auth_service import validate_token
from ..services.blacklist_service import (
    add_email_to_blacklist,
)


blacklist_bp = Blueprint("blacklist", __name__)


# 1. Add an email to the blacklist
@blacklist_bp.route("/blacklist", methods=["POST"])
def create():
    data = request.get_json()
    auth_header = request.headers.get("Authorization")
    
    is_valid_token, status_code_token, message_token = validate_token(auth_header)
    if not is_valid_token:
        return {"msg": message_token}, status_code_token
    
    return add_email_to_blacklist(data)
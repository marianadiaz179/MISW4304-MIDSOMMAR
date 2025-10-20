import re
import uuid
from flask import request

from ..services.auth_service import validate_token
from ..models.models import Blacklist, db


# --------------------- Utils ---------------------

def validate_data(data):
    # Validate parameters are present
    required_params = ["email", "app_uuid"]
    for param in required_params:
        if param not in data:
            return False, 400, f"Missing parameter {param}"

    # Validate data types
    for param in required_params:
        if not isinstance(data[param], str):
            return False, 400, f"{param} must be a string."

    # Validate email
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, data["email"]):
        return False, 400, "email is not a valid email"

    # Validate app_uuid
    try:
        uuid.UUID(data["app_uuid"], version=4)
    except ValueError:
        return False, 400, "app_uuid is not a valid UUID"

    # If blocked_reason is present, validate it
    if "blocked_reason" in data:
        if not isinstance(data["blocked_reason"], str):
            return (
                False,
                400,
                "blocked_reason must be a string.",
            )
        if len(data["blocked_reason"]) > 255:
            return (
                False,
                400,
                "blocked_reason must have a maximum of 255 characters",
            )
    return True, 200, None

# --------------------- Services ---------------------
def add_email_to_blacklist(data):
    # Validate data
    is_data_valid, status_code_data, message_data = validate_data(data)
    if not is_data_valid:
        return {"msg": message_data}, status_code_data

    # Check if email is already blacklisted
    blacklisted = Blacklist.query.filter_by(email=data["email"]).first()
    if blacklisted:
        return {"msg": "Email is already in the blacklist"}, 409

    # Add email to blacklist
    blacklist = Blacklist(
        email=data["email"],
        app_uuid=data["app_uuid"],
        client_ip=request.remote_addr,
        blocked_reason=data.get("blocked_reason"),
    )
    db.session.add(blacklist)
    db.session.commit()

    # Return response
    return {"msg": "Email added to the blacklist"}, 201

def is_email_blacklisted(email):
    # Check if email is blacklisted
    blacklisted = Blacklist.query.filter_by(email=email).first()

    # Return response
    if not blacklisted:
        return {"blacklisted": False}, 200
    else:
        return {
            "blacklisted": True,
            "blocked_reason": blacklisted.blocked_reason or "No especificado",
        }, 200
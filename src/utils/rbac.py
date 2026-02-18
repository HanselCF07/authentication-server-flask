from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt
from src.models import user, role, role_permission


def check_permission_in_database(user_public_key, permission):
    verify_user = user.User.query.filter_by(user_public_key=user_public_key, user_status_id=1, record_status=1).first()
    if not verify_user:
        return False

    verify_role = role.Role.query.filter_by(role_id=verify_user.role_id, record_status=1).first()
    if not verify_role:
        return False

    record_role_permission = role_permission.RolePermission.query.filter_by(role_id=verify_role.role_id, record_status=1).all()
    if len(record_role_permission) > 0:
        for item in record_role_permission:
            if item.permission in permission:
                return True

    return False


# Decorator to check if the user has the required permission
def permission_required(permission):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            # Obtener el user_public_key del token JWT
            user_public_key = get_jwt().get("key") # Obtener el user_public_key del token JWT

            if not user_public_key: 
                return jsonify(msg="Access denied"), 403
            
            result = check_permission_in_database(user_public_key, permission)

            if not result:
                return jsonify(msg="Access denied"), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
from flask import Blueprint, jsonify
from flask.views import MethodView
from src.repository import protected_repository as ProtectedRepository

protected_bp = Blueprint("protected", __name__)

# Register the view with its prefix
protected_bp.add_url_rule( "/api/v1/vg-hc-store/authentication/protected/data", view_func=ProtectedRepository.Data.as_view("protectedData") )

protected_bp.add_url_rule( "/api/v1/vg-hc-store/authentication/protected/user-status", view_func=ProtectedRepository.UserStatus.as_view("protectedUserStatus") )
protected_bp.add_url_rule( "/api/v1/vg-hc-store/authentication/protected/roles", view_func=ProtectedRepository.Roles.as_view("protectedRoles") )
protected_bp.add_url_rule( "/api/v1/vg-hc-store/authentication/protected/role-permissions", view_func=ProtectedRepository.RolePermissions.as_view("protectedRolePermissions") )
protected_bp.add_url_rule( "/api/v1/vg-hc-store/authentication/protected/profiles", view_func=ProtectedRepository.Profiles.as_view("protectedProfiles") )

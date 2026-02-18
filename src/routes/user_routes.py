from flask import Blueprint
from flask.views import MethodView
from src.repository import user_repository as UserRepository

user_bp = Blueprint("user", __name__)

# Register the view with its prefix


#user_bp.add_url_rule( "/profile", view_func=UserRepository.Profile.as_view("profile") )
#user_bp.add_url_rule( "/default/viewer", view_func=UserRepository.DefaultViewer.as_view("defaultViewer") )

user_bp.add_url_rule( "/api/v1/vg-hc-store/authentication/user/sign-in-ct", view_func=UserRepository.SignInCustomer.as_view("userSignInCustomer") )
user_bp.add_url_rule( "/api/v1/vg-hc-store/authentication/user/login", view_func=UserRepository.Login.as_view("userLogin") )
user_bp.add_url_rule( "/api/v1/vg-hc-store/authentication/user/logout", view_func=UserRepository.Logout.as_view("userLogout") )


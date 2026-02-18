from flask import jsonify
from flask.views import MethodView
from src import db
from src.utils.rbac import permission_required
from src.utils.utilMethods import Methods as util
from src.utils.utilStrings import Messages
from src.models import profile, role, role_permission, user_status


class Data(MethodView):
    # Example of using the permissions decorator
    @permission_required( ["Full Access", "Basic Access", "Manager"] )
    def get(self):
        return jsonify({"msg": "Content protected from the repository"})

    # Example of using the permissions decorator
    @permission_required( ["Full Access", "Basic Access", "Manager"] )
    def post(self):
        return jsonify({"msg": "Content protected created"})
    
    @permission_required( ["Full Access", "Manager"] )
    def put(self):
        return jsonify({"msg": "Content protected updated"})

    # Example of using the permissions decorator
    @permission_required( ["Full Access"] )
    def delete(self):
        return jsonify({"msg": "Content protected deleted"})
    


class UserStatus(MethodView):
    @permission_required( ["Full Access", "Manager"] )
    def get(self):
        try:
            query = db.session.query(user_status.UserStatus)
            query = query.filter_by(record_status = 1)

            total = util.get_count(query)
            result = query.all()

            if len(result) > 0:
                schema = user_status.UserStatusSchema(many=True)
                json_data = schema.dump(result)
                return util.jsonResponseDefinitionTotal(json_data, Messages.SUCCESFUL_RESPONSE, 200, total)
            else:
                return util.generic_error_response(Messages.COULD_NOT_FIND+" User Status", 200)
        except Exception as e:
            #print(f"Error fetching user statuses: {e}")
            return util.generic_error_response("Server error", 500)
        finally:
            db.session.close()


class Roles(MethodView):
    @permission_required( ["Full Access", "Manager"] )
    def get(self):
        try:
            query = db.session.query(role.Role)
            query = query.filter_by(record_status = 1)

            total = util.get_count(query)
            result = query.all()

            if len(result) > 0:
                schema = role.RoleSchema(many=True)
                json_data = schema.dump(result)
                return util.jsonResponseDefinitionTotal(json_data, Messages.SUCCESFUL_RESPONSE, 200, total)
            else:
                return util.generic_error_response(Messages.COULD_NOT_FIND+" Role", 200)
        except Exception as e:
            #print(f"Error fetching roles: {e}")
            return util.generic_error_response("Server error", 500)
        finally:
            db.session.close()


class RolePermissions(MethodView):
    @permission_required( ["Full Access", "Manager"] )
    def get(self):
        try:
            query = db.session.query(role_permission.RolePermission)
            query = query.filter_by(record_status = 1)

            total = util.get_count(query)
            result = query.all()

            if len(result) > 0:
                schema = role_permission.RolePermissionSchema(many=True)
                json_data = schema.dump(result)
                return util.jsonResponseDefinitionTotal(json_data, Messages.SUCCESFUL_RESPONSE, 200, total)
            else:
                return util.generic_error_response(Messages.COULD_NOT_FIND+" Role Permission", 200)
        except Exception as e:
            #print(f"Error fetching role permissions: {e}")
            return util.generic_error_response("Server error", 500)
        finally:
            db.session.close()


class Profiles(MethodView):
    @permission_required( ["Full Access", "Manager"] )
    def get(self):
        try:
            query = db.session.query(profile.Profile)
            query = query.filter_by(record_status = 1)

            total = util.get_count(query)
            result = query.all()

            if len(result) > 0:
                schema = profile.ProfileSchema(many=True)
                json_data = schema.dump(result)
                return util.jsonResponseDefinitionTotal(json_data, Messages.SUCCESFUL_RESPONSE, 200, total)
            else:
                return util.generic_error_response(Messages.COULD_NOT_FIND+" Profile", 200)
        except Exception as e:
            #print(f"Error fetching profiles: {e}")
            return util.generic_error_response("Server error", 500)
        finally:
            db.session.close()




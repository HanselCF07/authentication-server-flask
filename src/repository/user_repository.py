from src import db, bcrypt
from flask import request, jsonify, make_response
from flask.views import MethodView
from flask_jwt_extended import create_access_token, get_jwt, set_access_cookies, unset_jwt_cookies
from marshmallow import Schema, fields, ValidationError
from src.models import user, customer, profile, role, user_status
import re, uuid


class SignInCustomer(MethodView):
    def post(self):
        try:
            try:
                data = user.UserCustomerCreateSchema().load(request.json)
            except ValidationError as err:
                return jsonify(errors=err.messages), 400

            # verify valid email with regex
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, data["email"]):
                return jsonify(msg="Invalid email format"), 400
            
            # Check if email is already registered
            validate_email = user.User.query.filter_by(email=data["email"]).first()
            if validate_email:
                return jsonify(msg="Email already registered"), 400
            
             # verify valid password with regex
            password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#@$!%*?&])[A-Za-z\d#@$!%*?&]{8,}$'
            if not re.match(password_regex, data["password"]):
                return jsonify(msg="Invalid password format"), 400

            # hash password (en producción, usar una librería como bcrypt)
            hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')

            # Create a new user instance
            new_user = user.User(
                username=data["email"],
                email=data["email"],
                password=hashed_password,  # En producción, asegúrate de hashear la contraseña
                user_status_id=1,  # Asignar un estado por defecto
                role_id=2,  # Asignar un rol por defecto (ej. cliente)
                profile_id=2  # Asignar un perfil por defecto o permitir nulo
            )

            # Save the new user to the database
            db.session.add(new_user)
            db.session.flush()

            # generate a unique public key for the user (ej. UUID o similar)
            generated_base_part_1 = uuid.uuid4().hex[:32] # Genera una parte base del UUID
            new_user.user_public_key = f"{generated_base_part_1}{new_user.user_id}"
            db.session.flush()

            # Create a new customer instance linked to the user
            new_customer = customer.Customer(
                user_id=new_user.user_id,
                name=data["name"],
                address=data["address"],
                phone=data["phone"],
                status=1  # Asignar un estado por defecto
            )
            db.session.add(new_customer)
            db.session.flush()
           
            # Commit all changes to the database
            db.session.commit()
            return jsonify({"message": "User registered successfully"}), 201
        except Exception as e:
            print(f"Error during user registration: {e}")
            db.session.rollback()
            return jsonify(msg="Server error"), 500
        finally:
            db.session.close()


class Login(MethodView):
    def post(self):
        try:
            data = request.get_json()

            # verify valid email with regex
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, data["username"]):
                return jsonify(msg="Invalid Username"), 400            

            user = validate_user(data["username"], data["password"])

            if not user:
                return jsonify(msg="Invalid credentials"), 401

            access_token = create_access_token(
                identity=user["user_public_key"],
                additional_claims={"key": user["user_public_key"]}
            )

            response = make_response(jsonify({"message": "Login successful"}), 200)
            
            # Se recomienda el esquema 'Bearer' por estándar
            response.headers["Authorization"] = f"Bearer {access_token}"

            # Guardar token en cookie
            # set_access_cookies(response, access_token)
            return response
        except Exception as e:
            return jsonify(msg="Server error", error=str(e)), 500


class Logout(MethodView):
    def post(self):
        response = make_response(jsonify({"message": "Logout successful"}), 200)

        # Eliminar token de cookies
        #unset_jwt_cookies(response)
        return response




def validate_user(username, password):
    try:
        # Aquí iría la consulta a BD para obtener el usuario por username
        verify_user = user.User.query.filter_by(username=username, record_status=1).first()

        if not verify_user:
            return None
        if bcrypt.check_password_hash(verify_user.password, password):
            return {"username": verify_user.username, "user_public_key": verify_user.user_public_key, "role": verify_user.role.name}

        return None
    except Exception as e:
        print(f"Error validating user: {e}")
        raise e



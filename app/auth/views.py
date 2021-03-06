import datetime
from flask import request, make_response, jsonify
from app.models import User
from flask.views import MethodView
from app import create_access_token


class UserRegistrationAPI(MethodView):
    """ Register users """

    def post(self):

        data = request.get_json()

        user = User.query.filter_by(email=data['email']).first()

        if not user:

            new_user = User(email=data['email'], admin=False, password=data['password'])
            new_user.save()

            response = jsonify({
                "status": "Success",
                "message": "User registered successfully."
            })

            response.status_code = 201

        else:
            response = jsonify({
                "message": "User already registered. Kindly Login"
            })

            response.status_code = 409

        return make_response(response)


class LoginAPI(MethodView):
    def post(self):

        try:

            data = request.get_json()
            user = User.query.filter_by(email=data['email']).first()

            # User exists and password matches database password
            if user and user.is_password_valid(data['password']):

                expires = datetime.timedelta(minutes=20)

                access_token = create_access_token(identity=user.id, expires_delta=expires)

                if access_token:
                    response = jsonify({
                        "message": "User has logged in!",
                        "access_token": access_token
                    })

                    response.status_code = 200
                    return make_response(response)

            else:
                response = jsonify({
                    "message": "Invalid email or password, Please try again"
                })

                response.status_code = 401

                return make_response(response)

        except Exception as e:
            response = jsonify({
                "message": str(e)
            })

            return make_response(response), 500



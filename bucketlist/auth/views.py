from flask import request, make_response, url_for, jsonify
from bucketlist.models import User
from flask.views import MethodView
from bucketlist import create_access_token

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

            response.status_code = 202

        return make_response(response)



    def get(self, id=None):
        if id:
            user = User.query.filter_by(id=id).first()

            if user:

                response = jsonify({
                    "email": user.email,
                    "admin": user.admin
                })

                response.status_code = 200
            else:

                response = jsonify({
                    "status": "Fail",
                    "message": "User does not exist"
                })

                response.status_code = 404

            return make_response(response)

        else:

            users = User.get_all()
            user_results = []

            for user in users:
                user_obj = {
                    "email": user.email,
                    "admin": user.admin
                }
                user_results.append(user_obj)

            response = jsonify({"users": user_results})

            return make_response(response), 200

    def put(self, id=None):
        if id:
            user = User.query.filter_by(id=id).first()
            data = request.get_json()

            if user:

                response = jsonify({
                    "email": data['email'],
                    "admin": data['admin']
                })

                response.status_code = 200

            else:
                response = jsonify({
                    "status": "Fail",
                    "message": "Cannot update non-existing user"
                })

                response.status_code = 404

        return make_response(response)

class LoginAPI(MethodView):
    def post(self):

        try:

            data = request.get_json()
            user = User.query.filter_by(email=data['email']).first()

            # User exists and password matches database password
            if user and user.is_password_valid(data['password']):

                access_token = create_access_token(identity=user.id)

                if access_token:
                    response = jsonify({
                        "message": "User has logged in!",
                        "access_token": access_token
                    })

                    response.status_code = 200
                    return make_response(response)
                else:
                    return make_response(jsonify({"message":"No identity"}))

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


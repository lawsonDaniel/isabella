from flask_restful import Resource
from flask import request
from services.user_service import UserService

class LoginController(Resource):
    def __init__(self, app):
        self.app = app
        self.user_service = UserService(app)  # Pass app to UserService

    def post(self):
        data = request.get_json()  # Use get_json() to parse the JSON request
        print(data)  # Consider removing this in production for security
        return self.user_service.login(data)  # Call the login method

    
class registerController(Resource):
    def __init__(self, app):
        self.app = app
        self.user_service = UserService(app)  # Pass app to UserService
    def post(self):
        data = request.get_json()
        if data['password'] != data['confirm_password']:
            return {
                'message': 'Password must match',
                'sucess':False
            }, 400
        if len(data['password']) < 6:
            return {
                'message': 'Password must be at least 6 characters',
                'sucess':False
            }, 400
        return self.user_service.register(data)
    
    from flask_restful import Resource


class GoogleAuthController(Resource):
    def __init__(self, app):
        self.app = app
        self.user_service = UserService(app)  # Pass app to UserService

    def get(self):
        """Initiates Google OAuth login process."""
        return self.user_service.google_login()

class GoogleAuthCallbackController(Resource):
    def __init__(self, app):
        self.app = app
        self.user_service = UserService(app)  # Pass app to UserService

    def get(self):
        """Handles the OAuth callback from Google after login."""
        return self.user_service.google_authorize()


class PasswordResetController(Resource):
    def __init__(self, app):
        self.app = app
        self.user_service = UserService(app)

    def post(self):
        data = request.get_json()
        return self.user_service.request_password_reset(data)

class VerifyOtpController(Resource):
    def __init__(self, app):
        self.app = app
        self.user_service = UserService(app)

    def post(self):
        data = request.get_json()
        return self.user_service.verify_otp(data)


        
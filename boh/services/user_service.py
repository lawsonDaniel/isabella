import os
import random
from models.link_model import Link
from models.user_model import User
from db_config import db
from schema.schema import UserSchema
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import  create_access_token
from sib_api_v3_sdk import  Configuration, ApiClient, TransactionalEmailsApi, SendSmtpEmail
from pprint import pprint
from flask import url_for
from authlib.integrations.flask_client import OAuth
import datetime
from sqlalchemy import case, desc, func, or_
from utils.upload import upload_image_to_cloudinary
from datetime import datetime, timedelta

user_schema = UserSchema()


class UserService:
    def __init__(self, app):
        self.app = app
        self.app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        
        self.app.config['MAIL_SENDER'] = os.getenv('MAIL_SENDER')
        self.app.config['MAIL_SENDER'] = os.getenv('MAIL_SENDER')
        self.app.config['API_KEY']= os.getenv('API_KEY')
        self.app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID')
        self.app.config['GOOGLE_CLIENT_SECRET'] = os.getenv('GOOGLE_CLIENT_SECRET')
        self.app.config['GOOGLE_DISCOVERY_URL'] = "https://accounts.google.com/.well-known/openid-configuration"
        self.app.config['GOOGLE_REDIRECT_URI'] = os.getenv('GOOGLE_REDIRECT_URI')
        
        self.oauth = OAuth(self.app)
        self.google = self.oauth.register(
            name='google',
            client_id=self.app.config['GOOGLE_CLIENT_ID'],
            client_secret=self.app.config['GOOGLE_CLIENT_SECRET'],
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            authorize_params=None,
            access_token_url='https://oauth2.googleapis.com/token',
            access_token_params=None,
            refresh_token_url=None,
            redirect_uri=self.app.config['GOOGLE_REDIRECT_URI'],
            client_kwargs={'scope': 'openid email profile'}
        )

        
    def register(self, data):  # Changed to an instance method
        # Validate and deserialize input data
        try:
            # Check if the user already exists
            if User.query.filter_by(email=data['email']).first():
                return {
                    "message": "User with email already exists",
                    "success": False
                }, 400
            
            # Prepare user data
            data.pop('confirm_password', None)  # Remove 'confirm_password' if it exists
            data['password'] = generate_password_hash(data['password'])
            data['otp'] = str(random.randint(100000, 999999))
            
            # Load user data
            user = user_schema.load(data)

            # Add the new user to the database
            db.session.add(user)
            db.session.commit()
            self.send_email(data['email'], data['first_name'],data['otp'])
            # Remove sensitive information from response data
            response_data = {key: value for key, value in data.items() if key not in ['otp', 'password']}
            return {
                'message': 'User Registered Successfully',
                'data': response_data,
                'success': True
            }, 201

        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            return {
                "message": "Invalid input",
                "errors": str(e),
                "success": False
            }, 400

    def login(self, data):
        try:
            user = User.query.filter_by(email=data['email']).first()
            if not user or not check_password_hash(user.password, data['password']):
                return {
                    "message": "Invalid username or password",
                    "success": False
                }, 401
            
            expires = timedelta(weeks=1)  # Use timedelta directly

            # Generate JWT token
            token = create_access_token(identity={'user_id': user.id}, expires_delta=expires)
            
            # Remove unnecessary fields
            userData = user_schema.dump(user)
            del userData["password"]
            del userData["otp"]
            del userData["otp_expires_at"]

            return {
                'message': 'Login successful',
                'success': True,
                'data': userData,
                'token': token
            }, 200
            
        except Exception as e:
            return {
                "message": "Invalid input",
                "errors": str(e),
                "success": False
            }, 400
            
    def request_password_reset(self, data):
        email = data.get('email')
        user = User.query.filter_by(email=email).first()
        if not user:
            return {"message": "User with this email does not exist.", "success": False}, 404

        otp = str(random.randint(100000, 999999))
        user.otp = otp
        user.otp_expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        db.session.commit()

        self.send_email(user.email, user.first_name, otp)
        return {"message": "OTP has been sent to your email.", "success": True}, 200    
    
        # OTP Verification
    def verify_otp(self, data):
        email = data.get('email')
        otp = data.get('otp')
        user = User.query.filter_by(email=email).first()
        if not user:
            return {"message": "User with this email does not exist.", "success": False}, 404

        if user.otp != otp or user.otp_expiration < datetime.datetime.utcnow():
            return {"message": "Invalid or expired OTP.", "success": False}, 400

        return {"message": "OTP verified successfully.", "success": True}, 200
    
    
        # Reset Password
    from sqlalchemy import func, desc, or_

    
    def leaderboard(self, page, per_page, search, current_user_id, start_date=None, end_date=None):
        try:
            # Parse date strings if provided
            if start_date:
               # Convert the ISO 8601 date string to a datetime object
                start_date = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
            if end_date:
                # Convert the ISO 8601 date string to a datetime object
                end_date = datetime.fromisoformat(end_date.replace("Z", "+00:00"))

            # Base query to aggregate links count and sub count for each user
            query = (
                db.session.query(
                    User,
                    func.coalesce(
                        func.count(case((Link.video_id.isnot(None), 1))), 0
                    ).label('links_count'),  # Count links with video_id
                    func.coalesce(
                        func.count(case((Link.video_id.is_(None), 1))), 0
                    ).label('sub_count')  # Count links without video_id
                )
                .join(Link, User.id == Link.user_id)  # Only include users with links
                .group_by(User.id)  # Group by User to calculate counts
            )

            # Apply filter for links' created_at date range if provided
            if start_date and end_date:
                query = query.filter(Link.created_at.between(start_date, end_date))
            elif start_date:
                query = query.filter(Link.created_at >= start_date)
            elif end_date:
                query = query.filter(Link.created_at <= end_date)

            # Apply search filter if a search term is provided
            if search:
                search_filter = or_(
                    User.first_name.ilike(f'%{search}%'),
                    User.last_name.ilike(f'%{search}%')
                )
                query = query.filter(search_filter)

            # Order users by links count in descending order
            query = query.order_by(func.coalesce(func.count(case((Link.video_id.isnot(None), 1))), 0).desc())

            # Paginate the results
            top_users = query.offset((page - 1) * per_page).limit(per_page).all()

            # Fetch the logged-in user's rank and link/sub counts
            user_rank_query = (
                db.session.query(
                    User.id,
                    func.rank().over(
                        order_by=func.coalesce(
                            func.count(case((Link.video_id.isnot(None), 1))), 0
                        ).desc()
                    ).label('rank'),  # Rank based on links count
                    func.coalesce(
                        func.count(case((Link.video_id.isnot(None), 1))), 0
                    ).label('links_count'),
                    func.coalesce(
                        func.count(case((Link.video_id.is_(None), 1))), 0
                    ).label('sub_count')
                )
                .join(Link, User.id == Link.user_id)  # Only include users with links
                .group_by(User.id)
            )

            # Apply the same date range filter to rank query
            if start_date and end_date:
                user_rank_query = user_rank_query.filter(Link.created_at.between(start_date, end_date))
            elif start_date:
                user_rank_query = user_rank_query.filter(Link.created_at >= start_date)
            elif end_date:
                user_rank_query = user_rank_query.filter(Link.created_at <= end_date)

            # Get the rank and other details for the logged-in user
            logged_in_user_data = user_rank_query.filter(User.id == current_user_id).first()

            # If the logged-in user exists in the leaderboard
            if logged_in_user_data:
                logged_in_user = db.session.query(User).filter_by(id=current_user_id).first()
                user_rank = logged_in_user_data.rank
                logged_in_user_info = {
                    "id": logged_in_user.id,
                    "first_name": logged_in_user.first_name,
                    "last_name": logged_in_user.last_name,
                    "email": logged_in_user.email,
                    "links_count": logged_in_user_data.links_count,
                    "sub_count": logged_in_user_data.sub_count,
                    "rank": user_rank
                }
            else:
                logged_in_user_info = None

            # Serialize the top users
            users_data = []
            for user, links_count, sub_count in top_users:
                users_data.append({
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "links_count": links_count,
                    "sub_count": sub_count
                })

            # Avoid appending the logged-in user if they are already in the leaderboard
            if logged_in_user_info and logged_in_user_info["id"] not in [user["id"] for user in users_data]:
                users_data.append(logged_in_user_info)

            return {
                "message": "Leaderboard retrieved successfully",
                "success": True,
                "data": users_data,
            }, 200

        except Exception as e:
            return {
                "message": "An Error occurred while retrieving leaderboard",
                "success": False,
                "error": str(e)
            }, 500


    def reset_password(self, data):
        email = data.get('email')
        new_password = data.get('new_password')
        user = User.query.filter_by(email=email).first()
        if not user:
            return {"message": "User with this email does not exist.", "success": False}, 404

        user.password = generate_password_hash(new_password)
        user.otp = None
        user.otp_expiration = None
        db.session.commit()

        return {"message": "Password has been reset successfully.", "success": True}, 200
        

    def send_email(self, mail, name,otp):
        configuration = Configuration()
        configuration.api_key['api-key'] =  self.app.config['API_KEY']

        # Create an instance of the API client
        api_client = ApiClient(configuration)
        api_instance = TransactionalEmailsApi(api_client)

        # Define the email parameters
        send_email = SendSmtpEmail(
            sender={"name": "lawblaze", "email": "lawblaze4@gmail.com"},
            to=[{"email": mail, "name": name}],  # Replace with the recipient's email and name
            subject="My subject",
            html_content=f'<p>Congratulations! your otp {otp}.</p>'
        )

        # Make the call to send the transactional email
        try:
            api_response = api_instance.send_transac_email(send_email)
            pprint(api_response)
        except Exception as e:
            print("Exception when calling TransactionalEmailsApi->send_transac_email: %s\n" % e)
            
    def google_login(self):
        """Redirect to Google's OAuth login page."""
        return self.google.authorize_redirect(url_for('googleauthcallbackcontroller', _external=True))

    def google_authorize(self):
        """Handle Google's OAuth callback and authenticate the user."""
        token = self.google.authorize_access_token()  # Fetch the access token
        user_info = self.google.parse_id_token(token)

        # Check if the user already exists
        user = User.query.filter_by(email=user_info['email']).first()
        if user:
            expires = datetime.timedelta(weeks=1)
              # Generate JWT token
            token= create_access_token(identity={'user_id': user.id}, expires_delta=expires)
            return { 
                'message': 'Login successful',
                'success': True,
                'token': token
            }, 200

        else:
            # If the user doesn't exist, register them
            data = {
                'email': user_info['email'],
                'first_name': user_info['given_name'],
                'last_name': user_info['family_name'],
                'password': generate_password_hash(str(random.randint(100000, 999999))),  # Create a random password
                'otp': str(random.randint(100000, 999999))
            }
            
            # Load user data
            user = user_schema.load(data)
            db.session.add(user)
            db.session.commit()

            self.send_email(data['email'], data['first_name'], data['otp'])
            
            # Generate JWT token for new user
            token = jwt.encode({'user_id': user.id}, self.app.config['SECRET_KEY'], algorithm='HS256')
            
            return {
                'message': 'User registered and logged in via Google',
                'token': token,
                'success': True
            }, 200
    def get_auth_user(id):
            try:
                user = User.query.filter_by(id=id).first()
                if not user:
                    return {
                        "message": "User not found",
                        "success": False,
                    }, 404
                user_data = user_schema.dump(user)
                del user_data["password"]
                del user_data["otp"]
                del user_data["otp_expires_at"]
                del user_data["email_verified"]
                return {
                    "message":"User found",
                    "success": True,
                    "data": user_data
                }
            except Exception as e:
                return {
                    "message": "An Error occurred while updating",
                    "success": False,
                    "error": str(e)  # Convert the exception to a string
                }, 500
    def update_user(id,data):
            try:
                user = User.query.filter_by(id=id).first()
                if not user:
                    return {
                        "message": "User not found",
                        "success": False,
                    }, 404

                # Update first_name and last_name if provided
                if 'first_name' in data and data['first_name']:
                    user.first_name = data['first_name']
                if 'last_name' in data and data['last_name']:
                    user.last_name = data['last_name']

                # Handle image upload if provided
                if 'image' in data and data['image']:
                    result = upload_image_to_cloudinary(data['image'], public_id=f"user_{id}")
                    if not result['success']:
                        return {"message": "Image upload failed", "success": False}, 500
                    user.image = result['url']

                # Commit the changes to the database
                db.session.commit()
                
                # Serialize the user object
                user_data = user_schema.dump(user)
                del user_data["password"]
                del user_data["otp"]
                del user_data["otp_expires_at"]
                del user_data["email_verified"]
                return {
                    "message": "User updated successfully",
                    "success": True,
                    "data": user_data  # Return the serialized user data
                }, 200  # Use 200 for successful updates

            except Exception as e:
                return {
                    "message": "An Error occurred while updating",
                    "success": False,
                    "error": str(e)  # Convert the exception to a string
                }, 500
    def make_admin(data):
        # Ensure data is valid
        if not data or 'email' not in data:
            return {"message": "Invalid data provided.", "success": False}, 400

        email = data.get('email').strip() # Ensure email is normalized
        user = User.query.filter_by(email=email).first()

        if not user:
            return {"message": "User with this email does not exist.", "success": False}, 404

        try:
            user.userType = "Admin"  # Ensure "Admin" is a valid userType in your model
            db.session.commit()
            return {"message": "Admin Created Successfully", "success": True}, 200
        except Exception as e:
            db.session.rollback()  # Rollback in case of failure
            return {"message": f"An error occurred: {str(e)}", "success": False}, 500

from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.subscription_service import SubscriptionService

class SubscriptionLinkController(Resource):
  
   def get(self,user_id):
        user_ip = request.remote_addr
        # Call the function here correctly
        return SubscriptionService.subscribe_to_youtube(user_id, user_ip)

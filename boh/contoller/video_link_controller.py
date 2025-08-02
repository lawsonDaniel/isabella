from flask import request
from flask_restful import Resource
from services.video_service import VideoService
from flask_jwt_extended import jwt_required, get_jwt_identity

class VideoLinkController(Resource):
    def __init__(self, app):
        self.app = app
        self.video_service = VideoService()  # Pass app to VideoService

    
    def get(self, video_ref,user_id):
        user_ip = request.remote_addr 
        return VideoService.get_video_by_ref(video_ref,user_ip,user_id)
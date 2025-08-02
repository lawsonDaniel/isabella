from flask_restful import Resource
from services.video_service import VideoService
from flask import request

class AllVideoController(Resource):
    def __init__(self, app):
        self.app = app
        self.video_service = VideoService()  # Pass app to VideoService

    def get(self):
         page = request.args.get('page', 1, type=int)  # Default page is 1
         per_page = request.args.get('per_page', 10, type=int)  # Default items per page is 10
         search = request.args.get('search', '', type=str) 
         category = request.args.get('category', type=str)
         return VideoService.get_all_videos(page, per_page,search, category)
from flask_restful import Resource
from flask import request
from services.video_service import VideoService
from utils.upload import upload_image_to_cloudinary


class VideoController(Resource):
    def __init__(self, app):
        self.app = app
        self.video_service = VideoService()  # Pass app to VideoService

    def get(self):
        video_url = request.args.get('url')  # Use request.args to get query parameters

        if not video_url:
            return {
                'message': 'Video URL is required',
                'success': False
            }, 400

        # Fetch video data using VideoService
        video_data = self.video_service.fetch_video_data(video_url)

        return video_data  # Return the fetched video data
    def post(self):
        data = request.json
        full_url = request.url
        base_url = "/".join(full_url.split("/")[:3])
        print('url',base_url)
        errors = []

        if not data.get('title'):
            errors.append("The video title is missing.")
        if not data.get('link'):
            errors.append("The video link is missing.")
        if not data.get('summary'):
            errors.append("The video description is missing.")
        if not data.get('image'):
            errors.append("The video image is missing.")

        if errors:
            return {
                "message": "Validation failed.",
                "errors": errors,
                "success":False
            },400
        return self.video_service.upload_Video(data,base_url)
            
        
        
        
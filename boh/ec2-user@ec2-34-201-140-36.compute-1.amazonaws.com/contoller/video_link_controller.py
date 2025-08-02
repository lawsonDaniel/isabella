from flask_restful import Resource
from services.video_service import VideoService

class VideoLinkController(Resource):
    def __init__(self, app):
        self.app = app
        self.video_service = VideoService()  # Pass app to VideoService

    def get(self, video_ref):
        return VideoService.get_video_by_ref(video_ref)
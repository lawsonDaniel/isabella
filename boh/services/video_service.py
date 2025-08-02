import os
from db_config import db
from models.link_model import Link
from models.user_model import User
from schema.schema import UserSchema, VideoSchema, LinkSchema
from flask import current_app, redirect
from urllib.parse import urlparse, parse_qs
import requests
from utils.upload import upload_image_to_cloudinary
import string
import random
from models.video_model import Video
from datetime import datetime, timedelta
from sqlalchemy import func

user_schema = UserSchema()
video_schema = VideoSchema()
link_schema = LinkSchema()
class VideoService:
    @staticmethod
    def fetch_video_data(url):
        """
        Fetch video title and summary based on the provided URL.
        """
        platform = VideoService.identify_platform(url)

        if platform == 'youtube':
            return VideoService.fetch_youtube_data(url)
        elif platform == 'facebook':
            return VideoService.fetch_facebook_data(url)
        elif platform == 'instagram':
            return VideoService.fetch_instagram_data(url)
        else:
            return {'message': 'Unsupported platform'}, 400

    @staticmethod
    def identify_platform(url):
        print("url getting here",url)
        """
        Identify the platform (YouTube, Facebook, Instagram) based on the URL.
        """
        if 'youtube.com' in url or 'youtu.be' in url:
            return 'youtube'
        elif 'facebook.com' in url:
            return 'facebook'
        elif 'instagram.com' in url:
            return 'instagram'
        return None

    @staticmethod
    def fetch_youtube_data(url):
        """
        Fetch video data from YouTube using the YouTube Data API.
        """
        video_id = VideoService.extract_youtube_id(url)
        api_key = current_app.config['YOUTUBE_API_KEY']
        api_url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}'

        response = requests.get(api_url)
        data = response.json()

        if 'items' in data and data['items']:
            snippet = data['items'][0]['snippet']
            print("snippet",snippet)
            return {
               'message':'vide details found',
               'data': snippet,
               'success':True
            },200
        return {'message': 'Video not found'}, 404


    @staticmethod
    def extract_youtube_id(url):
        """
        Extracts the video ID from a YouTube URL, including standard and live stream URLs.
        """
        parsed_url = urlparse(url)
        if parsed_url.hostname == 'youtu.be':
            return parsed_url.path[1:]
        elif parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
            if parsed_url.path == '/watch' or '/live/':
                return parse_qs(parsed_url.query).get('v', [None])[0]
            elif '/live/' in parsed_url.path:
                # Extract the video ID from a live stream URL
                return parsed_url.path.split('/')[-1]
        return None

    
    @staticmethod
    def fetch_facebook_data(url):
        """
        Fetch video data from Facebook using the Facebook Graph API.
        """
        access_token = current_app.config.get('FACEBOOK_ACCESS_TOKEN')
        video_id = VideoService.extract_facebook_id(url)
        
        if not video_id or not access_token:
            return {'message': 'Invalid URL or missing access token'}, 400
        
        api_url = f'https://graph.facebook.com/v12.0/{video_id}?fields=title,description&access_token={access_token}'
        
        try:
            response = requests.get(api_url)
            data = response.json()
            # Log response for debugging
            print("Facebook API Response:", data)

            if 'title' in data and 'description' in data:
                return {
                    'title': data['title'],
                    'summary': data['description']
                }
            else:
                return {'message': 'Video not found or access restricted'}, 404
        except Exception as e:
            return {'message': f'Error fetching data from Facebook: {str(e)}'}, 500
        
    
    @staticmethod
    def extract_facebook_id(url):
        """
        Extracts the video ID from a Facebook URL.
        """
        parsed_url = urlparse(url)
        if 'facebook.com' in parsed_url.hostname and '/videos/' in parsed_url.path:
            return parsed_url.path.split('/videos/')[1].split('/')[0]
        return None


    @staticmethod
    def fetch_instagram_data(url):
        """
        Fetch video data from Instagram using the Instagram Graph API.
        """
        access_token = current_app.config.get('INSTAGRAM_ACCESS_TOKEN')
        media_id = VideoService.extract_instagram_id(url)
        
        if not media_id or not access_token:
            return {'message': 'Invalid URL or missing access token'}, 400
        
        api_url = f'https://graph.instagram.com/{media_id}?fields=caption,media_type,media_url&access_token={access_token}'
        
        try:
            response = requests.get(api_url)
            data = response.json()
            # Log response for debugging
            print("Instagram API Response:", data)
            
            if 'caption' in data and data[ 'media_type'] == 'VIDEO':
                return {
                    'title': 'Instagram Video',
                    'summary': data['caption']
                }
            else:
                return {'message': 'Video not found or not a video type'}, 404
        except Exception as e:
            return {'message': f'Error fetching data from Instagram: {str(e)}'}, 500
    
    @staticmethod
    def extract_instagram_id(url):
        """
        Extracts the media ID from an Instagram URL.
        """
        parsed_url = urlparse(url)
        if 'instagram.com' in parsed_url.hostname:
            return parsed_url.path.split('/')[-1]
        return None
    def generate_alphanumeric(self, length):
        # Create a pool of alphanumeric characters (letters and digits)
        characters = string.ascii_letters + string.digits
        # Generate a random string of the specified length
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string
    def upload_Video(self, data,base_url):
        try:
            # Upload thumbnail to Cloudinary server
            data['ref'] = self.generate_alphanumeric(10)
            video_thumbnail = upload_image_to_cloudinary(data['image'], data['ref'])
            print('vide url11', video_thumbnail['success'], video_thumbnail['url'])

            # Check if upload was successful
            if not video_thumbnail['success'] or not video_thumbnail['url']:
                return {
                    "message": "An error occurred while uploading thumbnail to Cloudinary server",
                    "success": False,
                }, 400  # Return a bad request status
            
           
            print('base url',base_url)
            data['image'] = video_thumbnail['url']
            
            print('reaching here111',data['image'])
            
            data['platform'] = self.identify_platform(data['link'])
            print('platform info',data['platform'])
            # Load video schema
            video = video_schema.load(data)

            # Add video to the database session and commit
            db.session.add(video)
            db.session.commit()

            return {
                "message": "Video successfully uploaded",
                "success": True,
            }, 201  # Created status

        except Exception as e:
            print("errror", e)
            # Return the error message as a string for JSON serialization
            return {
                "message": "An error occurred while uploading video",
                "success": False,
                "error": str(e)  # Convert the exception to a string
            }, 500  # Internal server error status
    def update_video(self, id, data):
        try:
            # Find the video by id
            video = Video.query.filter_by(id=id).first()  # Assuming 'id' is your identifier
            if not video:
                return {
                    "message": "Video not found",
                    "success": False,
                }, 404  # 404 for not found

            # Debugging: Print incoming data to check what is being sent
            print(f"Incoming data: {data}")

            # Update the video instance with only the provided fields
            for key, value in data.items():
                if hasattr(video, key):  # Ensure the field exists on the model
                    setattr(video, key, value)

            # Commit the changes to the database
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return {
                    "message": f"Error committing changes: {str(e)}",
                    "success": False,
                }, 500  # Internal server error

            return {
                "message": "Video successfully updated",
                "success": True,
            }, 200  # OK status, since it's an update, not a create

        except Exception as e:
            return {
                "message": f"An unexpected error occurred: {str(e)}",
                "success": False,
            }, 500  # Internal server error

    def get_video_by_ref(ref, ip, user_id):
        try:
            video = Video.query.filter_by(ref=ref).first()
            if not video:
                return {
                    "message": "Video not found",
                    "success": False,
                }, 404  # 404 for not found

            print(f"Retrieved video: {video}")  # Debugging line
            print("reaching here")
            video_data = video_schema.dump(video)
            
            if not video_data['link'].startswith('http'):
                return {
                    "message": "Invalid video link",
                    "success": False
                }, 400  # Bad request

            link_data = {
                "user_id": user_id,
                "video_id": video.id,
                "ip_addresses": [ip],
                "type": "video"
            }

            try:
                link = link_schema.load(link_data)
            except Exception as e:
                return {
                    "message": "Link schema loading error",
                    "success": False,
                    "error": str(e)
                }, 400  # Bad request

            # Check if the IP address already exists and last_click is over 24 hours ago
            existing_link = Link.query.filter(
                Link.ip_addresses.contains([ip]),
                Link.video_id == video.id,
                Link.user_id == user_id,
                Link.last_click >= datetime.utcnow() - timedelta(hours=24)  # Correct comparison
            ).first()
            print('existing_link', existing_link)
            if existing_link:
                existing_link.last_click = datetime.utcnow()
                db.session.commit()
                return redirect(video_data['link'], code=302)
            # Update user points if 24 hours have not passed
            user = User.query.filter_by(id=user_id).first()
           
            if user:
                if user.point is None:
                    user.point = 0 
                user.point += 1
                print("user points", user.point)
                db.session.add(user)
                db.session.commit()

            # Add the new link to the database
            db.session.add(link)
            db.session.commit()

            return redirect(video_data['link'], code=302)

        except Exception as e:
            return {
                "message": "An error occurred",
                "success": False,
                "error": str(e)
            }, 500  # Internal Server Error

        except AttributeError as e:
                return {
                    "message": "Invalid attribute error while retrieving video",
                    "success": False,
                    "error": str(e)
                }, 500
        except Exception as e:
                print(f"Error: {str(e)}")  # Log the exception
                return {
                    "message": "An error occurred while retrieving video",
                    "success": False,
                    "error": str(e)
                }, 500
  
    def get_video_by_ref_unauth(ref):
        try:
            video = Video.query.filter_by(ref=ref).first()
            if not video:
                return {
                    "message": "Video not found",
                    "success": False,
                }, 404  # 404 for not found

            video_data = video_schema.dump(video)
            
            if not video_data.get('link', '').startswith('http'):
                return {
                    "message": "Invalid video link",
                    "success": False
                }, 400  # Bad request

            return redirect(video_data['link'], code=302)  # Temporary redirect

        except AttributeError as e:
            return {
                "message": "Invalid attribute error while retrieving video",
                "success": False,
                "error": str(e)
            }, 500
        except Exception as e:
            logging.error(f"Error: {str(e)}")  # Log the exception
            return {
                "message": "An error occurred while retrieving video",
                "success": False,
                "error": str(e)
            }, 500


    def get_all_videos(page, per_page, search=None, category=None):
        try:
            # Start with the base query
            query = Video.query

            # Apply search filter if a search term is provided
            if search:
                search = search.strip().lower()  # Strip spaces and convert to lowercase
                query = query.filter(Video.title.ilike(f'%{search}%'))

            # Apply category filter if a category is provided
            if category:
                query = query.filter(Video.category == category)

            # Order videos by creation date (ascending order)
            query = query.order_by(Video.created_at.asc())  # Adjust the field name if necessary

            # Retrieve all videos with pagination
            videos = query.paginate(page=page, per_page=per_page, error_out=False)

            # Instantiate the Marshmallow schema for Video model
            video_schema = VideoSchema(many=True)  # many=True for a list of items

            # Serialize paginated video list using Marshmallow
            serialized_videos = video_schema.dump(videos.items)

            # Return serialized data and pagination info
            return {
                'videos': serialized_videos,
                'total_pages': videos.pages,
                'total_videos': videos.total,
                'current_page': videos.page,
                'has_next': videos.has_next,
                'has_prev': videos.has_prev
            }
        except Exception as e:
            return {
                "message": "An error occurred while retrieving videos",
                "success": False,
                "error": str(e)
            }, 500


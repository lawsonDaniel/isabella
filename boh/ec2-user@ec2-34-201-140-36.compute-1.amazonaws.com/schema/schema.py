from flask_marshmallow import Marshmallow
from models.user_model import User
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema  # Optional, for clarity
from models.video_model import Video
ma = Marshmallow()

# Define the User schema
class UserSchema(ma.SQLAlchemyAutoSchema):  # or use SQLAlchemyAutoSchema directly
    class Meta:
        model = User
        load_instance = True

    # # Nested videos relationship within UserSchema
    # videos = ma.Nested('VideoSchema', many=True, dump_only=True)
    

class VideoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Video
        load_instance = True

    # # To represent the user_id for the video
    # user_id = ma.auto_field()
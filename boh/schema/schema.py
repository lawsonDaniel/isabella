from flask_marshmallow import Marshmallow
from models.user_model import User
from models.video_model import Video
from models.booking_model import Booking
from models.link_model import Link  # Import the Link model
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

ma = Marshmallow()

# Define the User schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ('links',)  # Prevent recursion


# Define the Video schema
class VideoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Video
        load_instance = True
        exclude = ('links',)  # Prevent recursion

class BookingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Booking
        load_instance = True
     # For loading user and video by their IDs
    user_id = ma.Int(required=True)
        
# Define the Link schema, linking User and Video
class LinkSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Link
        load_instance = True

    # For loading user and video by their IDs
    user_id = ma.Int(required=True)
    video_id = ma.Int(required=False)

    # Automatically include user and video information for serialization (read-only)
    user = ma.Nested(UserSchema, dump_only=True)
    video = ma.Nested(VideoSchema, dump_only=True)

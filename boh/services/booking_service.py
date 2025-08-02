from models.user_model import User
from models.booking_model import Booking  # Assuming there's a Booking model defined
from schema.schema import UserSchema,BookingSchema
from db_config import db
from sqlalchemy import and_, or_

booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)  # Schema to serialize multiple bookings
user_schema = UserSchema()

class BookingService:
   
    @staticmethod
    def create_user_booking(id, data):
        try:
            # Verify data type
            if not isinstance(data, dict):
                raise ValueError(f"Expected data to be a dictionary, but got: {type(data)}")

            # Check if the user exists
            user = User.query.filter_by(id=id).first()
            if not user:
                return {
                    "message": "User not found",
                    "success": False,
                }, 404

            data['user_id'] = user.id  # Set user ID for the booking

            # Validate and load data using schema
            booking_info = booking_schema.load(data)
            
            # Add the booking info to the database
            db.session.add(booking_info)
            db.session.commit()
            
            # Prepare response data
            response_data = {key: value for key, value in data.items()}
            
            return {
                "message": "User booked successfully",
                "data": response_data,
                "success": True
            }, 201

        except Exception as e:
            print("Error:", e)  # Log the error for debugging
            return {
                "message": "An error occurred while creating booking",
                "success": False,
                "error": str(e)
            }, 500

    @staticmethod
    def get_all_user_bookings(name, date, page=1, per_page=10):
        try:
            # Base query to fetch all bookings, including user information
            query = Booking.query.join(User).add_columns(User).with_entities(Booking, User)

            # Apply filters if provided
            if name:
                    search_filter = or_(User.first_name.ilike(f'%{name}%'), 
                                        User.last_name.ilike(f'%{name}%'))
                    query = query.filter(search_filter)
            if date:
                query = query.filter(Booking.date == date)

            # Pagination
            paginated_results = query.paginate(page=page, per_page=per_page, error_out=False)
            
            # Serialize paginated results with filtered user fields
            result = []
            for booking, user in paginated_results.items:
                # Serialize booking and user data
                booking_data = booking_schema.dump(booking)
                user_data = user_schema.dump(user)

                # Remove sensitive fields from user data
                fields_to_remove = ['otp', 'otp_expires_at', 'password', 'point', 'email_verified']
                for field in fields_to_remove:
                    user_data.pop(field, None)  # Remove the field if it exists

                # Append the sanitized data
                result.append({
                    "booking": booking_data,
                    "user": user_data
                })

            return {
                "message": "User bookings fetched successfully",
                "data": result,
                "page": page,
                "per_page": per_page,
                "total_pages": paginated_results.pages,
                "total_items": paginated_results.total,
                "success": True
            }, 200

        except Exception as e:
            print("Error:", e)  # Log the error for debugging
            return {
                "message": "An error occurred while fetching bookings",
                "success": False,
                "error": str(e)
            }, 500

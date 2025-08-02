from contoller.admin_controller import AdminController
from contoller.leaderboard_controller import LeaderController
from contoller.user_controller import UserController
from contoller.auth_controller import LoginController,registerController
from contoller.image_controller import ImageController
from contoller.video_controller import VideoController 
from contoller.auth_controller import (
    LoginController, 
    GoogleAuthController, 
    GoogleAuthCallbackController, 
    PasswordResetController,
    VerifyOtpController)
from contoller.video_link_controller import VideoLinkController
from contoller.all_video_controller import AllVideoController
from contoller.video_unAuth_controller import VideoAuthLinkController
from contoller.booking_controller import BookingController
from contoller.subscription_link_controller import SubscriptionLinkController

def initialize_routes(api,app):
    api.add_resource(LoginController, '/login', resource_class_kwargs={'app': app})
    api.add_resource(registerController,'/register', resource_class_kwargs={'app': app})
    api.add_resource(UserController,'/user')
    api.add_resource(VideoController, '/video', resource_class_kwargs={'app': app})
    api.add_resource(AllVideoController, '/videos', resource_class_kwargs={'app': app})
    api.add_resource(VideoLinkController, '/video/<string:video_ref>/<int:user_id>', resource_class_kwargs={'app': app})
    api.add_resource(VideoAuthLinkController, '/video/<string:video_ref>', resource_class_kwargs={'app': app})
    api.add_resource(GoogleAuthController, '/login/google', resource_class_kwargs={'app': app})
    api.add_resource(GoogleAuthCallbackController, '/authorize/google', resource_class_kwargs={'app': app})
    api.add_resource(LeaderController,'/leaderboard',resource_class_kwargs={"app": app})
    api.add_resource(PasswordResetController, '/password-reset/request', resource_class_kwargs={"app": app})
    api.add_resource(VerifyOtpController, '/password-reset/verify',resource_class_kwargs={"app": app})
    api.add_resource(BookingController, '/booking')
    api.add_resource(AdminController, '/admin')
    api.add_resource(SubscriptionLinkController, '/subscribe/<int:user_id>')
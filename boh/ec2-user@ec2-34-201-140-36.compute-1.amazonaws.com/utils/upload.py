import os
import cloudinary
import cloudinary.uploader
import base64
import requests

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
)

def upload_image_to_cloudinary(link, public_id):
    try:
        # Upload the image to Cloudinary
        result = cloudinary.uploader.upload(
            link,
            resource_type="auto",  # Automatically detect the file type
            public_id=public_id  # Optional: Set a public ID for the uploaded asset
        )

        print("Result:", result)

        # Fetch the uploaded image as a binary file
        image_response = requests.get(result.get('secure_url'))
        image_response.raise_for_status()  # Raise an error for bad responses

        # Convert image to Base64
        base64_image = base64.b64encode(image_response.content).decode('utf-8')

        # Return the Base64 image
        return {
            "success": True,
            "message": "Image uploaded successfully.",
            "base64_image": base64_image,
            "url": result.get('secure_url')
        }

    except Exception as error:
        print("Error uploading image:", error)
        return {
            "success": False,
            "message": "Error uploading image:",
            "error": str(error),
        }

# Example usage:
# result = await upload_image_to_cloudinary("path/to/your/image.jpg", "your_public_id")
# print(result)

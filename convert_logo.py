
import base64
import os

def get_base64_image(image_path):
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
        # Get extension
        ext = image_path.split('.')[-1]
        return f"data:image/{ext};base64,{encoded_string}"

logo_path = r"c:\Users\Shravan\Desktop\MEDIBOT2.0\logo.png"
base64_logo = get_base64_image(logo_path)

# Show first 100 chars to verify
print(base64_logo[:100])

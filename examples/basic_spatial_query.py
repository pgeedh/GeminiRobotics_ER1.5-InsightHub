import google.generativeai as genai
import os
from PIL import Image

# -------------------------------------------------------------------------
# GEMINI ROBOTICS: BASIC SPATIAL QUERY
# -------------------------------------------------------------------------
# This script demonstrates how to ask Gemini 1.5 for specific 2D coordinates
# of objects in a scene, simulating a "perception" step for a robot.
# -------------------------------------------------------------------------

# 1. SETUP
# Export your API key: export GEMINI_API_KEY='your_key_here'
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Please set the GEMINI_API_KEY environment variable.")

genai.configure(api_key=api_key)

# 2. MODEL CONFIGURATION
# We use gemini-1.5-pro as it has superior vision capabilities for robotics
model = genai.GenerativeModel('gemini-1.5-pro-latest')

def robot_perception_query(image_path, prompt):
    print(f"🤖 Robot: analyzing {image_path}...")
    
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print(f"❌ Error: Image file '{image_path}' not found.")
        return

    # 3. SPATIAL PROMPT
    # We explicitly ask for bounding boxes or specific points.
    response = model.generate_content([prompt, img])
    
    print("\n🔍 Gemini Perception Output:")
    print("--------------------------------------------------")
    print(response.text)
    print("--------------------------------------------------")

if __name__ == "__main__":
    # Example usage
    # You would replace 'robot_view.jpg' with a frame from your robot's camera
    # CREATE A DUMMY IMAGE FOR DEMO if it doesn't exist
    if not os.path.exists("robot_view.jpg"):
        print("Creating dummy robot_view.jpg for demonstration...")
        Image.new('RGB', (640, 480), color = 'gray').save('robot_view.jpg')

    # Example 1: precise Grasping Point
    robot_perception_query(
        "robot_view.jpg", 
        "Assume you are a robot arm. specific the [x, y] pixel coordinates for the center of the largest object in this image. Format as JSON: {'target': 'name', 'coordinates': [x, y]}."
    )

    # Example 2: Scene Description for Navigation
    robot_perception_query(
        "robot_view.jpg",
        "Describe the obstacles in this image that would prevent a robot from moving forward. List them."
    )

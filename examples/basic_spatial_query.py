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
    
    # ---------------------------------------------------------
    # NEW: Visualization Logic
    # ---------------------------------------------------------
    visualize_results(image_path, response.text)

def visualize_results(image_path, response_text):
    """
    Parses the JSON output from Gemini and draws it on the image.
    Assumes format: [{'point': [y, x], 'label': 'name'}] normalized 0-1000
    """
    try:
        from PIL import ImageDraw
        import json
        import re
        
        # 1. Cleaner: Extract JSON block if it's wrapped in markdown
        json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(1))
        else:
            # Try raw parsing if no markdown code blocks
            data = json.loads(response_text)
            
        if not isinstance(data, list):
            print("⚠️ Response was not a list, skipping visualization.")
            return

        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        print(f"\n🎨 Drawing {len(data)} detected points on 'output_perception.jpg'...")
        
        for item in data:
            if 'point' in item:
                # Denormalize coordinates (0-1000 -> pixels)
                y, x = item['point']
                pixel_x = int((x / 1000) * width)
                pixel_y = int((y / 1000) * height)
                
                # Draw Circle
                r = 10  # radius
                draw.ellipse((pixel_x-r, pixel_y-r, pixel_x+r, pixel_y+r), fill='red', outline='white', width=2)
                
                # Draw Text Label
                if 'label' in item:
                    draw.text((pixel_x + 15, pixel_y - 10), item['label'], fill="white")
                    
        img.save("output_perception.jpg")
        print("✅ Saved visualization to: output_perception.jpg")
        
    except Exception as e:
        print(f"⚠️ Could not visualize results: {e}")
        print("Tip: Ensure the model output was valid JSON.")

if __name__ == "__main__":
    # Example usage
    # You would replace 'robot_view.jpg' with a frame from your robot's camera
    # CREATE A DUMMY IMAGE FOR DEMO if it doesn't exist
    if not os.path.exists("robot_view.jpg"):
        print("Creating dummy robot_view.jpg for demonstration...")
        Image.new('RGB', (640, 480), color = 'gray').save('robot_view.jpg')

    # Example 1: precise Grasping Point
    # We update the prompt to enforce strict JSON for the visualizer
    robot_perception_query(
        "robot_view.jpg", 
        "Point to the center of the image. Return JSON: [{'point': [y, x], 'label': 'center'}] with coordinates normalized 0-1000."
    )

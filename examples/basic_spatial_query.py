from google import genai
from google.genai import types
import os
from PIL import Image
from dotenv import load_dotenv

# -------------------------------------------------------------------------
# GEMINI ROBOTICS: BASIC SPATIAL QUERY
# -------------------------------------------------------------------------
# This script demonstrates how to ask Gemini Robotics ER 1.5 for specific 
# 2D coordinates of objects in a scene, simulating a "perception" step.
# -------------------------------------------------------------------------

# 1. SETUP
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Try looking for it in the environment variable if .env fails
    api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("⚠️ Warning: GEMINI_API_KEY not found. Please set it in .env or environment.")
    # For demo purposes, we might proceed but it will fail on the API call
else:
    print("✅ API Key loaded.")

# 2. CLIENT CONFIGURATION
# We use the new google.genai client for gemini-robotics-er-1.5-preview
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    print(f"Error initializing client: {e}")
    client = None

def robot_perception_query(image_path, prompt_text):
    print(f"🤖 Robot: analyzing {image_path}...")
    
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file '{image_path}' not found.")
        return

    # Load image bytes for the new API
    with open(image_path, 'rb') as f:
        image_bytes = f.read()

    # 3. SPATIAL PROMPT
    try:
        response = client.models.generate_content(
            model="gemini-robotics-er-1.5-preview",
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type='image/jpeg', # Adjust mime type if needed
                ),
                prompt_text
            ],
            config=types.GenerateContentConfig(
                temperature=0.5,
                # Thinking is supported in ER 1.5, good for reasoning
                thinking_config=types.ThinkingConfig(thinking_budget=1024) 
            )
        )
        
        print("\n🔍 Gemini Perception Output:")
        print("--------------------------------------------------")
        print(response.text)
        print("--------------------------------------------------")
        
        visualize_results(image_path, response.text)
        
    except Exception as e:
        print(f"❌ API Error: {e}")

def visualize_results(image_path, response_text):
    """
    Parses the JSON output from Gemini and draws it on the image.
    Assumes format: [{'point': [y, x], 'label': 'name'}] normalized 0-1000
    or [{'box_2d': [ymin, xmin, ymax, xmax], 'label': 'name'}]
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
            try:
                data = json.loads(response_text)
            except:
                print("⚠️ Could not parse JSON directly.")
                return
            
        if not isinstance(data, list):
            print("⚠️ Response was not a list, skipping visualization.")
            return

        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        print(f"\n🎨 Drawing {len(data)} detected items on 'output_perception.jpg'...")
        
        for item in data:
            # Handle Point
            if 'point' in item:
                y, x = item['point']
                pixel_x = int((x / 1000) * width)
                pixel_y = int((y / 1000) * height)
                r = 10
                draw.ellipse((pixel_x-r, pixel_y-r, pixel_x+r, pixel_y+r), fill='red', outline='white', width=2)
                if 'label' in item:
                    draw.text((pixel_x + 15, pixel_y - 10), item['label'], fill="white")
            
            # Handle Bounding Box
            elif 'box_2d' in item:
                ymin, xmin, ymax, xmax = item['box_2d']
                pixel_xmin = int((xmin / 1000) * width)
                pixel_xmax = int((xmax / 1000) * width)
                pixel_ymin = int((ymin / 1000) * height)
                pixel_ymax = int((ymax / 1000) * height)
                
                draw.rectangle([pixel_xmin, pixel_ymin, pixel_xmax, pixel_ymax], outline='red', width=3)
                if 'label' in item:
                    draw.text((pixel_xmin, pixel_ymin - 15), item['label'], fill="red")

        img.save("output_perception.jpg")
        print("✅ Saved visualization to: output_perception.jpg")
        
    except Exception as e:
        print(f"⚠️ Could not visualize results: {e}")

if __name__ == "__main__":
    # Example usage
    if not os.path.exists("robot_view.jpg"):
        print("Creating dummy robot_view.jpg for demonstration...")
        Image.new('RGB', (640, 480), color = 'gray').save('robot_view.jpg')

    # Example: Bounding Box query for ER 1.5
    robot_perception_query(
        "robot_view.jpg", 
        """
        Point to the center of the image. 
        Return bounding boxes as a JSON array with labels. 
        Format: [{"box_2d": [ymin, xmin, ymax, xmax], "label": "label"}] normalized to 0-1000.
        """
    )

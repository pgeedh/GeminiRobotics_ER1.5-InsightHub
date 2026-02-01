from google import genai
from google.genai import types
import os
import json
from dotenv import load_dotenv

# -------------------------------------------------------------------------
# GEMINI ROBOTICS: TASK DECOMPOSITION (THE "BRAIN")
# -------------------------------------------------------------------------
# This script shows how to use Gemini Robotics ER 1.5 as a high-level planner 
# that breaks complex Natural Language commands into low-level primitives.
# -------------------------------------------------------------------------

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("⚠️  Warning: GEMINI_API_KEY not set.")
    client = None
else:
    client = genai.Client(api_key=api_key)

# This is the "System Prompt" that defines the robot's capabilities
ROBOT_SYSTEM_PROMPT = """
You are a robot planner for a mobile manipulator (Arm + Wheels).
You have the following low-level implementation primitives:
1. move_to(location_name)
2. pick_object(object_name)
3. place_object(location_name)
4. open_gripper()
5. close_gripper()
6. find_object(object_name)

Given a high-level user command, break it down into a JSON list of steps.
Each step must use ONLY the primitives above.
Return ONLY valid JSON.
"""

def plan_mission(user_command):
    print(f"User Command: '{user_command}'")
    
    full_prompt = f"{ROBOT_SYSTEM_PROMPT}\n\nUser Command: {user_command}\nJSON Plan:"

    if client:
        try:
            response = client.models.generate_content(
                model="gemini-robotics-er-1.5-preview",
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2, # Lower temperature for deterministic planning
                    thinking_config=types.ThinkingConfig(thinking_budget=1024)
                )
            )
            plan_text = response.text
            
            # Cleanup markdown formatting if present
            if "```json" in plan_text:
                plan_text = plan_text.split("```json")[1].split("```")[0].strip()
            elif "```" in plan_text:
                plan_text = plan_text.split("```")[1].split("```")[0].strip()
                
            plan = json.loads(plan_text)
            
            print("\n📋 Generated Robot Plan (Gemini Robotics ER 1.5):")
            for i, step in enumerate(plan):
                print(f"  {i+1}. {step}")
                
        except Exception as e:
            print(f"Planner Error: {e}")
            fallback_demo()
    else:
        fallback_demo()

def fallback_demo():
    # Demonstrating what it WOULD look like
    print("\n[DEMO] Simulated Plan for 'Clean the apple off the table':")
    print("  1. {'action': 'move_to', 'target': 'table'}")
    print("  2. {'action': 'find_object', 'target': 'apple'}")
    print("  3. {'action': 'pick_object', 'target': 'apple'}")
    print("  4. {'action': 'move_to', 'target': 'trash_bin'}")
    print("  5. {'action': 'place_object', 'target': 'trash_bin'}")

if __name__ == "__main__":
    plan_mission("Find the apple on the kitchen table and throw it away.")

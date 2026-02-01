from google import genai
from google.genai import types
import os
import time
from dotenv import load_dotenv

# -------------------------------------------------------------------------
# GEMINI ROBOTICS: AGENTIC TOOL USE
# -------------------------------------------------------------------------
# Robots often face lack of knowledge (e.g. "Is this bottle recyclable?").
# This script demonstrates using Gemini's "Tools" (like Google Search) to 
# ground robot decisions in real-world data.
# -------------------------------------------------------------------------

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Mock tool output for demonstration
def mock_search_tool(query):
    print(f"\n[Tool Execution] Searching Google for: '{query}'...")
    time.sleep(1)
    if "recyclable" in query.lower():
        return "Search Result: Plastic #5 (PP) is generally recyclable in most modern curbside programs."
    return "No specific info found."

def run_agentic_robot(object_description):
    print(f"🤖 Robot Camera detected: {object_description}")
    print("🤔 Robot Reasoning: I need to decide which bin to put this in.")
    
    # NOTE: In the new google.genai API, tools are configured slightly differently:
    # tool = types.Tool(google_search=types.ToolGoogleSearch())
    # client.models.generate_content(..., config=types.GenerateContentConfig(tools=[tool]))
    
    # For this standalone script, we simulate the 'thought process':
    
    query = f"Is {object_description} recyclable?"
    search_result = mock_search_tool(query)
    
    # Now interact with the LLM with the context
    prompt = f"""
    You are a recycling robot.
    Object: {object_description}
    Knowledge Base Context: {search_result}
    
    Decision: Should I put this in 'Recycling' or 'Trash'? Explain briefly.
    """
    
    print("\n🧠 Gemini Deciding (Simulated context integration)...")
    # Simulated response
    print(f"--> Based on search results ('{search_result}'), this item ({object_description}) should go to RECYCLING because it is Polypropylene.")

if __name__ == "__main__":
    run_agentic_robot("Plastic container with symbol #5")

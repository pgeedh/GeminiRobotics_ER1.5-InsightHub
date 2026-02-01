#!/usr/bin/env python3
import os
import sys
import time
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import print as rprint
import questionary

# Import examples
# Ensure strict pathing for relative imports if run from root
sys.path.append(os.path.join(os.path.dirname(__file__), 'examples'))

try:
    from examples import basic_spatial_query
    from examples import task_decomposition
    from examples import tool_use_recycling
    from examples import video_anomaly_detection
except ImportError as e:
    # If package import fails, try direct import (context dependent)
    try:
        import basic_spatial_query
        import task_decomposition
        import tool_use_recycling
        import video_anomaly_detection
    except ImportError:
        pass # Will handle later or assuming run from root with python -m

load_dotenv()
console = Console()

def check_api_key():
    key = os.getenv("GEMINI_API_KEY")
    if not key or "your_api_key" in key:
        rprint("[bold red]❌ Warning: GEMINI_API_KEY is not set correctly in .env[/bold red]")
        rprint("[yellow]Please check your .env file before running these demos.[/yellow]")
        if not Confirm.ask("Do you want to continue anyway (simulated mode)?"):
            sys.exit(0)
        return False
    return True

def main():
    console.clear()
    console.print(Panel.fit(
        "[bold cyan]🤖 Gemini Robotics ER 1.5 - Insight Hub[/bold cyan]\n"
        "[white]Early Trusted Tester Interactive Suite[/white]",
        subtitle="v1.0.0"
    ))

    check_api_key()

    while True:
        try:
            choice = questionary.select(
                "Select a Repository Capability to Demo:",
                choices=[
                    "1. 👁️  Vision & Perception (Spatial Query)",
                    "2. 🧠  Brain & Planning (Task Decomposition)",
                    "3. 🛠️  Agentic Capabilities (Tool Use)",
                    "4. 🛡️  Safety & Auditing (Video Analysis)",
                    "5. Exit"
                ]
            ).ask()
        except KeyboardInterrupt:
            rprint("\n[yellow]Cancelled by user.[/yellow]")
            break

        if choice is None or "Exit" in choice:
            rprint("[green]Goodbye! 👋[/green]")
            break

        console.rule(f"[bold]{choice}[/bold]")

        if "Vision" in choice:
            rprint("[italic]Running: examples/basic_spatial_query.py[/italic]")
            
            # Allow user to drag and drop or press enter for default
            # NOTE: Removed only_to_existing=True as it causes compatibility issues with some prompt_toolkit versions
            # NOTE: Switched to .text() to avoid questionary.path() compatibility issues with prompt_toolkit
            image_path = questionary.text(
                "Drag and drop an image file here (or press Enter for default 'robot_view.jpg'):"
            ).ask()
            
            # If user just hit enter, use default
            if not image_path:
                image_path = "robot_view.jpg"
            
            if image_path is None:
                rprint("[yellow]Cancelled.[/yellow]")
                continue

            # Handle standard drag-and-drop quoting from some terminals
            image_path = image_path.strip().replace("'", "").replace('"', "")
            
            if not os.path.exists(image_path) and image_path == "robot_view.jpg":
                 rprint("[yellow]Default 'robot_view.jpg' not found. Creating a dummy one for you...[/yellow]")
                 from PIL import Image
                 Image.new('RGB', (640, 480), color = 'gray').save('robot_view.jpg')

            if os.path.exists(image_path):
                # Ask what to detect
                user_prompt = questionary.text(
                    "What would you like to detect/find? (Press Enter for 'Detect all humans and robots'):",
                    default="Detect all humans and robots and return bounding boxes."
                ).ask()

                basic_spatial_query.robot_perception_query(
                    image_path, 
                    f"""{user_prompt}
                    Return bounding boxes as a JSON array with labels. 
                    Format: [{{"box_2d": [ymin, xmin, ymax, xmax], "label": "label"}}] normalized to 0-1000."""
                )
                rprint("\n[bold green]✅ Perception Demo Complete[/bold green]")
            else:
                 rprint(f"[bold red]❌ Error: Image file '{image_path}' not found.[/bold red]")

        elif "Planning" in choice:
            rprint("[italic]Running: examples/task_decomposition.py[/italic]")
            command = Prompt.ask("Enter a robot command", default="Find the apple on the kitchen table and throw it away")
            task_decomposition.plan_mission(command)
            rprint("\n[bold green]✅ Planning Demo Complete[/bold green]")

        elif "Agentic" in choice:
            rprint("[italic]Running: examples/tool_use_recycling.py[/italic]")
            item = Prompt.ask("What object does the robot see?", default="Plastic container with symbol #5")
            tool_use_recycling.run_agentic_robot(item)
            rprint("\n[bold green]✅ Agentic Demo Complete[/bold green]")

        elif "Safety" in choice:
            rprint("[italic]Running: examples/video_anomaly_detection.py[/italic]")
            video_anomaly_detection.analyze_video_safety(
                "robot_incident_log_001.mp4",
                "1. Max speed 0.5m/s. 2. No humans in Red Zone. 3. Grip securely."
            )
            rprint("\n[bold green]✅ Safety Demo Complete[/bold green]")
        
        input("\nPress Enter to return to menu...")
        console.clear()

if __name__ == "__main__":
    main()

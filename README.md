# Gemini Robotics ER 1.5 Insight Hub <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Google_Gemini_logo.svg/2560px-Google_Gemini_logo.svg.png" align="right" width="100">

[![DeepMind](https://img.shields.io/badge/Maintained%20By-Google%20DeepMind%20Trusted%20Tester-4285F4?style=for-the-badge&logo=google)](https://deepmind.google/technologies/gemini/)
[![Gemini 1.5](https://img.shields.io/badge/Model-Gemini%20Robotics%20ER%201.5-blue?style=for-the-badge)](https://aistudio.google.com/)
[![Status](https://img.shields.io/badge/Community-Awesome%20List-green?style=for-the-badge)](https://github.com/google-gemini/cookbook)

> **🚀 INSIGHTS FROM THE EARLY TRUSTED TESTER PROGRAM**
> This repository is a curated collection of resources, patterns, and "better" updates for Gemini Robotics, maintained by an **Early Trusted Tester**.
>
> My goal is to bridge the gap between closed research and practical application. Here, you will find use-cases, cookbooks, and projects that push the boundaries of what's possible with Embodied Reasoning (ER) models.

---

## 🤖 What is Gemini Robotics ER 1.5?

**Gemini Robotics-ER 1.5** is a specialized Vision-Language-Action (VLA) model designed to be the "brain" of next-generation robots. Unlike standard LLMs, it features **Embodied Reasoning**: the ability to understand 3D space, physics, and causal relationships in the physical world.

### Key Capabilities
| Capability | Description | Application |
|------------|-------------|-------------|
| **Spatial Grounding** | Precise 2D/3D coordinate output (points, boxes). | Grasping, segmentation, navigation. |
| **Temporal Reasoning** | Understanding "what happened when" in video. | Success detection, security monitoring. |
| **Long-Horizon Planning** | Breaking complex tasks into primitives. | "Clean the kitchen" → 15 robot actions. |
| **Tool Use** | Natively calling external APIs (Search, Code). | Sorting trash by local rules, checking weather. |

---

## ⚡ Quick Start

### 1. Installation
```bash
pip install google-generativeai pillow numpy
```

### 2. Basic Perception Script
*See [`examples/basic_spatial_query.py`](./examples/basic_spatial_query.py) for the full runnable script.*

```python
import google.generativeai as genai
from PIL import Image

# Initialize the ER 1.5 Preview Model
model = genai.GenerativeModel('gemini-robotics-er-1.5-preview')

# Ask for precise coordinates
response = model.generate_content([
    "Point to the handle of the mug. Return [y, x] coordinates.",
    Image.open('robot_view.jpg')
])
print(response.text)
```

---

### 📸 Visual Use Case Gallery

Use these reference patterns to prompt the model effectively.

### 📍 Spatial Awareness & Finding Objects

#### 1. Pointing to Undefined/Novel Objects
*Ask the robot to identify everything, even if it hasn't seen it before.*
<img width="100%" alt="Pointing to items" src="./assets/pointing_undefined.png" />

#### 2. Abstract Description Finding ("Find all Fruit")
*The model understands categories, not just rigid labels.*
<img width="100%" alt="Fruit finding" src="./assets/find_fruit.png" />

#### 3. Serial Part Identification
*Drilling down into specific object parts (handle, rim, stem) for grasping.*
<img width="100%" alt="Part identification" src="./assets/part_identification.png" />

---

### 🗺️ Trajectory & Path Planning

#### 4. Collision-Free Path Planning
*Asking the model to generate waypoints `(x,y)` to navigate around obstacles.*
<img width="100%" alt="Path planning" src="./assets/obstacle_avoidance.png" />

#### 5. Complex Trajectories (e.g., Brushing)
*Fine-grained manipulation paths.*
<img width="100%" alt="Brushing path" src="./assets/trajectory_brushing.png" />

---

### 🧠 Reasoning & Logic

#### 6. "Reasoning by Counting"
*The model doesn't just guess; it can explain **why** it thinks there are 8 items.*
<img width="100%" alt="Counting reasoning" src="./assets/counting_reasoning.png" />

#### 7. Success Detection (Temporal Video Analysis)
*Did the robot actually finish the job? Compare start and end states.*
| Start State | End State |
|-------------|-----------|
| ![Start](./assets/success_start.png) | ![End](./assets/success_end.png) |

---

## 📂 Included Examples
| File | Focus | Description |
|------|-------|-------------|
| [`examples/basic_spatial_query.py`](./examples/basic_spatial_query.py) | **Vision** | Get X,Y coords for grasping handles. |
| [`examples/task_decomposition.py`](./examples/task_decomposition.py) | **Planning** | Break "clean table" into "pick, move, place". |
| [`examples/tool_use_recycling.py`](./examples/tool_use_recycling.py) | **Agentic** | Search Google to check if plastic is recyclable. |
| [`examples/video_anomaly_detection.py`](./examples/video_anomaly_detection.py) | **Video** | Audit long robot videos for safety violations. |
| [`INTERESTING_PROMPTS.md`](./INTERESTING_PROMPTS.md) | **Experiments** | "The Hazmat Navigator", "Grocery Packer", and other advanced prompts. |

---

## 🔮 Roadmap: Cookbooks & Projects

We are actively working on full-stack examples for the next release:
- [ ] **ROS 2 Integration Node**: Drop-in `ros2 run` package.
- [ ] **Sim-to-Real Pipeline**: Isaac Sim to Realman/Franka arm.
- [ ] **VLA Fine-tuning Guide**: How to adapt the model to *your* arm.

---

<p align="center">
  <i>Curated with ❤️ by Pruthvi Geedh.</i>
</p>

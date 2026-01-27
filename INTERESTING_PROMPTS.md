# 🧠 Interesting & Experimental Prompts

This collection pushes the boundaries of what **Gemini Robotics ER 1.5** can do. These prompts go beyond simple "pick and place" and explore physics reasoning, social awareness, and complex semantic limits.

> **🧪 Experimental**: These prompts rely on the model's "World Model" capabilities. Results may vary!

---

## 🏗️ Physics & Material Reasoning

### 1. The "Grocery Packer" (Physics + Safety)
*Ensures the robot understands object properties (fragility, weight) without explicit training.*

**Prompt:**
```text
I need to pack this grocery bag. Look at the items on the table.
1. Identify items that are heavy or durable (cans, jars).
2. Identify items that are fragile (eggs, bread, chips).
3. Output a packing plan: Return the coordinates of the heavy items first to place at the bottom, then the fragile items to place on top.
Format matches: [{"item": "name", "reason": "fragile/heavy", "coordinates": [y, x]}]
```

### 2. The "Hazmat Navigator" (Safety Zones)
*Planning paths based on semantic danger rather than just physical obstacles.*

**Prompt:**
```text
I am holding a hot soldering iron.
Plot a safe trajectory of 10 points from the workbench to the tool rack.
CRITICAL CONSTRAINT: The path must stay at least 20cm away from any flammable materials (paper, curtains, chemicals) visible in the image.
Point to the flammable hazards you are avoiding first.
```

---

## 🕵️ Temporal & Forensic Analysis (Video)

### 3. "What went wrong?" (Failure Analysis)
*Debugging robot failure by showing it a video of a failed grasp.*

**Prompt:**
```text
Watch the video of the failed pick attempt.
Analyze the moment the gripper touched the object (timestamp ~00:04).
Why did the object slip?
A) Gripper was not centered.
B) Object was too heavy.
C) Gripper moved too fast.
Provide the timestamp of the error and point to the gap between the finger and the object.
```

---

## 🧩 Complex Logic & Etiquette

### 4. The "Fancy Butler" (Social Norms)
*Using knowledge of human etiquette to guide robot action.*

**Prompt:**
```text
Look at this dining table setting.
Something is wrong according to formal dining etiquette.
1. Identify the misplaced utensil.
2. Point to where it currently is.
3. Point to where it *should* be.
Explain your reasoning.
```

### 5. The "Librarian" (OCR + Semantic Search)
*Finding objects based on text content or abstract genre.*

**Prompt:**
```text
Scan the bookshelf.
1. Find the book titled "The Great Gatsby". 
2. If you cannot find it, find a book that is in the same genre (Classic American Literature) and point to its spine.
3. Return the exact [y, x] point for the gripper to pull the book out.
```

---

## 🛠️ Code Generation from Visuals

### 6. The "IKEA Assembler" (Visual-to-Code)
*Translating visual assembly states into executable Python.*

**Prompt:**
```text
Look at the pile of parts (screws, dowels, boards).
Generate a Python script using the function `robot.insert(part, target_hole)`.
The script should assemble the two boards using the wooden dowels.
1. Identify the dowels (Part A).
2. Identify the holes on the board (Hole B).
3. Write the sequence to insert all 4 dowels.
```

---

*Verified by the Early Trusted Tester Program.*

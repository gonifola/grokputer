"""Blender Agent Bridge

Bridges OpenClaw to a running Blender instance.
Sends bpy (Blender Python) code for execution.

Connection methods:
1. Command Port (v1): localhost:5000 REST API running inside Blender
2. File watch (fallback): Write .py to watched folder, Blender auto-executes
3. Direct (standalone): Import and run bpy code in Blender's Python console

The Blender Agent handles:
- Mesh creation and manipulation
- Sacred geometry generators
- Materials and rendering
- STL/OBJ export
- Slicer pipeline (CuraEngine/PrusaSlicer CLI)
"""

import os
import json
import requests
from typing import Optional, Dict, Any

BLENDER_PORT = int(os.environ.get("BLENDER_PORT", "5000"))
BLENDER_HOST = os.environ.get("BLENDER_HOST", "localhost")


class BlenderBridge:
    """Bridge between OpenClaw and Blender."""

    def __init__(self):
        self.base_url = f"http://{BLENDER_HOST}:{BLENDER_PORT}"
        self.xai_key = os.environ.get("XAI_API_KEY", "")

    def is_running(self) -> bool:
        """Check if Blender Command Port is accessible."""
        try:
            response = requests.get(f"{self.base_url}/status", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    def execute_bpy(self, code: str) -> Dict[str, Any]:
        """Send bpy code to Blender for execution."""
        if not self.is_running():
            return {"error": "Blender not running or Command Port not active"}

        try:
            response = requests.post(
                f"{self.base_url}/execute",
                json={"code": code},
                timeout=60
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_scene_state(self) -> Dict[str, Any]:
        """Get current Blender scene state for context."""
        scene_code = """
import bpy
import json

objects = []
for obj in bpy.context.scene.objects:
    objects.append({
        "name": obj.name,
        "type": obj.type,
        "location": list(obj.location),
        "scale": list(obj.scale),
        "visible": obj.visible_get()
    })

result = {
    "scene_name": bpy.context.scene.name,
    "objects": objects,
    "selected": [o.name for o in bpy.context.selected_objects],
    "active": bpy.context.active_object.name if bpy.context.active_object else None
}
print(json.dumps(result))
"""
        return self.execute_bpy(scene_code)

    def generate_and_execute(self, natural_language: str) -> Dict[str, Any]:
        """Use Grok to generate bpy code from natural language, then execute."""
        scene = self.get_scene_state()

        system_prompt = f"""You are the Blender Agent inside Grokputer.
Generate Python code using bpy (Blender Python API) to accomplish the user's request.

Current scene state: {json.dumps(scene)}

Rules:
- Output ONLY valid Python code, no explanation
- Use bpy module (already imported in Blender)
- For sacred geometry, use exact golden ratio coordinates (phi = (1+sqrt(5))/2)
- Clean up default objects if needed (bpy.data.objects.remove)
- Add materials with colors when creating objects
- Handle errors gracefully
"""
        try:
            response = requests.post(
                "https://api.x.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.xai_key}"},
                json={
                    "model": "grok-2-latest",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": natural_language}
                    ],
                    "temperature": 0.3
                },
                timeout=30
            )
            code = response.json()["choices"][0]["message"]["content"]
            
            # Strip markdown code fences if present
            if code.startswith("```"):
                code = code.split("\n", 1)[1]
                code = code.rsplit("```", 1)[0]

            return self.execute_bpy(code)

        except Exception as e:
            return {"error": f"Blender agent error: {str(e)}"}

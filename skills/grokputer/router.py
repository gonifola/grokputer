"""Grokputer Intent Router

Classifies user input and routes to the appropriate agent:
- LOCAL: screen control, mouse, keyboard, app launching (OpenClaw native)
- CLOUD: API calls, email, social media, web search, trading
- BLENDER: 3D modeling, geometry, CAD, STL export, slicing
- DIRECT: pure conversation, no action needed
- CHAIN: multi-agent sequence
"""

import os
import json
import requests
from typing import Optional

XAI_API_KEY = os.environ.get("XAI_API_KEY", "")
XAI_BASE_URL = "https://api.x.ai/v1"
MODEL = "grok-2-latest"

ROUTER_SYSTEM_PROMPT = """
You are the Grokputer intent router. Your job is to classify user commands
and route them to the correct agent(s).

Agents available:
- LOCAL: Controls the user's physical computer. Screen capture, mouse clicks,
  keyboard input, opening/closing applications, window management, file
  system operations on the local machine.
- CLOUD: Handles API-based operations. Email (Gmail), social media (Twitter,
  Reddit), calendar, web search, browser automation, code execution in cloud
  sandboxes, app integrations (GitHub, Slack, Notion, etc.), crypto trading.
- BLENDER: 3D modeling via Blender Python API (bpy). Sacred geometry, mesh
  creation, modifiers, materials, rendering, STL export, slicer integration.
  Only active when Blender is running.
- DIRECT: Pure conversation. Questions, explanations, brainstorming. No
  action required.

Rules:
1. If a command requires multiple agents, return a CHAIN with ordered steps.
2. If ambiguous, use context memory to decide.
3. LOCAL is for anything touching the physical screen/desktop.
4. CLOUD is for anything that goes through an API.
5. BLENDER is specifically for 3D modeling tasks.
6. Some commands start LOCAL (open an app) then switch to another agent.

Respond with JSON only:
{
  "agent": "LOCAL" | "CLOUD" | "BLENDER" | "DIRECT" | "CHAIN",
  "chain": ["LOCAL", "BLENDER"],  // only if agent is CHAIN
  "confidence": 0.95,
  "reasoning": "brief explanation"
}
"""

context_memory: list = []
MAX_CONTEXT = 20


def classify(user_input: str) -> dict:
    """Classify user intent and return routing decision."""
    global context_memory

    messages = [
        {"role": "system", "content": ROUTER_SYSTEM_PROMPT},
        *context_memory[-MAX_CONTEXT:],
        {"role": "user", "content": user_input}
    ]

    try:
        response = requests.post(
            f"{XAI_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {XAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": messages,
                "temperature": 0.3,
                "response_format": {"type": "json_object"}
            },
            timeout=30
        )
        response.raise_for_status()
        result = json.loads(response.json()["choices"][0]["message"]["content"])

        # Update context
        context_memory.append({"role": "user", "content": user_input})
        context_memory.append({"role": "assistant", "content": json.dumps(result)})

        return result

    except Exception as e:
        return {
            "agent": "DIRECT",
            "confidence": 0.0,
            "reasoning": f"Router error: {str(e)}",
            "error": True
        }


def route(user_input: str) -> str:
    """Route user input and return agent name(s)."""
    decision = classify(user_input)
    agent = decision.get("agent", "DIRECT")

    if agent == "CHAIN":
        chain = decision.get("chain", [])
        return f"CHAIN: {' -> '.join(chain)}"

    return agent


if __name__ == "__main__":
    # Quick test
    test_commands = [
        "Open Blender and make a stellated dodecahedron",
        "Post this to Twitter",
        "Move that window to the left monitor",
        "Search my email for invoices from last week",
        "Create a flower of life, export STL, slice for Ender 3",
        "What time is it?",
    ]

    for cmd in test_commands:
        result = classify(cmd)
        print(f"\n> {cmd}")
        print(f"  Agent: {result['agent']}")
        print(f"  Confidence: {result.get('confidence', 'N/A')}")
        print(f"  Reasoning: {result.get('reasoning', 'N/A')}")

# Grokputer Architecture

## Overview

Grokputer is a hybrid AI agent that merges two paradigms:

1. **Local-first agent** (OpenClaw) — controls your physical computer
2. **Cloud agent** — connects to 860+ apps via API

Both are orchestrated by a single **Grok Router** that classifies intent and dispatches to the right agent.

## Core Components

### 1. Grok Router (The Brain)

The router receives all input (voice, text, message) and decides which agent handles it.

```python
# Simplified router logic
def route(user_input: str) -> Agent:
    classification = grok_classify(user_input)
    
    if classification.requires_screen:
        return LocalAgent()      # OpenClaw handles it
    elif classification.requires_3d:
        return BlenderAgent()    # bpy execution
    elif classification.requires_api:
        return CloudAgent()      # Composio / API calls
    else:
        return GrokDirect()      # Pure conversation
```

**Classification signals:**
- Screen words: "click", "move window", "type into", "screenshot", "open [app name]"
- 3D words: "create", "model", "stellated", "sphere", "export STL", "slice"
- API words: "email", "tweet", "post", "search", "calendar", "trade"
- Ambiguous: Grok uses context memory to decide

### 2. Local Agent (OpenClaw)

OpenClaw provides:
- **Gateway** — WebSocket control plane (ws://127.0.0.1:18789)
- **Multi-channel inbox** — WhatsApp, Telegram, Slack, Discord, iMessage, etc.
- **Browser control** — Chrome/Chromium via CDP
- **Voice Wake + Talk Mode** — ElevenLabs TTS, always-on speech
- **Skills platform** — extensible via workspace skills
- **Node system** — macOS/iOS/Android device control

We use OpenClaw as-is (npm package), not a fork. Grokputer installs as an OpenClaw workspace skill.

### 3. Cloud Agent

Handles anything that goes through an API:
- **App integrations** — GitHub, Twitter, Gmail, Calendar, Slack, Notion, Jira, etc.
- **Browser automation** — Hyperbrowser for web scraping and form filling
- **Code execution** — Python/bash in sandboxed environments
- **Web research** — search, fetch, synthesize

### 4. Blender Agent (Voice to OmniCAD)

Handles 3D modeling commands:
- **bpy execution** — generates and runs Blender Python code
- **Sacred geometry** — pre-built generators (Star Mother, Flower of Life, etc.)
- **Scene awareness** — reads current Blender state for contextual commands
- **STL export** — print-ready mesh output
- **Slicer integration** — CuraEngine/PrusaSlicer CLI for G-code

## Data Flow

```
┌─────────────────────────────────────────┐
│               INPUT LAYER                │
│                                          │
│  Voice (Vosk/Whisper)                    │
│  Text (terminal, chat, WhatsApp, etc.)   │
│  Messaging (Telegram, Discord, Slack)    │
│  Vision (screenshot, camera)             │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│            GROK ROUTER                   │
│                                          │
│  1. Classify intent                      │
│  2. Check context memory (20+ turns)     │
│  3. Route to agent                       │
│  4. Handle multi-step chains             │
│     (Local → Cloud → Blender)            │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
┌─────────┐┌─────────┐┌─────────┐
│  LOCAL  ││  CLOUD  ││ BLENDER │
│  AGENT  ││  AGENT  ││  AGENT  │
│         ││         ││         │
│OpenClaw ││Composio ││  bpy    │
│Gateway  ││860+ apps││OmniCAD  │
│Screen   ││Browser  ││Sacred   │
│Voice    ││Code     ││Geometry │
│Files    ││Email    ││STL/Gcode│
└─────────┘└─────────┘└─────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│            OUTPUT LAYER                  │
│                                          │
│  Voice (ElevenLabs TTS)                  │
│  Screen actions (mouse, keyboard)        │
│  Messages (WhatsApp, Telegram, etc.)     │
│  Files (STL, G-code, documents)          │
│  API actions (tweet, email, trade)       │
└─────────────────────────────────────────┘
```

## Multi-Step Command Chains

Grokputer can chain agents for complex commands:

**Example: "Build a stellated dodecahedron, export STL, post a render to Twitter"**

1. Blender Agent → generates geometry via bpy
2. Blender Agent → exports STL file
3. Blender Agent → renders viewport image
4. Cloud Agent → posts render image to Twitter with caption

**Example: "Open Blender, load my sacred geometry project, render it"**

1. Local Agent → opens Blender application
2. Local Agent → navigates to File → Open
3. Blender Agent → takes over once Blender is running
4. Blender Agent → executes render command

## OpenClaw Integration

Grokputer installs as an OpenClaw workspace skill:

```
~/.openclaw/
├── openclaw.json          # Config (model: xai/grok-2-latest)
├── workspace/
│   ├── AGENTS.md          # Agent routing rules
│   ├── SOUL.md            # Grokputer personality
│   ├── skills/
│   │   ├── grokputer/
│   │   │   ├── SKILL.md   # Skill manifest
│   │   │   ├── router.py  # Intent classifier
│   │   │   ├── cloud.py   # Cloud agent bridge
│   │   │   └── blender.py # Blender agent bridge
│   │   └── solana/
│   │       ├── SKILL.md   # Molt Claw trading skill
│   │       └── trader.py  # Solana trading logic
```

### OpenClaw Config

```json
{
  "agent": {
    "model": "xai/grok-2-latest"
  },
  "channels": {
    "whatsapp": { "enabled": true },
    "telegram": { "enabled": true },
    "discord": { "enabled": true }
  },
  "browser": {
    "enabled": true
  }
}
```

## Grok API Integration

Grokputer uses xAI's Grok API for all intelligence:

```python
import os
import requests

XAI_API_KEY = os.environ["XAI_API_KEY"]
XAI_BASE_URL = "https://api.x.ai/v1"

def grok_chat(messages: list, model: str = "grok-2-latest") -> str:
    response = requests.post(
        f"{XAI_BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {XAI_API_KEY}"},
        json={
            "model": model,
            "messages": messages,
            "temperature": 0.7
        }
    )
    return response.json()["choices"][0]["message"]["content"]

def grok_classify(user_input: str, context: list) -> dict:
    """Classify intent and route to appropriate agent."""
    system_prompt = """
    You are the Grokputer router. Classify user intent into one of:
    - LOCAL: requires screen control, mouse, keyboard, opening apps
    - CLOUD: requires API calls (email, social, search, trading)
    - BLENDER: requires 3D modeling, geometry, CAD, STL
    - DIRECT: pure conversation, no action needed
    - CHAIN: requires multiple agents in sequence (list them)
    
    Respond with JSON: {"agent": "...", "chain": [...], "reasoning": "..."}
    """
    return grok_chat([
        {"role": "system", "content": system_prompt},
        *context,
        {"role": "user", "content": user_input}
    ])
```

## Roadmap

### Phase 1: Foundation (Current)
- [x] Grok API wired
- [x] Voice to OmniCAD Blender addon
- [x] Sacred geometry scripts
- [ ] OpenClaw installation + config
- [ ] Grok Router (intent classification)
- [ ] Grokputer OpenClaw skill

### Phase 2: Integration
- [ ] Cloud agent bridge (Composio)
- [ ] Multi-step command chains
- [ ] Voice input (Vosk v1)
- [ ] Voice output (ElevenLabs)

### Phase 3: Trading (Molt Claw)
- [ ] Solana wallet integration
- [ ] Token price monitoring
- [ ] Trade execution via Jupiter/Raydium
- [ ] Risk management rules

### Phase 4: Platform
- [ ] Multi-vertical system prompts
- [ ] Vertical marketplace
- [ ] Self-Operating Computer integration (screenshot + vision)
- [ ] Community skills registry

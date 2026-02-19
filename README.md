# 🧠 Grokputer

**One brain. Multiple hands. Powered by Grok.**

Grokputer is a hybrid AI agent that combines:
- **Local screen control** (mouse, keyboard, see your screen) — via [OpenClaw](https://github.com/openclaw/openclaw)
- **Cloud API integrations** (860+ apps, browser automation, code execution) — via cloud agent layer
- **3D modeling engine** (Blender bpy, sacred geometry, voice-to-CAD) — via [Voice to OmniCAD](https://github.com/gonifola/voice-to-omnicad)

All powered by **Grok** (xAI) as the central intelligence.

## Architecture

```
You (voice/text)
    │
    ▼
┌─────────────────────────────┐
│      Grok Router (brain)     │
│   xAI grok-2-latest API      │
│   Intent classification      │
│   Context memory (20+ turns) │
└──────────┬──────────────────┘
           │
    ┌──────┼──────────┐
    ▼      ▼          ▼
┌───────┐ ┌────────┐ ┌──────────┐
│ Local │ │ Cloud  │ │ Blender  │
│ Agent │ │ Agent  │ │ Agent    │
├───────┤ ├────────┤ ├──────────┤
│Screen │ │860+    │ │bpy code  │
│Mouse  │ │apps    │ │Sacred    │
│Keys   │ │Browser │ │geometry  │
│Files  │ │Code    │ │STL export│
│Shell  │ │Email   │ │Slicer    │
│Apps   │ │Social  │ │Voice I/O │
└───────┘ └────────┘ └──────────┘
```

## How It Works

You say something. Grok figures out which agent handles it:

| You say | Agent | What happens |
|---------|-------|--------------|
| "Open Blender and make a stellated dodecahedron" | Local → Blender | Opens app locally, then runs bpy script |
| "Post this to Twitter" | Cloud | Tweets via API |
| "Move that window to the left" | Local | PyAutoGUI moves the window |
| "Search my email for invoices" | Cloud | Searches Gmail via API |
| "Create a flower of life, export STL, slice for Ender 3" | Blender | Full pipeline: model → STL → G-code |
| "What's on my screen right now?" | Local | Screenshot → Grok vision |

## Stack

| Component | Technology | Status |
|-----------|-----------|--------|
| Brain | xAI Grok API (grok-2-latest) | ✅ Wired |
| Local Agent | OpenClaw (Node.js gateway) | 🔧 Integration |
| Cloud Agent | Composio (860+ apps) | ✅ Available |
| Blender Agent | Voice to OmniCAD addon (bpy) | ✅ Working |
| Voice Input | Vosk (offline) → Whisper (GPU) | 🔧 v1 wiring |
| Voice Output | ElevenLabs TTS | 📋 Planned |
| Screen Control | PyAutoGUI + screenshot loop | 📋 Planned |
| Slicer | CuraEngine / PrusaSlicer CLI | 📋 Planned |

## Verticals

Same core engine, different system prompts + geometry libraries:

1. 🔮 Sacred Geometry (launch) — Flower of Life, Metatron's Cube, Star Mother, stellated compounds
2. 🏗️ Architecture — residential, geodesic domes
3. 🚢 Naval Architecture — hull design, interiors
4. ✈️ Aviation — wing profiles, drone frames
5. 🌪️ Wind Tunnel — CFD-lite via Blender fluid sim
6. 🌿 Nature — fractal trees, coral, terrain, L-systems
7. 🏙️ City Modeling — procedural blocks, urban planning
8. 🛋️ Interior Design — voice-generate rooms in any designer's style
9. 🤖 Drone Engineering — frames, prop guards, motor mounts
10. 🚗 Automotive — body panels, chassis, suspension
11. ⚙️ Engines — pistons, crankshafts, turbo housings
12. 💻 Electronics — PCB layout, enclosures
13. 🖥️ Computers — custom cases, fan shrouds, GPU brackets
14. 🧬 AI Self-Optimization / Goodtek — visualize AI architectures
15. 🦾 Robotics — joint assemblies, actuators, grippers
16. 🏥 Medical Devices — prosthetics, surgical guides, dental aligners

## Quick Start

```bash
# Prerequisites: Node >= 22, Python 3.10+

# 1. Install OpenClaw (local agent)
npm install -g openclaw@latest
openclaw onboard --install-daemon

# 2. Clone Grokputer
git clone https://github.com/gonifola/grokputer.git
cd grokputer

# 3. Set your Grok API key
export XAI_API_KEY="your-xai-key-here"

# 4. Install Grokputer skill into OpenClaw
cp -r skills/grokputer ~/.openclaw/workspace/skills/

# 5. Start the gateway
openclaw gateway --port 18789 --verbose

# 6. Talk to Grokputer
openclaw agent --message "What can you do?" --thinking high
```

## Why Not Just Fork OpenClaw?

OpenClaw is the **local agent foundation** — it handles screen control, messaging, files, shell, browser.

Grokputer **adds**:
- Grok as the brain (instead of Claude/GPT)
- Cloud agent layer (860+ app integrations via Composio)
- Blender/CAD agent (voice-to-3D modeling, sacred geometry, STL export, slicer)
- Multi-vertical system prompts
- Solana trading capabilities (Molt Claw)

Grokputer installs **on top of** OpenClaw as a skill/workspace, not as a fork.

## Related Projects

- [Voice to OmniCAD](https://github.com/gonifola/voice-to-omnicad) — Blender addon for voice-controlled 3D modeling
- [Sacred Geometry Blender](https://github.com/gonifola/sacred-geometry-blender) — Blender scripts for sacred geometry generation
- [OpenClaw](https://github.com/openclaw/openclaw) — The local agent foundation

## License

MIT

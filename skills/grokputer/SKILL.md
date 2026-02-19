---
name: grokputer
description: Grok-powered hybrid AI agent — routes commands to local, cloud, or Blender agents
author: gonifola
version: 0.1.0
---

# Grokputer Skill

This skill adds hybrid agent capabilities to OpenClaw:

1. **Intent Router** — classifies natural language into LOCAL / CLOUD / BLENDER / CHAIN
2. **Cloud Bridge** — connects to 860+ apps via API (email, social, search, trading)
3. **Blender Bridge** — sends bpy commands to a running Blender instance
4. **Chain Executor** — handles multi-step commands across agents

## Usage

Once installed, just talk naturally:

- "Make a stellated dodecahedron and post a render to Twitter"
- "Check my email for anything from Elizabeth about the interior design project"
- "Open Blender, create a flower of life, export STL, slice for my Ender 3"
- "Buy 0.5 SOL worth of $BONK if it dips below 0.00001"

Grokputer figures out which agent handles each part.

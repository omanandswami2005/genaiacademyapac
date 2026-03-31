---
title: "Travel Guide Agent — Gen AI Academy APAC"
subtitle: "ADK Agent with MCP Integration | Cloud Run Deployment"
author: "Omanand Swami"
---

# Slide 1: Project Overview

## Travel Guide Agent 🌍

**An AI-powered travel assistant built with Google ADK + MCP**

### What it does
- Answers questions about **any country, city, or landmark** in the world
- Provides **real-time data** from REST Countries API and Wikipedia
- Generates **practical travel tips** based on country data

### Tech Stack
| Component | Technology |
|-----------|-----------|
| AI Framework | Google Agent Development Kit (ADK) |
| LLM | Gemini 2.5 Flash (Vertex AI) |
| Protocol | Model Context Protocol (MCP) |
| Deployment | Google Cloud Run |
| Language | Python 3.12 |

---

# Slide 2: Architecture & MCP Integration

## How It Works

```
User Query: "Tell me about Japan"
         │
         ▼
┌─────────────────────────────┐
│  ADK Travel Guide Agent     │
│  (Gemini 2.5 Flash)         │
│                             │
│  1. Understands user intent │
│  2. Selects right MCP tools │
│  3. Combines data into      │
│     rich response           │
└────────────┬────────────────┘
             │ MCP (stdio)
             ▼
┌─────────────────────────────┐
│  Travel MCP Server          │
│                             │
│  Tools exposed via MCP:     │
│  • get_country_info()       │
│    → REST Countries API     │
│  • get_wikipedia_summary()  │
│    → Wikipedia API          │
│  • get_travel_advisory()    │
│    → Generated tips         │
└─────────────────────────────┘
```

### Key Design Decisions
- **MCP separates AI reasoning from data access** — the agent focuses on understanding & responding while the MCP server handles all external API calls
- **Stdio transport** — MCP server runs as a subprocess for simplicity and security
- **Synchronous agent definition** — required for Cloud Run deployment compatibility

---

# Slide 3: Outcomes & Demo

## Results

### Example Interaction
> **User**: "Tell me about visiting France"
>
> **Agent**: Uses `get_country_info("France")` → gets capital, population, languages, currencies
> Then `get_wikipedia_summary("France")` → gets rich historical context
> Then `get_travel_advisory("France")` → gets practical tips
>
> Combines everything into a comprehensive, engaging travel guide response

### What I Learned
1. **MCP standardizes AI-to-tool communication** — plug-and-play external data sources
2. **ADK makes agent development feel like software development** — clear structure, tooling, deployment
3. **Cloud Run provides seamless serverless deployment** for ADK agents

### Deployment
- **Cloud Run URL**: [link to be added]
- **GitHub Repo**: [link to be added]

### Future Enhancements
- Add flight/hotel price checking via additional MCP tools
- Multi-language support
- Voice interaction via Gemini Live API

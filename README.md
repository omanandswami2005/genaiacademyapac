# Travel Guide Agent — Gen AI Academy APAC

> **Track 2: MCP + ADK** | Submitted for Gen AI Academy APAC Hackathon

An AI-powered Travel Guide Agent built with **Google Agent Development Kit (ADK)** and **Gemini 2.5 Flash**, connected to a custom **MCP server** that fetches real-time country data and Wikipedia summaries.

**Live Demo:** https://travel-guide-agent-rnedu666qq-uc.a.run.app/dev-ui/

---

## How It Works

The agent uses **Model Context Protocol (MCP)** — a standardized way for AI agents to connect to external tools and data sources. When you ask it about a country, it:

1. Calls `get_country_info` → REST Countries API (population, capital, currency, languages)
2. Calls `get_wikipedia_summary` → Wikipedia REST API (rich contextual description)
3. Calls `get_travel_advisory` → generates region-specific tips from the country data
4. Combines all results into a helpful, formatted response

## Architecture

```
┌──────────────────────────────────────┐
│   You (User)                         │
│   "Tell me about Japan"              │
└──────────────┬───────────────────────┘
               │ HTTP / WebSocket
               ▼
┌──────────────────────────────────────┐
│   ADK Travel Guide Agent             │
│   Model: Gemini 2.5 Flash (Vertex AI)│
│   Hosted: Google Cloud Run           │
└──────────────┬───────────────────────┘
               │ MCP — stdio transport
               ▼
┌──────────────────────────────────────┐
│   Travel MCP Server                  │
│                                      │
│  • get_country_info(country_name)    │
│  • get_wikipedia_summary(topic)      │
│  • get_travel_advisory(country_info) │
└──────┬───────────────┬───────────────┘
       │ HTTPS         │ HTTPS
       ▼               ▼
┌─────────────┐  ┌─────────────────────┐
│ REST        │  │ Wikipedia REST API  │
│ Countries   │  │ /page/summary/{topic}│
│ API v3.1    │  └─────────────────────┘
└─────────────┘
```

## Features

- **Real-time country data** — capital, population, languages, currencies, timezones, borders
- **Wikipedia summaries** — rich contextual descriptions for any place or landmark
- **Travel advisories** — region-specific tips (visas, transport passes, vaccinations, etc.)
- **Clean MCP architecture** — agent reasoning is fully decoupled from data retrieval
- **ADK web UI** — built-in chat interface served by Cloud Run

## Tech Stack

| Component | Technology |
|-----------|-----------|
| AI Agent | Google ADK (LlmAgent) |
| LLM | Gemini 2.5 Flash via Vertex AI |
| Tool Protocol | MCP (Model Context Protocol) — stdio |
| Data Sources | REST Countries API, Wikipedia REST API |
| Serving | FastAPI + uvicorn |
| Deployment | Google Cloud Run (us-central1) |
| GCP Project | genaiacademyapac-omni |

## Project Structure

```
genaiacademyapac/
├── travel_guide_agent/        # ADK Agent package
│   ├── __init__.py
│   └── agent.py               # LlmAgent with McpToolset
├── mcp_server/
│   └── travel_mcp_server.py   # Custom MCP server — 3 tools
├── main.py                    # FastAPI entry point (Cloud Run)
├── Dockerfile                 # python:3.12-slim container
├── .dockerignore
├── requirements.txt
└── README.md
```

## Local Development

### Prerequisites

- Python 3.12+
- Google Cloud SDK (`gcloud auth application-default login`)

### Setup

```bash
git clone <repo-url>
cd genaiacademyapac

python -m venv .venv
source .venv/bin/activate      # Linux/Mac
# .venv\Scripts\activate       # Windows

pip install -r requirements.txt

export GOOGLE_CLOUD_PROJECT=genaiacademyapac-omni
export GOOGLE_CLOUD_LOCATION=us-central1
export GOOGLE_GENAI_USE_VERTEXAI=True
```

### Run locally

```bash
# ADK web UI at http://localhost:8000/dev-ui/
adk web

# Or run the FastAPI server directly
python main.py
```

### Example queries

```
Tell me about Japan
What's the capital of Brazil and what should I visit?
Give me a travel guide for France
What languages do they speak in Switzerland?
Tell me about the Eiffel Tower
```

## Deployment

```bash
gcloud run deploy travel-guide-agent \
  --source . \
  --region us-central1 \
  --project genaiacademyapac-omni \
  --allow-unauthenticated \
  --memory=1Gi \
  --timeout=300 \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=genaiacademyapac-omni,GOOGLE_CLOUD_LOCATION=us-central1,GOOGLE_GENAI_USE_VERTEXAI=True"
```

**Live URL:** https://travel-guide-agent-rnedu666qq-uc.a.run.app

## API Usage

```bash
# Create a session
curl -X POST https://travel-guide-agent-rnedu666qq-uc.a.run.app/apps/travel_guide_agent/users/{user_id}/sessions \
  -H "Content-Type: application/json" -d '{}'

# Send a message (returns SSE stream)
curl -X POST https://travel-guide-agent-rnedu666qq-uc.a.run.app/run_sse \
  -H "Content-Type: application/json" \
  -d '{"app_name":"travel_guide_agent","user_id":"{user_id}","session_id":"{session_id}","new_message":{"role":"user","parts":[{"text":"Tell me about Japan"}]}}'
```

## License

MIT

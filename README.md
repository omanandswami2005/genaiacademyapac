# Travel Guide Agent — Gen AI Academy APAC

An AI-powered Travel Guide Agent built with **Google Agent Development Kit (ADK)** that uses **Model Context Protocol (MCP)** to connect to external data sources — a custom MCP server providing real-time country information and Wikipedia summaries.

## Architecture

```
┌──────────────────────────┐
│   ADK Travel Guide Agent │
│   (Gemini 2.5 Flash)     │
│                          │
│  "Ask me about any       │
│   country or place!"     │
└──────────┬───────────────┘
           │ MCP (stdio)
           ▼
┌──────────────────────────┐
│   Travel MCP Server      │
│                          │
│  Tools:                  │
│  • get_country_info()    │
│  • get_wikipedia_summary │
│  • get_travel_advisory() │
└──────────┬───────────────┘
           │ HTTP
           ▼
┌──────────────────────────┐
│  External APIs           │
│  • REST Countries API    │
│  • Wikipedia API         │
└──────────────────────────┘
```

## Features

- **Country Information**: Get detailed info about any country including capital, population, languages, currencies, and more via REST Countries API
- **Wikipedia Summaries**: Fetch Wikipedia summaries about any topic — cities, landmarks, cultures, history
- **Travel Advisory**: Get travel tips based on country region and details
- **MCP Integration**: Clean separation between AI reasoning (ADK Agent) and data retrieval (MCP Server)

## Tech Stack

- **Google ADK** — Agent Development Kit for building the AI agent
- **Gemini 2.5 Flash** — LLM powering the agent via Vertex AI
- **MCP (Model Context Protocol)** — Standardized protocol connecting agent to tools
- **Cloud Run** — Serverless deployment on Google Cloud
- **Python 3.12** — Runtime

## Project Structure

```
genaiacademyapac/
├── travel_guide_agent/        # ADK Agent package
│   ├── __init__.py
│   └── agent.py               # Agent definition with MCP toolset
├── mcp_server/
│   └── travel_mcp_server.py   # Custom MCP server with travel tools
├── main.py                    # FastAPI entry point for Cloud Run
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container image for Cloud Run
├── .gitignore
└── README.md
```

## Local Development

### Prerequisites

- Python 3.12+
- Node.js (for npx, if using community MCP servers)
- Google Cloud SDK (gcloud CLI)

### Setup

```bash
# Clone the repo
git clone <repo-url>
cd genaiacademyapac

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GOOGLE_CLOUD_PROJECT=genaiacademyapac-omni
export GOOGLE_CLOUD_LOCATION=us-central1
export GOOGLE_GENAI_USE_VERTEXAI=True
```

### Run locally

```bash
# Using ADK web UI
adk web

# Or run the FastAPI server directly
python main.py
```

### Test the agent

Ask questions like:
- "Tell me about Japan"
- "What's the capital of Brazil and what are the must-see places?"
- "Give me a travel guide for visiting France"
- "What languages do they speak in Switzerland?"

## Deployment

```bash
# Deploy to Cloud Run
gcloud run deploy travel-guide-agent \
  --source . \
  --region us-central1 \
  --project genaiacademyapac-omni \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=genaiacademyapac-omni,GOOGLE_CLOUD_LOCATION=us-central1,GOOGLE_GENAI_USE_VERTEXAI=True"
```

## Cloud Run URL

> **Live:** https://travel-guide-agent-rnedu666qq-uc.a.run.app

## License

MIT

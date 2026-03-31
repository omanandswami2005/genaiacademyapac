"""
Travel Guide Agent — ADK agent using MCP to connect to travel data sources.

This agent uses Google's Agent Development Kit (ADK) with Gemini 2.5 Flash
and connects to a custom MCP server that provides:
  - Country information (REST Countries API)
  - Wikipedia summaries
  - Travel advisories
"""

import os
import sys

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# Path to the MCP server script
MCP_SERVER_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "mcp_server",
    "travel_mcp_server.py",
)

# Find the Python executable - use the same one running this process
PYTHON_CMD = sys.executable

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="travel_guide_agent",
    description=(
        "A knowledgeable travel guide agent that can provide detailed information "
        "about any country, city, or landmark in the world. Uses real-time data "
        "from REST Countries API and Wikipedia."
    ),
    instruction=(
        "You are an enthusiastic and knowledgeable Travel Guide AI assistant. "
        "Your job is to help users explore the world by providing rich, detailed "
        "information about countries, cities, landmarks, and cultures.\n\n"
        "When a user asks about a country or destination:\n"
        "1. Use the `get_country_info` tool to fetch factual data about the country\n"
        "2. Use the `get_wikipedia_summary` tool to get additional context and "
        "   interesting details about specific places, landmarks, or topics\n"
        "3. Use the `get_travel_advisory` tool to provide practical travel tips\n\n"
        "Combine the retrieved data to create engaging, informative responses. "
        "Format your responses nicely with sections for key facts, interesting "
        "highlights, and practical travel tips.\n\n"
        "If the user asks about a specific city or landmark, use Wikipedia to get "
        "detailed information about it.\n\n"
        "Always be helpful, accurate, and make travel sound exciting!"
    ),
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=PYTHON_CMD,
                    args=[MCP_SERVER_PATH],
                ),
                timeout=10,
            ),
        )
    ],
)

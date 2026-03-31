"""
Travel MCP Server — Exposes travel data tools via Model Context Protocol.

Tools:
  - get_country_info: Fetches country details from REST Countries API
  - get_wikipedia_summary: Fetches Wikipedia summary for any topic
  - get_travel_advisory: Generates travel tips based on country data
"""

import asyncio
import json
import sys

import httpx
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as mcp_types


app = Server("travel-data-mcp-server")


async def _fetch_country_info(country_name: str) -> dict:
    """Fetch country information from REST Countries API."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(
            f"https://restcountries.com/v3.1/name/{country_name}",
            params={"fullText": "false"},
        )
        if resp.status_code != 200:
            return {"error": f"Country '{country_name}' not found (HTTP {resp.status_code})"}

        data = resp.json()
        if not data:
            return {"error": f"No results for '{country_name}'"}

        country = data[0]
        return {
            "name": country.get("name", {}).get("common", country_name),
            "official_name": country.get("name", {}).get("official", ""),
            "capital": country.get("capital", ["N/A"]),
            "region": country.get("region", "N/A"),
            "subregion": country.get("subregion", "N/A"),
            "population": country.get("population", 0),
            "area_km2": country.get("area", 0),
            "languages": country.get("languages", {}),
            "currencies": {
                k: v.get("name", "") for k, v in country.get("currencies", {}).items()
            },
            "timezones": country.get("timezones", []),
            "flag_emoji": country.get("flag", ""),
            "borders": country.get("borders", []),
            "continent": country.get("continents", []),
            "maps_url": country.get("maps", {}).get("googleMaps", ""),
        }


async def _fetch_wikipedia_summary(topic: str) -> dict:
    """Fetch Wikipedia summary for a given topic."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(
            "https://en.wikipedia.org/api/rest_v1/page/summary/"
            + topic.replace(" ", "_"),
        )
        if resp.status_code != 200:
            return {"error": f"Wikipedia article for '{topic}' not found"}

        data = resp.json()
        return {
            "title": data.get("title", topic),
            "summary": data.get("extract", "No summary available."),
            "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
            "thumbnail": data.get("thumbnail", {}).get("source", ""),
            "description": data.get("description", ""),
        }


def _generate_travel_advisory(country_info: dict) -> dict:
    """Generate travel tips based on country data."""
    name = country_info.get("name", "Unknown")
    region = country_info.get("region", "Unknown")
    languages = country_info.get("languages", {})
    currencies = country_info.get("currencies", {})
    population = country_info.get("population", 0)

    lang_list = list(languages.values()) if languages else ["Unknown"]
    currency_list = list(currencies.values()) if currencies else ["Unknown"]

    tips = [
        f"Welcome to {name}! Here are some travel tips:",
        f"- Located in {region} ({country_info.get('subregion', 'N/A')})",
        f"- Official language(s): {', '.join(lang_list)}",
        f"- Currency: {', '.join(currency_list)}",
        f"- Population: {population:,}",
    ]

    if population > 100_000_000:
        tips.append("- This is a very populous country, expect bustling cities!")
    elif population < 1_000_000:
        tips.append("- A smaller nation — great for intimate travel experiences!")

    if region == "Europe":
        tips.append("- Tip: Consider a Eurail pass if visiting multiple European countries.")
    elif region == "Asia":
        tips.append("- Tip: Check visa requirements well in advance for Asian countries.")
    elif region == "Africa":
        tips.append("- Tip: Check vaccination requirements before traveling.")
    elif region in ("Americas", "South America", "North America"):
        tips.append("- Tip: The Americas offer incredible geographical diversity!")
    elif region == "Oceania":
        tips.append("- Tip: Perfect for nature lovers and beach enthusiasts!")

    tips.append(f"- Google Maps: {country_info.get('maps_url', 'N/A')}")

    return {"country": name, "advisory": "\n".join(tips)}


# --- MCP Tool Handlers ---

@app.list_tools()
async def list_tools() -> list[mcp_types.Tool]:
    """Advertise available travel tools."""
    return [
        mcp_types.Tool(
            name="get_country_info",
            description=(
                "Get detailed information about a country including capital, "
                "population, languages, currencies, region, area, timezones, "
                "and borders. Uses the REST Countries API."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "country_name": {
                        "type": "string",
                        "description": "Name of the country to look up (e.g., 'Japan', 'Brazil', 'France')",
                    }
                },
                "required": ["country_name"],
            },
        ),
        mcp_types.Tool(
            name="get_wikipedia_summary",
            description=(
                "Get a Wikipedia summary about any topic — countries, cities, "
                "landmarks, cultures, historical events, etc."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic to search on Wikipedia (e.g., 'Eiffel Tower', 'Tokyo', 'Great Wall of China')",
                    }
                },
                "required": ["topic"],
            },
        ),
        mcp_types.Tool(
            name="get_travel_advisory",
            description=(
                "Get travel tips and advisory for a specific country. "
                "Provides language, currency, regional tips, and practical advice."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "country_name": {
                        "type": "string",
                        "description": "Name of the country to get travel tips for",
                    }
                },
                "required": ["country_name"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[mcp_types.Content]:
    """Handle tool execution requests from MCP clients."""
    try:
        if name == "get_country_info":
            country_name = arguments.get("country_name", "")
            if not country_name:
                return [mcp_types.TextContent(type="text", text=json.dumps({"error": "country_name is required"}))]
            result = await _fetch_country_info(country_name)

        elif name == "get_wikipedia_summary":
            topic = arguments.get("topic", "")
            if not topic:
                return [mcp_types.TextContent(type="text", text=json.dumps({"error": "topic is required"}))]
            result = await _fetch_wikipedia_summary(topic)

        elif name == "get_travel_advisory":
            country_name = arguments.get("country_name", "")
            if not country_name:
                return [mcp_types.TextContent(type="text", text=json.dumps({"error": "country_name is required"}))]
            country_info = await _fetch_country_info(country_name)
            if "error" in country_info:
                result = country_info
            else:
                result = _generate_travel_advisory(country_info)

        else:
            result = {"error": f"Unknown tool: {name}"}

        return [mcp_types.TextContent(type="text", text=json.dumps(result, indent=2))]

    except Exception as e:
        error_msg = json.dumps({"error": f"Tool execution failed: {str(e)}"})
        return [mcp_types.TextContent(type="text", text=error_msg)]


async def run_server():
    """Run the MCP server over stdio."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=app.name,
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    print("Starting Travel MCP Server...", file=sys.stderr)
    asyncio.run(run_server())

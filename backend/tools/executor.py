from tools.utils import summarize_url
import logging
from tools.hn import fetch_hn_digest

logger = logging.getLogger(__name__)


async def execute_tool(name: str, inputs: dict) -> str:
    logger.info("Executing tool: %s with inputs: %s", name, inputs)

    match name:
        case "get_hn_digest":
            return await fetch_hn_digest(inputs.get("limit", 10))
        case "summarize_url":
            return await summarize_url(url=inputs.get("url"))

        case _:
            logger.warning("Unknown tool: %s", name)
            return f"Error: unknown tool '{name}'"

from asyncio import Queue
from services.models import LLMMessage
import json
import logging
import httpx
from tools.registry import TOOLS
from tools.executor import execute_tool

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def stream_llm(
        self,
        model: str | None = None,
        temperature: float | None = None,
        messages: list[LLMMessage] | None = None,
        title_queue: Queue[str] | None = None,
    ):
        logger.info("Sending request to %s", self.base_url)

        model = model or "qwen3.5-9B"
        temperature = temperature if temperature is not None else 0.9

        message = None
        if messages is None:
            messages = []

        if len(messages) > 0:
            logger.info(messages[-1].content)
            title_payload = {
                "model": "qwen3.5-9B",
                "messages": [
                    {
                        "role": "user",
                        "content": f"""
                            Summarize the intent of {messages[-1].content}.
                            Use 3 words top.
                        """,
                    }
                ],
                "chat_template_kwargs": {"enable_thinking": False},
                "stream": False,
                "temperature": 0.9,
            }
            async with httpx.AsyncClient(timeout=30) as client:
                r = await client.post(self.base_url, json=title_payload)
                response = r.json()
                logger.debug("LLM raw response: %s", json.dumps(response, indent=2))

            logger.info(r)
            message = response["choices"][0]["message"]

        if message and message["content"] and title_queue:
            await title_queue.put(message["content"])

        payload = {
            "model": model,
            "messages": [m.model_dump(exclude_none=True) for m in messages or []],
            "chat_template_kwargs": {"enable_thinking": False},
            "stream": False,
            "temperature": temperature,
            "tools": TOOLS,
        }

        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(self.base_url, json=payload)
            response = r.json()
            logger.debug("LLM raw response: %s", json.dumps(response, indent=2))

        message = response["choices"][0]["message"]

        if not message.get("tool_calls"):
            yield message["content"]
            return

        tool_call = message["tool_calls"][0]
        tool_name = tool_call["function"]["name"]
        tool_inputs = json.loads(tool_call["function"]["arguments"])

        logger.info("Tool call: %s with %s", tool_name, tool_inputs)

        tool_result = await execute_tool(tool_name, tool_inputs)

        messages = (messages or []) + [
            LLMMessage(
                role="assistant",
                tool_calls=[tool_call],
            ),
            LLMMessage(
                role="tool",
                tool_call_id=tool_call["id"],
                content=tool_result,
            ),
        ]

        payload["messages"] = [m.model_dump(exclude_none=True) for m in messages]
        payload["stream"] = True
        payload.pop("tools")

        async with httpx.AsyncClient(timeout=30) as client:
            async with client.stream("POST", self.base_url, json=payload) as response:
                async for line in response.aiter_lines():
                    if not line or not line.startswith("data: "):
                        continue
                    data_str = line[6:]
                    if data_str == "[DONE]":
                        break
                    data = json.loads(data_str)
                    delta = data["choices"][0]["delta"].get("content")
                    if delta:
                        yield delta

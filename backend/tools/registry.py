TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_hn_digest",
            "description": (
                "Fetches HackerNews front page and summarizes top stories. "
                "Use when the user asks about tech news, HackerNews, what's trending, "
                "or wants a news summary."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of top stories to fetch, default 10",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_url",
            "description": ("Fetches an url and summarize the content of the web page"),
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "url to summarize",
                    }
                },
                "required": [],
            },
        },
    },
]

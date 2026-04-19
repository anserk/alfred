import httpx
import logging

logger = logging.getLogger(__name__)


async def fetch_hn_digest(limit: int = 10) -> str:
    logger.info("Fetching HN top %d stories", limit)

    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get("https://hacker-news.firebaseio.com/v0/topstories.json")
        r.raise_for_status()
        ids = r.json()[:limit]

        stories = []
        for story_id in ids:
            r = await client.get(
                f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            )
            r.raise_for_status()
            story = r.json()
            stories.append(
                {
                    "title": story.get("title"),
                    "url": story.get("url", ""),
                    "score": story.get("score", 0),
                    "comments": story.get("descendants", 0),
                }
            )

    lines = [
        f"- {s['title']} (score: {s['score']}, comments: {s['comments']}) {s['url']}"
        for s in stories
    ]

    return "\n".join(lines)

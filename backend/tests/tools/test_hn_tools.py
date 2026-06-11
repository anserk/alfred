import httpx
import pytest
import respx
from httpx import Response

from tools.hn import fetch_hn_digest


@pytest.mark.asyncio
@respx.mock
async def test_fetch_hn_returns_empty_string_when_no_top_stories():
    respx.get("https://hacker-news.firebaseio.com/v0/topstories.json").mock(
        return_value=Response(200, json=[])
    )
    result = await fetch_hn_digest(limit=2)
    assert result == ""


@pytest.mark.asyncio
@respx.mock
async def test_fetch_hn_digest_raises_when_topstories_request_fails():
    respx.get("https://hacker-news.firebaseio.com/v0/topstories.json").mock(
        return_value=Response(status_code=500, json="error")
    )

    with pytest.raises(httpx.HTTPStatusError):
        await fetch_hn_digest(limit=2)


@pytest.mark.asyncio
@respx.mock
async def test_fetch_hn_digest_defaults_missing_optional_story_fields():
    respx.get("https://hacker-news.firebaseio.com/v0/topstories.json").mock(
        return_value=Response(200, json=[101])
    )

    respx.get("https://hacker-news.firebaseio.com/v0/item/101.json").mock(
        return_value=Response(
            status_code=200,
            json={
                "title": "First story",
                "url": "https://example.com/first",
            },
        )
    )

    result = await fetch_hn_digest(limit=1)

    assert result == "- First story (score: 0, comments: 0) https://example.com/first"


@pytest.mark.asyncio
@respx.mock
async def test_fetch_hn_digest_skips_stories_with_missing_required_fields():
    respx.get("https://hacker-news.firebaseio.com/v0/topstories.json").mock(
        return_value=Response(200, json=[101, 102, 103])
    )

    respx.get("https://hacker-news.firebaseio.com/v0/item/101.json").mock(
        return_value=Response(
            200,
            json={
                "title": "First story",
                "url": "https://example.com/first",
                "score": 42,
                "descendants": 7,
            },
        )
    )

    respx.get("https://hacker-news.firebaseio.com/v0/item/102.json").mock(
        return_value=Response(
            200,
            json={
                "url": "https://example.com/second",
                "score": 13,
                "descendants": 2,
            },
        )
    )

    respx.get("https://hacker-news.firebaseio.com/v0/item/103.json").mock(
        return_value=Response(
            200,
            json={
                "title": "Second story",
                "score": 13,
                "descendants": 2,
            },
        )
    )

    result = await fetch_hn_digest(limit=3)

    assert result == "- First story (score: 42, comments: 7) https://example.com/first"


@pytest.mark.asyncio
@respx.mock
async def test_fetch_hn_digest_raises_when_story_request_fails():
    respx.get("https://hacker-news.firebaseio.com/v0/topstories.json").mock(
        return_value=Response(200, json=[101])
    )

    respx.get("https://hacker-news.firebaseio.com/v0/item/101.json").mock(
        return_value=Response(
            status_code=500,
            json={},
        )
    )

    with pytest.raises(httpx.HTTPStatusError):
        await fetch_hn_digest(limit=1)


@pytest.mark.asyncio
@respx.mock
async def test_fetch_hn_digest_formats_limited_top_stories():
    respx.get("https://hacker-news.firebaseio.com/v0/topstories.json").mock(
        return_value=Response(200, json=[101, 102, 103])
    )

    respx.get("https://hacker-news.firebaseio.com/v0/item/101.json").mock(
        return_value=Response(
            200,
            json={
                "title": "First story",
                "url": "https://example.com/first",
                "score": 42,
                "descendants": 7,
            },
        )
    )

    respx.get("https://hacker-news.firebaseio.com/v0/item/102.json").mock(
        return_value=Response(
            200,
            json={
                "title": "Second story",
                "url": "https://example.com/second",
                "score": 13,
                "descendants": 2,
            },
        )
    )

    result = await fetch_hn_digest(limit=2)

    assert result == "\n".join(
        [
            "- First story (score: 42, comments: 7) https://example.com/first",
            "- Second story (score: 13, comments: 2) https://example.com/second",
        ]
    )

    requested_paths = [call.request.url.path for call in respx.calls]

    assert "/v0/item/101.json" in requested_paths
    assert "/v0/item/102.json" in requested_paths
    assert "/v0/item/103.json" not in requested_paths

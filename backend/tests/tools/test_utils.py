import httpx
import pytest
import respx
from httpx import Response
from tools.utils import summarize_url


@pytest.mark.asyncio
@respx.mock
async def test_fetch_hn_returns_empty_string_when_no_top_stories():
    url = "http://example.com/story/1"
    route = respx.get(url=url).mock(
        return_value=Response(200, text=("some text, should be returned by this call"))
    )
    result = await summarize_url(url)

    assert route.called
    assert isinstance(result, str)
    assert result

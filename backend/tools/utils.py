from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from httpx import URL
import httpx
import logging
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

logger = logging.getLogger(__name__)

LANGUAGE = "english"
SENTENCES_COUNT = 10


async def summarize_url(url: URL | str):
    logger.info("Summary for %s...", url)

    headers = {"User-Agent": "alfred/1.0"}

    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.get(str(url))
        response.raise_for_status()
        text = response.text

    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))

    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    lines = []
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        logger.info(sentence)
        lines.append(str(sentence))

    return "\n".join(lines)

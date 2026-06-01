import httpx
import os

URIMALSAEM_API_KEY = os.getenv("URIMALSAEM_API_KEY", "")
BASE_URL = "https://opendict.korean.go.kr/api/search"


async def get_classical_words(keywords: list[str]) -> dict[str, str]:
    """키워드 목록을 우리말샘 API에 검색해서 고어 치환 목록 반환"""
    substitutions = {}

    async with httpx.AsyncClient() as client:
        for word in keywords:
            classical = await _search_word(client, word)
            if classical:
                substitutions[word] = classical

    return substitutions


async def _search_word(client: httpx.AsyncClient, word: str) -> str | None:
    try:
        response = await client.get(
            BASE_URL,
            params={
                "key": URIMALSAEM_API_KEY,
                "q": word,
                "req_type": "json",
                "part": "word",
                "sort": "popular",
                "num": 1,
            },
            timeout=5.0,
        )
        data = response.json()
        items = data.get("channel", {}).get("item", [])
        if items:
            return items[0].get("word")
    except Exception:
        pass
    return None

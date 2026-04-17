import time
import requests

NOMINATIM_BASE_URL = "https://nominatim.openstreetmap.org"
CACHE_TTL_SECONDS = 300

_cache: dict[str, tuple[float, list[dict]]] = {}


def search_places(query: str, limit: int = 5) -> list[dict]:
    normalized_query = query.strip().lower()

    cached = _cache.get(normalized_query)
    now = time.time()

    if cached:
        timestamp, data = cached
        if now - timestamp < CACHE_TTL_SECONDS:
            return data

    response = requests.get(
        f"{NOMINATIM_BASE_URL}/search",
        params={
            "q": query,
            "format": "jsonv2",
            "limit": limit,
            "countrycodes": "br",
        },
        headers={
            "User-Agent": "mobility-nav/1.0",
            "Accept-Language": "pt-BR",
        },
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    normalized_results = []
    for item in data:
        normalized_results.append(
            {
                "name": item.get("display_name", "Unknown place"),
                "lat": float(item["lat"]),
                "lng": float(item["lon"]),
            }
        )

    _cache[normalized_query] = (now, normalized_results)
    return normalized_results

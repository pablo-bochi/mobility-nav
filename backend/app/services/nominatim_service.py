import requests

NOMINATIM_BASE_URL = "https://nominatim.openstreetmap.org"


def search_places(query: str, limit: int = 5) -> list[dict]:
    response = requests.get(
        f"{NOMINATIM_BASE_URL}/search",
        params={
            "q": query,
            "format": "jsonv2",
            "limit": limit,
        },
        headers={
            "User-Agent": "mobility-nav/1.0"
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

    return normalized_results

import json
from pathlib import Path

from lastfrontier.validation import verify_city


JSON_FILE = (
    Path(__file__).resolve().parent
    / "data"
    / "custom_cities.json"
)


def load_custom_cities():
    with open(JSON_FILE, "r") as file:
        return json.load(file)


def save_custom_cities(cities):
    with open(JSON_FILE, "w") as file:
        json.dump(cities, file, indent=2)


def clean_cities(limit: int = None):
    city_list = load_custom_cities()

    unique_cities = []
    seen = set()

    for city in city_list:
        normalized = city.strip().casefold()

        if normalized in seen:
            continue

        if not verify_city(city):
            continue

        seen.add(normalized)
        unique_cities.append(city)

    if limit is not None:
        unique_cities = unique_cities[:limit]

    save_custom_cities(unique_cities)

    return unique_cities
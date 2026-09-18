from dataclasses import dataclass
from getpass import getpass
from pathlib import Path
import os

from dotenv import load_dotenv


CONFIG_DIR = Path.home() / ".config" / "lastfrontier"
ENV_FILE = CONFIG_DIR / ".env"


@dataclass
class Config:
    open_weather_api_key: str
    census_api: str
    alaska_511_api: str
    legiscan_api: str
    db_host: str
    db_name: str
    db_user: str
    db_pass: str
    db_port: int


def configure():
    CONFIG_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("\nLastFrontier configuration")
    print("--------------------------")

    open_weather_api_key = getpass("OpenWeather API key: ")
    census_api = getpass("Census API key: ")
    alaska_511_api = getpass("Alaska 511 API key: ")
    legiscan_api = getpass("Legiscan API key: ")

    db_host = input("Database host [localhost]: ").strip() or "localhost"
    db_name = input("Database name [lastfrontier]: ").strip() or "lastfrontier"
    db_user = input("Database user [lastfrontier]: ").strip() or "lastfrontier"
    db_pass = getpass("Database password: ")
    db_port = input("Database port [5432]: ").strip() or "5432"

    ENV_FILE.write_text(
        f"""OPEN_WEATHER_API_KEY={open_weather_api_key}
CENSUS_API={census_api}
ALASKA_511_API={alaska_511_api}
LEGISCAN_API={legiscan_api}
DB_HOST={db_host}
DB_NAME={db_name}
DB_USER={db_user}
DB_PASS={db_pass}
DB_PORT={db_port}
""",
        encoding="utf-8",
    )

    print(f"\nConfiguration saved to:\n{ENV_FILE}")


def update_config(key, value):

    if not ENV_FILE.exists():

        raise RuntimeError(
            "LastFrontier is not configured.\n"
            "Run:\n\n"
            "    lastfrontier configure\n"
        )

    lines = ENV_FILE.read_text(
        encoding="utf-8"
    ).splitlines()

    for index, line in enumerate(lines):

        if line.startswith(f"{key}="):

            lines[index] = f"{key}={value}"

            break

    else:

        lines.append(f"{key}={value}")

    ENV_FILE.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def load_config():

    if not ENV_FILE.exists():

        raise RuntimeError(
            "LastFrontier is not configured.\n"
            "Run:\n\n"
            "    lastfrontier configure\n"
        )

    load_dotenv(
        ENV_FILE,
        override=True,
    )

    required = [
        "OPEN_WEATHER_API_KEY",
        "CENSUS_API",
        "ALASKA_511_API",
        "LEGISCAN_API",
        "DB_HOST",
        "DB_NAME",
        "DB_USER",
        "DB_PASS",
        "DB_PORT",
    ]

    missing = [name for name in required if not os.getenv(name)]

    if missing:

        raise RuntimeError(
            "Missing configuration values:\n"
            + "\n".join(
                f"  - {name}"
                for name in missing
            )
        )

    try:
        db_port = int(os.environ["DB_PORT"])

    except ValueError:
        raise RuntimeError("DB_PORT must be an integer.")

    return Config(
        open_weather_api_key=os.environ["OPEN_WEATHER_API_KEY"],
        census_api=os.environ["CENSUS_API"],
        alaska_511_api=os.environ["ALASKA_511_API"],
        legiscan_api=os.environ["LEGISCAN_API"],
        db_host=os.environ["DB_HOST"],
        db_name=os.environ["DB_NAME"],
        db_user=os.environ["DB_USER"],
        db_pass=os.environ["DB_PASS"],
        db_port=db_port,
    )
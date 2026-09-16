import argparse
import sys
from getpass import getpass

from lastfrontier.config import (
    configure,
    load_config,
    update_config
)

from lastfrontier.tables_config import (
    required_table_create,
    required_table_insert,
)

def add_table_parser(subparsers, command, table_name, help_text):
    table_parser = subparsers.add_parser(
        command,
        help=help_text,
        description=help_text,
    )

    table_parser.set_defaults(
        table_name=table_name
    )


def main():

    parser = argparse.ArgumentParser(
        description=(
            "LastFrontier is a CLI package that allows users to create "
            "tables in PostgreSQL databases and ingest data directly "
            "from the command line."
        )
    )

    # Actions
    actions = parser.add_mutually_exclusive_group()

    actions.add_argument(
        "-c",
        "--create",
        action="store_true",
        help="create the table",
    )

    actions.add_argument(
        "-i",
        "--insert",
        action="store_true",
        help="insert data into the table",
    )

    # Tables
    subparsers = parser.add_subparsers(
        dest="command",
        metavar="<command>",
    )

    configure_parser = subparsers.add_parser(
        "configure",
        help="create or update LastFrontier configuration",
        description="Create or update LastFrontier configuration.",
    )

    configure_parser.add_argument(
        "--db-name",
    )

    configure_parser.add_argument(
        "--db-host",
    )

    configure_parser.add_argument(
        "--db-user",
    )

    configure_parser.add_argument(
        "--db-port",
        type=int,
    )

    configure_parser.add_argument(
        "--db-pass",
        action="store_true",
    )

    configure_parser.add_argument(
        "--open-weather-api-key",
        action="store_true",
    )

    configure_parser.add_argument(
        "--census-api",
        action="store_true",
    )

    configure_parser.add_argument(
        "--alaska-511-api",
        action="store_true",
    )

    add_table_parser(
        subparsers,
        command="alaskan-cities",
        table_name="alaskan_cities",
        help_text="Table containing city name, latitude, and longitude.",
    )

    add_table_parser(
        subparsers,
        command="air-pollution",
        table_name="air_pollution",
        help_text="Table containing air pollution data in select cities.",
    )

    add_table_parser(
        subparsers,
        command="weather",
        table_name="weather",
        help_text="Table containing current weather data in select cities.",
    )

    add_table_parser(
        subparsers,
        command="traffic-events",
        table_name="traffic_events",
        help_text="Table containing traffic events across Alaska.",
    )

    try:

        args = parser.parse_args()

        if args.command == "configure":

            updates = {
                "DB_NAME": args.db_name,
                "DB_HOST": args.db_host,
                "DB_USER": args.db_user,
                "DB_PORT": args.db_port,
            }

            if args.db_pass:
                updates["DB_PASS"] = getpass("Database password: ")

            if args.open_weather_api_key:
                updates["OPEN_WEATHER_API_KEY"] = getpass(
                    "OpenWeather API key: "
                )

            if args.census_api:
                updates["CENSUS_API"] = getpass(
                    "Census API key: "
                )

            if args.alaska_511_api:
                updates["ALASKA_511_API"] = getpass(
                    "Alaska 511 API key: "
                )

            updates = {
                key: value
                for key, value in updates.items()
                if value is not None
            }

            if not updates:

                configure()

            else:

                for key, value in updates.items():
                    update_config(
                        key,
                        str(value)
                    )

                print("\nConfiguration updated.")

            return

        if not args.create and not args.insert:

            parser.error(
                "one of -c/--create or -i/--insert is required"
            )

        config = load_config()

        if args.create:

            success, message = required_table_create(
                table_name=args.table_name,
                config=config
            )

            print(message)

            if not success:
                sys.exit(1)

        elif args.insert:

            success, message = required_table_insert(
                table_name=args.table_name,
                config=config
            )

            if message:
                print(message)

            if not success:
                sys.exit(1)

    except Exception:

        import traceback
        traceback.print_exc()

        sys.exit(1)

if __name__ == "__main__":
    main()
import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_FILE)

from lastfrontier.required_tables import (
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
    actions = parser.add_mutually_exclusive_group(required=True)

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
        required=True,
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

    try:

        args = parser.parse_args()

        if args.create:

            success, message = required_table_create(
                table_name=args.table_name
            )

            print(message)

            if not success:
                sys.exit(1)

        elif args.insert:

            success = required_table_insert(
                table_name=args.table_name
            )

            if not success:
                sys.exit(1)

    except Exception:

        import traceback
        traceback.print_exc()

        sys.exit(1)


if __name__ == "__main__":
    main()
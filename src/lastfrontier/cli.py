import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv
import os


ENV_FILE = (
    Path(__file__).resolve().parent.parent / ".env"
)

load_dotenv(ENV_FILE)

from lastfrontier.required_tables import (
    required_table_create,
    required_table_insert,
)

class CustomHelpFormatter(argparse.HelpFormatter):

    def add_usage(
        self,
        usage,
        actions,
        groups,
        prefix=None
    ):
        pass


def add_table_parser(
    subparsers,
    command,
    table_name,
    help_text
):

    table_parser = subparsers.add_parser(
        command,
        help=help_text,
        description=help_text,
        formatter_class=CustomHelpFormatter
    )

    actions = table_parser.add_mutually_exclusive_group(
        required=True
    )

    actions.add_argument(
        "--create",
        action="store_true",
        help="Create the table."
    )

    actions.add_argument(
        "--insert",
        action="store_true",
        help="Insert data into the table."
    )

    table_parser.set_defaults(
        table_name=table_name
    )


def main():

    parser = argparse.ArgumentParser(
        description="Digest data into database",
        formatter_class=CustomHelpFormatter
    )

    subparsers = parser.add_subparsers(
        dest="command",
        metavar="<command>",
        required=True
    )

    add_table_parser(
        subparsers,
        command="alaskan-cities",
        table_name="alaskan_cities",
        help_text="Create or update the alaskan_cities table."
    )

    add_table_parser(
        subparsers,
        command="air-pollution",
        table_name="air_pollution",
        help_text="Create or update the air_pollution table."
    )

    add_table_parser(
        subparsers,
        command="weather",
        table_name="weather",
        help_text="Create or update the weather table."
    )

    try:

        args = parser.parse_args()

        if args.create:

            success, message = required_table_create(
                table_name=args.table_name
            )

            if not success:
                print(message)
                sys.exit(1)

            print(message)

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

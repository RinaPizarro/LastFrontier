import argparse
import sys 

from lastfrontier.user_cities import all_cities_list
from lastfrontier.required_tables import (
    weather_table,
    air_pollution_table,
    cities_table,
)

def main():
    parser = argparse.ArgumentParser(
        description="Digest data into database"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand 1: add alaskan_cities table
    parser_one = subparsers.add_parser("alaskan-cities", help="Create and update alaskan_cities table in database")
    parser_one.set_defaults(func=cities_table)

    # Subcommand 2: add air_pollution_table
    parser_two = subparsers.add_parser("air-pollution", help="Creates and air_pollution table in database")
    parser_two.set_defaults(func=air_pollution_table)

    # Subcommand 3: add weather
    parser_three = subparsers.add_parser("weather", help="Creates and weather table in database")
    parser_three.set_defaults(func=weather_table)

    # Subcommand 4: update user_cities list
    parser_four = subparsers.add_parser("user-cities", help="Update list of selected cities")
    parser_four.set_defaults(func=all_cities_list)

    try:
        args = parser.parse_args()
        args.func()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1) 

if __name__ == "__main__":
    main()
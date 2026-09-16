import json

from datetime import datetime, timezone

# Get Universal Coordinated Time (UTC) at runtime
def universal_time():
    universal_time = datetime.now(timezone.utc)

    return universal_time.isoformat(
        timespec="seconds"
    )

def flatten_dict(
    output,
    parent_key="",
    separator="."
):
    columns = {}

    for key, value in output.items():

        if parent_key:
            new_key = f"{parent_key}{separator}{key}"
        else:
            new_key = key

        if isinstance(value, dict):

            columns.update(
                flatten_dict(
                    output=value,
                    parent_key=new_key,
                    separator=separator
                )
            )

        elif isinstance(value, list):

            columns[new_key] = json.dumps(
                value,
                ensure_ascii=False
            )

        else:

            columns[new_key] = value

    return columns

# Retrieve column names from JSON dictionary
def output_headers_list(output):
    columns_headers = []

    columns_headers.append("time_utc")

    flattened_output = flatten_dict(
        output=output
    )

    for key in flattened_output.keys():
        columns_headers.append(key)

    return columns_headers

# Retrieve column values from JSON dictionary
def output_values_list(output):
    column_values = []

    column_values.append(
        universal_time()
    )

    flattened_output = flatten_dict(
        output=output
    )

    for value in flattened_output.values():
        column_values.append(value)

    return column_values

# Retrieve column names with values from JSON dictionary
def output_to_dict(headers_output, values_output):

    if len(headers_output) != len(values_output):
        return (
            False,
            "There is not enough values for the existing columns.")

    my_dict = dict(
        zip(
            headers_output,
            values_output
        )
    )

    return True, my_dict

def output_records_list(output):

    if isinstance(output, dict):

        return [output]

    elif isinstance(output, list):

        return [
            item
            for item in output
            if isinstance(item, dict)
        ]

    return []

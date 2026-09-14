
from datetime import datetime, timezone

# Get Universal Coordinated Time (UTC) at runtime
def universal_time():
    universal_time = datetime.now(timezone.utc)

    return universal_time.isoformat(
        timespec="seconds"
    )

# Retrieve column names from JSON dictionary
def output_headers_list(output):
    columns_headers = []

    columns_headers.append("time_utc")

    for key, value in output.items():

        if isinstance(value, dict):

            for nested_key, nested_value in value.items():

                if isinstance(nested_value, dict):

                    for sub_key in nested_value.keys():
                        columns_headers.append(
                            f"{key}.{nested_key}.{sub_key}"
                        )

                else:
                    columns_headers.append(
                        f"{key}.{nested_key}"
                    )

        elif isinstance(value, list):

            for item in value:

                if isinstance(item, dict):

                    for nested_key, nested_value in item.items():

                        if isinstance(nested_value, dict):

                            for sub_key in nested_value.keys():
                                columns_headers.append(
                                    f"{key}.{nested_key}.{sub_key}"
                                )

                        else:
                            columns_headers.append(
                                f"{key}.{nested_key}"
                            )

        else:
            columns_headers.append(key)

    return columns_headers

# Retrieve column values from JSON dictionary
def output_values_list(output):
    column_values = []

    column_values.append(
        universal_time()
    )

    for key, value in output.items():

        if isinstance(value, dict):

            for nested_key, nested_value in value.items():

                if isinstance(nested_value, dict):

                    for sub_key, sub_value in nested_value.items():
                        column_values.append(
                            sub_value
                        )

                else:
                    column_values.append(
                        nested_value
                    )

        elif isinstance(value, list):

            for item in value:

                if isinstance(item, dict):

                    for nested_key, nested_value in item.items():

                        if isinstance(nested_value, dict):

                            for sub_key, sub_value in nested_value.items():
                                column_values.append(
                                    sub_value
                                )

                        else:
                            column_values.append(
                                nested_value
                            )

        else:
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
from datetime import datetime, timezone


def universal_time():
    return datetime.now(timezone.utc).isoformat(
        timespec="seconds"
    )


def output_headers_list(output):
    columns_headers = ["time_utc"]

    for key, value in output.items():
        if key == "weather" and isinstance(value, list) and value:
            for weather_key in value[0].keys():
                columns_headers.append(f"weather_{weather_key}")
        else:
            columns_headers.append(key)

    return columns_headers


def output_values_list(output):
    column_values = [universal_time()]

    for key, value in output.items():
        if key == "weather" and isinstance(value, list) and value:
            for weather_value in value[0].values():
                column_values.append(weather_value)
        else:
            column_values.append(value)

    return column_values


def output_to_dict(headers_output, values_output):

    if len(headers_output) != len(values_output):
        return (
            False,
            "There is not enough values for the existing columns."
        )

    return True, dict(
        zip(
            headers_output,
            values_output
        )
    )


def output_records_list(output):

    if isinstance(output, dict):
        return [output]

    if isinstance(output, list):
        return [
            item
            for item in output
            if isinstance(item, dict)
        ]

    return []
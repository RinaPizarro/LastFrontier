from datetime import datetime, timezone


def universal_time():
    return datetime.now(timezone.utc).isoformat(
        timespec="seconds"
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


def output_to_columns(output, parent_key=""):

    columns = {}

    for key, value in output.items():

        column_name = (
            f"{parent_key}_{key}"
            if parent_key
            else key
        )

        if isinstance(value, dict):
            columns.update(
                output_to_columns(value, column_name)
            )

        elif isinstance(value, list):

            if value and isinstance(value[0], dict):
                columns.update(
                    output_to_columns(
                        value[0],
                        column_name
                    )
                )

        else:
            columns[column_name] = value

    return columns


def output_headers_list(output):

    columns = output_to_columns(output)

    return [
        "time_utc",
        *columns.keys()
    ]


def output_values_list(output):

    columns = output_to_columns(output)

    return [
        universal_time(),
        *columns.values()
    ]


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
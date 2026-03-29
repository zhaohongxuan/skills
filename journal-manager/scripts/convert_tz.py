import sys
from datetime import datetime
from zoneinfo import ZoneInfo

def convert_timezone(file_path, from_tz, to_tz):
    with open(file_path, "r") as file:
        lines = file.readlines()

    converted_lines = []
    for line in lines:
        if line.startswith("["):
            timestamp, rest = line[1:].split("]", 1)
            dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=ZoneInfo(from_tz))
            dt_converted = dt.astimezone(ZoneInfo(to_tz))
            new_timestamp = dt_converted.strftime("%Y-%m-%dT%H:%M:%S %Z")
            converted_lines.append(f"[{new_timestamp}]{rest}")
        else:
            converted_lines.append(line)

    with open(file_path, "w") as file:
        file.writelines(converted_lines)

    print(f"Converted timestamps in {file_path} from {from_tz} to {to_tz}.")
# Re-dates time values from given created values.

import os
import csv
from datetime import datetime

def change_date(input_file, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    output_file = os.path.join(output_directory, os.path.basename(input_file))

    correction_count = 0
    rows = []

    with open(input_file, "r") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames

        for row in reader:
            time_value = row["time"]
            if time_value.startswith("1970"):
                created_value = row.get("created", "")
                row["time"] = created_value[:24]  # Update time value with created time
                correction_count += 1

            rows.append(row)

    with open(output_file, "w", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print("Data processing complete for", input_file)
    print("Number of corrections:", correction_count)

input_file = "manual/station-SD.csv"
output_directory = "re-dated"

change_date(input_file, output_directory)

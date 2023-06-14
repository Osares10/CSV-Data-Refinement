# Rounds the time values in the CSV files to the nearest 10 minutes.

import os
import csv
from datetime import datetime, timedelta

def round_to_nearest_ten_minutes(time_str):
    time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%fZ")
    rounded_time = time - timedelta(minutes=time.minute % 10,
                                    seconds=time.second,
                                    microseconds=time.microsecond)
    return rounded_time.strftime("%Y-%m-%d %H:%M")

input_directory = "re-dated"
output_directory = "rounded"

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for filename in os.listdir(input_directory):
    if filename.endswith(".csv"):
        input_file = os.path.join(input_directory, filename)
        output_file = os.path.join(output_directory, filename)

        with open(input_file, "r") as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames

            with open(output_file, "w", newline="") as outfile:
                writer = csv.DictWriter(outfile, fieldnames=headers)
                writer.writeheader()

                for row in reader:
                    row["time"] = round_to_nearest_ten_minutes(row["time"])
                    writer.writerow(row)

        print("Data processing complete for", filename)

print("All files processed successfully.")

import os
import csv
import random
import string
import time
import re
from datetime import datetime
from threading import Lock


def consumer_task(regex_pattern, window_duration, data_lock, throughput_data, latency_data):
    print("Sleeping...")
    time.sleep(window_duration)
    pattern = re.compile(regex_pattern)
    count = 1
    window_id = 1

    while True:
        start_time = None
        data = ""
        timestamp = None
        retries = 0

        total_matches = 0
        total_latency = 0

        for i in range(count, count + window_duration):
            while retries < 3:  # Retry up to 3 times if the file doesn't exist
                filename = os.path.join("output_2", f"{i}.csv")
                
                if not os.path.exists(filename):
                    print(f"File {filename} does not exist. Retrying after a second.")
                    retries += 1
                    time.sleep(1)  # Retry after 1 second
                else:
                    break  # File exists, exit the retry loop
            
            if retries == 3:
                matches = len(re.findall(pattern, data))
                print(f"Window {window_id} having {start_time} - {timestamp}: Matches: {matches}")
                print("Ending the process due to multiple file not found errors.")
                return
            
            print("Reading", filename)
            with open(filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    timestamp = datetime.strptime(row['t'], '%Y-%m-%d %H:%M:%S')
                    event = row['char']

                    if start_time is None:
                        start_time = timestamp

                    time_difference = (timestamp - start_time).total_seconds()

                    if time_difference < window_duration:
                        data += event
                    else:
                        matches = len(re.findall(pattern, data))
                        print(f"Window {window_id} having {start_time} - {timestamp}: Matches: {matches}")

                        total_matches += matches
                        total_latency += time_difference
                        start_time = timestamp
                        data = ""

        time.sleep(window_duration)
        window_id += 1
        count += window_duration

        with data_lock:
            # Calculate and append the average throughput and latency to the lists
            average_throughput = total_matches / window_duration
            average_latency = total_latency / window_duration
            throughput_data.append(average_throughput)
            latency_data.append(average_latency)

        

if __name__ == '__main__':
    regex_pattern = r'([BCDFGHJKLMNPQRSTVWXYZ][AEIOU])+[BCDFGHJKLMNPQRSTVWXYZ]?'
    window_duration = 10  # Fixed window duration of 10 seconds
    duration = 60
    data_lock = Lock()
    throughput_data = []  # List to store throughput data
    latency_data = []  # List to store latency data
    consumer_task(regex_pattern, window_duration, data_lock, throughput_data, latency_data)

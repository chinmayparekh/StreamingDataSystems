import os
import csv
import random
import string
import time
import re
from datetime import datetime
from threading import Lock
from datetime import timedelta


def consumer_task(regex_pattern, window_duration, data_lock, throughput_data, latency_data,end):
    print("Sleeping...")
    time.sleep(end)
    pattern = re.compile(regex_pattern)
    count = 1
    window_id = 1

    latency_data.append(end)
    print("Running with latency ",end)
    while True:
        start_time = None
        data = ""
        timestamp = None
        retries = 0

        total_matches = 0
        total_events=0
        latency=0
        for i in range(count, count + window_duration):
            print("Reading from ",count, count+window_duration-1)
            while retries < 5:  # Retry up to 3 times if the file doesn't exist
                filename = os.path.join("data", f"{i}.csv")
                
                if not os.path.exists(filename):
                    print(f"File {filename} does not exist. Retrying after a second.")
                    retries += 1
                    time.sleep(1)  # Retry after 1 second
                else:
                    break  # File exists, exit the retry loop
            
            if retries == 5:
                matches = len(re.findall(pattern, data))
                total_matches += matches
                print(f"Window {window_id} having {start_time} - {timestamp}: Matches: {matches}")
                print("Ending the process due to multiple file not found errors.")
                average_throughput = total_matches / window_duration
                throughput_data.append(average_throughput)
                return
            
            print("Reading", filename)
            with open(filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    total_events+=1
                    timestamp = datetime.strptime(row['t'], '%Y-%m-%d %H:%M:%S')
                    event = row['char']

                    if start_time is None:
                        start_time = timestamp

                    time_difference = (timestamp - start_time).total_seconds()
                    
                    if time_difference < window_duration:
                        data += event
                        currentTime = datetime.now()
                        difference = (currentTime - timestamp).total_seconds()
                        latency += (difference/1000000)

        matches = len(re.findall(pattern, data))
        print(f"Window {window_id} having {start_time} - {timestamp}: Matches: {matches}")
        total_matches += matches
        start_time = timestamp
        data = ""
        window_id += 1
        count += window_duration

        with data_lock:
            # Calculate and append the average throughput and latency to the lists
            average_throughput = total_matches / window_duration
            throughput_data.append(average_throughput)

            latency_data.append(latency)
            
        

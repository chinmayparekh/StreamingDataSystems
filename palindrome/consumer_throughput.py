import os
import csv
import time
import re
from datetime import datetime
from threading import Lock
from datetime import timedelta

def findPattern(data,pattern,timings,indices):
    print(pattern)
    print(len(data),len(timings),len(indices))
    return 1

def checkValid(input_string):
    # Extract digits from the input string
    
    extracted_digits = [int(match) for match in re.findall(r'\d+', input_string)]
    print(extracted_digits)
    # Check if the extracted digits are sorted in descending order
    is_sorted_descending = all(extracted_digits[i] >= extracted_digits[i + 1] for i in range(len(extracted_digits) - 1))
    print(is_sorted_descending)
    return extracted_digits, is_sorted_descending

def consumer_task(palindromic_pattern, window_duration, matches_data, throughput_data, latency_data):
    print("Sleeping...")
    time.sleep(window_duration)
    count = 1
    window_id = 1
    while True:
        start_time = None
        data = ""
        timestamp = None
        retries = 0
        timings=[]
        indices=[]
        total_matches = 0
        total_events=0
        latency=0
        for i in range(count, count + window_duration):
            while retries < 5:  # Retry up to 3 times if the file doesn't exist
                filename = os.path.join("data", f"{i}.csv")
                
                if not os.path.exists(filename):
                    print(f"File {filename} does not exist. Retrying after a second.")
                    retries += 1
                    time.sleep(1)  # Retry after 1 second
                else:
                    break  # File exists, exit the retry loop
            currentTime = datetime.now()
            if retries == 5:
                #Adding the matches
                matches = findPattern(data,palindromic_pattern,timings,indices)
                total_matches += matches
                matches_data.append(matches)
                #Adding the throughput
                if(start_time is not None):
                    difference = (currentTime - start_time).total_seconds()
                    average_throughput = total_events / difference
                    throughput_data.append(average_throughput)

                print(f"Window {window_id} having {start_time} - {timestamp}: Matches: {matches}")
                print("Ending the process due to multiple file not found errors.")
                
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
                        timings.append(timestamp)
                        indices.append(total_events)
        #Adding latency
        currentTime = datetime.now()
        difference = (currentTime - start_time).total_seconds()
        latency = (difference/1000000)
        latency_data.append(latency)
        #Adding matches
        matches = findPattern(data,palindromic_pattern,timings,indices)
        total_matches += matches
        matches_data.append(matches)
        #Adding throughput
        average_throughput = total_events / difference
        throughput_data.append(average_throughput)
        #Printing matches
        print(f"Window {window_id} having {start_time} - {timestamp}: Matches: {matches}")
        start_time = timestamp
        data = ""
        timings.clear()
        time.sleep(window_duration)
        #Adding latency for the window 
        latency_data.append(window_duration)
        #Fixing the file number and window_id
        window_id += 1
        count += window_duration

        

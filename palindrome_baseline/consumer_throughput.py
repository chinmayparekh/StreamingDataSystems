import os
import csv
import time
import re
from datetime import datetime
from threading import Lock
from datetime import timedelta
def decode(pattern):
    character=""
    interval=0
    for char in pattern:
        if char.isalpha():
            character=char
        elif char.isdigit():
            interval=char
    return character,interval

def transform_data(data,timings,indices,pattern):
    data_count = {}
    
    for index in indices:
        timing = int(timings[index])
        
        if timing not in data_count:
            data_count[timing] = 0
        
        if data[index] == pattern:
            data_count[timing] += 1
    return data_count

def transform_time(timings): 
    first_timing = timings[0]
    time_diffs_seconds = [(timing - first_timing).total_seconds() for timing in timings]
    return time_diffs_seconds

def compute_occurence(data, window_size):
    result = []
    for i in range(len(data) - window_size + 1):
        window_data = {k: v for k, v in data.items() if k in range(i, i + window_size)}
        print(window_data)
        window_result = 0  # Initialize the window result to zero
        
        # Calculate the result for the current window
        for k, v in window_data.items():
            if k == i:
                continue
            try:
                start = window_data[i]  # Try to access the start value for the window
            except KeyError:
                start = 0  # Handle the KeyError by setting start to 0
            
            product = v * start
            window_result += product
        
        result.append(window_result)
    return result

def findPattern(data,pattern,timings):
    character,interval=decode(pattern)
    time_diff=transform_time(timings)
    indices=list(range(len(data)))
    data=transform_data(data,time_diff,indices,character)
    print(data)
    result=compute_occurence(data,int(interval))
    return sum(result)

def checkValid(input_string):
    # Extract digits from the input string
    
    extracted_digits = [int(match) for match in re.findall(r'\d+', input_string)]
    # Check if the extracted digits are sorted in descending order
    is_sorted_descending = all(extracted_digits[i] >= extracted_digits[i + 1] for i in range(len(extracted_digits) - 1))
    return extracted_digits, is_sorted_descending

def consumer_task(palindromic_pattern, window_duration, matches_data, throughput_data, latency_data):
    print("Sleeping...")
    time.sleep(window_duration)
    count = 1
    window_id = 1
    pattern_chars = set(palindromic_pattern)

    while True:
        start_time = None
        data = ""
        timestamp = None
        retries = 0
        timings=[]
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
                matches = findPattern(data,palindromic_pattern,timings)
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
                        if event in pattern_chars:
                            data += event
                            timings.append(timestamp)
        #Adding latency
        currentTime = datetime.now()
        difference = (currentTime - start_time).total_seconds()
        latency = (difference/1000000)
        latency_data.append(latency)
        #Adding matches
        matches = findPattern(data,palindromic_pattern,timings)
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

        

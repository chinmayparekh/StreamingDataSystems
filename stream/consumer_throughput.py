import os
import csv
import time
import re
from datetime import datetime
from threading import Lock
from datetime import timedelta


def consumer_task(regex_pattern, window_duration,slice_duration, matches_data, throughput_data, latency_data):
    print("Sleeping...")
    time.sleep(slice_duration)
    pattern = re.compile(regex_pattern)
    count = 1
    window_id = 1
    total_matches = 0
    print_data=count+window_duration
    total_events=0
    latency=0
    start_time = None
    window_start_time=None
    data = ""
    timestamp = None

    while True:
        
        retries = 0
        index=1
        
        for i in range(count, count + slice_duration):
            index=i
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
                matches = len(re.findall(pattern, data))
                total_matches += matches
                matches_data.append(total_matches)
                #Adding the throughput
                difference = (currentTime - start_time).total_seconds()
                average_throughput = total_events / difference
                throughput_data.append(average_throughput)

                print(f"Window {window_id} having {start_time} - {timestamp}: Matches: {total_matches}")
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
                        window_start_time=timestamp

                    time_difference = (timestamp - start_time).total_seconds()
                    
                    if time_difference <= slice_duration:
                        data += event
                        
        
        #Adding matches
        matches = len(re.findall(pattern, data))
        total_matches += matches
        # print("Prev start ",start_time)
        start_time=timestamp
        # print("New start ",start_time)

        data=""
        #Printing matches
        if(index%10==0):
            index=1
            #Adding latency
            currentTime = datetime.now()
            difference = (currentTime - window_start_time).total_seconds()
            print("Total events = ",total_events)
            # print(start_time," is the start time")
            latency = (difference/1000000)
            latency_data.append(latency)
            average_throughput = total_events / (difference)
            throughput_data.append(average_throughput)
            print(f"Window {window_id} having {start_time} - {timestamp}: Matches: {total_matches}")
            start_time = timestamp
            data = ""
            window_id += 1
            # count += window_duration
            print_data+=window_duration
            window_start_time=start_time
            matches_data.append(total_matches)
            total_events=0
            total_matches=0
        count+=slice_duration
        time.sleep(slice_duration)
        #Adding latency for the window 
        latency_data.append(slice_duration)
        

        

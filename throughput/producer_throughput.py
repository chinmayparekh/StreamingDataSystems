import os
import csv
import random
import string
import time
from datetime import datetime
from threading import Event, Lock
import random 

def generate_data(throughput_per_second, duration, end_event, generated_data):
    if not os.path.exists("data"):
        os.makedirs("data")

    file_number = random. randint(0,1000)
    events_per_file = 0
    start = time.time()
    end = start + duration
    while time.time() < end:
        filename = f"data/{file_number}.csv"  # Construct the filename
        print("Writing", filename)
        file_number += 1  # Increment the file number

        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['t', 'integer', 'char']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            start_time = time.time()  # Get the start time
            end_time = start_time + 1       
            while True:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                integer = random.randint(1, 10)
                char = random.choice(string.ascii_uppercase)
                writer.writerow({'t': timestamp, 'integer': integer, 'char': char})
                elapsed_time = time.time() - start_time  # Calculate elapsed time
                events_per_file += 1  # Counting the number of rows

                if elapsed_time >= 1 or events_per_file>=throughput_per_second:  # Check if 1 second has passed
                    current_time = time.time()
                    time_to_next_second = 1.0 - (current_time - int(current_time))
                    time.sleep(time_to_next_second)
                    generated_data.append(events_per_file)
                    events_per_file = 0
                    break

    print("Data generation completed.")
    end_event.set()  # Signal the end of data generation


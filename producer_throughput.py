import os
import csv
import random
import string
import time
from datetime import datetime
from threading import Event, Lock

def generate_data(throughput_per_second, duration, end_event, data_lock, generated_data):
    if not os.path.exists("output_2"):
        os.makedirs("output_2")

    file_number = 1  # Initialize the file number
    events_per_file = 0
    start = time.time()
    end = start + duration
    while time.time() < end:
        filename = f"output_2/{file_number}.csv"  # Construct the filename
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
                    with data_lock:
                        time.sleep(end_time - time.time())
                        generated_data.append(events_per_file)
                    events_per_file = 0
                    break

    print("Data generation completed.")
    end_event.set()  # Signal the end of data generation

if __name__ == '__main__':
    duration = 60
    throughput_per_second = 10000
    end_event = Event()
    data_lock = Lock()
    generated_data = []

    generate_data(throughput_per_second, duration, end_event, data_lock, generated_data)

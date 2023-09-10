# import os
# import csv
# import random
# import string
# import time
# import re
# from datetime import datetime
# from threading import Thread,Event,Lock
# import consumer as consumer, producer as producer

# def main():
#     regex_pattern = r'([BCDFGHJKLMNPQRSTVWXYZ][AEIOU])+[BCDFGHJKLMNPQRSTVWXYZ]?'
#     duration=60
#     throughput_per_second=10000
#     window_duration = 10  # Fixed window duration of 10 seconds
#     producer_thread = Thread(target=producer.generate_data, args=(throughput_per_second, duration))
#     producer_thread.start()

#     consumer_thread = Thread(target=consumer.consumer_task, args=(regex_pattern,window_duration,duration))
#     consumer_thread.start()

#     producer_thread.join()
#     consumer_thread.join()

# if __name__ == '__main__':
#     main()
import os
import csv
import random
import string
import time
import re
from datetime import datetime
from threading import Thread, Event, Lock
import consumer as consumer
import producer as producer
import matplotlib.pyplot as plt  # Import matplotlib for plotting

def main():
    regex_pattern = r'([BCDFGHJKLMNPQRSTVWXYZ][AEIOU])+[BCDFGHJKLMNPQRSTVWXYZ]?'
    duration = 60
    throughput_per_second = 10000
    window_duration = 10  # Fixed window duration of 10 seconds

    current_time = time.time()
    time_to_next_second = 1.0 - (current_time - int(current_time))
    print(f"Waiting {time_to_next_second:.3f} seconds until the next second starts.")
    time.sleep(time_to_next_second)
    # Create an event to signal the end of data generation
    data_generation_event = Event()

    # Create a lock for accessing the shared data (if needed)
    data_lock = Lock()
    data_lock_consumer = Lock()

    # Create a variable to hold the generated data
    generated_data = []
    throughput_data=[]
    latency_data=[]
    # Start the producer thread
    producer_thread = Thread(target=producer.generate_data, args=(throughput_per_second, duration, data_generation_event, data_lock, generated_data))
    producer_thread.start()

    # Start the consumer thread
    consumer_thread = Thread(target=consumer.consumer_task, args=(regex_pattern, window_duration, data_lock_consumer,throughput_data, latency_data))
    consumer_thread.start()

    # Wait for the producer thread to finish
    producer_thread.join()
    data_generation_event.set()  # Signal the end of data generation

    # Wait for the consumer thread to finish
    consumer_thread.join()

    # Extract the generated data from the shared variable
    data = generated_data
    print(data)
    print(latency_data)
    print(throughput_data)
    # Plot a line graph
    x_values = list(range(1, len(data) + 1))
    y_values = data
    plt.plot(x_values, y_values)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Events per second')
    plt.title('Throughput Over Time')
    plt.show()

if __name__ == '__main__':
    main()

import time
from datetime import datetime
from threading import Thread, Event, Lock
import consumer_throughput as consumer
import producer_throughput as producer
import matplotlib.pyplot as plt  # Import matplotlib for plotting
import os
def main():
    if not os.path.exists("throughput_15000"):
        os.makedirs("throughput_15000")
    regex_pattern = r'([BCDFGHJKLMNPQRSTVWXYZ][AEIOU])+[BCDFGHJKLMNPQRSTVWXYZ]?'
    duration = 20
    throughput_per_second = 13000
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
    matches_data=[]
    # Start the producer thread
    producer_thread = Thread(target=producer.generate_data, args=(throughput_per_second, duration, data_generation_event, data_lock, generated_data))
    producer_thread.start()

    # Start the consumer thread
    consumer_thread = Thread(target=consumer.consumer_task, args=(regex_pattern, window_duration, matches_data,throughput_data, latency_data))
    consumer_thread.start()

    # Wait for the producer thread to finish
    producer_thread.join()
    data_generation_event.set()  # Signal the end of data generation

    # Wait for the consumer thread to finish
    consumer_thread.join()

    # Plot a line graph for Throughput Over Time
    x_values = list(range(1, len(generated_data) + 1))
    y_values = generated_data
    plt.plot(x_values, y_values)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Events per second')
    plt.title('Throughput Over Time')
    plt.savefig("throughput_15000/Producer_throughput.jpg")  # Save the plot as an image
    plt.show()  # Show the plot

    # Plot a line graph for Consumer Throughput Over Time
    x_values = list(range(1, len(throughput_data) + 1))
    y_values = throughput_data
    plt.plot(x_values, y_values)
    plt.xlabel('Window id')
    plt.ylabel('Matches per window id')
    plt.title('Consumer Throughput Over Time')
    plt.savefig("throughput_15000/Consumer_throughput.jpg")  # Save the plot as an image
    plt.show()  # Show the plot
    print("Throughput for producer ",generated_data)

    print("Throughput for consumer ",throughput_data)
    print("Latency = ",latency_data)
 
    print("Matches = ",matches_data)

if __name__ == '__main__':
    main()

# duration = 20
# throughput_per_second = 15000
# window_duration = 10 
# Throughput for producer  [15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 10105, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000]
# Throughput for consumer  [12634.879443876624, 10721.344278727021, 195.7]
# Latency =  [1.1871898e-05, 10, 1.3534217e-05, 10]
# Matches =  [19803, 17099, 1957]


# duration = 20
# throughput_per_second = 13000
# window_duration = 10 
# Throughput for producer  [13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000]
# Throughput for consumer  [10883.983765784707, 9804.293671573543, 11.93643417182046]
# Latency =  [1.1944156e-05, 10, 1.3463488999999999e-05, 10]
# Matches =  [17121, 17215, 1970]
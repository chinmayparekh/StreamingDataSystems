import time
from datetime import datetime
from threading import Thread, Event, Lock
import consumer_throughput as consumer
import producer_throughput as producer
import matplotlib.pyplot as plt  # Import matplotlib for plotting
import os
def main():
    if not os.path.exists("sanityCheck"):
        os.makedirs("sanityCheck")
    palindromic_pattern="A[2]B[2]C[2]"
    flag = consumer.checkValid(palindromic_pattern)
    if(flag[1]):
        duration = 20
        throughput_per_second = 100
        window_duration = 10  # Fixed window duration of 10 seconds

        current_time = time.time()
        time_to_next_second = 1.0 - (current_time - int(current_time))
        print(f"Waiting {time_to_next_second:.3f} seconds until the next second starts.")
        time.sleep(time_to_next_second)
        # Create an event to signal the end of data generation
        data_generation_event = Event()

        # Create a lock for accessing the shared data (if needed)
        data_lock = Lock()

        # Create a variable to hold the generated data
        generated_data = []
        throughput_data=[]
        latency_data=[]
        matches_data=[]
        # Start the producer thread
        producer_thread = Thread(target=producer.generate_data, args=(throughput_per_second, duration, data_generation_event, data_lock, generated_data))
        producer_thread.start()

        # Start the consumer thread
        consumer_thread = Thread(target=consumer.consumer_task, args=(palindromic_pattern,window_duration, matches_data,throughput_data, latency_data))
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
        plt.savefig("sanityCheck/Producer_throughput.jpg")  # Save the plot as an image
        plt.show()  # Show the plot

        # Plot a line graph for Consumer Throughput Over Time
        x_values = list(range(1, len(throughput_data) + 1))
        y_values = throughput_data
        plt.plot(x_values, y_values)
        plt.xlabel('Window id')
        plt.ylabel('Matches per window id')
        plt.title('Consumer Throughput Over Time')
        plt.savefig("sanityCheck/Consumer_throughput.jpg")  # Save the plot as an image
        plt.show()  # Show the plot

        # Plot a line graph for Matches Over Time
        x_values = list(range(1, len(matches_data) + 1))
        y_values = matches_data
        plt.plot(x_values, y_values)
        plt.xlabel('Window id')
        plt.ylabel('Matches per window id')
        plt.title('Matches')
        plt.savefig("sanityCheck/Matches.jpg")  # Save the plot as an image
        plt.show()  # Show the plot

        print("Throughput for producer ",generated_data)
        print("Throughput for consumer ",throughput_data)
        print("Latency = ",latency_data)
        print("Matches = ",matches_data)
    else:
        print("Invalid pattern")

if __name__ == '__main__':
    main()

# Sanity Check
# Throughput for producer  [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
# Throughput for consumer  [99.56094618342571, 99.30652269074598, 6.627070802232766]
# Latency =  [1.0044099e-05, 10, 1.0069832e-05, 10]
# Matches =  [9801, 9801, 0]
import time
from datetime import datetime
from threading import Thread, Event, Lock
import producer_throughput as producer
import matplotlib.pyplot as plt  # Import matplotlib for plotting
import os
def main():
    if not os.path.exists("throughput_150000_only_producer"):
        os.makedirs("throughput_150000_only_producer")
    duration = 100
    throughput_per_second = 150000

    current_time = time.time()
    time_to_next_second = 1.0 - (current_time - int(current_time))
    print(f"Waiting {time_to_next_second:.3f} seconds until the next second starts.")
    time.sleep(time_to_next_second)
    # Create an event to signal the end of data generation
    data_generation_event_1 = Event()
    data_generation_event_2 = Event()


    # Create a variable to hold the generated data
    generated_data_1 = []
    generated_data_2 = []

    # Start the producer thread
    producer_thread_1 = Thread(target=producer.generate_data, args=(throughput_per_second, duration, data_generation_event_1, generated_data_1))
    producer_thread_1.start()

    # Start the producer thread
    producer_thread_2 = Thread(target=producer.generate_data, args=(throughput_per_second, duration, data_generation_event_2, generated_data_2))
    producer_thread_2.start()


    # Wait for the producer thread to finish
    producer_thread_1.join()
    producer_thread_2.join()

    generated_data=[]
    for i in range(len(generated_data_2)):
        generated_data.append(generated_data_1[i]+generated_data_2[i])
    # Plot a line graph for Throughput Over Time
    x_values = list(range(1, len(generated_data) + 1))
    y_values = generated_data
    plt.plot(x_values, y_values)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Events per second')
    plt.title('Throughput Over Time')
    plt.savefig("throughput_150000_only_producer/Producer_throughput.jpg")  # Save the plot as an image
    plt.show()  # Show the plot

    # Plot a line graph for Consumer Throughput Over Time
    # x_values = list(range(1, len(throughput_data) + 1))
    # y_values = throughput_data
    # plt.plot(x_values, y_values)
    # plt.xlabel('Window id')
    # plt.ylabel('Matches per window id')
    # plt.title('Consumer Throughput Over Time')
    # plt.savefig("throughput_75000/Consumer_throughput.jpg")  # Save the plot as an image
    # plt.show()  # Show the plot

    # # Plot a line graph for Matches Over Time
    # x_values = list(range(1, len(matches_data) + 1))
    # y_values = matches_data
    # plt.plot(x_values, y_values)
    # plt.xlabel('Window id')
    # plt.ylabel('Matches per window id')
    # plt.title('Matches')
    # plt.savefig("throughput_75000/Matches.jpg")  # Save the plot as an image
    # plt.show()  # Show the plot

    print("Throughput for producer ",generated_data)
    # print("Throughput for consumer ",throughput_data)
    # print("Latency = ",latency_data)
    # print("Matches = ",matches_data)

if __name__ == '__main__':
    main()


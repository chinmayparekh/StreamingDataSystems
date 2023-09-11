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
    duration = 100
    throughput_per_second = 15000
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
    consumer_thread = Thread(target=consumer.consumer_task, args=(regex_pattern, window_duration,matches_data,throughput_data, latency_data,duration))
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

    # Plot a line graph for Matches Over Time
    x_values = list(range(1, len(matches_data) + 1))
    y_values = matches_data
    plt.plot(x_values, y_values)
    plt.xlabel('Window id')
    plt.ylabel('Matches per window id')
    plt.title('Matches')
    plt.savefig("throughput_15000/Matches.jpg")  # Save the plot as an image
    plt.show()  # Show the plot
    
    print("Throughput for producer ",generated_data)
    print("Throughput for consumer ",throughput_data)
    print("Latency = ",latency_data)
    print("Matches = ",matches_data)

if __name__ == '__main__':
    main()
# duration = 100
# throughput_per_second = 15000
# window_duration = 10 
# Throughput for producer  [15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000]
# Throughput for consumer  [1472.2692925800034, 1603.108782751165, 1754.8468020496657, 1938.5425659619477, 2189.692507174418, 2502.2021881457867, 2938.7509638368474, 3556.7899250084038, 4499.946450637237, 6129.528710344707, 764.9476117978584]
# Latency =  [100, 0.00010188353499999999, 9.356819799999999e-05, 8.5477547e-05, 7.7377718e-05, 6.8502769e-05, 5.9947194000000005e-05, 5.1042093e-05, 4.2172859000000005e-05, 3.3333730000000005e-05, 2.4471702e-05]
# Matches =  [19501, 19759, 19665, 19694, 19557, 19554, 19605, 19830, 19803, 19611, 1963]

# duration = 100
# throughput_per_second = 13000
# window_duration = 10 
# Throughput for producer  [13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000]
# Throughput for consumer  [1278.9194303484294, 1395.7295442897944, 1536.5776397221869, 1708.9757800534499, 1930.5762407724396, 2231.514745514711, 2643.1326473197764, 3236.8541641830034, 4183.680434526061, 5907.740990274632, 759.7046572174601]
# Latency =  [100, 0.000101648311, 9.314125400000001e-05, 8.46036e-05, 7.6068954e-05, 6.733740799999999e-05, 5.8256393e-05, 4.9184062e-05, 4.0162452e-05, 3.1073119e-05, 2.2005026999999997e-05]
# Matches =  [17064, 16966, 17082, 17178, 17087, 17099, 17051, 17157, 17116, 17015, 1651]
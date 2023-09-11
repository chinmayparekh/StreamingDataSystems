import time
from datetime import datetime
from threading import Thread, Event, Lock
import consumer_throughput as consumer
import producer_throughput as producer
import matplotlib.pyplot as plt  # Import matplotlib for plotting
import os
def main():
    if not os.path.exists("throughput_150000"):
        os.makedirs("throughput_150000")
    regex_pattern = r'([BCDFGHJKLMNPQRSTVWXYZ][AEIOU])+[BCDFGHJKLMNPQRSTVWXYZ]?'
    duration = 100
    throughput_per_second = 150000
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
    plt.savefig("throughput_150000/Producer_throughput.jpg")  # Save the plot as an image
    plt.show()  # Show the plot

    # Plot a line graph for Consumer Throughput Over Time
    x_values = list(range(1, len(throughput_data) + 1))
    y_values = throughput_data
    plt.plot(x_values, y_values)
    plt.xlabel('Window id')
    plt.ylabel('Matches per window id')
    plt.title('Consumer Throughput Over Time')
    plt.savefig("throughput_150000/Consumer_throughput.jpg")  # Save the plot as an image
    plt.show()  # Show the plot

    # Plot a line graph for Matches Over Time
    x_values = list(range(1, len(matches_data) + 1))
    y_values = matches_data
    plt.plot(x_values, y_values)
    plt.xlabel('Window id')
    plt.ylabel('Matches per window id')
    plt.title('Matches')
    plt.savefig("throughput_150000/Matches.jpg")  # Save the plot as an image
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


# duration = 100
# throughput_per_second = 13000
# window_duration = 10 
# Throughput for producer  [13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 6769, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 5867, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 7825, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 8150, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000, 13000]
# Throughput for consumer  [11070.748298276958, 9742.490975080957, 8351.67946566094, 8432.324498678849, 7241.912239224821, 7378.830521204261, 6845.4559553519975, 6700.28785271809, 6792.714009549407, 2611.8688544483844]
# Latency =  [1.1742657e-05, 10, 1.334361e-05, 10, 1.4819654e-05, 10, 1.5416864e-05, 10, 1.6966099e-05, 10, 1.7617968000000002e-05, 10, 1.8234724e-05, 10, 1.8678302e-05, 10, 1.9138153e-05, 10]
# Matches =  [16929, 17087, 14548, 17150, 14243, 15359, 14684, 14683, 16992, 8488]

# duration = 100
# throughput_per_second = 50000
# window_duration = 10 
# Throughput for producer  [50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 16299, 1304, 2282, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 5173, 326, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 5866, 5543, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 1956, 5156, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 28357, 3585, 30723, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 1181, 1630, 18836, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 25064]
# Throughput for consumer  [31789.275252208165, 18572.36163857954, 18854.591220527425, 17009.164654951794, 15773.080148054141, 16444.510035885876, 13143.046029863972, 10591.359125294011, 4484.380401302659]
# Latency =  [1.5728575e-05, 10, 1.9915884e-05, 10, 2.1506644999999998e-05, 10, 2.418749e-05, 10, 2.5810558e-05, 10, 2.9089161e-05, 10, 3.3044699e-05, 10, 3.5089642e-05, 10]
# Matches =  [65705, 28925, 39826, 39826, 46802, 62514, 43992, 29032, 22946]

# duration = 100
# throughput_per_second = 150000
# window_duration = 10 
# Throughput for producer  [92160, 92855, 93395, 93714, 92790, 83604, 2609, 4563, 69276, 72038, 90684, 94615, 93373, 93207, 93490, 883, 7740, 87997, 92049, 106537, 137286, 93735, 92256, 93165, 93525, 4074, 679, 88068, 86618, 91594, 111375, 93460, 92849, 93979, 91743, 5216, 1659, 59673, 87084, 93411, 91051, 91666, 93232, 93731, 93878, 18257, 2608]
# Throughput for consumer  [32193.17276287341, 36341.00311911332, 33103.83848225301, 31713.308139084435, 18891.127109917623]
# Latency =  [2.1564447999999998e-05, 10, 2.0732174e-05, 10, 2.0954428e-05, 10, 2.2006345e-05, 10]
# Matches =  [60843, 61023, 66920, 63473, 61155]
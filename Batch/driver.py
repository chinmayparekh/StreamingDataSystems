import time
from datetime import datetime
from threading import Thread, Event, Lock
import consumer_throughput as consumer
import producer_throughput as producer
import matplotlib.pyplot as plt  # Import matplotlib for plotting
import os
def main():
    if not os.path.exists("throughput_75000"):
        os.makedirs("throughput_75000")
    regex_pattern = r'([BCDFGHJKLMNPQRSTVWXYZ][AEIOU])+[BCDFGHJKLMNPQRSTVWXYZ]?'
    duration = 20
    throughput_per_second = 75000
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
    plt.savefig("throughput_75000/Producer_throughput.jpg")  # Save the plot as an image
    plt.show()  # Show the plot

    
    # Plot a line graph for Consumer Throughput Over Time
    x_values = list(range(1, len(throughput_data) + 1))
    y_values = throughput_data
    plt.plot(x_values, y_values)
    plt.xlabel('Window id')
    plt.ylabel('Matches per window id')
    plt.title('Consumer Throughput Over Time')
    plt.savefig("throughput_75000/Consumer_throughput.jpg")  # Save the plot as an image
    plt.show()  # Show the plot

    # Plot a line graph for Matches Over Time
    x_values = list(range(1, len(matches_data) + 1))
    y_values = matches_data
    plt.plot(x_values, y_values)
    plt.xlabel('Window id')
    plt.ylabel('Matches per window id')
    plt.title('Matches')
    plt.savefig("throughput_75000/Matches.jpg")  # Save the plot as an image
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

# duration = 100
# throughput_per_second = 25000
# window_duration = 10 
# Throughput for producer  [25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000, 25000]
# Throughput for consumer  [2419.647522396112, 2601.8210978446564, 2814.6646143032995, 3099.352778275947, 3453.5983573139, 3901.755117140131, 4483.081513862746, 5263.165096962764, 6382.365473138793, 8104.354784274557, 960.269317901114]
# Latency =  [100, 0.00010332083400000001, 9.6086545e-05, 8.8820529e-05, 8.0662002e-05, 7.2388267e-05, 6.4073729e-05, 5.5765214e-05, 4.7499935e-05, 3.917043e-05, 3.0847613e-05]
# Matches =  [32924, 32889, 32814, 32835, 32951, 32956, 32803, 32729, 32916, 32663, 3252]

# duration = 100
# throughput_per_second = 50000
# window_duration = 10 
# Throughput for producer  [50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 12006]
# Throughput for consumer  [4732.94540156538, 5028.606131126014, 5391.2764144509665, 5811.664368385876, 6296.204301755665, 6870.239087480554, 7549.992767861928, 8274.871777965596, 9191.046714634616, 10390.112569388808, 277.6065056573598]
# Latency =  [100, 0.000105642461, 9.9431132e-05, 9.2742416e-05, 8.6033874e-05, 7.9412925e-05, 7.2777671e-05, 6.6225229e-05, 6.0423896999999994e-05, 5.4400768e-05, 4.8122674e-05]
# Matches =  [65249, 65544, 65764, 65635, 65506, 65648, 65519, 65882, 65809, 65534, 1554]

# duration = 100
# throughput_per_second = 75000
# window_duration = 10 
# Throughput for producer  [75000, 75000, 75000, 75000, 75000, 75000, 75000, 67491, 75000, 75000, 75000, 75000, 55514, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 63555, 75000, 75000, 70969, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 66073]
# Throughput for consumer  [6901.3549908192745, 7204.059125997221, 7868.367788198982, 8307.589866162623, 8801.943112267096, 9356.496475613621, 9797.271792381986, 11049.231160611535, 11935.440913647499, 8427.930273249394]
# Latency =  [100, 0.000107586264, 0.00010140311, 9.531837099999999e-05, 9.0278891e-05, 8.520845799999999e-05, 8.0158209e-05, 7.497230000000001e-05, 6.787802600000001e-05, 6.2838064e-05]
# Matches =  [87409, 85780, 98242, 98499, 98150, 98341, 76329, 98248, 98333, 67515]

# duration = 100
# throughput_per_second = 150000
# window_duration = 10 
# Throughput for producer  [91706, 91860, 90898, 92283, 93020, 92279, 90840, 92650, 92112, 92521, 91017, 91371, 92821, 92376, 91884, 92566, 92576, 92112, 90083, 91790, 92000, 91823, 91816, 89176, 92704, 91110, 91637, 91670, 92129, 91926, 92098, 90891, 91493, 91942, 90523, 92857, 92285, 92961, 92864, 91680, 91985, 91655, 91979, 92114, 91847, 92343, 91802, 90958, 91260, 91509, 78447]
# Throughput for consumer  [8374.704892515068, 9586.745695497477, 11207.603489103178, 13579.859100511285, 17106.60729776028, 2002.7563269989691]
# Latency =  [100, 0.000109874797, 9.5819377e-05, 8.172942600000001e-05, 6.771749199999999e-05, 5.3631441e-05]
# Matches =  [60244, 60326, 60053, 60001, 60242, 10259]
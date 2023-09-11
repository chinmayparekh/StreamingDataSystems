import os
import time

input_file = 'stream.csv'
temp_file = 'unique_words.txt'

# Function to check and write a character to the temp file if it's not already present
def checkAndWrite(char):
    is_repetition = False
    
    # Open the temporary file for reading
    with open(temp_file, 'r') as temp_read:
        for line in temp_read:
            if char == line.strip():
                # print("Duplicate")
                is_repetition = True
                break

    # If the character is not a repetition, append it to the temporary file
    if not is_repetition:
        with open(temp_file, 'a') as temp:
            temp.write(char + '\n')

# Start the timer
start_time = time.time()

# Open the input stream file for reading
with open(input_file, 'r') as stream:
    for line in stream:
        char=line.strip()
        # print(char)
        checkAndWrite(char)

# End the timer
end_time = time.time()

# Calculate and print the execution time
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.2f} seconds")
print("Unique characters extracted and saved to 'unique_words.txt'")

# Data = 20,000
# Execution time: 16.47 seconds
# Unique characters extracted and saved to 'unique_words.txt'
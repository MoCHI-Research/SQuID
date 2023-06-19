# The starting menu for the QuAD system
from gptconnection import openai_sys_chatcompletion
import csv
import os
import time
import math
import threading

# A flag to tell the thread to stop
stop_thread = False
final_time_elapsed = 0

"""
Show the total elapsed time of the program
Parameters:
    None
Returns:
    None
"""
def show_time_elapsed():
    global final_time_elapsed
    start_time = time.time()

    while not stop_thread:
        time.sleep(0.1)  # update every second
        elapsed_time = time.time() - start_time
        print(f"Time elapsed: {elapsed_time:.1f} seconds", end='\r')  # end='\r' overwrites the line

        if stop_thread:
            final_time_elapsed = elapsed_time

"""
Convert the gpt responses into a CSV file
Parameters:
    input_string(string): The GPT response that will be converted into a CSV file
Returns:
    output.csv: the CSV file that contains the converted responses
"""
def convert_gpt_to_csv(input_string):
    output_filename = 'output.csv'
    
    lines = input_string.split('\n')
    
    group_name = ''
    group_data = []
    csv_data = []

    # Parse the lines
    for line in lines:
        line = line.strip()
        if line.startswith('Group'):
            if group_name:
                csv_data.append((group_name, group_data))
            group_name = line.split(':', 1)[1].strip()
            group_data = []
        elif line.startswith('-'):
            group_data.append(line[2:])  # Skip the leading "- "

    if group_name and group_data:  # Add the last group
        csv_data.append((group_name, group_data))
        
    file_exists = os.path.exists(output_filename)

    # Write to CSV
    with open(output_filename, 'a' if file_exists else 'w', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:  # Write the header only if the file didn't exist
            writer.writerow(['Group', 'Items'])
        for data in csv_data:
            group = data[0]
            for item in data[1]:
                writer.writerow([group, item])

"""
Asks GPT for a response for the data chunks then calls 'convert_gpt_to_csv' to compile the responses into a CSV file
Parameters:
    list_of_data(list): the list of each data point
    completed_gpt_requests(int): the number of chunks completed
    num_of_gpt_requests(int): the final number of chunk requests to GPT
    gpt_template(string): the template prompt that asks GPT to generate our data
Returns:
    completed_gpt_requests(int): the number of completed GPT requests to fulfill the while loop conditional 
"""
def ask_and_compile_gpt(parsed_list_of_data, completed_gpt_requests, num_of_gpt_requests, gpt_template):
    
    user_input_string = ''
    for data in parsed_list_of_data:
        user_input_string += data

    response = openai_sys_chatcompletion(gpt_template, user_input_string)
    completed_gpt_requests += 1
    print(f"Successfully generated {completed_gpt_requests}/{num_of_gpt_requests} GPT responses.\n")
    time.sleep(1)
    convert_gpt_to_csv(response)
    print(f"Successfully converted {completed_gpt_requests}/{num_of_gpt_requests} GPT responses to a CSV.\n")
    
    return completed_gpt_requests

"""
Grabs the data points from a CSV file and asks GPT to sort them by group labels like an affinity diagram
Parameters:
    file(csv file): the user's csv file that contains all of their data
Returns:
    None
"""
def label_datapoints(file):
    
    if os.path.exists('output.csv'):
        os.remove('output.csv')
        print("'output.csv' deleted successfully.")
    
    print("Generating GPT response . . .\n")
    list_of_data = []
    chunk_size = 25
    
    gpt_template = 'group_data'
    with open(file, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            list_of_data.append(row[0])
    
    num_of_gpt_requests = math.ceil(len(list_of_data) / chunk_size)
    completed_gpt_requests = 0
    
    print("Average time: " + str(math.ceil(num_of_gpt_requests * 19.88 / 60)) + " minutes\n")

    # x and y are the indices indicating the chunks of data to parse through
    x = 0
    y = chunk_size

    while completed_gpt_requests < num_of_gpt_requests:
        completed_gpt_requests = ask_and_compile_gpt(list_of_data[x:y], completed_gpt_requests, num_of_gpt_requests, gpt_template)
        x = y
        y += chunk_size  
        if y > len(list_of_data):
            y = len(list_of_data)
    
    print("Job's done.")
    

# # A function that accepts file inputs and returns the inputted file
# def file_input():
#     filename = input("Filename: ")
#     file_out = open(filename, "r")
#     return file_out

# # A simple menu system that takes in an integer from the user to select a feature
# def menu():
#     print("[1] Regenerate all group labels\n[2] Reason for a label\n[3] Change label merge threshold\n[4] Create an Affinity Diagram\n")
#     user_choice = int(input("Choice: "))
#     match user_choice:
#         case 1:
#             print("Regenerate all group labels")
#         case 2:
#             print("Reason for a label")
#         case 3:
#             print("Change label merge threshold")
#         case 4:
#             label_datapoints(file_input())


def main():
    global stop_thread

    # # Start the loading thread for the time elapsed
    loading_thread = threading.Thread(target=show_time_elapsed)
    loading_thread.start()

    label_datapoints('student_dataset.csv')
    
    # Stop the loading thread and show the total amount of time elapsed
    stop_thread = True
    loading_thread.join()
    print(f"Final time elapsed: {final_time_elapsed:.1f} seconds")
    
if __name__ == "__main__":
    main()



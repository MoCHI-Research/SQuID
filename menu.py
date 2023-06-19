# The starting menu for the QuAD system
from gptconnection import openai_chatcompletion
import csv
import os
import time
import threading
import json

GPT_TEMPLATES = json.load(open('prompts.json'))

# A flag to tell the thread to stop
stop_thread = False
final_time_elapsed = 0

def show_time_elapsed():
    global final_time_elapsed
    start_time = time.time()
    while True:
        time.sleep(0.1)  # update every second
        elapsed_time = time.time() - start_time
        print(f"Time elapsed: {elapsed_time:.1f} seconds", end='\r')  # end='\r' overwrites the line
        if stop_thread:
            final_time_elapsed = elapsed_time
            break

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

# Grabs the data points from a CSV file and asks GPT to sort them by group labels like an affinity diagram
def label_datapoints(file):
    print("Generating GPT response . . .\n")
    
    gpt_template = GPT_TEMPLATES['group_data']
    with open(file, newline='') as f:
        reader = csv.reader(f)
        count2 = 0
        count = 0
        for row in reader:
            gpt_template += (row[0]) + '\n'
            if count == 25:
                response = openai_chatcompletion(gpt_template)
                print('Successfully generated one GPT response.\nGenerating a CSV file . . .')
                convert_gpt_to_csv(response)
                count = -1
            count += 1
            if count2 == 100:
                break
            count2 += 1
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
    # Begin loading the labels with their datapoints
    label_datapoints('student_dataset.csv')
    # convert_gpt_to_csv('input.txt')
    
    
    
# # Start the loading thread
loading_thread = threading.Thread(target=show_time_elapsed)
loading_thread.start()

main()

# # Stop the loading thread
stop_thread = True
loading_thread.join()
print(f"Final time elapsed: {final_time_elapsed:.1f} seconds")

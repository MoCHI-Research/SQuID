# The starting menu for the QuAD system
from gptconnection import openai_sys_chatcompletion, openai_example_chatcompletion
from merge_labels import merge_labels
import csv
import os
import time
import re
import math
import threading

# GLOBAL VARIABLES
SIZE_OF_BATCHES = 75
DATASET_PATH = "datasets/"

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
    global stop_thread
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
Convert the gpt responses, with numbers representing data points, into a CSV file
Parameters:
    gpt_response(string): The GPT response that includes data points as numbers
    data_list(list of strings): the list of all data points concerned
Returns:
    output.csv: the CSV file that contains the converted responses
"""
def convert_num_to_csv(gpt_response, data_list):
    output_filename = 'output.csv'
    group_name = ''
    group_data = []
    csv_data = []

    response_include = [False for _ in range(len(data_list))]

    lines = gpt_response.split('\n')

    for line in lines:
        line = line.strip()
        if line.startswith('Group'):
            if group_name:
                csv_data.append((group_name, group_data))
            group_name = line.split(':', 1)[1].strip()
            group_data = []
        elif line:
            sentence_indices = (re.findall("[0-9]+", line))

            for sent_index in sentence_indices:
                current_index = int(sent_index)
                if current_index < len(data_list):
                    group_data.append(data_list[current_index])
                    response_include[current_index] = True

    if group_name and group_data:  # Add the last group
        csv_data.append((group_name, group_data))

    not_grouped_data = []
    for current_index in range(len(response_include)):
        if not response_include[current_index]:
            not_grouped_data.append(data_list[current_index])
    csv_data.append(('Not Grouped', not_grouped_data))

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
Asks GPT for a response for the data batches then calls 'convert_gpt_to_csv' to compile the responses into a CSV file
Parameters:
    list_of_data(list): the list of each data point
    completed_gpt_requests(int): the number of batches completed
    num_of_gpt_requests(int): the final number of batches requests to GPT
    gpt_template(string): the template prompt that asks GPT to generate our data
Returns:
    completed_gpt_requests(int): the number of completed GPT requests to fulfill the while loop conditional
"""
def ask_and_compile_gpt(parsed_list_of_data, completed_gpt_requests, num_of_gpt_requests, gpt_template):

    data_num = len(parsed_list_of_data)

    response = None
    user_input_string = ''

    #for data in parsed_list_of_data:
        #user_input_string += data

    for i in range(data_num):
        current_data = str(i) + ". " + parsed_list_of_data[i] + "\n"
        user_input_string += current_data

    while response == None:
        response = openai_example_chatcompletion(gpt_template, "user_example", "response_example", user_input_string)
        #response = openai_sys_chatcompletion(gpt_template, user_input_string)

    print(response)

    completed_gpt_requests += 1
    print(f"Successfully generated {completed_gpt_requests}/{num_of_gpt_requests} GPT responses.\n")
    time.sleep(1)
    #convert_gpt_to_csv(response)
    convert_num_to_csv(response, parsed_list_of_data)
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
    batch_size = SIZE_OF_BATCHES

    #gpt_template = 'group_data'
    #gpt_template = 'group_data_no_example'
    gpt_template = 'group_data_in_numbers'
    with open(file, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                list_of_data.append(row[0])

    # Initial check to see if batch is bigger than the dataset
    if batch_size > len(list_of_data):
        batch_size = len(list_of_data)


    num_of_gpt_requests = math.ceil(len(list_of_data) / batch_size)
    completed_gpt_requests = 0

    print(f'Batches to complete: {num_of_gpt_requests}')

    # x and y are the indices indicating the batches of data to parse through
    x = 0
    y = batch_size

    while completed_gpt_requests < num_of_gpt_requests:
        completed_gpt_requests = ask_and_compile_gpt(list_of_data[x:y], completed_gpt_requests, num_of_gpt_requests, gpt_template)
        x = y
        y += batch_size
        if y > len(list_of_data):
            y = len(list_of_data)

    print("Job's done.")


# # A function that accepts file inputs and returns the inputted file
def file_input():
    file_out = input("Filename: ")
    return file_out

# # Retrieves all data with the label_to_search
def retrieve_data_with_label(label_to_search, filename = "output.csv"):
    # Check if file exists
    if not os.path.isfile(filename):
        print(f"File '{filename}' does not exist in the current directory. Please go back to the menu and create an affinity diagram to use this feature.")
    else:
        # Open the file and search
        all_data_with_label = []
        label_and_data = ()
        with open(filename, 'r') as file:
             csv_reader = csv.reader(file)
             for row in csv_reader:
                 if len(row) > 0:
                     if row[0] == label_to_search:
                        label_and_data = (row[0], row[1])
                        all_data_with_label.append(label_and_data)

    return all_data_with_label

# # Generates a reason through GPT for labeling the data with label 
def generate_reason(all_data, data_index, label):
    print("Data: " + str(all_data[int(data_index) - 1][1]))
    print("Label: " + label)

    data = all_data[int(data_index) - 1][1]
    user_input_string = "Provide a reason for giving the label " + label + " to the the following data: " + data
    response = None
    gpt_template = "provide_reason"

    # Prompts GPT-4 for the reason
    while response == None:
        response = openai_sys_chatcompletion(gpt_template, user_input_string)

    return response


def change_merge_threshold(merge_threshold):
    print("Your label merge threshold is currently:", merge_threshold)
    print("\nNote: The higher the threshold is, the more unlikely groups will get merged, and the more groups the end result will have. Our suggested threshold is 0.91.\n")
    new_threshold = 0
    user_input = input("Enter a new threshold, which is a decimal between 0 and 1(exclusive). Press enter to continue: ")
    while (not new_threshold) and user_input != "":
        try:
            new_threshold = float(user_input)
            if new_threshold <= 0 or new_threshold >= 1:
                print("Your input is outside of the valid threshold range. it should be a decimal between 0 and 1(exclusive).\n")
                new_threshold = 0
                user_input = input("Enter a new threshold, which is a decimal between 0 and 1(exclusive). Press enter to continue: ")
            else:
                merge_threshold = new_threshold
        except:
            print("Your input is not valid. Please try again.\n")
            user_input = input("Enter a new threshold, which is a decimal between 0 and 1(exclusive). Press enter to continue: ")

    print("Your label merge threshold is now", merge_threshold)
    return merge_threshold


# A simple menu system that takes in an integer from the user to select a feature
def menu():
    exit = 0
    global stop_thread

    merge_threshold = 0.91

    while(exit != 1):
        print("\n[1] Create an Affinity Diagram\n[2] Reason for a label\n[3] Change label merge threshold\n[4] Regenerate all group labels\n[5] Readability scores\n[6] Merge groups that are identical or similar\n[7] Exit\n")
        user_choice = input("Choice: ")
        match user_choice:
            case '1' | '4':
                file = file_input()
                time.sleep(1.5)

                # Start the loading thread for the time elapsed
                loading_thread = threading.Thread(target=show_time_elapsed)
                loading_thread.start()

                try:
                    label_datapoints(DATASET_PATH + file)
                except PermissionError:
                    print("Failed to access the output file. Please close it if it is open. Going back to the main menu...\n")
                except FileNotFoundError:
                    print("Failed to find the file. Please check your file name and make sure it is in the dataset directory. Going back to the main menu...\n")

                stop_thread = True
                loading_thread.join()
                print(f"Final time elapsed: {final_time_elapsed:.1f} seconds")

            case '2':
                reason_for_label()
            case '3':
                merge_threshold=change_merge_threshold(merge_threshold)


            case '5':
                print("Readability scores not yet implemented . . .")
            case '6':
                loading_thread = threading.Thread(target=show_time_elapsed)
                loading_thread.start()

                merge_labels(merge_threshold = merge_threshold)

                stop_thread = True
                loading_thread.join()
                print(f"Final time elapsed: {final_time_elapsed:.1f} seconds")
            case '7':
                print("Exiting the program . . .\n")
                exit = 1
            case _:
                print("That is not an option. Please select an option from the list.\n")
        time.sleep(3)

def main():
    menu()


if __name__ == "__main__":
    main()

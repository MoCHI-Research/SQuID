# The starting menu for the QuAD system
from gptconnection import openai_sys_chatcompletion, openai_example_chatcompletion
from merge_labels import merge_labels
import csv
import os
import time
import re
import math
import threading
from interface import start_interface


# GLOBAL VARIABLES
SIZE_OF_BATCHES = 75
DATASET_PATH = "datasets/"

# A flag to tell the thread to stop
stop_thread = False
final_time_elapsed = 0


#----------------------------------------------------------------------#
#                       Miscellaneous Functions                        # ------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------#

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

#----------------------------------------------------------------------#
#                       Running Affinity Diagram                       # ------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------#

def convert_to_csv(gpt_response, data_list, prev_data, not_grouped_data):
    """
    Convert the gpt responses, with numbers representing data points, into a CSV file
    Parameters:
        gpt_response(string): The GPT response that includes data points as numbers
        data_list(list of strings): the list of all data points concerned
    Returns:
        output.csv: the CSV file that contains the converted responses
    """
    output_filename = 'output.csv'
    group_name = ''
    group_data = []
    csv_data = []
    response_include = [False for _ in range(len(data_list))]
    lines = gpt_response.split('\n')
    file_exists = os.path.exists(output_filename)

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
                #If a data (secondary label) is "Not Grouped," do not put it in any of the groups
                if current_index < len(data_list) and not data_list[current_index] == "Not Grouped":
                    group_data.append(data_list[current_index])
                    response_include[current_index] = True

    if group_name and group_data:  # Add the last group
        csv_data.append((group_name, group_data))

    for current_index in range(len(response_include)):
        if not response_include[current_index]:
            not_grouped_data.append(data_list[current_index])

    if len(not_grouped_data) > 0:
        csv_data.append(('Not Grouped', not_grouped_data))

    # If file exists, then that means we are dealing with a layer count > 1
    # First: Save all of the previous data into a list
    # Then: Create a new list that appends the information from the previous data with the new label associated with that row
    # Else: This is a new file, so initialize the CSV file 
    if file_exists and len(prev_data) > 0:
        # This is where the appending prev_data to the csv list will happen
        for data in csv_data:
            for i in range(len(data[1])):
                for j in range(len(prev_data)):
                    if data[1][i] == prev_data[j][0]:
                        prev_data[j].insert(0,data[0])
        # Writes to the output file with the new column
        with open(output_filename, 'w', newline='') as file:
            writer=csv.writer(file)
            for data in prev_data:
                writer.writerow(data)
            file.close()
    else:
    # If the output_file exists, then append the information. If it doesn't exist, then write the initial data_labels
        with open(output_filename, 'a' if file_exists else 'w', newline='') as file:
            writer = csv.writer(file)
            for data in csv_data:
                group = data[0]
                for item in data[1]:
                    writer.writerow([group, item])
            file.close()

def gpt_responses(list_of_data, completed_gpt_requests, num_of_gpt_requests, gpt_template, prev_data):
    """
    Asks GPT for a response for the data batches then calls 'convert_to_csv' to compile the responses into a CSV file
    Parameters:
        list_of_data(list): the list of each data point
        completed_gpt_requests(int): the number of batches completed
        num_of_gpt_requests(int): the final number of batches requests to GPT
        gpt_template(string): the template prompt that asks GPT to generate our data
    Returns:
        completed_gpt_requests(int): the number of completed GPT requests to fulfill the while loop conditional
    """
    parsed_list_of_data = []
    not_grouped = []

    for data in list_of_data:
        if data == "Not Grouped":
            not_grouped.append(data)
        else:
            parsed_list_of_data.append(data)

    data_num = len(parsed_list_of_data)
    response = None
    user_input_string = ''

    for i in range(data_num):
        current_data = str(i) + ". " + parsed_list_of_data[i] + "\n"
        user_input_string += current_data

    while response == None:
        response = openai_example_chatcompletion(gpt_template, "user_example", "response_example", user_input_string)
    print("Response:",response)

    completed_gpt_requests += 1
    print(f"Successfully generated {completed_gpt_requests}/{num_of_gpt_requests} GPT responses.\n")
    convert_to_csv(response, parsed_list_of_data, prev_data, not_grouped)
    print(f"Successfully converted {completed_gpt_requests}/{num_of_gpt_requests} GPT responses to a CSV.\n")
    return completed_gpt_requests

def initialize_gpt_responses(num_of_gpt_requests, list_of_data, completed_gpt_requests, gpt_template, batch_size, hierarchy):
    """Creates a one-layer deep affinity diagram"""
    start = 0
    end = batch_size
    prev_data = []
    output_filename = 'output.csv'

    # If the output_file exists and if we are creating the hierarchy (hierarchy == True), we will save the previous data into prev_data
    # so that we can write the new labels into the associated row it belongs to
    if os.path.exists(output_filename) and hierarchy:
        with open(output_filename, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                prev_data.append(row)

    while completed_gpt_requests < num_of_gpt_requests:
        completed_gpt_requests = gpt_responses(list_of_data[start:end], completed_gpt_requests, num_of_gpt_requests, gpt_template, prev_data)
        start = end
        end += batch_size
        if end > len(list_of_data):
            end = len(list_of_data)

def unique_labels(first_pass_completed, merge_threshold):
    """
    1. Take in the output.csv file
    2. Check the 0th col, put each unique label into a list
        if elem not in list:
            put_in_list
    3. Run GPT on it
    """
    file = 'output.csv'

    # First, grab all unique label names
    # Then check if the first element of a col is already in unique_labels
    # If it isn't, add it
    unique_labels = []
    with open(file, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] not in unique_labels and row[0] != 'Group' and row[0] != '':
                unique_labels.append(row[0])

    valid_label_num = len(unique_labels)
    if "Not Grouped" in unique_labels:
        valid_label_num -= 1

    # Checks if the first pass has been completed or not
    # If it hasn't, then that means unique_labels will not contain any duplicate information (not guaranteed, assumption)
    # Else, if unique_labels > 1 and first_pass_completed == True,
    # We check every label that was previously assigned.
    # If there exists a duplicate label in unique_labels that appears as an already assigned label (excluding 'Not Grouped')
    # Then we return. Else, run the next hierarchy level
    if first_pass_completed == False:
        affinity_diagram(file, merge_threshold, unique_labels, True, True)
    elif valid_label_num > 1:
        with open(file, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] in unique_labels and row[1] != 'Not Grouped':
                    return
        affinity_diagram(file, merge_threshold, unique_labels, True, True)

def affinity_diagram(file, merge_threshold, list_of_data = None, hierarchy = False, first_pass_completed = False):
    """
    Grabs the data points from a CSV file and asks GPT to sort them by group labels like an affinity diagram
    Parameters:
        file(csv file): the user's csv file that contains all of their data
    Returns:
        None
    """
    if list_of_data == None:
        list_of_data = []
    print("Generating GPT response . . .\n")
    batch_size = SIZE_OF_BATCHES
    gpt_template = 'group_data_in_numbers'

    # Checks if the length of the list_of_data (unique_datapoints) is 0
    # If it is, then that means we're dealing with the first pass
    # If it isn't, then we're not and we don't need to construct list_of_data
    if len(list_of_data) == 0:
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

    # Calls GPT for one run of batches over a list of datapoints
    initialize_gpt_responses(num_of_gpt_requests, list_of_data, completed_gpt_requests, gpt_template, batch_size, hierarchy)
    merge_labels(merge_threshold, original_file = "output.csv", output_file = "output.csv")

    # default file_name is output.csv
    # Starts creating the hierarchy of labels
    unique_labels(first_pass_completed, merge_threshold)
    
def initialize_affinity_diagram(file, merge_threshold):
    """
    Initializes the affinity diagramming process by first removing then
    creating an output.csv file
    """ 
    if os.path.exists('output.csv'):
        os.remove('output.csv')
        print("'output.csv' deleted successfully.")
    affinity_diagram(file, merge_threshold, list_of_data = [])
    
    #Add header to the file
    with open('output.csv',newline='') as f:
        r = csv.reader(f)
        data = [line for line in r]
    if data: 
        with open('output.csv','w',newline='') as f:
            w = csv.writer(f)
            header = []
            for i in range(len(data[0]) - 1, 0, -1):
                header.append("Pass " + str(i))
            header.append("Data Item")
            w.writerow(header)
            w.writerows(data)

    print("Job's done.")

#----------------------------------------------------------------------#
#                         Auxiliary Functions                          # ------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------#

# # Retrieves all data with the label_to_search
def retrieve_data_with_label(label_to_search, column_num, filename = "output.csv"):
    if not os.path.isfile(filename):
        print(f"File '{filename}' does not exist in the current directory. Please go back to the menu and create an affinity diagram to use this feature.")
    else:
        # Open the file and search
        all_data_with_label = []
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[column_num] == label_to_search:
                    data = row[column_num + 1]
                    label_and_data = (label_to_search, data)
                    all_data_with_label.append(label_and_data)

    return all_data_with_label

# # Returns how many passes there are by counting number of columns in output.csv
def num_columns(filename = "output.csv"):
    if not os.path.isfile(filename):
        print(f"File '{filename}' does not exist in the current directory. Please go back to the menu and create an affinity diagram to use this feature.")
    else:
        with open(filename, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            first_row = next(csv_reader)
            column_count = len(first_row)
            column_count -= 1
            return column_count

# # Returns all unique labels from a given column number
def column_labels(column_num, filename = "output.csv"):
    unique_entries = set()

    with open(filename, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            if len(row) > column_num:
                entry = row[column_num]
                unique_entries.add(entry)

    unique_entries = list(unique_entries)

    return unique_entries


# # Generates a reason through GPT for labeling the data with label
def generate_reason(all_data, data_index, label):
    print("Data: " + str(all_data[int(data_index) - 1][1]))
    print("Label: " + str(label))

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


def main():
    start_interface()

if __name__ == "__main__":
    main()

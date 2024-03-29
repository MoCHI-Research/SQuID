# The starting menu for the QuAD system
from gptconnection import openai_sys_chatcompletion, openai_example_chatcompletion
from merge_labels import merge_labels
import csv
import os
import time
import re
import math
import sys
import threading
import asyncio
import customtkinter

# GLOBAL VARIABLES
SIZE_OF_BATCHES = 75
FORCE_STOP = 50
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
#                         New Diagramming Process                      # ------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------#

"""
Checks if the passed integer is an existing pass in the csv file
used in ui.py
"""
def valid_pass(pass_num):
    output_path = os.path.join(os.path.dirname(sys.argv[0]), 'output.csv')
    if not os.path.exists(output_path):
        return False

    with open(output_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        num_columns = len(next(reader))

    if pass_num >= num_columns - 1:
        return False
    else:
        return True

"""
Removes dictionary key-value pair duplicates
used in ui.py
"""
def remove_dict_duplicates(dictionary):
    unique_dict = {}
    for key, value in dictionary.items():
        if key not in unique_dict.keys():
            unique_dict[key] = value
    return unique_dict


"""
Grabs the associated key value pairs from a given column
and the column to the right
used in ui.py
"""
def retrieve_pass(column_number):
    output_path = os.path.join(os.path.dirname(sys.argv[0]), 'output.csv')
    if not os.path.exists(output_path):
        return False  # 'output.csv' file does not exist

    column_dict = {}

    with open(output_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) > column_number + 1:  # Ensure column exists and cell to the right exists
                column_dict[row[column_number]] = row[column_number + 1]

    return column_dict

"""
Sets up an output file
used in menu.py
used in ui.py
"""
def set_output_file(delete=False):
    # output_file = customtkinter.filedialog.asksaveasfilename(
    #     defaultextension=".csv", 
    #     filetypes=[("Text Files", "*.csv"), ("All Files", "*.*")], 
    #     initialfile="output.csv", 
    #     title="Save File")

    output_file = os.path.join(os.path.dirname(sys.argv[0]), 'output.csv')
    if delete and os.path.exists(output_file):
        os.remove(output_file)

    return output_file

"""
Checks if data exists in the file
used in menu.py
"""
def existing_data(file):
    with open(file, 'r', newline='') as file:
            reader = csv.reader(file)
            existing_data = list(reader)

    if existing_data:
        return True
    else:
        return False

"""
Adds headers to csv
used in ui.py
"""
def add_headers_to_csv(file_path):
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)

    num_columns = len(data[0])
    headers = ["Data"]
    headers += [f'Label Level {i}' for i in range(1, num_columns)]

    data.insert(0, headers)

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

"""
Saves accepted data to file (or writes orig data in
first column if process has yet to began)
used in ui.py
"""
def save_data(data, output_file, first_pass=False):
    output_file = set_output_file()
    if first_pass:
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            for item in data:
                writer.writerow([item])
    else:
        with open(output_file, mode='r') as file:
            reader = csv.reader(file)
            header = next(reader)
            right_column_index = len(header) - 1
            header_key = header[right_column_index]
            
            
            header.append(data[header_key])

            rows = []
            for row in reader:
                key = row[right_column_index]
                try:
                    row.append(data[key])
                except KeyError:
                    print(data)
                    print("Key Error with key: ", [key])
                    row.append("Not Grouped")
                rows.append(row)

        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)
    return output_file

"""
Writes accepted data to output file
not used anywhere; could delete(?)
"""
def write_tuples_to_file(data):
    output_file = set_output_file()
    if existing_data(output_file):
        print("No existing data")
    else:
        print("There exists data")

"""
Determines size of batches
used in ui.py
"""
def set_batch_size(data_size):
    global SIZE_OF_BATCHES
    if SIZE_OF_BATCHES > data_size:
        batch_size = data_size
    else:
        batch_size = SIZE_OF_BATCHES
    return batch_size

"""
Returns an array of all data items from csv
used in ui.py start_event()
"""
def set_data_list(file):
    list_of_data = []
    with open(file, newline='') as f:
        # reader = csv.reader(f)
        # for row in reader:
        #     if row:
        #         list_of_data.append(row[0])
        for line in f:
            #list_of_data.append(line.strip("\r"))
            line = line.strip("\n")
            line = re.sub(r'(?is)\r', '\n', line) # Make sure to use \n for proper dictionary key index
            list_of_data.append(line)

        
        # print("aaaaaaaaaa")
        # for datum in list_of_data:
        #     print([datum])
        
    return list_of_data

"""
Processes a small subset of data items by prompting gpt
Change name to something; process_batch() exists here and in ui.py --------------->>>>>>>>>>>>>>>>>>>>>>>=
"""
def process_batch(gpt_template, user_input_string):
    results = None
    while results == None:
        results = openai_example_chatcompletion(gpt_template, "user_example", "response_example", user_input_string)
    return results

"""
Returns a numbered list of given data as a string
Used in ui.py process_batch()
"""
def numbered_data(data):
    user_input_string = ""
    current_data = ""
    for num in range(len(data)):
        current_data = str(num) + ". " + data[num] + "\n"
        user_input_string += current_data
    return user_input_string

"""
Processes raw gpt response for csv creation
Used in ui.py process_batch()
"""
def process_results(results, batch):
    batch_message = """
    #----------------------------------------------------------------------#
    #                         Batch In Progress                            #
    #----------------------------------------------------------------------#
    """
    print(batch_message)
    response_included = [False for _ in range(len(batch))]

    formatted_data = format_results(results)
    response_included = check_missing_data(len(batch), formatted_data, response_included)
    formatted_data = adjust_data(formatted_data, response_included)
    adjust_message = """
    #----------------------------------------------------------------------#
    #                         Adjusted Data                                #
    #----------------------------------------------------------------------#
    """
    print(adjust_message)
    print(formatted_data)
    csv_data = indices_to_data(formatted_data, batch)
    csv_message = """
    #----------------------------------------------------------------------#
    #                               CSV DATA                               #
    #----------------------------------------------------------------------#
    """
    print(csv_message)
    print(csv_data)
    return csv_data

"""
Formats results into a list of tuples in the format -> (Group Label, [indices])
"""
def format_results(results):
    group_data = []
    result_list = results.split('\n')
    for j in range(len(result_list)):
        line = result_list[j]
        if line.startswith("Group"):
            if j > FORCE_STOP:
                return group_data
            group_name = re.search(r'Group \d+: (.+)', line).group(1)
        elif re.search(r'\d+\,', line):
            indices = []
            for i in line.split(','):
                i = i.strip()
                if i[-1] == '.':
                    i = i[:-1]
                indices.append(int(i))
            group_data.append((group_name, indices))
        elif re.search(r'\d+\.', line):
            indices = [int(re.search(r'(\d+)\.', item).group(1)) for item in line.split() if re.search(r'\d+\.', item)]
            group_data.append((group_name, indices))
        elif re.search(r'\b\d+\b', line):
            single_digit = int(re.search(r'\b(\d+)\b', line).group(1))
            group_data.append((group_name, [single_digit]))

    return group_data

"""
Changes the index values to the batch data
"""
def indices_to_data(formatted_data, batch):
    csv_format = []

    for group_label, indices in formatted_data:
        updated_indices = []
        for i in indices:
            if i < len(batch):
                updated_indices.append(batch[i])
        if updated_indices:
            csv_format.append((group_label, updated_indices))

    return csv_format

"""
Adds ungrouped data to the formatted_data
"""
def adjust_data(formatted_data, response_included):
    if all(response_included):
        return formatted_data
    else:
        not_grouped_indices = []
        for i in range(len(response_included)):
            if not response_included[i]:
                not_grouped_indices.append(i)
        formatted_data.append(("Not Grouped", not_grouped_indices))
        return formatted_data

"""
Checks if each data number was grouped
"""
def check_missing_data(data_len, formatted_data, response_included):
    print("Formatted Data: ", formatted_data)
    print("Response Included: ", response_included)
    for group_label, indices in formatted_data:
        for index in indices:
            if index < data_len:
                response_included[index] = True

    return response_included


"""
Changes string to have line breaks
"""
def add_linebreaks(sentence: str):
    words = sentence.split()
    num_words = len(words)
    words_with_newlines = [word + ("\n" if (i + 1) % 10 == 0 and i + 1 != num_words else " ") for i, word in enumerate(words)]
    modified_string = ''.join(words_with_newlines)
    return modified_string

"""
Returns the set batch size
"""
def get_batch_size():
    global SIZE_OF_BATCHES
    return SIZE_OF_BATCHES



#----------------------------------------------------------------------#
#                         Auxiliary Functions                          # ------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------#

# # Retrieves all data with the label_to_search
def retrieve_data_with_label(label_to_search, column_num, filename = "output.csv"):
    filename = os.path.join(os.path.dirname(sys.argv[0]), filename)
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
    filename = os.path.join(os.path.dirname(sys.argv[0]), filename)
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
    filename = os.path.join(os.path.dirname(sys.argv[0]), filename)

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
def generate_reason(data, label):
    print("Data: " + data)
    print("Label: " + label)

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

# The starting menu for the QuAD system
from gptconnection import openai_chatcompletion
import csv
import os

def convert_gpt_to_csv(input_string):
    # Convert the input_string into lines
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

    # Write to CSV
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Group', 'Items'])
        for data in csv_data:
            group = data[0]
            for item in data[1]:
                writer.writerow([group, item])
    print("Successfully created 'output.csv'")

# Grabs the data points from a CSV file and asks GPT to sort them by group labels like an affinity diagram
def label_datapoints(file):
    print("Generating GPT response . . .\n")
    
    gpt_template = "Group the following data based on similarity using as many groups as you find appropriate:\n"
    with open(file, newline='') as f:
        reader = csv.reader(f)
        count = 0
        for row in reader:
            gpt_template += (row[0]) + '\n'
            if count == 10:
                break
            count += 1
    response = openai_chatcompletion(gpt_template)
    print('Successfully generated GPT response.\nGenerating CSV file . . .')
    
    convert_gpt_to_csv(response)

# A function that accepts file inputs and returns the inputted file
def file_input():
    filename = input("Filename: ")
    file_out = open(filename, "r")
    return file_out

# A simple menu system that takes in an integer from the user to select a feature
def menu():
    print("[1] Regenerate all group labels\n[2] Reason for a label\n[3] Change label merge threshold\n[4] Create an Affinity Diagram\n")
    user_choice = int(input("Choice: "))
    match user_choice:
        case 1:
            print("Regenerate all group labels")
        case 2:
            print("Reason for a label")
        case 3:
            print("Change label merge threshold")
        case 4:
            label_datapoints(file_input())

label_datapoints('student_dataset.csv')
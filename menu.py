# The starting menu for the QuAD system
from gptconnection import openai_chatcompletion
import csv
import os



def label_datapoints(file):
    gpt_template = "Group the following data based on similarity using as many groups as you find appropriate:\n"
    with open(file, newline='') as f:
        reader = csv.reader(f)
        count = 0
        for row in reader:
            gpt_template += (row[0]) + '\n'
            if count == 10:
                break
            count += 1
    print(openai_chatcompletion(gpt_template))

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
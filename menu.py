# The starting menu for the QuAD system

# A function that accepts file inputs and returns the inputted file
def file_input():
    filename = input("Filename: ")
    file = open(filename, "r")
    return file

# A simple menu system that takes in an integer from the user to select a feature
def menu():
    print("[1] Regenerate all group labels\n[2] Reason for a label\n[3] Change label merge threshold\n")
    user_choice = int(input("Choice: "))
    match user_choice:
        case 1:
            print("Regenerate all group labels")
        case 2:
            print("Reason for a label")
        case 3:
            print("Change label merge threshold")
    
    
        
menu()

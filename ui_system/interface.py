from tkinter import *




def create_menu():
    window = Tk()

    window.title("Menu Prototype")
    
    new_project_label = Label(window, text="New Project")
    prompts_label = Label(window, text="Prompts")
    settings_label = Label(window, text="Settings")
    
    new_project_label.grid(column = 5, row = 3)
    prompts_label.grid(column = 5, row = 4)
    settings_label.grid(column = 5, row = 5)
    
    window.mainloop()

create_menu()
import tkinter as tk
import customtkinter as ctk

def foo():
    print("bar")


def create_menu():
    window = tk.Tk()
    window.title("Menu Prototype")
    
    width = 500
    height = 200
    
    window.geometry(str(width) + 'x' + str(height))
    
    screen_width = window.winfo_screenwidth()  # Width of the screen
    screen_height = window.winfo_screenheight() # Height of the screen
    # Calculate Starting X and Y coordinates for Window
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height)
    
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))
    
    file_button = ctk.CTkButton(master=window, text="File", corner_radius=10, command=foo)
    generate_labels_button = ctk.CTkButton(master=window, text="Generate Labels", corner_radius=10, command=foo)
    merge_threshold_button = ctk.CTkButton(master=window, text="Change Merge Threshold", corner_radius=10, command=foo)
    regen_labels_button = ctk.CTkButton(master=window, text="Regenerate Labels", corner_radius=10, command=foo)
    merge_similar_button = ctk.CTkButton(master=window, text="Merge Similar Labels", corner_radius=10, command=foo)
    
    file_button.place(relx=0.5,rely=0.1,anchor=tk.CENTER)
    generate_labels_button.place(relx=0.5,rely=0.3,anchor=tk.CENTER)
    merge_threshold_button.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
    regen_labels_button.place(relx=0.5,rely=0.7,anchor=tk.CENTER)
    merge_similar_button.place(relx=0.5,rely=0.9,anchor=tk.CENTER)
    
    window.mainloop()

create_menu()


"""
Create an affinity diagram
Reason for a label
Change label merge threshold
Regeneratae all group labels
Merge identical / similar groups
"""
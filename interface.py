import tkinter as tk
import customtkinter as ctk
from menu import label_datapoints
from menu import reason_for_label
from menu import merge_labels
from menu import change_merge_threshold

DATASET_PATH = "datasets/"

ctk.set_appearance_mode("System")

"""Class for the app's interface"""    
class App(ctk.CTk):
    """Constructor for the App class."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("SQUID Prototype")   
        width = 600
        height = 400
        
        self.geometry(str(width) + 'x' + str(height))
        
        screen_width = self.winfo_screenwidth()  # Width of the screen
        screen_height = self.winfo_screenheight() # Height of the screen
        # Calculate Starting X and Y coordinates for Window
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height)
        
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        
        self.textbox = ctk.CTkTextbox(master=self,width=200,height=30)
        self.textbox.place(relx=0.5,rely=0.1,anchor=tk.CENTER)
        
        self.filename = ''
        self.merge_threshold = 0.91
        
        #Buttons for interaction
        file_button = ctk.CTkButton(master=self, text="Submit File", corner_radius=10, command=self.set_file)
        generate_labels_button = ctk.CTkButton(master=self, text="Generate Labels", corner_radius=10, command=self.gen_labels)
        reason_for_labels_button = ctk.CTkButton(master=self, text="Reason for Labels", corner_radius=10, command=self.reason_labels)
        merge_threshold_button = ctk.CTkButton(master=self, text="Change Merge Threshold", corner_radius=10, command=self.change_thresh)
        merge_similar_button = ctk.CTkButton(master=self, text="Merge Similar Labels", corner_radius=10, command=self.merge)
        regen_labels_button = ctk.CTkButton(master=self, text="Regenerate Labels", corner_radius=10, command=self.gen_labels)
        
        file_button.place(relx=0.5,rely=0.2,anchor=tk.CENTER)
        generate_labels_button.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
        reason_for_labels_button.place(relx=0.5,rely=0.6,anchor=tk.CENTER)
        merge_threshold_button.place(relx=0.5,rely=0.7,anchor=tk.CENTER)
        merge_similar_button.place(relx=0.5,rely=0.8,anchor=tk.CENTER)
        regen_labels_button.place(relx=0.5,rely=0.9,anchor=tk.CENTER)

        


    def foo(self):
        print("bar")
        
    def set_file(self):
        self.filename = self.textbox.get('1.0', 'end-1c')
        print('File: "' + self.filename + '"' + ' submitted')
        
    def gen_labels(self):
        label_datapoints(DATASET_PATH + self.filename)
        
    def reason_labels(self):
        reason_for_label()
        
    def change_thresh(self):
        self.merge_threshold = change_merge_threshold(self.merge_threshold)
        
    def merge(self):
        merge_labels(self.merge_threshold)

if __name__ == "__main__":
    app = App()
    # Runs the app
    app.mainloop()   

"""
Create an affinity diagram
Reason for a label
Change label merge threshold
Regeneratae all group labels
Merge identical / similar groups
"""
import tkinter as tk
import customtkinter as ctk
    
class App(ctk.CTk):
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
        
        textbox = ctk.CTkTextbox(master=self,width=200,height=30)
        textbox.place(relx=0.5,rely=0.1,anchor=tk.CENTER)
        filename = ''
        
        file_button = ctk.CTkButton(master=self, text="Submit File", corner_radius=10, command=lambda : print(textbox.get('1.0', tk.END)))
        generate_labels_button = ctk.CTkButton(master=self, text="Generate Labels", corner_radius=10, command=self.foo)
        merge_threshold_button = ctk.CTkButton(master=self, text="Change Merge Threshold", corner_radius=10, command=self.foo)
        regen_labels_button = ctk.CTkButton(master=self, text="Regenerate Labels", corner_radius=10, command=self.foo)
        merge_similar_button = ctk.CTkButton(master=self, text="Merge Similar Labels", corner_radius=10, command=self.foo)
        
        file_button.place(relx=0.5,rely=0.2,anchor=tk.CENTER)
        generate_labels_button.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
        merge_threshold_button.place(relx=0.5,rely=0.6,anchor=tk.CENTER)
        regen_labels_button.place(relx=0.5,rely=0.7,anchor=tk.CENTER)
        merge_similar_button.place(relx=0.5,rely=0.8,anchor=tk.CENTER)

    def foo(self):
        print("bar")

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
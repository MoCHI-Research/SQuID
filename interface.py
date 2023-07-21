import tkinter as tk
from tkinter import font as tkfont
import os
from menu import *
from tkinter import filedialog
from merge_labels import merge_labels
from tkinter import Scrollbar, Canvas


"""
Main program that runs everything
Superclass:
    tk.Tk: creates a subclass of the Tk module that we modify to our needs with classes
"""
class SampleApp(tk.Tk):

    """
    Main function
    Parameters:
        self: instance of the class to access attributes and methods
        *args: positional arguments
        **kwargs: keyword arguments
    Returns:
        None
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1000x1000")
        self.title("SQuID")

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.text_font = tkfont.Font(family = 'Times', size = 14)
        self.message_font = tkfont.Font(family = 'Helvetica', size = 18)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage,
                  CreateAffinityDiagram,
                  ReasonForLabel, NotAValidLabel, DataWithLabel, GenerateGPTReason, NotAnIntegerError, IntegerOutsideRangeError,
                  ChangeMergeThreshold,
                  MergeGroups, FinishedMerging,
                  PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    """
    Brings the selected frame to the forefront and runs the tailored update function
    Parameters:
        self: this is always passed to each function
        page_name: the name of the frame we want to bring forward
        *args: anything this is being passed to the update function
    Returns:
        None
    """
    def show_frame(self, page_name, *args):
        frame = self.frames[page_name]
        frame.tkraise()
        frame.update_status(*args)

    """
    Pop up a message box from a frame
    Parameters:
        current_frame(tk.Frame): the current frame which the message box is popped from
        message(string): the message that appears in the message box
        box_size(string): string that specifies size of the message box
    """
    def popup_message(self, current_frame, message, box_size = "200x100"):
        top_box = tk.Toplevel(current_frame)
        top_box.title("Message")
        top_box.geometry(box_size)

        message_label = tk.Label(top_box, text = message, font = self.message_font)
        message_label.place(relx = 0.5, rely = 0.5, anchor = "center")

"""
Virtual class for creating frames. Do not create object using this class.
Superclass: tk.Frame
"""
class WorkFrame(tk.Frame):
    """Constructor for WorkFrame class"""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.labels = []            #Keeps track of labels that might be cleared
        self.merge_threshold = 0.91
        self.file_path = ""
        self.reason_status = "Please input an appropriate integer"

    """
    Clears certain text labels that exist on the frame
    """
    def clear_screen(self):
        for label in self.labels:
            label.destroy()
        self.labels = []

    """
    Virtual method for updating status of the frame
    """
    def update_status(self, *args):
        return


"""
Main start page with all features
Superclass:
    WorkFrame: a subclass of tk.Frame
"""
class StartPage(WorkFrame):
    """Constructor of the class"""
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        label = tk.Label(self, text="SQuID Interface", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        creatediagram_button = tk.Button(self, text="Create an Affinity Diagram", command=lambda: controller.show_frame("CreateAffinityDiagram"))
        reasonforlabel_button = tk.Button(self, text="Generate a Reason for a Label", command=lambda: controller.show_frame("ReasonForLabel"))
        changemergethreshold_button = tk.Button(self, text="Change Merge Threshold", command=lambda: controller.show_frame("ChangeMergeThreshold"))
        regenlabels_button = tk.Button(self, text="Regenerate All Group Labels", command=lambda: controller.show_frame("CreateAffinityDiagram"))
        mergegroups_button = tk.Button(self, text="Merge Groups That Are Identical or Similar", command=lambda: controller.show_frame("MergeGroups"))

        creatediagram_button.pack()
        reasonforlabel_button.pack()
        changemergethreshold_button.pack()
        regenlabels_button.pack()
        mergegroups_button.pack()


class CreateAffinityDiagram(WorkFrame):
    """Constructor of the class"""
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        label = tk.Label(self, text="Creating an Affinity Diagram", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_frame("StartPage"))
        button.pack()


"""
Prompts user for the label
Superclass:
    WorkFrame: a subclass of tk.Frame
"""
class ReasonForLabel(WorkFrame):
    """Constructor of the class"""
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        label = tk.Label(self, text="Which label are we curious about?", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.label_entry = tk.Entry(self)
        self.label_entry.pack()

        label_button = tk.Button(self, text="Submit Label", command=self.label_submission)
        label_button.pack()

        start_page_button = tk.Button(self, text="Go Back to Start Page", command = lambda: self.controller.show_frame("StartPage"))
        start_page_button.pack()

    """
    Grabs label entry after button press, retrieves all data w/ the label, and brings DataWithLabel frame to forefront
    """
    def label_submission(self):
        entered_label = self.label_entry.get()
        all_data = retrieve_data_with_label(entered_label)
        print("Length: " + str(len(all_data)))
        if len(all_data) > 0:
            self.controller.show_frame("DataWithLabel", all_data, entered_label)
        else:
            self.controller.show_frame("NotAValidLabel")

class NotAValidLabel(WorkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        notvalid_label = tk.Label(self, text="Label is Not Valid", font=controller.title_font)
        notvalid_label.pack(side="top", fill="x", pady=10)

        message_label = tk.Label(self, text="The label you entered is not a valid label. Please go back and try again.")
        message_label.pack()

        start_page_button = tk.Button(self, text="Re-Enter a Label", command = lambda: self.controller.show_frame("ReasonForLabel"))
        start_page_button.pack()
        start_page_button = tk.Button(self, text="Start Page", command = lambda: self.controller.show_frame("StartPage"))
        start_page_button.pack()



"""
Prints out all data with the label the user entered in ReasonForLabel frame
Superclass:
    WorkFrame: a subclass of tk.Frame
"""
class DataWithLabel(WorkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.labels_frame = None
        self.data_num = None

        label = tk.Label(self, text="Data:", font=controller.title_font)
        label.pack(pady=10)

        status_label = tk.Label(self, text=self.reason_status, font=("Arial", 14, "bold italic"))
        status_label.pack()

        self.data_num = tk.Entry(self)
        self.data_num.pack()

        data_num_button = tk.Button(self, text="Submit Data Number", command=self.submit_data_number)
        data_num_button.pack()

        start_page_button = tk.Button(self, text="Go Back to Start Page", command=lambda: self.controller.show_frame("StartPage"))
        start_page_button.pack()

        # Scroll wheel implemented
        self.canvas = Canvas(self, width=400, height=400)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.labels_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.labels_frame, anchor=tk.NW)

        scrollbar = Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.bind("<MouseWheel>", self.on_mousewheel)

    def submit_data_number(self):
        data_number = self.data_num.get()
        if data_number.isdigit():
            if int(data_number) > len(self.all_data) or int(data_number) < 1:
                self.controller.show_frame("IntegerOutsideRangeError")
            else:
                self.controller.show_frame("GenerateGPTReason", self.all_data, self.entered_label, data_number)
        else:
            self.controller.show_frame("NotAnIntegerError", data_number)

    def update_status(self, data, label):
        self.all_data = data
        self.entered_label = label
        self.clear_screen()
        count = 1
        for element in data:
            label = tk.Label(self.labels_frame, text=str(count) + ": " + element[1], font=('Arial', 14), anchor='w', wraplength=952, justify='left')
            label.pack(fill='both')
            self.labels.append(label)
            count += 1

        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

"""
Template to make a new frame
Superclass:
    WorkFrame: a subclass of tk.Frame
"""
class NotAnIntegerError(WorkFrame):
    """
    Parameters:
        parent: widget/frame that contains the current frame
        controller: instance of the class that allows for library methods to be called
    """
    def __init__(self, parent, controller):
        super().__init__(parent, controller)


        errortitle_label = tk.Label(self, text="Error", font=controller.title_font)
        errortitle_label.pack()

        error_label = tk.Label(self, text="The entry you entered was not an integer. Please go back and enter an appropriate integer.", font=controller.text_font)
        error_label.pack(side="top", fill="x", pady=10)

        button = tk.Button(self, text="ReEnter an Integer", command = lambda: controller.show_frame("DataWithLabel"))
        button.pack()

        button = tk.Button(self, text="Start Page", command = lambda: controller.show_frame("StartPage"))
        button.pack()

class IntegerOutsideRangeError(WorkFrame):
    """
    Parameters:
        parent: widget/frame that contains the current frame
        controller: instance of the class that allows for library methods to be called
    """
    def __init__(self, parent, controller):
        super().__init__(parent, controller)


        errortitle_label = tk.Label(self, text="Error", font=controller.title_font)
        errortitle_label.pack()

        error_label = tk.Label(self, text="The integer you entered was not an available data number. Please go back and enter an appropriate integer.", font=controller.text_font)
        error_label.pack(side="top", fill="x", pady=10)

        button = tk.Button(self, text="ReEnter an Integer", command = lambda: controller.show_frame("DataWithLabel"))
        button.pack()

        button = tk.Button(self, text="Start Page", command = lambda: controller.show_frame("StartPage"))
        button.pack()

"""
Generates the reason for giving the data the label it was given and displays it.
Superclass:
    WorkFrame: a subclass of tk.Frame
"""
class GenerateGPTReason(WorkFrame):
    """Constructor of the class"""
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.this_frame = None

        heading = tk.Label(self, text="GPT Response/Reason: ", font=controller.title_font)
        heading.pack()

        self.this_frame = tk.Frame(self)
        self.this_frame.pack()

        start_page_button = tk.Button(self, text="Start Page", command = lambda: self.controller.show_frame("StartPage"))
        start_page_button.pack()

    """
    Prints out the gpt response for providing the data with given label
    Parameters:
        all_data: an array of tuples that has the following layout [(Label, DataEntry), ..., (Label, DataEntry)]
        label: the label in question
        data_index: the index of the data with the label. ex: all_data[data_index - 1][1]
    """
    def update_status(self, all_data, label, data_index):
        self.clear_screen()
        gpt_response = generate_reason(all_data, data_index, label)
        display_gpt_response = tk.Label(self.this_frame, text=gpt_response, font=('Arial', 14), wraplength=600)
        display_gpt_response.pack(anchor='center')
        self.labels.append(display_gpt_response)

"""
Frame to change the merge threshold
Parent class:
    WorkFrame: a sub class of tk.Frame
"""
class ChangeMergeThreshold(WorkFrame):
    """Constructor of the class"""
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.current_value = tk.DoubleVar()

        self.label = tk.Label(self, text="Changing Merge Threshold", font=controller.title_font)
        self.label.pack(side="top", fill="x", pady=10)
        
        self.current_threshold = tk.Label(self, text="Current Threshold: " + str(self.merge_threshold))
        self.current_threshold.pack()
        
        self.restraints_label = tk.Label(self, text="Slide the label to change the merge threshold, then press the 'Change threshold' button")
        self.restraints_label.pack()
        
        self.slider = tk.Scale(self, from_=1, to=99, orient="horizontal", variable=self.current_value)
        self.slider.pack()
        
        self.update_button = tk.Button(self, text="Change threshold",command=self.update_threshold)
        self.update_button.pack()
        
        self.button = tk.Button(self, text="Go back to start page", command=lambda: controller.show_frame("StartPage"))
        self.button.pack()
        
    """Updates the merge_threshold variable"""
    def update_threshold(self):
        self.merge_threshold = self.slider.get() / 100
        self.current_threshold = tk.Label(self, text=str(self.merge_threshold))
        self.update_page()
        
    """Supposed to update the threshold visual to allow users see what the current threshold is, not working"""
    def update_page(self):
        self.current_threshold.destroy()
        # self.current_threshold.pack_forget()
        
        

"""
Frame to begin merging groups that are similar
Superclass:
    WorkFrame: a sub class of tk.Frame
"""
class MergeGroups(WorkFrame):
    """Constructor of the class"""
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        label = tk.Label(self, text="Select a File to Merge Groups From", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        select_button = tk.Button(self, text="Select File", command=self.select_file_to_merge)
        select_button.pack(pady=10)

    """
    Allows user to select file from directory
    """
    def select_file_to_merge(self):
        file_path = filedialog.askopenfilename()
        self.file_path = file_path
        finished_merging = merge_labels(merge_threshold = self.merge_threshold, original_file = self.file_path)
        if finished_merging:
            self.controller.show_frame("FinishedMerging")

"""
Lets user know that merging was finished
Superclass:
    WorkFrame: a subclass of tk.Frame
"""
class FinishedMerging(WorkFrame):
    """
    Parameters:
        parent: widget/frame that contains the current frame
        controller: instance of the class that allows for library methods to be called
    """
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        label = tk.Label(self, text="Finished Merging Groups", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button = tk.Button(self, text="Start Page", command = lambda: controller.show_frame("StartPage"))
        button.pack()


"""
Frame to begin creating an affinity diagram
Superclass:
    WorkFrame: a subclass of tk.Frame
"""
class CreateAffinityDiagram(WorkFrame):
    """Constructor of the class"""
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        title_label = tk.Label(self, text = "Creating an Affinity Diagram", font = controller.title_font)
        title_label.pack()

        hint_label = tk.Label(self, text = "Please select a csv file:", font = controller.text_font)
        hint_label.pack()

        select_file_button = tk.Button(self, text = "Select a File", command = self.select_file_to_group)
        select_file_button.pack()

        self.file_status_box = tk.Label(self, text = "No file uploaded yet", font = controller.text_font)
        self.file_status_box.pack()

        diagram_button = tk.Button(self, text = "Create affinity diagram", command = lambda: label_datapoints(self.file_path))
        diagram_button.pack()

        save_button = tk.Button(self, text = "Save result as", command = self.save_result)
        save_button.pack()

        startpage_button = tk.Button(self, text="Start Page", command = lambda: controller.show_frame("StartPage"))
        startpage_button.pack()

    """
    Select a file to make affinity diagram from
    """
    def select_file_to_group(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path = file_path
        if self.file_path:
            self.file_status_box.config(text = "File uploaded: " + self.file_path)
        else:
            self.file_status_box.config(text = "No file uploaded yet")

    """
    Save the result to a user-specified place
    Parameters:
        original_path: the path by which one grabs the original file to save to their specified place
    """
    def save_result(self, original_path = "output.csv"):
        file_path = filedialog.asksaveasfilename(initialfile = "output.csv")
        with open(original_path, 'r') as old_file, open(file_path, 'w') as new_file:
            new_file.write(old_file.read())

            old_file.close()
            new_file.close()




"""
Template to make a new frame
Superclass:
    WorkFrame: a subclass of tk.Frame
"""
class PageTwo(WorkFrame):
    """
    Parameters:
        parent: widget/frame that contains the current frame
        controller: instance of the class that allows for library methods to be called
    """
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button = tk.Button(self, text="Go to the start page", command = lambda: controller.show_frame("StartPage"))
        button.pack()

        button = tk.Button(self, text="Start Page", command = lambda: controller.show_frame("StartPage"))
        button.pack()




if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

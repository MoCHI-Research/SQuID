from tkinter import filedialog
from menu import *
from typing import List, Tuple
import customtkinter
import time
import os
import asyncio


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

UNIQUE_LABELS = set()
ACCEPTED_DATA = {}
REJECTED_DATA = []
COMPLETED_GPT_REQUESTS = 0
NUM_DATA_PROCESSED = 0
NUM_GPT_REQUESTS = 0
LEN_OF_ORIG_DATA = 0
TOTAL_UNPROCESSED_DATA = 0
NUM_PASSES = 0


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # App configurations
        self.title("SQuID")
        self.geometry("1200x600")

        # Grid configurations
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Merge threshold
        self.merge_threshold = 0.91

        # Frame placeholders
        self.alert_frame = None
        self.pass_or_stop_frame = None

        # Creating class/frame instances
        self.FeatureFrame = FeatureFrame(self, controller=self)
        self.ReasonForLabel = ReasonForLabel(self, controller=self)
        self.AdjustMergeThreshold = AdjustMergeThreshold(self, controller=self)
        self.CreateAffinityDiagram = CreateAffinityDiagram(self, controller=self)

        # Displaying instances
        self.FeatureFrame.grid(row=0, column=0, sticky="nesw")
        self.ReasonForLabel.grid(row=0, column=1, sticky="nsew")
        self.AdjustMergeThreshold.grid(row=0, column=1, sticky="nsew")
        self.CreateAffinityDiagram.grid(row=0, column=1, sticky="nsew")

        # Sets up final visual touch aspects
        self.FeatureFrame.create_affinity_diagram_event()

    def return_threshold(self):
        return self.merge_threshold

    def change_threshold(self, value):
        self.merge_threshold = value

    #----------------------------------------------------------------------#
    #                     Alert Frame Functions                            #
    #----------------------------------------------------------------------#
    """
    Creates alert frame
    """
    def create_alert_frame(self, alert_message):
        self.alert_frame = Alert(self, controller=self, alert_message=alert_message)
        self.alert_frame.grid(row=0, column=1, sticky="nsew")

    """
    Destroys alert frame if exists
    """
    def destroy_alert_frame(self):
        if self.alert_frame:
            self.alert_frame.destroy()

    #----------------------------------------------------------------------#
    #                   User Selection Frame Functions                     #
    #----------------------------------------------------------------------#
    """
    Creates user selection frame
    """
    def create_user_selection_frame(self, processed_data, unprocessed_data):
        global COMPLETED_GPT_REQUESTS
        self.user_selection_frame = UserSelection(self, controller=self, batch_num=COMPLETED_GPT_REQUESTS, grouped_data=processed_data, ungrouped_data=unprocessed_data)
        self.user_selection_frame.grid(row=0, column=1, sticky="nsew")

    """
    Destroys user selection frame if exists
    """
    def destroy_user_selection_frame(self):
        if self.user_selection_frame:
            self.user_selection_frame.destroy()

    """
    Raises user selection frame to forefront
    """
    def display_user_selection_frame(self):
        if self.user_selection_frame:
            self.user_selection_frame.tkraise()

    #----------------------------------------------------------------------#
    #                   Pass Or Stop Frame Functions                       #
    #----------------------------------------------------------------------#
    """
    Creates pass or stop frame
    """
    def create_pos_frame(self):
        global NUM_PASSES
        global LEN_OF_ORIG_DATA
        global ACCEPTED_DATA
        unique_labels = list(set(ACCEPTED_DATA.values()))
        message = """
        #----------------------------------------------------------------------#
        #                       Pass Or Stop Created                           #
        #----------------------------------------------------------------------#
        """
        print(message)
        print("Unique Labels: ", unique_labels)
        print("Length of Unique Labels: ", len(unique_labels))
        self.pass_or_stop_frame = PassOrStop(self, controller=self, num_pass=NUM_PASSES, num_data=LEN_OF_ORIG_DATA, num_unique_labels=len(unique_labels))
        self.pass_or_stop_frame.grid(row=0, column=1, sticky="nsew")

    """
    Destroys pass or stop frame if exists
    """
    def destroy_pos_frame(self):
        if self.pass_or_stop_frame:
            self.pass_or_stop_frame.destroy()

    """
    Raises pass or stop frame to forefront
    """
    def display_pos_frame(self):
        if self.pass_or_stop_frame:
            self.pass_or_stop_frame.tkraise()

class FeatureFrame(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.configure(fg_color="grey15")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=10)

        title = customtkinter.CTkLabel(self, text="Features", font=("Verdana", 22, "underline"))
        title.grid(row=0, column=0, sticky="nsew")

        self.create_affinity_diagram_button = customtkinter.CTkButton(self, text="Create an Affinity Diagram", width=230, height=50, fg_color="transparent", border_color="#3B8ED0", border_width=2, font=("Verdana", 14), command=self.create_affinity_diagram_event)
        self.create_affinity_diagram_button.grid(row=1, column=0, padx=(20, 20), pady=(15,15))

        self.reason_for_label_button = customtkinter.CTkButton(self, text="Generate a Reason for a Label", width=230, height=50, fg_color="transparent", border_color="#3B8ED0", border_width=2, font=("Verdana", 14), command=self.reason_for_label_event)
        self.reason_for_label_button.grid(row=2, column=0, padx=(20, 20), pady=(15,15))

        self.adjust_merge_threshold_button = customtkinter.CTkButton(self, text="Adjust Merge Threshold", width=230, height=50, fg_color="transparent", border_color="#3B8ED0", border_width=2, font=("Verdana", 14), command=self.adjust_merge_threshold_event)
        self.adjust_merge_threshold_button.grid(row=3, column=0, padx=(20, 20), pady=(15,15))

    def reset_button_indicators(self):
        self.create_affinity_diagram_button.configure(fg_color="transparent")
        self.reason_for_label_button.configure(fg_color="transparent")
        self.adjust_merge_threshold_button.configure(fg_color="transparent")

    def create_affinity_diagram_event(self):
        self.reset_button_indicators()
        self.create_affinity_diagram_button.configure(fg_color='#144870')
        self.controller.CreateAffinityDiagram.tkraise()

    def reason_for_label_event(self):
        self.reset_button_indicators()
        self.reason_for_label_button.configure(fg_color='#144870')
        self.controller.ReasonForLabel.tkraise()

    def adjust_merge_threshold_event(self):
        self.reset_button_indicators()
        self.adjust_merge_threshold_button.configure(fg_color='#144870')
        self.controller.AdjustMergeThreshold.tkraise()

class CreateAffinityDiagram(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.file_path = None
        self.grid_columnconfigure(0, weight=1)

        # Title label
        title = customtkinter.CTkLabel(self, text="Creating an Affinity Diagram", font=("Verdana", 22, "underline"))
        title.grid(row=0, column=0, pady=30)

        # Instructions
        instructions = "Press the \"Select File\" button below to upload a .csv file to begin creating an affinity diagram.\n Once you are ready, press the \"Start\" button and we will begin the affinity diagram making process. "
        instructions_label = customtkinter.CTkLabel(self, text=instructions, font=("Verdana", 14, "italic"))
        instructions_label.grid(row=1, column=0, pady=(10, 10))

        # Frame container for file button and entry
        file_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        file_frame.grid(row=2, column=0)

        # Select File Button
        select_file_button = customtkinter.CTkButton(file_frame, text="Select File", font=("Verdana", 14), command=self.select_file_to_group)
        select_file_button.grid(row=0, column=0, pady=30, padx=10)

        # File selection labels
        self.file_status_box = customtkinter.CTkEntry(file_frame, width=400, placeholder_text="Choose file to upload", font=("Verdana", 14, "italic"))
        self.file_status_box.grid(row=0, column=1, pady=30)
        self.file_status_box.configure(state="disabled")

        # Alert message
        self.alert_message = customtkinter.CTkLabel(self, text="")
        self.alert_message.grid(row=3, column=0, pady=(30, 2))

        # Start button
        start_button = customtkinter.CTkButton(self, text = "Start", font=("Verdana", 14), command = self.start_event)
        start_button.grid(row=4, column=0)

    """
    Prompts user to select a file
    """
    def select_file_to_group(self):
        file = filedialog.askopenfilename()
        if file:
            self.file_path = file
        if not self.file_path == None:
            self.file_status_box.configure(state="normal")
            self.file_status_box.delete("0", "end")
            self.file_status_box.insert("0", self.file_path.split("/")[-1])
            self.file_status_box.configure(state="disabled")
        else:
            self.file_status_box.configure(state="normal")
            self.file_status_box.configure(placeholder_text="Choose file to upload")
            self.file_status_box.configure(state="disabled")

    """
    Begins affinity diagram making process (with file validity check)
    """
    def start_event(self):
        if self.valid_file(self.file_path):
            global NUM_GPT_REQUESTS
            global LEN_OF_ORIG_DATA
            global COMPLETED_GPT_REQUESTS
            global TOTAL_UNPROCESSED_DATA
            global NUM_PASSES
            NUM_GPT_REQUESTS = 0
            LEN_OF_ORIG_DATA = 0
            COMPLETED_GPT_REQUESTS = 0
            TOTAL_UNPROCESSED_DATA = 0
            NUM_PASSES = 0

            output_file = set_output_file(True)
            data = set_data_list(self.return_and_clear_file())
            save_data(data, True)
            LEN_OF_ORIG_DATA = TOTAL_UNPROCESSED_DATA = len(data)

            batch_size = set_batch_size(LEN_OF_ORIG_DATA)
            NUM_GPT_REQUESTS = math.ceil(LEN_OF_ORIG_DATA / batch_size)
            alert_message = "Pass " + str(NUM_PASSES + 1) + "\nPlease wait as we process Batch " + str(COMPLETED_GPT_REQUESTS + 1) + " of " + str(NUM_GPT_REQUESTS)
            self.controller.create_alert_frame(alert_message)
            self.after(100, self.process_batch, data)

    """
    Returns and clears file path
    """
    def return_and_clear_file(self):
        file_path = self.file_path
        self.file_path = None
        return file_path

    """
    Processes a batch of data
    """
    def process_batch(self, data):
        global COMPLETED_GPT_REQUESTS
        selected_items = []
        batch_size = set_batch_size(len(data))

        batch = data[:batch_size]
        unprocessed_data = data[batch_size:]
        user_input_string = numbered_data(batch)
        results = process_batch('group_data_in_numbers', user_input_string)
        batch_banner = """
        #----------------------------------------------------------------------#
        #                               Batch                                  #
        #----------------------------------------------------------------------#
        """
        print(batch_banner)
        print(batch)
        results_banner = """
        #----------------------------------------------------------------------#
        #                               Results                                #
        #----------------------------------------------------------------------#
        """
        print(results_banner)
        print(results)
        processed_results = process_results(results, batch)
        COMPLETED_GPT_REQUESTS+=1
        self.controller.destroy_alert_frame()
        self.controller.create_user_selection_frame(processed_results, unprocessed_data)

    """
    Determines if there are more batches to process
    """
    def determine_next_steps(self, remaining_data):
        global COMPLETED_GPT_REQUESTS
        global NUM_GPT_REQUESTS
        global NUM_PASSES
        self.adjust_num_gpt_requests()

        if remaining_data:
            self.check_additional_batches()
            batch_size = set_batch_size(len(remaining_data))
            alert_message = "Pass " + str(NUM_PASSES + 1) + "\nPlease wait as we process Batch " + str(COMPLETED_GPT_REQUESTS + 1) + " of " + str(NUM_GPT_REQUESTS)
            self.controller.create_alert_frame(alert_message)
            self.after(100, self.process_batch, remaining_data)
        else:
            global ACCEPTED_DATA
            NUM_PASSES += 1
            save_data(ACCEPTED_DATA)
            self.controller.create_pos_frame()
            print("No more data to process")

    """
    Adjusts the number of batches that need to happen based
    on the amount of data that has not been processed
    """
    def adjust_num_gpt_requests(self):
        global REJECTED_DATA
        global NUM_GPT_REQUESTS
        global TOTAL_UNPROCESSED_DATA

        TOTAL_UNPROCESSED_DATA += len(REJECTED_DATA)
        NUM_GPT_REQUESTS = max(math.ceil(TOTAL_UNPROCESSED_DATA / get_batch_size()), NUM_GPT_REQUESTS)

    """
    Checks if the user wanted to go beyond the approx. number of batches
    and adjusts the numbers if so (to display on alert frame)
    """
    def check_additional_batches(self):
        global COMPLETED_GPT_REQUESTS
        global NUM_GPT_REQUESTS

        if COMPLETED_GPT_REQUESTS == NUM_GPT_REQUESTS:
            NUM_GPT_REQUESTS += 1


    """
    Checks if a given file path exists and is a csv
    """
    def valid_file(self, file):
        if file == None or file == "":
            self.alert_message.configure(text="You have not selected a .csv file yet.", text_color="#cc4125")
            return False
        elif not os.path.exists(file):
            self.alert_message.configure(text="The file entered does not exist.\nPlease go back and reselect.", text_color="#cc4125")
            return False
        elif not self.file_path.lower().endswith('.csv'):
            self.alert_message.configure(text="The file entered is not a .csv file.\nPlease go back and select a .csv file.", text_color="#cc4125")
            return False
        else:
            return True

    def reset(self):
        # File entry widget
        self.file_status_box.configure(state="normal")
        self.file_status_box.delete("0", "end")
        self.file_status_box.configure(placeholder_text="Choose file to upload")
        self.file_status_box.configure(state="disabled")

        # Alert message
        self.alert_message = customtkinter.CTkLabel(self, text="")


class UserSelection(customtkinter.CTkFrame):
    def __init__(self, parent, controller, batch_num: int, grouped_data: List[Tuple[str, List[str]]], ungrouped_data: List):
        super().__init__(parent)

        self.controller = controller

        # Configure grid
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)

        # Set private variables
        self.boxes_and_info = []
        self.grouped_data = grouped_data
        self.ungrouped_data = ungrouped_data

        # Title label
        global NUM_PASSES
        title = customtkinter.CTkLabel(self, text="Pass " + str(NUM_PASSES + 1) + ": Batch " + str(batch_num), font=("Verdana", 22))
        title.grid(row=0, column=1, pady=30)

        # Data Frame
        self.data_frame = customtkinter.CTkScrollableFrame(self, border_color="#3B8ED0", border_width=2, scrollbar_button_color="#3B8ED0", scrollbar_button_hover_color='#144870')
        self.data_frame.grid(row=1, column=1, padx=(20, 20), sticky="nsew")

        # Headers
        h_select = customtkinter.CTkLabel(self.data_frame, text="Remove", font=("Verdana", 14, "underline", "bold"))
        h_select.grid(row=0, column=0, padx=(20, 0), sticky="nw")
        h_data = customtkinter.CTkLabel(self.data_frame, text="Data", font=("Verdana", 14, "underline", "bold"))
        h_data.grid(row=0, column=2, sticky="nesw")
        h_label = customtkinter.CTkLabel(self.data_frame, text="Label", font=("Verdana", 14, "underline", "bold"))
        h_label.grid(row=0, column=4, sticky="nesw")


        # Button frame
        button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=1, sticky="nsew")
        button_frame.grid_columnconfigure(0, weight=1)
        # Buttons
        save_cont_button = customtkinter.CTkButton(button_frame, text="Save and Continue", command=self.save_cont_event)
        save_cont_button.grid(row=0, column=0, pady=(20, 0))

        global UNIQUE_LABELS
        print("GROUPED DATA WE WILL BE ADDING TO FRAME:", self.grouped_data)
        for label, datas in self.grouped_data:
            UNIQUE_LABELS.add(label)
            for data in datas:
                self.add_item(label, data)

    def add_item(self, label: str, data: str):
        self.data_frame.grid_columnconfigure((2, 4), weight=1)

        switch = customtkinter.CTkSwitch(self.data_frame, text="", onvalue=True, offvalue=False)
        switch.grid(row=len(self.boxes_and_info) + 1, column=0, padx=(35,0))

        first_dashes = customtkinter.CTkLabel(self.data_frame, text="--------", text_color="#3B8ED0")
        first_dashes.grid(row=len(self.boxes_and_info) + 1, column=1, pady=(10, 10), sticky="nesw")

        # displayed_label = customtkinter.CTkLabel(self.data_frame, text=label, wraplength=300)
        # displayed_label.grid(row=len(self.boxes_and_info) + 1, column=2, padx=(5, 5), pady=(10, 10), sticky="nsew")
        displayed_data = customtkinter.CTkLabel(self.data_frame, text=data, wraplength=300)
        displayed_data.grid(row=len(self.boxes_and_info) + 1, column=2, padx=(5,5), pady=(10,0), sticky="nsew")

        second_dashes = customtkinter.CTkLabel(self.data_frame, text="--------", text_color="#3B8ED0")
        second_dashes.grid(row=len(self.boxes_and_info) + 1, column=3, pady=(10, 10), sticky="nesw")

        # displayed_data = customtkinter.CTkLabel(self.data_frame, text=data, wraplength=300)
        # displayed_data.grid(row=len(self.boxes_and_info) + 1, column=4, padx=(5,5), pady=(10,0), sticky="nsew")
        displayed_label = customtkinter.CTkLabel(self.data_frame, text=label, wraplength=300)
        displayed_label.grid(row=len(self.boxes_and_info) + 1, column=4, padx=(5, 5), pady=(10, 10), sticky="nsew")

        self.boxes_and_info.append((switch, label, data))

    def save_cont_event(self):
        global REJECTED_DATA
        global ACCEPTED_DATA
        REJECTED_DATA = []

        for switch, label, data in self.boxes_and_info:
            if switch.get():
                REJECTED_DATA.append(data)
            else:
                ACCEPTED_DATA[data] = label

        remaining_data = REJECTED_DATA + self.ungrouped_data
        self.controller.CreateAffinityDiagram.determine_next_steps(remaining_data)

class Alert(customtkinter.CTkFrame):
    def __init__(self, parent, controller, alert_message: str):
        super().__init__(parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title = customtkinter.CTkLabel(self, text=alert_message, font=("Verdana", 22, "italic"))
        self.title.grid(row=0, column=0, sticky="nsew")

class PassOrStop(customtkinter.CTkFrame):
    def __init__(self, parent, controller, num_pass: int, num_data: int, num_unique_labels: int):
        super().__init__(parent)

        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.controller = controller

        # Messages
        completed_message = "Pass " + str(num_pass) + " Completed."
        saved_message = "Results have been saved."


        results_message = str(num_data) + " unique data points resulted in " + str(num_unique_labels) + " unique group labels."
        if num_unique_labels <= 5:
            suggestion_message = "We suggest saving the results but you are more than able to continue."
        else:
            suggestion_message = "We suggest another pass to process the new group labels made."


        choice_message = "To continue, click \"Generate Next Pass\", otherwise, click\n\"Save and End\" to end and go back to the file upload screen."

        # First Frame of Messages
        first_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        first_frame.grid(row=0, column=0)
        completed_label = customtkinter.CTkLabel(first_frame, text=completed_message, font=("Verdana", 22, "italic"))
        completed_label.grid(row=0, column=0, padx=(0,5), sticky="nsew")
        saved_label = customtkinter.CTkLabel(first_frame, text=saved_message, text_color="#3B8ED0", font=("Verdana", 22, "italic"))
        saved_label.grid(row=0, column=1, padx=(5, 0), sticky="nsew")

        # Second Frame of Messages
        second_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        second_frame.grid(row=1, column=0)
        results_label = customtkinter.CTkLabel(second_frame, text=results_message, text_color="#3B8ED0", font=("Verdana", 22, "italic"))
        results_label.grid(row=0, column=0, sticky="nsew")
        suggestion_label = customtkinter.CTkLabel(second_frame, text=suggestion_message, font=("Verdana", 22, "italic"))
        suggestion_label.grid(row=1, column=0, sticky="nsew")

        # Third Frame of Messages
        third_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        third_frame.grid(row=2, column=0)
        choice_label = customtkinter.CTkLabel(third_frame, text=choice_message, font=("Verdana", 22, "italic"))
        choice_label.grid(row=0, column=0, sticky="nsew")

        # Button Frame
        button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=3, column=0, sticky="nsew")
        button_frame.grid_columnconfigure((0, 1), weight=1)

        # Buttons
        gen_next_pass_button = customtkinter.CTkButton(button_frame, width=175, text="Generate Next Pass", command=self.gen_next_pass_event)
        gen_next_pass_button.grid(row=0, column=0, padx=(150, 0), pady=(20, 0))
        save_results_button = customtkinter.CTkButton(button_frame, width=175, text="Save and End", command=self.save_results_event)
        save_results_button.grid(row=0, column=1, padx=(0, 150), pady=(20, 0))

    def gen_next_pass_event(self):
        global REJECTED_DATA
        global ACCEPTED_DATA
        global LEN_OF_ORIG_DATA
        global TOTAL_UNPROCESSED_DATA
        global NUM_GPT_REQUESTS
        global COMPLETED_GPT_REQUESTS
        global UNIQUE_LABELS
        global NUM_DATA_PROCESSED
        global NUM_PASSES

        COMPLETED_GPT_REQUESTS = 0
        REJECTED_DATA = []
        NUM_DATA_PROCESSED = 0
        UNIQUE_LABELS = set()
        LEN_OF_ORIG_DATA = 0
        TOTAL_UNPROCESSED_DATA = 0


        data = list(set(ACCEPTED_DATA.values()))
        ACCEPTED_DATA = {}
        LEN_OF_ORIG_DATA = TOTAL_UNPROCESSED_DATA = len(data)
        batch_size = set_batch_size(LEN_OF_ORIG_DATA)
        NUM_GPT_REQUESTS = math.ceil(LEN_OF_ORIG_DATA / batch_size)

        alert_message = "Pass " + str(NUM_PASSES + 1) + "\nPlease wait as we process Batch " + str(COMPLETED_GPT_REQUESTS + 1) + " of " + str(NUM_GPT_REQUESTS)
        self.controller.create_alert_frame(alert_message)
        self.after(100, self.controller.CreateAffinityDiagram.process_batch, data)


    def save_results_event(self):
        global COMPLETED_GPT_REQUESTS
        global REJECTED_DATA
        global NUM_DATA_PROCESSED

        COMPLETED_GPT_REQUESTS = 0
        REJECTED_DATA = []
        NUM_DATA_PROCESSED = 0
        output_file = set_output_file()
        add_headers_to_csv(output_file)

        self.controller.CreateAffinityDiagram.reset()
        self.controller.CreateAffinityDiagram.tkraise()

class ReasonForLabel(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        title = customtkinter.CTkLabel(self, text="Let's generate a reason for a label!")
        title.grid(row=0, column=0)

class AdjustMergeThreshold(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        title = customtkinter.CTkLabel(self, text="Let's adjust merge threshold!")
        title.grid(row=0, column=0)

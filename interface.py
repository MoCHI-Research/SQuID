import tkinter as tk
from tkinter import font as tkfont
import os
import menu

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("1000x1000")

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, ReasonForLabel, DataWithLabel, GenerateGPTReason, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name, *args):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, 'update_data'):
            frame.update_data(*args)
        if page_name == "GenerateGPTReason":
            frame.update_gpt_reason(*args)
        if page_name == "DataWithLabel":
            frame.update_data_w_label(*args)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="SQUiD Interface", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Generate a Reason for a Label", command=lambda: controller.show_frame("ReasonForLabel"))
        button1.pack()


class ReasonForLabel(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Which label are we curious about?", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.label_entry = tk.Entry(self)
        self.label_entry.pack()

        label_button = tk.Button(self, text="Submit Label", command=self.label_submission)
        label_button.pack()

    def label_submission(self):
        entered_label = self.label_entry.get()
        all_data = menu.retrieve_data_with_label(entered_label)
        self.controller.show_frame("DataWithLabel", all_data, entered_label)


class DataWithLabel(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.labels_frame = None
        self.data_num = None
        self.labels = []  # List to store the created labels

        label = tk.Label(self, text="Data:", font=controller.title_font)
        label.pack(pady=10)

        self.labels_frame = tk.Frame(self)
        self.labels_frame.pack()

        self.data_num = tk.Entry(self)
        self.data_num.pack()

        data_num_button = tk.Button(self, text="Submit Data Number", command=self.submit_data_number)
        data_num_button.pack()

    def submit_data_number(self):
        data_number = int(self.data_num.get())
        self.controller.show_frame("GenerateGPTReason", self.all_data, self.entered_label, data_number)

    def update_data_w_label(self, data, label):
        self.all_data = data
        self.entered_label = label
        self.clear_screen()
        count = 1
        for element in data:
            label = tk.Label(self.labels_frame, text=str(count) + ": " + element[1], font=('Arial', 14))
            label.pack()
            self.labels.append(label)
            count += 1

    def clear_screen(self):
        for label in self.labels:
            label.destroy()
        self.labels = []


class GenerateGPTReason(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.this_frame = None
        self.responses = []

        heading = tk.Label(self, text="GPT Response/Reason: ", font=controller.title_font)
        heading.pack()

        self.this_frame = tk.Frame(self)
        self.this_frame.pack()

        start_page_button = tk.Button(self, text="Start Page", command=lambda: self.controller.show_frame("StartPage"))
        start_page_button.pack()

    def update_gpt_reason(self, all_data, label, data_index):
        self.clear_screen()
        gpt_response = menu.generate_reason(all_data, data_index, label)

        for i in range(0, len(gpt_response), 100):
            chunk = gpt_response[i:i+100]
            display_gpt_response = tk.Label(self.this_frame, text=chunk, font=('Arial', 14))
            display_gpt_response.pack()
            self.responses.append(display_gpt_response)

    def clear_screen(self):
        for response in self.responses:
            response.destroy()
        self.responses = []


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

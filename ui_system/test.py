import tkinter as tk

APP_WIDTH = 800
APP_HEIGHT = 600

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # Create a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        
        # Center GUI to middle of screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width - APP_WIDTH) / 2)
        y = int((screen_height - APP_HEIGHT) / 2)
        
        self.geometry(f'{APP_WIDTH}x{APP_HEIGHT}+{x}+{y}')
        
        # Add frames to dictionary
        for F in (StartPage, NewProjectPage, PromptsPage, SettingsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # Show a frame for the given page name
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        
        left_space = tk.Label(self, text="                                                                                              ")
        new_project_button = tk.Button(self, text="New Project", command=lambda: controller.show_frame(NewProjectPage))
        prompts_button = tk.Button(self, text="Prompts", command=lambda: controller.show_frame(PromptsPage))
        settings_button = tk.Button(self, text="Settings", command=lambda: controller.show_frame(SettingsPage))


        # Center the buttons
        left_space.grid(row=0,column=0)
        new_project_button.grid(row=1, column=1)
        prompts_button.grid(row=2, column=1)
        settings_button.grid(row=3, column=1)

        # Use grid's row and column configurations to center the buttons
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

class NewProjectPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="New Project Page")
        label.pack()

        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        back_button.pack()


class PromptsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Prompts Page")
        label.pack()

        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        back_button.pack()


class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Settings Page")
        label.pack()

        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        back_button.pack()


if __name__ == "__main__":
    app = Application()
    app.mainloop()

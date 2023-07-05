import tkinter
import customtkinter
import time
import threading
from menu import label_datapoints

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

# A flag to tell the thread to stop
stop_thread = False
final_time_elapsed = 0

APP_WIDTH = 720
APP_HEIGHT = 480

def show_time_elapsed():
    global final_time_elapsed
    global stop_thread
    start_time = time.time()

    while not stop_thread:
        time.sleep(0.1)  # update every second
        elapsed_time = time.time() - start_time
        print(f"Time elapsed: {elapsed_time:.1f} seconds", end='\r')  # end='\r' overwrites the line

        if stop_thread:
            final_time_elapsed = elapsed_time

def new_project_frame(input):
    
    file = input.get()
    
    print(file)
    
    time.sleep(1.5)
    
    global stop_thread
    # Start the loading thread for the time elapsed
    loading_thread = threading.Thread(target=show_time_elapsed)
    loading_thread.start()

    label_datapoints(file)
    
    stop_thread = True
    loading_thread.join()
    print(f"Final time elapsed: {final_time_elapsed:.1f} seconds")
    # npf = customtkinter.CTk()
    

def app_frame():
    app = customtkinter.CTk()
    app.title("SQUID")

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = int((screen_width - APP_WIDTH) / 2)
    y = int((screen_height - APP_HEIGHT) / 2)

    app.geometry(f'{APP_WIDTH}x{APP_HEIGHT}+{x}+{y}')
    
    input = customtkinter.CTkEntry(app, width=200, height=40)
    input.pack(padx=10, pady=10)

    new_project_button = customtkinter.CTkButton(app, text="Affinity Diagram", command=lambda: new_project_frame(input)) # Soon to change "Affinity Diagram" to "New Project"
    new_project_button.pack(padx=10, pady=10)
   
    prompts_button = customtkinter.CTkButton(app, text="Prompts")
    prompts_button.pack(padx=10, pady=10)
    
    settings_button = customtkinter.CTkButton(app, text="Settings")
    settings_button.pack(padx=10, pady=10)
    
    app.mainloop()

app_frame()
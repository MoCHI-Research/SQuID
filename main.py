from ui import App
import os

def main():
    os.environ["OPENAI_API_KEY"] = ""
    app = App()
    app.wm_minsize(width=1200, height=700)
    app.mainloop()
    os.environ["OPENAI_API_KEY"] = ""

if __name__ == "__main__":
    main()

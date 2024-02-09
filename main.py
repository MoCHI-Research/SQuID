from ui import App
from interface import SampleApp

def main():
    app = App()
    app.wm_minsize(width=1200, height=700)
    app.mainloop()

if __name__ == "__main__":
    main()

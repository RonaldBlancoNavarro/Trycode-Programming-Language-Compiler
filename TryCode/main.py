from mainFrame import MainFrame
from tkinter import *

def main():
    root = Tk()
    root.wm_title("Compilador TryCode")
    root.resizable(False, False)
    app = MainFrame(root)
    app.mainloop()

if __name__=="__main__":
    main()
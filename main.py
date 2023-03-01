from tkinter import *
from tkinter import ttk
# from utils import *
from disp import *

v_num = 0.001

root = Tk()
root.title(f"PyMM {v_num}")
root.minsize(900, 700)
root.maxsize(900, 1080)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

def main():
    window = MainWindow(root=root)

if __name__ == '__main__':
    main()
    root.mainloop()
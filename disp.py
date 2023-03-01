from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from utils import *

class MainWindow:
    def __init__(self, root) -> None:
        self.root = root

        self.main_frame = ttk.Frame(self.root)
        self.main_frame['padding'] = 5
        self.main_frame.grid(column=0, row=0, sticky=NSEW)

        root.option_add('*tearOff', FALSE)
        menubar = Menu(root)
        root['menu'] = menubar
        menu_file = Menu(menubar)
        # menu_edit = Menu(menubar)
        menu_edit = Menu(menubar)
        menubar.add_cascade(menu=menu_file, label='File')
        # menubar.add_cascade(menu=menu_edit, label='Edit')
        menubar.add_cascade(menu=menu_edit, label='Edit')

        menu_file.add_command(label="Open", command=self.placeholder_command)
        menu_file.add_command(label="Save", command=self.placeholder_command)
        menu_file.add_command(label="Save As...", command=self.placeholder_command)
        menu_file.add_command(label="Search", command=self.placeholder_command)

        menu_edit.add_command(label="undo", command=self.placeholder_command)
        menu_edit.add_command(label="redo", command=self.placeholder_command)
        menu_edit.add_command(label="undo", command=self.placeholder_command)

        # Tree Viewer

        self.tree_frame = Frame(self.main_frame, width=400, height=300)
        self.tree_frame.pack(expand=True, fill=BOTH)
        self.tree_canvas = Canvas(self.tree_frame, width=400, height=400)
        self.tree_inner_frame = Frame(self.tree_canvas)
        self.tree_canvas.create_window((0,0), window=self.tree_inner_frame, anchor=NW)
        self.tc_hbar = Scrollbar(self.tree_frame, orient=HORIZONTAL, command=self.tree_canvas.xview)
        self.tc_hbar.pack(side=BOTTOM, fill=X)
        self.tree_canvas.configure(xscrollcommand=self.tc_hbar.set, scrollregion=(0,0,1200,1200))
        self.tree_canvas.config(width=400, height=300)
        self.tree_canvas.pack(side=TOP, fill=BOTH, expand=True)

        


    def placeholder_command(self):
        pass
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

        self.tree_frame = Frame(self.main_frame, width=400, height=200)
        self.tree_frame.pack(expand=True, fill=BOTH)
        self.tree_canvas = Canvas(self.tree_frame, width=400, height=200)
        self.tree_inner_frame = Frame(self.tree_canvas)
        self.tree_canvas.create_window((0,0), window=self.tree_inner_frame, anchor=NW)
        self.tc_hbar = Scrollbar(self.tree_frame, orient=HORIZONTAL, command=self.tree_canvas.xview)
        self.tc_hbar.pack(side=BOTTOM, fill=X)
        self.tree_canvas.configure(xscrollcommand=self.tc_hbar.set, scrollregion=(0,0,1200,200))
        self.tree_w = 1200
        self.tree_h = 200
        self.tree_canvas.config(width=400, height=200)
        self.tree_canvas.pack(side=TOP, fill=BOTH, expand=True)
        
        # Tree itself

        self.listboxes = []
        self.listbox_1_choices = ["alphabet", "numbers"]
        self.listbox_1_choices_var = StringVar(value=self.listbox_1_choices)
        self.listbox_1 = Listbox(self.tree_inner_frame, listvariable=self.listbox_1_choices_var)
        self.listbox_1.pack(side=RIGHT)
        self.listboxes.append(self.listbox_1)

        # Button to test

        self.test_btn = ttk.Button(self.main_frame, text="test", command=self.widen_tree)
        self.test_btn.pack()

        # Lower section Frame

        self.lower_frame = Frame(self.main_frame)
        self.lower_frame.pack(side=BOTTOM)

        # Title and tags section

        self.tt_frame = LabelFrame(self.lower_frame, text="Title And Tags")
        self.tt_frame.pack(side=LEFT)

        self.tt_title = Label(self.tt_frame, text="Title:")
        self.tt_title.grid(column=0, row=0, sticky=NSEW)
        self.disp_title = StringVar()
        self.tt_title_var = Label(self.tt_frame, textvariable=self.disp_title)
        self.tt_title_var.grid(column=1, row=0, sticky=NSEW)
        self.disp_title.set("DEFAULT TITLE")
        self.tt_tags = LabelFrame(self.tt_frame, text="Tags")
        self.tt_tags.grid(column=0, row=1, columnspan=2, sticky=NSEW)

        # Desc Section

        self.desc_frame = LabelFrame(self.lower_frame, text="Description")
        self.desc_frame.pack(side=RIGHT)
        self.desc_entry = Text(self.desc_frame, width=40, height=10)
        self.desc_entry.pack()



    def placeholder_command(self):
        pass

    def widen_tree(self):
        self.tree_w += 200
        self.tree_canvas.configure(scrollregion=(0,0,self.tree_w,300))
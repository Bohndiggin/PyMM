from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from utils import *

nodes_out_of_tree = [
    Node('', 'First Node', 'This is the first Node'),
    Node('First Node', 'First Node Child', 'This ia a child of Node1'),
    Node('', 'Second Node', 'This is another Root node')    
    ]

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

        # Tree Viewer .insert(PARENT, LOCATION/INDEX, NAME, text=DISPLAY_TEXT)

        self.tree = ttk.Treeview(self.main_frame, columns=('desc', 'tags'))
        self.tree.column('desc', width=100, anchor='center')
        self.tree.column('tags', width=100, anchor='center')
        self.tree.heading('desc', text='Description')
        self.tree.heading('tags', text='Tags')
        self.tree.pack(side=TOP, fill='both', expand=True)
        self.tree.insert('', 'end', 'name', text="UH")
        self.tree.insert('', 0, 'Other Name', text="Something Else")
        self.tree.set('Other Name', 'desc', 'klsdjlkajsdflkjkljsdlkfajkldfjlkjasdklfj')
        # Treeview chooses the id:
        self.id = self.tree.insert('', 'end', text='Tutorial')

        # Inserted underneath an existing node:
        self.tree.insert('Other Name', 'end', text='Canvas')
        self.tree.insert(self.id, 'end', 'tree', text='Tree')

        self.tree.insert('tree', 0, 'newboi1', text='newboi1')
        self.tree.insert('tree', 1, 'newboi2', text='newboi2')

        self.tree.bind('<<TreeviewSelect>>', self.tree_select)

        node_list_to_tree(nodes_out_of_tree, self.tree)

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
        self.desc_text_box = Text(self.desc_frame, width=40, height=10)
        self.desc_text_box.pack()



    def placeholder_command(self):
        pass

    def widen_tree(self):
        self.tree_w += 200
        self.tree_canvas.configure(scrollregion=(0,0,self.tree_w,300))
    
    def tree_select(self, event):
        selected = self.tree.selection()[0]
        print("You selected, " +  selected)
        info = self.tree.item(selected)
        content = info['text']
        print(info)
        self.disp_title.set(content)
        try:
            desc_of_selected = info['values'][0]
        except:
            desc_of_selected = info['values']
        self.desc_text_box.delete('1.0', 'end')
        self.desc_text_box.insert('1.0', desc_of_selected)
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from utils import *

nodes_out_of_tree = [
    Node('', 'ROOT', 'This is the Root Node', node_id=0),
    Node(0, 'First Node Child', 'This ia a child of Node1', node_id=1),
    Node(0, 'Second Node', 'This is NOT another Root node', node_id=2)    
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

        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(side=TOP, fill=BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame, columns=('desc', 'tags', 'id'))
        self.tree.column('desc', width=500, anchor='center')
        self.tree.column('tags', width=100, anchor='center')
        self.tree.column('id', width=10, anchor='center')
        self.tree.heading('desc', text='Description')
        self.tree.heading('tags', text='Tags')
        self.tree.heading('id', text='Node ID')
        self.tree.pack(side=LEFT, fill='both', expand=True)

        self.tree_scroll_bar = ttk.Scrollbar(self.tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree_scroll_bar.pack(side=RIGHT, fill=Y)

        self.tree.configure(yscrollcommand=self.tree_scroll_bar.set)

        self.tree.bind('<<TreeviewSelect>>', self.tree_select)

        node_list_to_tree(nodes_out_of_tree, self.tree)

        # Lower section Frame

        self.lower_frame = Frame(self.main_frame)
        self.lower_frame.pack(side=BOTTOM)

        self.add_node_btn = ttk.Button(self.lower_frame, command=self.add_node, text='Add Node')
        self.add_node_btn.pack(side=BOTTOM)
        self.tree_edit_btn = ttk.Button(self.lower_frame, command=self.edit_mode, text='Edit Tree')
        self.tree_edit_btn.pack(side=BOTTOM)
        
        self.move_up_btn = ttk.Button(self.lower_frame, command=self.move_node_up_level, text='Move Node Up')
        self.move_up_btn.pack(side=BOTTOM)
        
        # Title and tags section

        self.title_tags_frame = LabelFrame(self.lower_frame, text="Title And Tags")
        self.title_tags_frame.pack(side=LEFT)

        self.title_tags_title = Label(self.title_tags_frame, text="Title:")
        self.title_tags_title.grid(column=0, row=0, sticky=NSEW)
        self.disp_title = StringVar()
        self.title_tags_title_var = Entry(self.title_tags_frame, textvariable=self.disp_title)
        self.title_tags_title_var.grid(column=1, row=0, sticky=NSEW)
        self.disp_title.set("DEFAULT TITLE")
        self.title_tags_tags = LabelFrame(self.title_tags_frame, text="Tags")
        self.title_tags_tags.grid(column=0, row=1, columnspan=2, sticky=NSEW)
        self.title_tags_title_var.bind('<Return>', self.tree_select)

        # Desc Section

        self.desc_frame = LabelFrame(self.lower_frame, text="Description")
        self.desc_frame.pack(side=RIGHT)
        self.desc_text_box = Text(self.desc_frame, width=40, height=10)
        self.desc_text_box.pack()
        self.desc_text_box.bind('<Return>', self.tree_select)

        self.prev_selected_id = 0
        self.edit_mode_var = False



    def placeholder_command(self):
        pass

    def widen_tree(self):
        self.tree_w += 200
        self.tree_canvas.configure(scrollregion=(0,0,self.tree_w,300))
    
    def tree_select(self, event):
        if self.prev_selected_id:
            self.edit_node(self.prev_selected_id)
        selected = self.tree.selection()[0]
        # print("You selected, " +  selected)
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
        self.prev_selected_id_info = self.tree.item(selected)
        self.prev_selected_id = self.prev_selected_id_info['values'][-1]
        if self.edit_mode_var:
            self.move_nodes(event=event)
        return "break"

    def add_node(self):
        try:
            selected = self.tree.selection()[0]
        except:
            selected = ''
        nodes_out_of_tree.append(Node(selected, 'node '+ str(len(nodes_out_of_tree)), 'Description', node_id=len(nodes_out_of_tree)))
        node_to_tree(nodes_out_of_tree[-1], self.tree)

    def edit_node(self, prev_selected_id):
        print(nodes_out_of_tree[prev_selected_id])
        new_desc = self.desc_text_box.get(1.0, 'end-1c')
        selected_node = nodes_out_of_tree[prev_selected_id]
        selected_node.edit_desc(new_desc)
        self.tree.set(prev_selected_id, 'desc', new_desc)
        new_title = self.title_tags_title_var.get()
        selected_node.edit_title(new_title)
        self.tree.item(prev_selected_id, text=new_title)
        print(nodes_out_of_tree[prev_selected_id])
    
    def edit_mode(self):
        if self.edit_mode_var:
            self.edit_mode_var = False
        else:
            self.edit_mode_var = True

    def move_nodes(self, event): # Using the mouse to move nodes. How tho?
        pass

    def move_node_up_level(self):
        selected = self.tree.selection()[0]
        selected_info = self.tree.item(selected)
        selected_id = selected_info['values'][-1]
        selected_node = nodes_out_of_tree[selected_id]
        selected_node_parent = int(selected_node.parent)
        parent_id = nodes_out_of_tree[selected_node_parent].parent
        # parent_parent_id = nodes_out_of_tree[parent_id].parent
        selected_node.parent = parent_id
        self.tree.move(selected_id, parent_id, 'end')
        
    def move_node_down_level(self):
        pass
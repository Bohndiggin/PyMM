from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from utils import *

# root_node = Node('', 'ROOT', 'This is the Root Node', node_id=0)
# home_node = Node(root_node, 'HOME', 'This is Home', node_id=1)

# nodes_out_of_tree = [root_node]


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

        menu_file.add_command(label="Open", command=self.load_data)
        menu_file.add_command(label="Save", command=self.save_window)
        menu_file.add_command(label="Save As JSON", command=self.save_as_json_window)
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

        self.backend_node_tree = NodeTree('treename', tk_tree=self.tree)
        self.backend_node_tree.add_node_to_tree(self.backend_node_tree.nodes[1], 'Test', 'Tesging', self.tree)
        # save_to_json(self.backend_node_tree)
        # print(load_from_json('save.json'))
        # print(load_from_pickle('save.pkl'))
        # save_to_pickle(self.backend_node_tree)
        
        print('WORKED')
        # node_list_to_tree(nodes_out_of_tree, self.tree)

        # Lower section Frame

        self.lower_frame = Frame(self.main_frame)
        self.lower_frame.pack(side=BOTTOM)

        # self.add_node_btn = ttk.Button(self.lower_frame, command=self.add_node, text='Add Node')
        # self.add_node_btn.pack(side=BOTTOM)
        self.add_child_node_btn = ttk.Button(self.lower_frame, command=self.add_child_node, text='Add Child Node')
        self.add_child_node_btn.pack(side=BOTTOM)
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

    def add_child_node(self):
        try:
            selected = self.tree_to_node()
        except:
            selected = ''
        print(selected)
        title_of_node = 'node ' + str(len(self.backend_node_tree.nodes))
        self.backend_node_tree.add_node_to_tree(selected, title_of_node, 'DEFAULT', self.tree)
        print(self.backend_node_tree.nodes[-1].parent)
        

    def edit_node(self, prev_selected_id):
        # print(nodes_out_of_tree[prev_selected_id])
        new_desc = self.desc_text_box.get(1.0, 'end-1c')
        selected_node = self.backend_node_tree.nodes[prev_selected_id]
        selected_node.edit_desc(new_desc)
        self.tree.set(prev_selected_id, 'desc', new_desc)
        new_title = self.title_tags_title_var.get()
        selected_node.edit_title(new_title)
        self.tree.item(prev_selected_id, text=new_title)
        print(self.backend_node_tree.nodes[prev_selected_id])
    
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
        selected_node = self.backend_node_tree.nodes[selected_id]
        # selected_node_parent = int(selected_node.parent)
        parent_id = self.find_parent(selected)
        # parent_parent_id = nodes_out_of_tree[parent_id].parent
        selected_node.parent = int(parent_id.node_id)
        self.tree.move(selected_id, parent_id, 'end')

    def move_node_up_level_two(self):
        selected_node = self.tree_to_node()
        selected_grand_parent = self.find_parent(selected=selected_node.node_id)
        self.tree.move(selected_node.node_id, selected_grand_parent, 'end')
        
    def move_node_down_level(self):
        pass

    # def add_node(self):
    #     try:
    #         selected = self.tree.selection()[0]
    #     except:
    #         selected = ''
    #     parent_id = int(self.find_parent(selected=selected))
    #     parent = nodes_out_of_tree[parent_id]
    #     nodes_out_of_tree.append(Node(parent, 'node '+ str(len(nodes_out_of_tree)), 'Description', node_id=len(nodes_out_of_tree)))
    #     node_to_tree(nodes_out_of_tree[-1], self.tree)

    def find_parent(self, selected):
        selected_info = self.tree.item(selected)
        selected_id = selected_info['values'][-1]
        selected_node = self.backend_node_tree.nodes[selected_id]
        # print('+++' , selected_node)
        selected_node_parent = int(selected_node.parent.node_id)
        # print('+=+=+', selected_node_parent)
        parent_id = self.backend_node_tree.nodes[selected_node_parent].parent
        # print(parent_id)
        return parent_id
    
    def tree_to_node(self):
        selected = self.tree.selection()[0]
        selected_info = self.tree.item(selected)
        selected_id = selected_info['values'][-1]
        selected_node = self.backend_node_tree.nodes[selected_id]
        return selected_node
    
    def redraw_tree(self): #Function to draw tree from scratch
        self.tree.delete(0)
        self.backend_node_tree.node_list_to_tree(self.tree)

    def delete_node(self):
        selected_node = self.tree_to_node()

    def load_data(self, **kwargs):
        file_name = kwargs.get('filename', None)
        if file_name:
            try:
                self.backend_node_tree = load_from_pickle(file_name)
                print('Loaded!')
            except:
                temporary_var = load_from_json(file_name, self.tree)
                print(temporary_var)
        else:
            file_name = filedialog.askopenfilename(initialfile='save.pkl', defaultextension='.pkl', filetypes=[("All Files","*.*"),("Pickle","*.pkl")])
            try:
                self.backend_node_tree = load_from_pickle(file_name)
                print('Loaded with prompt!')
            except:
                self.backend_node_tree = load_from_json(file_name, tk_tree=self.tree)
                # print(temporary_var)
                # print(json.loads(temporary_var, object_hook=lambda x: json_decoder_hook(x, self.tree)))
                print(self.backend_node_tree)
        self.redraw_tree()

    def save_window(self):
        filename = filedialog.asksaveasfilename(initialfile='save.pkl', defaultextension=".pkl",filetypes=[("All Files","*.*"),("Pickle","*.pkl")])
        save_to_pickle(self.backend_node_tree, filename=filename)
        print('Saved!')
        self.load_data(filename=filename)
    
    def save_as_json_window(self):
        filename = filedialog.asksaveasfilename(initialfile='save.json', defaultextension=".json",filetypes=[("All Files","*.*"),("JSON","*.json")])
        save_to_json(self.backend_node_tree, filename=filename)
        print('Exported!')
        self.load_data(filename=filename)

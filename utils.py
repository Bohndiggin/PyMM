import pandas as pd
import json, pickle, jsonpickle
from opyml import OPML, Outline

class Node:
    def __init__(self, parent, title="", desc="", children=[], node_id=0) -> None:
        self.parent = parent
        self.title = title
        self.desc = desc
        self.tags = []
        self.children = children
        self.node_id = node_id

    def edit_desc(self, new_desc):
        self.desc = new_desc

    def edit_title(self, new_title):
        self.title = new_title

    def add_tags(self, new_tag):
        self.tags.append(Tag(new_tag))

    def get_grandparent_id(self):
        return self.parent.parent.node_id

    def __repr__(self) -> str:
        return str(self.node_id)
    
class NodeTree:
    def __init__(self, tree_name, **kwargs) -> None:
        self.tree_name = tree_name
        tk_tree = kwargs.get('tk_tree', None)
        # nodes = kwargs.get('node_list', None)
        loaded_tree = kwargs.get('loaded_tree', 0)
        if loaded_tree:
            self.nodes = []
        else:
            root_node = Node('', 'ROOT', 'This is the Root Node', node_id=0)
            home_node = Node(root_node, 'HOME', 'This is Home', node_id=1)
            self.nodes = [root_node, home_node]
            self.node_list_to_tree(tk_tree)
            # for i in nodes:
            #     self.nodes.append(Node(i['parent'], i['title'], i['desc'], node_id=i['node_id']))
            # #print('++++')
            # #print(self.nodes)
            # #print('++++')
            # # self.node_list_to_tree()

    def add_node_to_tree(self, selected, title, desc, tree):
        new_node = Node(selected, title=title, desc=desc, node_id=len(self.nodes))
        selected.children.append(new_node)
        self.nodes.append(new_node)
        self.node_to_tree(new_node, tree=tree)

    def node_to_tree(self, node, tree):
        tree.insert(node.parent, 'end', node.node_id, text=node.title)
        tree.set(node.node_id, 'desc', node.desc)
        tree.set(node.node_id, 'id', node.node_id)

    def node_list_to_tree(self, tree):
        for i in self.nodes:
            node_to_tree(i, tree=tree)

    def save_to_json(self):
        json_data = jsonpickle.encode(self)
        #print(json_data)

    def __repr__(self) -> str:
        return f'{self.tree_name} a tree with {len(self.nodes)} nodes'

class Tag:
    def __init__(self, title) -> None:
        self.title = title
    def __repr__(self) -> str:
        return f'{self.title}, a Tag'
    
def node_to_tree(node, tree):
    tree.insert(node.parent, 'end', node.node_id, text=node.title)
    tree.set(node.node_id, 'desc', node.desc)
    tree.set(node.node_id, 'id', node.node_id)

def node_list_to_tree(list_of_nodes, tree):
    for i in list_of_nodes:
        node_to_tree(i, tree=tree)

def tree_to_node(node_id):
    pass

def node_import(list_of_nodes):
    pass

def node_export(list_of_nodes):
    pass

def json_decoder_hook(obj, tk_tree, node_tree):
    print(obj)
    print(type(obj))
    pass
    # TODO sort by node_id then insert them one at a time. may not need json decoder hook.
    try:
        type_of_obj = obj.get('py/object')
        if type_of_obj == 'utils.Node':
            node_tree.add_node_to_tree()
        elif type_of_obj == 'utils.NodeTree':
            print('tree found')
            return 'TEMP TREE'
        else:
            pass
    except:
        pass
    # try:
    #     print(obj['node_id'])
    #     # print('found!')
    #     print('+++++++++', obj['parent'], obj['title'], obj['desc'], node_id=obj['node_id'])
    #     new_obj = Node(obj['parent'], obj['title'], obj['desc'], node_id=obj['node_id'])
    #     print(new_obj.parent)
    #     node_tree.nodes.append(new_obj)
    #     print(node_tree.nodes)
    # except:
    #     print('not node')
    # new_tree = NodeTree(obj['tree_name'], tk_tree=tk_tree, node_list=obj['nodes'])

def save_to_json(node_tree, filename='save.json'):
    # node_tree_as_pickle = pickle.(node_tree)
    json_data = jsonpickle.encode(node_tree)
    #print(type(json_data))
    with open(filename, 'w') as f:
        f.write(json_data)
    #print(type(json_data))

def load_from_json(filepath, tk_tree):
    with open(filepath, 'r') as f:
        new_tree = NodeTree('loaded_tree', tk_tree=tk_tree, loaded_tree=1)
        # obj_bring = json.load(f)
        json.load(f, object_hook=lambda x: json_decoder_hook(x, tk_tree, new_tree))
        # print('SOMETHIN', loaded)
        #print(type(loaded))
        # print(new_tree.nodes[1].parent, 'NODE')
        print(new_tree)
        print(type(new_tree))
    node_list_to_tree(new_tree.nodes, tree=tk_tree)
    return new_tree
        
def save_to_pickle(node_tree, filename='save.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(node_tree, f)

def load_from_pickle(filepath):
    with open(filepath, 'rb') as f:
        loaded = pickle.load(f)
    return loaded

def load_from_opml(filepath):
    with open(filepath, 'r') as f:
        document = OPML()
        loaded = document.from_xml(f.read())
        doc_as_xml = loaded.to_xml()
    return doc_as_xml

print(load_from_opml('testing_stuff\D_D.opml'))

import pandas as pd

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

    def get_parent_id(self):
        pass

    def __repr__(self) -> str:
        return f'{self.title} is a Node with the description: {self.desc}, its parent is {self.parent}'
    
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

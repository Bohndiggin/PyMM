import pandas as pd

class Tree:
    def __init__(self) -> None:
        pass

class Node:
    def __init__(self, parent, desc="", title="", children=[]) -> None:
        self.parent = parent
        self.title = title
        self.desc = desc
        self.tags = []
        self.children = children

    def edit_desc(self, new_desc):
        self.desc = new_desc

    def edit_title(self, new_title):
        self.title = new_title

    def add_tags(self, new_tag):
        self.tags.append(Tag(new_tag))

    def __repr__(self) -> str:
        return f'{self.title} is a Node.'
    
class Tag:
    def __init__(self, title) -> None:
        self.title = title
    def __repr__(self) -> str:
        return f'{self.title}, a Tag'
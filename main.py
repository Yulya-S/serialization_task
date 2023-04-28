from enum import Enum


class Alignment(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class Widget():
    def __init__(self, parent):
        self.parent = parent
        self.childrens = []
        if self.parent is not None:
            self.parent.add_children(self)

    def add_children(self, children: "Widget"):
        self.childrens.append(children)

    def to_binary(self):
        return b"0"

    @classmethod
    def from_binary(self, data):
        pass

    def __str__(self):
        return f"{self.__class__.__name__}{self.childrens}"

    def __repr__(self):
        return str(self)


class MainWindow(Widget):
    def __init__(self, title: str):
        super().__init__(None)
        self.title = title


class Layout(Widget):
    def __init__(self, parent, alignment: Alignment):
        super().__init__(parent)
        self.alignment = alignment


class LineEdit(Widget):
    def __init__(self, parent, max_length: int = 10):
        super().__init__(parent)
        self.max_length = max_length


class ComboBox(Widget):
    def __init__(self, parent, items):
        super().__init__(parent)
        self.items = items


def serialization(app):
    d = dict()
    d["type"] = str(app).split('[')[0]
    if d["type"] == 'MainWindow':
        d["value"] = app.title
    elif d["type"] == 'Layout':
        d["value"] = app.alignment
    elif d["type"] == 'LineEdit':
        d["value"] = app.max_length
    elif d["type"] == 'ComboBox':
        d["value"] = app.items
    d["children"] = [serialization(i) for i in app.childrens]
    return d


def deserialization(dict, parent=''):
    if dict["type"] == 'MainWindow':
        parent = MainWindow(dict["value"])
    elif dict["type"] == 'Layout':
        parent = Layout(parent, dict["value"])
    elif dict["type"] == 'LineEdit':
        parent = LineEdit(parent, dict["value"])
    elif dict["type"] == 'ComboBox':
        parent = ComboBox(parent, dict["value"])
    if dict['children'] != []:
        for i in dict['children']:
            deserialization(i, parent)
    return parent


app = MainWindow("Application")
layout1 = Layout(app, Alignment.HORIZONTAL)
layout2 = Layout(app, Alignment.VERTICAL)

edit1 = LineEdit(layout1, 20)
edit2 = LineEdit(layout1, 30)

box1 = ComboBox(layout2, [1, 2, 3, 4])
box2 = ComboBox(layout2, ["a", "b", "c"])

dess = serialization(app)
print(dess)

print(app)
dess = deserialization(dess)
print(dess)

bts = app.to_binary()
print(f"Binary data length {len(bts)}")
print(f"Binary data length {len(dess.to_binary())}")

new_app = MainWindow.from_binary(bts)
print(new_app)
print(MainWindow.from_binary(dess.to_binary()))

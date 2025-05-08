from .point import Point

from .rectangle import Rectangle

class RTree:
    head: Rectangle
    max_size: int

    def __init__(self, max_size: int = 3):
        """Inits the tree, takes an argument of max size for the b value,
        this b value deafults to 3
        """
        self.max_size = max_size

        self.head = Rectangle(self.max_size)
        self.head.insert_rect(Rectangle(self.max_size))

    def insert(self, id, x, y):
        """inserts a point, constantly makes new head nodes and inserts the return into the new head,
        means newer nodes are closer to the top of the tree
        """

        p = Point(id, x, y)
        split = self.head.insert(p)

        if split is not None:
            new_head = Rectangle(self.head.max_size)
            new_head.insert_rect(self.head)
            new_head.insert_rect(split)
            self.head = new_head            
            

    #chat gpt generated to visualise and validate tree structure - I was sick of looking at debugging traces
    def print_horizontal_tree(self):
        """Chat gpt generated to visualise tree structure"""
        from collections import deque

        def get_label(obj):
            if hasattr(obj, 'is_leaf') and not obj.is_leaf():
                return f"Rect[{obj.x_min},{obj.y_min}]-[{obj.x_max},{obj.y_max}]"
            elif hasattr(obj, 'is_leaf') and obj.is_leaf():
                return f"Leaf[{obj.x_min},{obj.y_min}]-[{obj.x_max},{obj.y_max}]"
            else:  # Point
                return f"({obj.x},{obj.y})"

    # Perform a BFS to collect nodes at each level
        queue = deque([(self.head, 0)])
        levels = {}

        while queue:
            node, depth = queue.popleft()
            levels.setdefault(depth, []).append(node)

            if hasattr(node, 'data_list'):
                for child in node.data_list:
                    queue.append((child, depth + 1))

    # Print tree level by level
        max_width = max(len(nodes) for nodes in levels.values())
        spacing = 12

        for depth in sorted(levels):
            labels = [get_label(node) for node in levels[depth]]
            indent = " " * ((max_width - len(labels)) * spacing // 2)
            line = indent + (" " * spacing).join(labels)
            print(line)
            if depth < max(levels):
                branch_indent = " " * ((max_width - len(labels)) * spacing // 2 + spacing // 2 - 1)
                branches = branch_indent + ("|" + " " * (spacing - 1)) * len(labels)
                print(branches)


        
if __name__ == "__main__":
    tree = RTree(5)
    tree.insert(1, 9, 2)
    tree.insert(2, 5, 4)
    tree.insert(3, 6, 7)
    tree.insert(4, 8, 6)
    tree.insert(5, 1, 9)
    tree.insert(6, 4, 7)
    tree.insert(7, 2, 5)
    tree.insert(8, 1, 4)
    tree.insert(9, 4, 7)
    tree.insert(10, 6, 2)
    tree.print_horizontal_tree()
    
    
    
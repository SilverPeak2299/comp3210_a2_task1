import math

B = 6  # Maximum number of entries per node

class RTreeNode:
    def __init__(self, is_leaf=True):
        """
        Initialize an R-Tree node.

        Args:
            is_leaf (bool): Whether this node is a leaf node.
        """
        self.is_leaf = is_leaf
        self.entries = []  # Each entry is either a point or a child node with MBR
        self.children = []  # Used if not a leaf
        self.mbr = None  # Minimum Bounding Rectangle (x_min, y_min, x_max, y_max)

    def compute_mbr(self):
        """
        Recompute the MBR (Minimum Bounding Rectangle) for this node based on entries.
        """
        if self.is_leaf:
            coords = [(p.x, p.y) for p in self.entries]
        else:
            coords = [child.mbr for child in self.children]

        x_coords = [x for pair in coords for x in pair[::2]]
        y_coords = [y for pair in coords for y in pair[1::2]]
        self.mbr = (min(x_coords), min(y_coords), max(x_coords), max(y_coords))
    
    def min_dist_to_point(self, qx, qy):
        """
        Compute the minimum Euclidean distance from the given point to this node's MBR.
    
        Args:
            qx (float): X-coordinate of the query point.
            qy (float): Y-coordinate of the query point.
    
        Returns:
            float: Minimum distance from the point to the node's MBR.
        """
        x_min, y_min, x_max, y_max = self.mbr
    
        cx = max(x_min, min(qx, x_max))
        cy = max(y_min, min(qy, y_max))
    
        # Euclidean distance to the closest point in the MBR
        return math.hypot(qx - cx, qy - cy)

class RTree:
    def __init__(self):
        """Initialize the R-Tree with an empty root node."""
        self.root = RTreeNode()

    def insert(self, node, point):
        """
        Insert a point into the R-Tree, starting at the given node.

        Args:
            node (RTreeNode): The node to begin insertion.
            point (Point): The point to insert.
        """
        if node.is_leaf:
            node.entries.append(point)
            if len(node.entries) > B:
                self._handle_overflow(node)
        else:
            best_child = self._choose_subtree(node, point)
            self.insert(best_child, point)

        node.compute_mbr()

    def _choose_subtree(self, node, point):
        """
        Choose the best child node to insert the point into, based on MBR expansion.

        Args:
            node (RTreeNode): Internal node.
            point (Point): Point to be inserted.

        Returns:
            RTreeNode: The chosen child node.
        """
        best_child = None
        min_increase = float('inf')
        px, py = point.x, point.y

        for child in node.children:
            x_min, y_min, x_max, y_max = child.mbr
            area_before = (x_max - x_min) * (y_max - y_min)
            new_x_min = min(x_min, px)
            new_y_min = min(y_min, py)
            new_x_max = max(x_max, px)
            new_y_max = max(y_max, py)
            area_after = (new_x_max - new_x_min) * (new_y_max - new_y_min)
            increase = area_after - area_before

            if increase < min_increase:
                min_increase = increase
                best_child = child

        return best_child

    def _handle_overflow(self, node):
        """
        Handle overflow in a node by splitting it.

        Args:
            node (RTreeNode): The node to split.
        """
        if node == self.root:
            # Special case: split root and create new root
            left, right = self._split_node(node)
            new_root = RTreeNode(is_leaf=False)
            new_root.children = [left, right]
            new_root.compute_mbr()
            self.root = new_root
        else:
            left, right = self._split_node(node)
            # Replace the node in its parent with the two new nodes
            parent = self._find_parent(self.root, node)
            parent.children.remove(node)
            parent.children.extend([left, right])
            if len(parent.children) > B:
                self._handle_overflow(parent)

    def _split_node(self, node):
        """
        Split a node into two nodes.

        Args:
            node (RTreeNode): Node to split.

        Returns:
            tuple: Two new RTreeNode instances resulting from the split.
        """
        entries = node.entries if node.is_leaf else node.children
        midpoint = len(entries) // 2
        group1 = entries[:midpoint]
        group2 = entries[midpoint:]

        left = RTreeNode(is_leaf=node.is_leaf)
        right = RTreeNode(is_leaf=node.is_leaf)

        if node.is_leaf:
            left.entries = group1
            right.entries = group2
        else:
            left.children = group1
            right.children = group2

        left.compute_mbr()
        right.compute_mbr()

        return left, right

    def _find_parent(self, current, target):
        """
        Find the parent of a given node.

        Args:
            current (RTreeNode): Current node in traversal.
            target (RTreeNode): Node whose parent is being searched.

        Returns:
            RTreeNode: The parent node of the target.
        """
        if current.is_leaf:
            return None

        for child in current.children:
            if child == target:
                return current
            parent = self._find_parent(child, target)
            if parent:
                return parent

        return None
        
    
    def print_rtree_structure(self, node, prefix=""):
        """
    Recursively prints the R-tree structure with box-drawing characters.

    Args:
        node (RTreeNode): The root or current node of the R-tree.
        prefix (str): Used internally to manage indentation during recursion.
        """
        def mbr_str(mbr):
            x1, y1, x2, y2 = mbr
            return f"[{x1:.2f},{y1:.2f}]-[{x2:.2f},{y2:.2f}]"

        node_desc = "Leaf" if node.is_leaf else "Rect"
        print(f"{prefix}{node_desc} {mbr_str(node.mbr)}")

        if not node.is_leaf:
            n = len(node.children)
            for i, child in enumerate(node.children):
                is_last = (i == n - 1)
                branch = "└── " if is_last else "├── "
                extension = "    " if is_last else "│   "
                self.print_rtree_structure(child, prefix + branch)
            else:
                # You can include point-level details if you want
                pass  # Or add: for pt in node.entries: print(f"{prefix}    • Point: ({pt['x']}, {pt['y']})")
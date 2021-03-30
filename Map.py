import Stack

class Node:

    ''' Node of Red-Black Tree '''

    def __init__(self, key, value, left=None, right=None, parent=None, red=True):
        self.key = key # Key
        self.value = value # Value
        self.left = left # Left child
        self.right = right # Right child
        self.parent = parent # Parent
        self.red = red # Color (True=Red, False=Black)


class Map:

    ''' Red-Black Tree '''

    def __init__(self, root=None): 
        self.root = root
        self.nil = Node(None, None, parent=root, red=False)
        if self.root is not None: # If root is passed
            self.root.left = self.nil
            self.root.right = self.nil

    def left_rotate(self, node):
        
        ''' Left rotate the node '''

        child = None
        if node.right is not None: # If node has right child
            child = node.right
        if node == self.root: 
            self.root = child # Child is root
            temp = child.left 
            child.left = node # Child's left child is node
            child.parent = None # Child parent is None, because root has no parent
            node.right = temp # Node right is prev child's left child
            temp.parent = node
            node.parent = child # Parent of node is child
        else:
            child.parent = node.parent # Parent of child is node's parent
            if node.parent.right == node:
                node.parent.right = child
            else:
                node.parent.left = child
            temp = child.left
            child.left = node # Child's left child is node
            node.right = temp # Node right is prev child's left child
            temp.parent = node
            node.parent = child # Parent of node is child
            

    def right_rotate(self, node):
        ''' Right rotate the node '''
        child = None
        if node.left is not None: # If node has left child
            child = node.left
        if node == self.root:
            self.root = child # Child is root
            temp = child.right 
            child.right = node # Child's right child is node
            child.parent = None # Child parent is None, because root has no parent
            node.left = temp # Node left is prev child's right child
            temp.parent = node
            node.parent = child # Parent of node is child
        else:
            child.parent = node.parent # Parent of child is node's parent
            if node.parent.right == node:
                node.parent.right = child
            else:
                node.parent.left = child
            temp = child.right
            child.right = node # Child's right child is node
            node.left = temp # Node left is prev child's right child
            temp.parent = node
            node.parent = child # Parent of node is child

    def insert_balance(self, node):

        ''' Balance tree after insertion '''

        balanceNode = node
        while balanceNode.parent is not None and balanceNode.parent.red == True: # While balanceNode is not root and balanceNode's parent color is red
            gp = balanceNode.parent.parent # Grand parent of balanceNode
            p = balanceNode.parent # Parent of balanceNode
            if gp is not None and gp.left == p: # If parent is left child
                if gp.right.red: # If 'uncle' is red
                    # Make gp's children black, gp red. balanceNode is gp now
                    gp.left.red = False 
                    gp.right.red = False
                    gp.red = True
                    balanceNode = gp
                elif p.right == balanceNode: # If balanceNode is right child
                    balanceNode = p # balanceNode is p now
                    self.left_rotate(balanceNode) # Rotate balanceNode to the left
                else:    
                    # Make parent black, gp red. Rotate gp to the right
                    p.red = False
                    gp.red = True
                    self.right_rotate(gp)
            elif gp is not None: # If parent is right child
                if gp.left.red: # If 'uncle' is red
                    # Make gp's children black, gp red. balanceNode is gp now
                    gp.left.red = False
                    gp.right.red = False
                    gp.red = True
                    balanceNode = gp
                elif p.left == balanceNode: # If balanceNode is left child
                    balanceNode = p # balanceNode is p now
                    self.right_rotate(balanceNode) # Rotate balanceNode to the right
                else:
                    # Make parent black, gp red. Rotate gp to the left
                    p.red = False
                    gp.red = True
                    self.left_rotate(gp)
            else: # If gp is None
                break
        self.root.red = False # Set root color to black

    def insert(self, key, value, root=None):

        ''' Insertion of [key, value] pair '''

        if self.empty(): # If tree is empty
            self.root = Node(key, value, self.nil, self.nil, red=False) # Insert node as a root
        else:
            if root is None: # Pass root only inside insert method. Set to tree root by default
                root = self.root
            if root.key == key: # If pair with passed key already exists
                raise Exception(f"Pair with key={key} already exists")
            if root.key > key: # Go to the left subtree
                if root.left == self.nil: # Found place to insert
                    root.left = Node(key, value, self.nil, self.nil, parent=root) # Insert the new node
                    if root != self.root: # If new node's parent is not root
                        self.insert_balance(root.left) # Balance the tree
                else:
                    self.insert(key, value, root.left) # Insert to the left subtree
            else: # Go to the right subtree
                if root.right == self.nil: # Found place to insert
                    root.right = Node(key, value, self.nil, self.nil, parent=root) # Insert the new node
                    if root != self.root: # If new node's parent is not root
                        self.insert_balance(root.right) # Balance the tree
                else:
                    self.insert(key, value, root.right) # Insert to the right subtree

    def remove_balance(self, node, parent=None):

        ''' Balance tree after deleting an element with color black '''

        if parent is None: # Pass parent only if node is nil, because we can't get parent of nil
            parent = node.parent
        while node != self.root and not node.red: # While node is not root of the tree and node's color is black
            if node != self.nil:
                parent = node.parent # Get parent
            if node == parent.left: # If node is left child
                w = parent.right # Brother of node
                if w.red: # If brother is red
                    # Make brother black, parent red. Rotate parent to the left and get new brother of node
                    w.red = False
                    parent.red = True
                    self.left_rotate(parent)
                    w = parent.right
                if not w.left.red and not w.right.red: # If brother's children are black
                    # Make brother red. Change current node to it's parent
                    w.red = True
                    node = parent
                else:
                    if not w.right.red: # If brother's right child is black
                        # Make brother's left child black, brother red. Rotate brother to the right and get new brother of node
                        w.left.red = False
                        w.red = True
                        self.right_rotate(w)
                        w = parent.right
                    # Make brother's color same as parent's color. Make parent and brother's right child black. Rotate parent to the left and change current node to tree root
                    w.red = parent.red
                    parent.red = False
                    w.right.red = False
                    self.left_rotate(parent)
                    node = self.root
            else:  # If node is right child
                w = parent.left # Brother of node
                if w.red: # If brother is red
                    # Make brother black, parent red. Rotate parent to the right and get new brother of node
                    w.red = False
                    parent.red = True
                    self.right_rotate(parent)
                    w = parent.left
                if not w.left.red and not w.right.red: # If brother's children are black
                    # Make brother red. Change current node to it's parent
                    w.red = True
                    node = parent
                else:
                    if not w.left.red: # If brother's left child is black
                        # Make brother's right child black, brother red. Rotate brother to the left and get new brother of node
                        w.right.red = False
                        w.red = True
                        self.left_rotate(w)
                        w = parent.left
                    # Make brother's color same as parent's color. Make parent and brother's left child black. Rotate parent to the right and change current node to tree root
                    w.red = parent.red
                    parent.red = False
                    w.left.red = False
                    self.right_rotate(parent)
                    node = self.root
        node.red = False # Change current node color to black
            
    def remove(self, key):

        ''' Deleting pair by key '''

        if self.empty(): # If tree is empty
            raise Exception("Map is empty")
        else:
            node_to_delete = None
            cur = self.root
            while cur != self.nil and cur.key != key: # Find node to delete
                if cur.key > key: # Go to the left subtree
                    cur = cur.left
                else: # Go to the right subtree
                    cur = cur.right
            if cur == self.nil: # If node is not found
                raise Exception(f"Pair with key={key} doesn't exist")
            node_to_delete = cur
            if node_to_delete.left == self.nil and node_to_delete.right == self.nil: # If node to delete has no children
                if node_to_delete != self.root: 
                    if node_to_delete.parent.left == node_to_delete: # If node to delete is left child
                        node_to_delete.parent.left = self.nil
                    else: # If node to delete is right child
                        node_to_delete.parent.right = self.nil 
                    if not node_to_delete.red: # If deleted node was black
                        self.remove_balance(self.nil, node_to_delete.parent) # Balance tree
                else: # If node to delete is tree root
                    self.root = self.nil # If node to delete is root of the tree
            elif node_to_delete.left != self.nil and node_to_delete.right == self.nil: # If node to delete has only left child
                if node_to_delete != self.root:
                    if node_to_delete.parent.left == node_to_delete: # If node to delete is left child
                        node_to_delete.parent.left = node_to_delete.left
                    else: # If node to delete is right child
                        node_to_delete.parent.right = node_to_delete.left
                    if not node_to_delete.red: # If deleted node was black
                        self.remove_balance(node_to_delete.left) # Balance tree
                else: # If node to delete is tree root
                    # Copy left child's [key, value] to tree root and delete left child of tree root
                    self.root.key, self.root.value = self.root.left.key, self.root.left.value
                    self.root.left = self.nil
            elif node_to_delete.right != self.nil and node_to_delete.left == self.nil: # If node to delete has only right child
                if node_to_delete != self.root:
                    if node_to_delete.parent.left == node_to_delete: # If node to delete is left child
                        node_to_delete.parent.left = node_to_delete.right
                    else: # If node to delete is right child
                        node_to_delete.parent.right = node_to_delete.right
                    if not node_to_delete.red: # If deleted node was black
                        self.remove_balance(node_to_delete.right) # Balance tree
                else: # If node to delete is tree root
                    # Copy right child's [key, value] to tree root and delete right child of tree root
                    self.root.key, self.root.value = self.root.right.key, self.root.right.value
                    self.root.right = self.nil
            else: # If node to delete has both children
                node_to_delete = node_to_delete.right
                while  node_to_delete.left != self.nil: # Find smallest element is right subtree
                     node_to_delete = node_to_delete.left
                cur.key, cur.value = node_to_delete.key,  node_to_delete.value # Copy smallest element's [key, value] to node to delete and delete smallest element
                if cur.right != node_to_delete: # If smallest is node to delete right children
                    node_to_delete.parent.left = self.nil
                    if not node_to_delete.red: # If deleted node was black
                        self.remove_balance(self.nil, node_to_delete.parent) # Balance tree
                else:
                    cur.right = node_to_delete.right
                    cur.right.parent = cur
                    if not node_to_delete.red: # If deleted node was black
                        self.remove_balance(cur.right) # Balance tree

    def find(self, key):

        ''' Find element by key ''' 

        if self.empty(): # If tree is empty
            raise Exception("Map is empty")
        cur = self.root
        while cur != self.nil and cur.key != key: # Find element
            if cur.key > key:
                cur = cur.left
            else:
                cur = cur.right
        if cur == self.nil: # If element is not found return None
            return None
        else: # Return element's value
            return cur.value

    def clear(self):

        ''' Clear tree '''

        while not self.empty(): # Remove tree root while tree is not empty
            self.remove(self.root.key)
    
    def get_keys(self):

        ''' Get keys of tree '''

        keys = []
        if self.empty(): # If tree is empty return empty list
            return keys
        it = DFT_Iterator(self)
        while it.has_next(): # Append all keys to list using dft iterator
            keys.append(next(it).key)
        return keys

    def get_values(self):

        ''' Get values of tree '''

        values = []
        if self.empty(): # If tree is empty return empty list
            return values
        it = DFT_Iterator(self)
        while it.has_next(): # Append all values to list using dft iterator
            values.append(next(it).value)
        return values

    def __str__(self):

        ''' String representation of the tree '''

        result = []
        if self.empty(): # If tree is empty return '[]'
            return str(result)
        it = DFT_Iterator(self)
        while it.has_next(): # Append all [key, value] pairs to list using dft iterator
            node = next(it)
            result.append([node.key, node.value])
        return str(result)

    def __getitem__(self, key):

        ''' Get element's value by key using [] operator '''

        return self.find(key)

    def __setitem__(self, key, value):

        ''' Set element's value by key using [] operator '''

        if self.empty(): # If tree is empty
            raise Exception("Map is empty")
        cur = self.root
        while cur != self.nil and cur.key != key: # Find element
            if cur.key > key:
                cur = cur.left # Go to the left subtree
            else:
                cur = cur.right # Go to the right subtree
        if cur == self.nil: # Is element is not found
            raise Exception(f"Map doesn't have a pair with key={key}")
        else:
            cur.value = value # Set new value to the element

    def empty(self):

        ''' Check if tree is empty '''

        if self.root is None or self.root == self.nil:
            return True
        return False


class DFT_Iterator:

    ''' Iterator for depth-first traversal '''
    
    def __init__(self, tree):
        self.stack = Stack.Stack() # Initialize stack
        self.stack.push(tree.root) # Push root node to the stack
        self.nil = tree.nil

    def __next__(self): 
        if self.has_next():
            temp = self.stack.pop() # Get the top node from the stack
            if temp.right is not None and temp.right != self.nil: # Push right child to the stack if it exists
                self.stack.push(temp.right)
            if temp.left is not None and temp.left != self.nil: # Push left child to the stack if it exists
                self.stack.push(temp.left)
            return temp # Return current node
        else:
            raise StopIteration # If traversal is done

    def has_next(self):
        if self.stack.isEmpty():
            return False
        else:
            return True

"""
File: linkedbst.py
Author: Ken Lambert
"""
from tqdm import tqdm
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
import random
import time

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.word) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.word
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""
        cur_node = self._root
        while True:
            if cur_node is None:
                return None
            elif BSTNode(item).num == cur_node.num:
                return cur_node.word
            elif BSTNode(item).num < cur_node.num:
                return cur_node.left
            else:
                return cur_node.right

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            cur_node = self._root
            while True:
                if BSTNode(item).num < cur_node.num:
                    if cur_node.left == None:
                        cur_node.left = BSTNode(item)
                        break
                    else:
                        cur_node = cur_node.left
                # New item is greater or equal,
                # go right until spot is found
                elif cur_node.right == None:
                    cur_node.right = BSTNode(item)
                    break
                else:
                    cur_node = cur_node.right
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.num = currentNode.num
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.num == BSTNode(item).num:
                itemRemoved = currentNode.num
                break
            parent = currentNode
            if currentNode.num > BSTNode(item).num:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise.
        """
        probe = self._root
        while probe != None:
            if probe.num == BSTNode(item).num:
                oldData = probe.data
                probe.num = BSTNode(item).num
                return oldData
            elif probe.num > BSTNode(item).num:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        return max(i.count('|') for i in str(self).split('\n'))

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < 2 * log(self._size + 1, 2) - 1
        

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high.
        :param low:
        :param high:
        :return:
        '''
        lyst = list()
        result = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node)
                recurse(node.right)

        recurse(self._root)
    
        for value in lyst:
            if BSTNode(low).num <= value.num <= BSTNode(high).num:
                result.append(value.word)
        return result

    def add_center(self, lst):
        """Recursivly ads centers to the tree"""
        if lst:
            if len(lst) == 1:
                self.add(lst[0])
            else:
                lst1, lst2 = lst[:len(lst) // 2], lst[len(lst) // 2 + 1:]
                self.add(lst[len(lst) // 2])

            if len(lst1) == 1:
                self.add(lst1[0])
            else:
                self.add_center(lst1)
            
            if len(lst2) == 1:
                self.add(lst2[0])
            else:
                self.add_center(lst2)
    
    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        elements = sorted([i for i in self])
        self.clear()
        self.add_center(elements)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node)
                recurse(node.right)

        recurse(self._root)
    
        for value in lyst:
            if value.num > BSTNode(item).num:
                return value.word
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.right)
                lyst.append(node)
                recurse(node.left)

        recurse(self._root)
    
        for value in lyst:
            if value.num < BSTNode(item).num:
                return value.word
        return None
        
    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, 'r', encoding='utf-8') as f:
            words = f.read().split('\n')
        
        # 5000 in list, alplabetic order, searching 1000
        #-----------------------------------------------
        search_list = words[:5000]
        to_search = random.sample(search_list, 1000)

        print('\nSearching in alpabetic python list')
        start_time = time.time()
        for i in tqdm(to_search):
            search_list.index(i)
        time_1 = time.time() - start_time 

        # 5000 in tree, alplabetic order, searching 1000
        #-----------------------------------------------
        search_list = words[:5000]
        # print(search_list)
        print('\nBuildingn alphabetic tree, it will take some time, sorry')
        for val in tqdm(search_list):
            self.add(val)

        print('\nSearching in alphabetic tree')
        start_time = time.time()
        for i in tqdm(to_search):
            self.find(i)
        time_2 = time.time() - start_time

        self.clear()

        # 5000 in tree, random order, searching 1000
        #-----------------------------------------------
        random.shuffle(search_list)
        print('\nBuilding random tree')
        for val in tqdm(search_list):
            self.add(val)

        print('\nSearching in random tree')
        start_time = time.time()
        for i in tqdm(to_search):
            self.find(i)
        time_3 = time.time() - start_time

        # 5000 in tree, balanced order, searching 1000
        #-----------------------------------------------
        self.rebalance()
        print('\nSearching in balanced tree')
        start_time = time.time()
        for i in tqdm(to_search):
            self.find(i)
        time_4 = time.time() - start_time

        print('\nConclusion')
        print('-----------')
        print(f'Searching in python alphabetic list = {time_1}')
        print(f'Searching in alphabetic order tree = {time_2}')
        print(f'Searching in random order tree = {time_3}')
        print(f'Searching in balanced order tree = {time_4}')
        print('\nTwo last results are the fastest, second result(alphabetic order tree) \
should be the slowest, and will be if we take more words, and normal list search is just ok.\n')

        return {'list_search': time_1, "alphabetic_tree": time_2, "random_tree": time_3, 'balanced_tree': time_4}

tree = LinkedBST()
tree.demo_bst('binary_trees_speed\words.txt')
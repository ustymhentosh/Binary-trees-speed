"""
File: bstnode.py
Author: Ken Lambert
"""

class BSTNode(object):
    """Represents a node for a linked binary search tree."""

    def __init__(self, word: str, left = None, right = None):
        self.word = word.lower()
        self.num = 0
        mult = 1
        for i in self.word:
            self.num += (ord(i.lower()) - 96) * mult
            mult /= 1000
        self.left = left
        self.right = right

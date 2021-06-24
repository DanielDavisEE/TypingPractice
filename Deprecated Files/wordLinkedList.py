"""
A support module for Typing_practive.py, used for storing the words and frequencies
Author: Daniel Davis
"""
    
class Node:
    '''Node class for linked list
    support class only
    '''
    def __init__(self, word, count):
        self.word = word
        self.count = count
        self.next_node = None
    
        
class linkedList():
    '''Linked list class for back button
    the top item is the current screen in the content framee
    '''
    def __init__(self):
        self.head=None
        
    def append(self, word, count):
        '''add item to list
        '''
        new_screen = Node(word, count)
        new_screen.next_node = self.head
        self.head = new_screen        
    
    def pop(self):
        '''remove item from list
        '''
        if self.head is None:
            raise IndexError('Empty List')
        else:
            item = self.head
            self.head = item.next_node
            return item.word, item.count
    
    def peek(self):
        """return item at the otp of the list
        """
        if self.head is None:
            pass
        else:
            return self.head.value
        
    def return_head(self):
        '''returns self.head'''
        return self.head
               
    def __str__(self):
        """Returns a string representation of the list for the stack starting
        from the beginning of the list. Items are separated by ->
        and ending with -> None
        See doctests in class docstring
        """
        value = self.head
        result = 'List for stack is: '
        while value is not None:
            result += '{}, {} -> '.format(value.word, value.count)
            value = value.next_node
        result += 'None'
        return result
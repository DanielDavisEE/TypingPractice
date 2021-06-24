'''
This is a typing practice game
Author: Daniel Davis

To Do:
-widget placement, formatting and font
-create new wordlist by parsing books to get word frequency
-change get_words() to account for word frequency
-find the range in unicode/utf-8 over which english and korean symbols occur
-implement new game modes
-implement a timer and words/sec calculator
-implement a system for checking words typed against words displayed
-should probably just switch linkedList over to standard python list, it does literally nothing extra
-convert from:
from tkinter import *
from tkinter.ttk import *
to:
import tkinter as tk
import tkinter.ttk as ttk

Future Feature Ideas:
-historical data
-plot wpm over time

Game Mode Ideas:
-Letters only (countdown/timed/no limit)
-Words (countdown/timed/no limit)
'''

import tkinter as tk
import tkinter.ttk as ttk
import random, dictionary_filter

class TypingGame:
    def __init__(self, window, language_dict, language='English'):
        #Defining main window parameters
        window.geometry('900x400')
        window.title("Typing Practice")
        window.update_idletasks()
        self.window = window   
        
        self.language_dict = language_dict
        self.language_options = list(language_dict.keys())
        self.language = language
        self.previous_screens = linkedList()
        
        #Set up the initial content frame
        self.content = ttk.Frame(window)
        self.change_screens(self.home_screen)

        
    def change_screens(self, screen, back_screen=False):
        '''changes the content in the window'''
        #destroy the old content frame
        self.content.destroy()
        
        content = tk.Frame(self.window, bg='Red')
        content.grid(sticky=tk.N+tk.S)
        
        self.content = content
        if not back_screen:
            self.previous_screens.append(screen)
        screen()
        
        self.centre_widget(self.content)
        
        
    def home_screen(self):
        '''the gui for the homescreen'''
        
        title_block = ttk.Label(self.content, text='Typing Practice', font='Helvetica 24 bold')
        title_block.grid(row=0, column=0, columnspan=2, pady=(30,15))
        
        game1_button = ttk.Button(self.content, text='Words', command= lambda: self.change_screens(self.typing_game1))
        game1_button.grid(row=1, column=0, padx=10, pady=10, ipady=10, columnspan='2')
        self.game1_button = game1_button
        
        settings_button = ttk.Button(self.content, text='Settings', command= lambda: self.change_screens(self.settings_screen))
        settings_button.grid(row=2, column=0, padx=10, pady=10, ipady=10)
        self.settings_button = settings_button
        
        exit_button = ttk.Button(self.content, text='Quit', command=window.destroy)
        exit_button.grid(row=2, column=1, padx=10, pady=10, ipady=10)
        self.exit_button = exit_button
        
        self.set_ipadx(self.game1_button, 320)
        self.set_ipadx(self.settings_button, 150)
        self.set_ipadx(self.exit_button, 150)
            
    
    def settings_screen(self):
        '''screen with various options ie language choice'''
        title_block = ttk.Label(self.content, text='Settings', font='Helvetica 24 bold')
        title_block.grid(row=0, column=0, columnspan=2, pady=(30,15))
        #Centre title block within window, provided content frame is the same size as window
        title_block.update_idletasks()
        width = title_block.winfo_width()
        excess = (self.content.winfo_width() - width) / 2
        title_block.grid_configure(padx=excess)
        
        language_choice_label = tk.Label(self.content, font='Helvetica 16', text='Language Options')
        language_choice_label.grid(row=1, column=0)
        
        language_choice = ttk.Combobox(self.content, values=self.language_options)
        language_choice.grid(row=2, column=0, columnspan=2, padx=10, pady=10, ipady=10, ipadx=50)
        language_choice.set(self.language)
        self.language_choice = language_choice
        
        apply_button = ttk.Button(self.content, text='Apply', command=self.apply_settings)
        apply_button.grid(row=3, column=0, padx=10, pady=10, ipady=10)
        self.apply_button = apply_button
        
        apply_and_back_button = ttk.Button(self.content, text='OK', command=lambda: [self.apply_settings(), self.back_screen()])
        apply_and_back_button.grid(row=3, column=1, padx=10, pady=10, ipady=10)
        self.apply_and_back_button = apply_and_back_button
        
        self.set_ipadx(self.language_choice, 320)
        self.set_ipadx(self.apply_button, 150)
        self.set_ipadx(self.apply_and_back_button, 150)
        
        
    def apply_settings(self, back=False):
        '''apply changes to settings'''
        if self.language != self.language_choice.get():
            self.language = self.language_choice.get()

        
    def typing_game1(self):
        '''practice typing words from a word list, no time limit'''
        words = self.get_words()
        
        words_display = tk.Label(self.content, text=words, font='Helvetica 16')
        words_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10, ipady=10)
        words_display.update_idletasks()
        self.words_display = words_display
        
        words_entry = ttk.Entry(self.content, text='')
        words_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10, ipady=10)
        self.words_entry = words_entry
        
        settings_button = ttk.Button(self.content, text='Settings', command= lambda: self.change_screens(self.settings_screen))
        settings_button.grid(row=2, column=0, padx=10, pady=10, ipady=10)
        self.settings_button = settings_button
        
        home_button = ttk.Button(self.content, text='Home', command=self.home_reset)
        home_button.grid(row=2, column=1, padx=10, pady=10, ipady=10)
        self.home_button = home_button

        
        self.set_ipadx(self.words_entry, words_display.winfo_width())
        self.set_ipadx(self.settings_button, 150)
        self.set_ipadx(self.home_button, 150)        
        
        
    def back_screen(self):
        '''destroys current screen, creates previous screen'''
        #Remove current screen from list and check what last screen was
        self.previous_screens.pop()
        new_screen = self.previous_screens.peek()
        
        #Change to previous screen
        self.change_screens(new_screen, True)
            
    def home_reset(self):
        self.previous_screens = linkedList()
        self.change_screens(self.home_screen)
  
  
    def file_to_list(self):
        '''takes a file of line separated words and creates a list'''
        filename = self.language_dict[self.language]
        with open(filename) as infile:
            language_word_list = infile.read().split('\n')
        return language_word_list
            

    def dict_to_linked_list(self, word_freq_dict):
        '''takes a dictionary of words to counts, creates a linked list, and total word count'''
        total = 0
        word_list = linkedList()
        for key in word_freq_dict:
            pass
        return word_list, total

    def get_words(self):
        '''generates a list of words from the main word list of no more than 60chars'''
        language_word_list = self.file_to_list()
        list_length = len(language_word_list)
        test_length = ''
        sub_word_list = []
        
        while True:
            num = random.randint(1, list_length)
            new_word = language_word_list[num]
            if len(new_word) > 10:
                continue
            test_length += new_word
            if len(test_length) > 60:
                break
            sub_word_list.append(new_word)
            
        return sub_word_list
        
        
    def centre_widget(self, widget_name):
        '''takes the name of a widget and centres it horizontally within its master window'''
        widget_name.update_idletasks()
        current_width = widget_name.winfo_width()
        master_width = widget_name.master.winfo_width()
        padx_width = (master_width - current_width) / 2
        widget_name.grid_configure(padx=padx_width)
        
        
    def set_ipadx(self, widget_name, total_width):
        '''sets the ipadx of a variable according to desired width and current width'''
        widget_name.update_idletasks()
        width = widget_name.winfo_width()   
        excess = (total_width - width) / 2
        widget_name.grid_configure(ipadx=excess)            
        
    
class Node:
    '''Node class for linked list
    support class only
    '''
    def __init__(self, screen):
        self.value = screen
        self.next_node = None
    
        
class linkedList():
    '''Linked list class for back button
    the top item is the current screen in the content framee
    '''
    def __init__(self):
        self.head=None
        
    def append(self, screen):
        '''add item to list
        '''
        new_screen = Node(screen)
        new_screen.next_node = self.head
        self.head = new_screen        
    
    def pop(self):
        '''remove item from list
        '''
        if self.is_len_one():
            pass
        else:
            item = self.head
            self.head = item.next_node
    
    def peek(self):
        """return item at the otp of the list
        """
        if self.head is None:
            pass
        else:
            return self.head.value    
    
    def is_len_one(self):
        '''return None if the list has no items
        '''
        return self.head.next_node is None
               
    def __str__(self):
        """Returns a string representation of the list for the stack starting
        from the beginning of the list. Items are separated by ->
        and ending with -> None
        See doctests in class docstring
        """
        value = self.head
        result = 'List for stack is: '
        while value is not None:
            result += '{} -> '.format(value.value)
            value = value.next_node
        result += 'None'
        return result    


if __name__ == '__main__':
    language_dict = {'English': 'Texts\\English\\english_word_list.txt',
                     'Korean': 'korean word list.txt'}
    window = tk.Tk()
    typingGui = TypingGame(window, language_dict)
    window.mainloop()
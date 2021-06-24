'''
This is a typing practice game
Author: Daniel Davis
'''

import tkinter as tk
import tkinter.ttk as ttk
import random

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
        self.previous_screens = []
        
        back_button = ttk.Button(window, text='Back', command=self.back_screen)
        back_button.grid(sticky='NW', padx=10, pady=10)
        
        #Set up the initial content frame
        self.content = ttk.Frame(window)
        self.change_screens(self.home_screen)

#-------------------------------------------------------------------------------
#       Screens
#-------------------------------------------------------------------------------
        
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
        
        language_choice_label = tk.Label(self.content, font='Helvetica 16', text='Language Options:')
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
        
    
    def results_screen(self, game_type, time_limit=False):
        '''displays result after a round of an activity'''

        title_block = ttk.Label(self.content, text='Results', font='Helvetica 24 bold')
        title_block.grid(row=0, column=0, columnspan=2, pady=(30,15))        
        
        #Words typed
        words_typed_label = ttk.Label(self.content, text='Number of Words Typed:', font='Helvetica 14')
        words_typed_label.grid(row=1, column=0, columnspan=1, padx=10, pady=10, ipady=10)
        
        words_typed = ttk.Label(self.content, text=self.word_count, font='Helvetica 14')
        words_typed.grid(row=1, column=1, columnspan=1, padx=10, pady=10, ipady=10)
        
        #% Accuracy
        word_accuracy_label = ttk.Label(self.content, text='Typing Accuracy:', font='Helvetica 14')
        word_accuracy_label.grid(row=2, column=0, columnspan=1, padx=10, pady=10, ipady=10)
        
        if self.word_count_correct == 0:
            word_accuracy_text = '0.0%'
        else:
            word_accuracy_text = '{:.1f}%'.format((self.word_count_correct/self.word_count)*100)
        
        word_accuracy = ttk.Label(self.content, text=word_accuracy_text, font='Helvetica 14')
        word_accuracy.grid(row=2, column=1, columnspan=1, padx=10, pady=10, ipady=10)
        #WPM
        
        #Time typed for (if not an activity with a time limit)
        replay_button = ttk.Button(self.content, text='Replay', command= lambda: self.change_screens(self.previous_screens[-2]))
        replay_button.grid(row=3, column=0, padx=10, pady=10, ipady=10, sticky='E')
        self.replay_button = replay_button
        
        home_button = ttk.Button(self.content, text='Home', command=self.home_reset)
        home_button.grid(row=3, column=1, padx=10, pady=10, ipady=10, sticky='W')
        self.home_button = home_button        

        self.set_ipadx(self.replay_button, 150)
        self.set_ipadx(self.home_button, 150)   
        
 
    def typing_game1(self):
        '''practice typing words from a word list, no time limit'''

        language_word_list, total = self.file_to_list()
        self.language_list_info = (language_word_list, total)        
        
        words = self.get_words()
        self.words = words
        self.word_count_correct = 0
        self.word_count = 0
        
        words_display = tk.Frame(self.content)
        words_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10, ipady=10)
        words_display.update_idletasks()
        self.words_display = words_display
        
        word_to_type = tk.Label(self.words_display, text= words[0], font='Helvetica 17')
        word_to_type.pack(side=tk.LEFT)
        word_to_type.update_idletasks()
        self.word_to_type = word_to_type
        
        next_words = tk.Label(self.words_display, text=words[1:], font='Helvetica 13')
        next_words.pack(side=tk.LEFT)
        next_words.update_idletasks()
        self.next_words = next_words
        
        words_entry = tk.Entry(self.content, text='', font='Helvetica 17')
        words_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10, ipady=10)
        words_entry.bind("<space>", lambda e: self.submit(words))
        self.words_entry = words_entry
        
        settings_button = ttk.Button(self.content, text='Settings', command= lambda: self.change_screens(self.settings_screen))
        settings_button.grid(row=2, column=0, padx=10, pady=10, ipady=10, sticky='E')
        self.settings_button = settings_button
        
        home_button = ttk.Button(self.content, text='Home', command=self.home_reset)
        home_button.grid(row=2, column=1, padx=10, pady=10, ipady=10, sticky='W')
        self.home_button = home_button

        self.set_ipadx(self.words_entry, 320)
        self.set_ipadx(self.settings_button, 150)
        self.set_ipadx(self.home_button, 150)
        
                    
#-------------------------------------------------------------------------------
#       Screen Manipulation
#-------------------------------------------------------------------------------
        

    def change_screens(self, screen, back_screen=False):
        '''changes the content in the window'''
        #destroy the old content frame
        self.content.destroy()
        
        content = tk.Frame(self.window)
        content.grid(sticky=tk.N+tk.S)
        
        self.content = content
        if not back_screen:
            self.previous_screens.append(screen)
        screen()
        
        self.centre_widget(self.content)
    
        
    def back_screen(self):
        '''destroys current screen, creates previous screen'''
        try:
            #Remove current screen from list and check what last screen was
            self.previous_screens.pop()
            new_screen = self.previous_screens[-1]
            
            #Change to previous screen
            self.change_screens(new_screen, True)
        except IndexError:
            pass
            
            
    def home_reset(self):
        self.previous_screens = []
        self.change_screens(self.home_screen)

            
#-------------------------------------------------------------------------------
#       Word Functions
#-------------------------------------------------------------------------------  


    def file_to_list(self):
        '''takes a file of line separated words and creates a list'''
        filename = self.language_dict[self.language]
        word_freq_list = []
        
        with open(filename, 'r', encoding='utf-8-sig') as infile:
            language_word_list = infile.read().split('\n')
        language_word_list.pop()
        total = 0
        for item in language_word_list:
            item = item.split(',')
            total += int(item[1])
            word_freq_list.append((item[0], int(item[1]))) 
        return word_freq_list, total  


    def get_single_word(self):
        '''return a random single word from a word list'''
        language_word_list, total = self.language_list_info[0], self.language_list_info[1]       
        num = random.randint(1, total)
        running_total = 0
        current_word = 0
        while True:
            running_total += language_word_list[current_word][1]
            if running_total >= num:
                new_word = language_word_list[current_word][0]
                break
            current_word += 1
        return new_word

    def get_words(self, sub_word_list = []):
        '''generates a list of words from the main word list of no more than 50chars and 10 words'''
        test_length = ''.join(sub_word_list)
        
        while len(sub_word_list) < 10:
            
            new_word = self.get_single_word()
                
            if len(new_word) > 10 or len(new_word) == 1:
                continue
            
            test_length += new_word
            if len(test_length) > 50:
                break
            sub_word_list.append(new_word)
            
        return sub_word_list
        

#-------------------------------------------------------------------------------
#       Widget Formatting
#-------------------------------------------------------------------------------      
    
    
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
        

#-------------------------------------------------------------------------------
#       Misc
#-------------------------------------------------------------------------------    

    def submit(self, word_list):
        ''''''
        word_displayed = self.word_to_type['text']
        word_typed = self.words_entry.get()
        
        if word_displayed == word_typed:
            self.word_count_correct += 1
        self.word_count += 1
        word_list.pop(0)
        word_list = self.get_words(word_list)
        
        self.word_to_type['text'] = word_list[0]
        self.next_words['text'] = word_list[1:]
        self.words_entry.delete(0, 'end')
        return 'break'
        
    
    def apply_settings(self, back=False):
        '''Settings Screen Support Function
        apply changes to settings'''
        if self.language != self.language_choice.get():
            self.language = self.language_choice.get()

#-------------------------------------------------------------------------------
#       Deprecated Functions
#-------------------------------------------------------------------------------   

    def dict_to_linked_list(self, word_freq_dict):
        '''takes a dictionary of words to counts, creates a linked list, and total word count. Isn't currently useable, replaced by file_to_linked_list since 
        recreating the list over and over took way too long.'''
        total = 0
        word_list = wordLinkedList.linkedList()
        for key in word_freq_dict:
            total += word_freq_dict[key]
            word_list.append(key, word_freq_dict[key])
        return word_list, total  


    def file_to_linked_list(self):
        '''takes a file of line separated words and creates a linked list
        deprecated
        '''
        filename = self.language_dict[self.language]
        word_freq_dict = {}
        with open(filename) as infile:
            language_word_list = infile.read().split('\n')
        for item in language_word_list:
            item_list = item.split(',')
            word_freq_dict[item_list[0]] = int(item_list[1])
            
        total = 0
        word_list = wordLinkedList.linkedList()
        for key in word_freq_dict:
            total += word_freq_dict[key]
            word_list.append(key, word_freq_dict[key])
        return word_list, total
            

if __name__ == '__main__':
    language_dict = {'English': 'D:\Daniel Davis\Documents\Coding\Python\Typing Project\\english_word_frequency_counts.txt',
                     'Korean': 'korean word list.txt'}
    window = tk.Tk()
    typingGui = TypingGame(window, language_dict)
    window.mainloop()
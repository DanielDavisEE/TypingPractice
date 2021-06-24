'''
This is a typing practice game
Author: Daniel Davis

New Screen Format:

def X_screen(self):
        #Create Frame to contain everything which will be displayed
        self.X_frame = tk.Frame(self.window, name='X_frame')
        self.X_frame.pack(fill=tk.BOTH, expand=1)
        
        self.add_to_screen_dict(self.home_screen)
        #Create the 'back' and 'home' buttons
        self.window_buttons(self.X_frame)
        #Create a Frame for the main content
        self.content = tk.Frame(self.X_frame)
        self.content.grid(row=0, column=0)
        
        #Add frame content here
        #Remember to change the X_screen and X_frame to more appropriate names
        #Ditto if using the example widgets below
        
        #This must go after all other child widgets have been created and formatted
        self.centre_widget(self.content)
        
Some Potential Content:
z
**Title Block**
title_block = ttk.Label(self.content, text='Title_Text', font='Helvetica 24 bold')
title_block.grid(row=0, column=0, columnspan=2, pady=(30,15))

**Double Column Width Button**
double_col_button = ttk.Button(self.content, text='Button_Text', command=self.command)
double_col_button.grid(row=0, column=0, padx=10, pady=10, ipady=10, columnspan='2')
self.double_col_button = double_col_button

self.set_ipadx(self.double_col_button, 320)

**Single Column Width Button**
single_col_button = ttk.Button(self.content, text='Button_Text', command=self.command)
single_col_button.grid(row=0, column=0, padx=10, pady=10, ipady=10)
self.single_col_button = single_col_button

self.set_ipadx(self.single_col_button, 150)
    

'''

import tkinter as tk
import tkinter.ttk as ttk
import random, time

class TypingGame:
    
    def __init__(self, window, language_dict, language='English'):
        #Defining main window parameters
        window.geometry('900x400')
        window.title("Typing Practice")
        window.update_idletasks()
        self.window = window   
        
        background_colour = '#f0f0f0'
        window.tk_setPalette(background=background_colour) 
        window.bind("<Tab>", lambda e: 'break')
        
        #Defining Class variables
        self.language_dict = language_dict
        self.language_options = list(language_dict.keys())
        self.language = language
        self.previous_screens = []
        self.screen_dict = {}
        self.timer_isRunning = False
        self.time_elapsed = 0
        
        #Creates the word list for the default language
        language_word_list, total = self.file_to_list()
        self.language_list_info = (language_word_list, total)

        language_alphabet, total = self.file_to_list_letters()
        self.language_alphabet_info = (language_alphabet, total)
        
        self.type_dict = {'words_no_time': ['words', False],
                     'words_countdown': ['words', True, 60, '{:.2f}'],
                     'words_timed': ['words', True, 0,'{:.1f}'],
                     'letters_no_time': ['alphabet', False],
                     'letters_countdown': ['alphabet', True, 60, '{:.2f}'],
                     'letters_timed': ['alphabet', True, 0, '{:.1f}']}        
        
        #Create the first screen
        self.home_screen()

#-------------------------------------------------------------------------------
#       Screens
#-------------------------------------------------------------------------------
        
    def home_screen(self):
        '''the gui for the homescreen'''
        #Create Frame to contain everything which will be displayed
        self.home_frame = tk.Frame(self.window, name='home_frame')
        self.home_frame.pack(fill=tk.BOTH, expand=1)
        
        self.add_to_screen_dict(self.home_screen)
        #Create the 'back' and 'home' buttons
        self.window_buttons(self.home_frame)
        #Create a Frame for the main content
        self.content = tk.Frame(self.home_frame)
        self.content.grid(row=0, column=0)
        
        #Frame Content
        title_block = ttk.Label(self.content, text='Home', font='Helvetica 24 bold')
        title_block.grid(row=0, column=0, columnspan=2, pady=(30,15))
        
        game1_button = ttk.Button(self.content, text='Words', command= lambda: self.change_screens(self.game_select))
        game1_button.grid(row=1, column=0, padx=10, pady=10, ipady=10, columnspan='2')
        self.game1_button = game1_button
        
        game2_button = ttk.Button(self.content, text='Letters', command= lambda: self.change_screens(lambda: self.game_select(True)))
        game2_button.grid(row=2, column=0, padx=10, pady=10, ipady=10, columnspan='2')
        self.game2_button = game2_button        
        
        settings_button = ttk.Button(self.content, text='Settings', command= lambda: self.change_screens(self.settings_screen))
        settings_button.grid(row=3, column=0, padx=10, pady=10, ipady=10)
        self.settings_button = settings_button
        
        exit_button = ttk.Button(self.content, text='Quit', command=window.destroy)
        exit_button.grid(row=3, column=1, padx=10, pady=10, ipady=10)
        self.exit_button = exit_button
        
        #Correct the sizing/spacing of widgets
        self.set_ipadx(self.game1_button, 320)
        self.set_ipadx(self.game2_button, 320)
        self.set_ipadx(self.settings_button, 150)
        self.set_ipadx(self.exit_button, 150)
        self.centre_widget(self.content)
        
        
    def game_select(self, letters=False):
        '''the gui for the homescreen'''
        #Create Frame to contain everything which will be displayed
        self.game_select_frame = tk.Frame(self.window, name='game_select_frame')
        self.game_select_frame.pack(fill=tk.BOTH, expand=1)
        
        self.add_to_screen_dict(self.game_select)
        #Create the 'back' and 'home' buttons
        self.window_buttons(self.game_select_frame)
        #Create a Frame for the main content
        self.content = tk.Frame(self.game_select_frame)
        self.content.grid(row=0, column=0)
        
        game_dict = {'Word': [lambda: self.typing_game('words_countdown'),
                              lambda: self.typing_game('words_timed'),
                              lambda: self.typing_game('words_no_time')],
                     'Letter': [lambda: self.typing_game('letters_countdown'),
                                lambda: self.typing_game('letters_timed'),
                                lambda: self.typing_game('letters_no_time')]}
        #Frame Content
        game_mode = 'Word'
        if letters:
            game_mode = 'Letter'
        
        title_block = ttk.Label(self.content, text='{} Typing Practice'.format(game_mode), font='Helvetica 24 bold')
        title_block.grid(row=0, column=0, columnspan=2, pady=(30,15))
        
        game1_button = ttk.Button(self.content, text='Countdown', command= lambda: self.change_screens(game_dict[game_mode][0]))
        game1_button.grid(row=1, column=0, padx=10, pady=10, ipady=10, columnspan='2')
        self.game1_button = game1_button
        
        game2_button = ttk.Button(self.content, text='Timed', command= lambda: self.change_screens(game_dict[game_mode][1]))
        game2_button.grid(row=2, column=0, padx=10, pady=10, ipady=10, columnspan='2')
        self.game2_button = game2_button
        
        game3_button = ttk.Button(self.content, text='Free Write', command= lambda: self.change_screens(game_dict[game_mode][2]))
        game3_button.grid(row=3, column=0, padx=10, pady=10, ipady=10, columnspan='2')
        self.game3_button = game3_button        
        
        settings_button = ttk.Button(self.content, text='Settings', command= lambda: self.change_screens(self.settings_screen))
        settings_button.grid(row=4, column=0, padx=10, pady=10, ipady=10)
        self.settings_button = settings_button
        
        home_button = ttk.Button(self.content, text='Home', command=self.home_reset)
        home_button.grid(row=4, column=1, padx=10, pady=10, ipady=10, sticky='W')
        self.home_button = home_button   
        
        #Correct the sizing/spacing of widgets
        self.set_ipadx(self.game1_button, 320)
        self.set_ipadx(self.game2_button, 320)
        self.set_ipadx(self.game3_button, 320)
        self.set_ipadx(self.settings_button, 150)
        self.set_ipadx(self.home_button, 150)
        self.centre_widget(self.content)        
        
    
    def settings_screen(self):
        '''screen with various options ie language choice'''
        #Create Frame to contain everything which will be displayed
        self.settings_frame = tk.Frame(self.window, name='settings_frame')
        self.settings_frame.pack(fill=tk.BOTH, expand=1)

        self.add_to_screen_dict(self.settings_screen)        
        
        #Create the 'back' and 'home' buttons
        self.window_buttons(self.settings_frame)
        #Create a Frame for the main content
        self.content = tk.Frame(self.settings_frame)
        self.content.grid(sticky='ns', row=0, column=0)        
        
        #Frame Content
        title_block = ttk.Label(self.content, text='Settings', font='Helvetica 24 bold')
        title_block.grid(row=0, column=0, columnspan=2, pady=(30,15))
        
        language_choice_label = tk.Label(self.content, font='Helvetica 14', text='Language Options:')
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
        
        #Correct the sizing/spacing of widgets
        self.set_ipadx(self.language_choice, 320)
        self.set_ipadx(self.apply_button, 150)
        self.set_ipadx(self.apply_and_back_button, 150)
        self.centre_widget(self.content)

        
    def typing_game(self, game_type):
        '''practice typing letters from a word list, no time limit
        '''
        game_item_list = self.type_dict[game_type]
                
        words = self.get_items([], game_item_list[0])
        self.words = words
        self.word_count_correct = 0
        self.word_count = 0
        
        if game_item_list[0] == 'words':
            next_words_list = words[1:]
            submit_function = self.submit_word
            submit_key = '<space>'
            words_entry_exists = True
        elif game_item_list[0] == 'alphabet':
            next_words_list = ' '+'   '.join(words[1:])
            submit_function = self.submit_letter
            submit_key = '<Key>'
            words_entry_exists = False
            
        #Create Frame to contain everything which will be displayed
        game_frame = tk.Frame(self.window, name=game_type)
        game_frame.pack(fill=tk.BOTH, expand=1)
        
        self.add_to_screen_dict(lambda: self.typing_game(game_type))
        #Create the 'back' and 'home' buttons
        self.window_buttons(game_frame)
        #Create a Frame for the main content
        self.content = tk.Frame(game_frame)
        self.content.grid(row=0, column=0)    

        self.content.bind("<Return>", lambda e: self.change_screens(self.results_screen), add="+")
      
        #Frame Content
        words_display = tk.Frame(self.content)
        words_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10, ipady=10)
        words_display.update_idletasks()
        self.words_display = words_display
        
        word_to_type = tk.Label(self.words_display, text= words[0], font='Helvetica 18')
        word_to_type.pack(side=tk.LEFT)
        word_to_type.update_idletasks()
        self.word_to_type = word_to_type
        
        next_words = tk.Label(self.words_display, text=next_words_list, font='Helvetica 13')
        next_words.pack(side=tk.LEFT)
        next_words.update_idletasks()
        self.next_words = next_words
        
        if words_entry_exists:
            words_entry = tk.Entry(self.content, text='', font='Helvetica 17')
            words_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10, ipady=10)
            words_entry.bind(submit_key, submit_function, add="+")
            words_entry.bind("<Return>", lambda e: self.change_screens(self.results_screen), add="+")
            words_entry.focus()
            self.words_entry = words_entry
            self.set_ipadx(self.words_entry, 320)
        else:
            self.words_display.focus()
            self.words_display.bind(submit_key, submit_function, add="+")
        
        settings_button = ttk.Button(self.content, text='Settings', command=lambda: self.change_screens(self.settings_screen))
        settings_button.grid(row=2, column=0, padx=10, pady=10, ipady=10, sticky='E')
        self.settings_button = settings_button
        
        results_button = ttk.Button(self.content, text='Done', command=lambda: self.change_screens(self.results_screen))
        results_button.grid(row=2, column=1, padx=10, pady=10, ipady=10, sticky='W')
        self.results_button = results_button
        
        if game_item_list[1]:
            time_display = ttk.Label(self.content, text='', font='Helvetica 20 bold')
            time_display.grid(row=4, column=0, columnspan=2, pady=(30,15))
            time_display['text'] = game_item_list[3].format(game_item_list[2])
            self.time_display = time_display
            if words_entry_exists:
                words_entry.bind("<Key>", lambda e: self.run_timer(game_item_list[2]), add="+")
            self.content.bind("<Key>", lambda e: self.run_timer(game_item_list[2]), add="+")

        self.set_ipadx(self.settings_button, 150)
        self.set_ipadx(self.results_button, 150)
        self.centre_widget(self.content)      
        
    
    def results_screen(self):
        '''displays result after a round of an activity'''
        #Create Frame to contain everything which will be displayed
        self.results_frame = tk.Frame(self.window, name='results_frame')
        self.results_frame.pack(fill=tk.BOTH, expand=1)
        
        self.add_to_screen_dict(self.results_screen)
        #Create the 'back' and 'home' buttons
        self.window_buttons(self.results_frame)
        #Create a Frame for the main content
        self.content = tk.Frame(self.results_frame)
        self.content.grid(row=0, column=0)               
        
        #Frame Content
        title_block = ttk.Label(self.content, text='Results', font='Helvetica 24 bold')
        title_block.grid(row=0, column=0, columnspan=2, pady=(30,15))        
        
        #Words typed
        game = self.window.winfo_atomname(self.previous_screens[-1])
        
        label_text = 'Words'
        if self.type_dict[game[1:]][0] == 'alphabet':
            label_text = 'Letters'
        words_typed_label = ttk.Label(self.content, text='Number of {} Typed:'.format(label_text), font='Helvetica 14')
        words_typed_label.grid(row=1, column=0, columnspan=1, padx=10, pady=10, ipady=10)
        
        words_typed = ttk.Label(self.content, text='{} of {}'.format(self.word_count_correct, self.word_count), font='Helvetica 14')
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
        if self.type_dict[game[1:]][1]:
            wpm_label = ttk.Label(self.content, text='{} per Minute:'.format(label_text), font='Helvetica 14')
            wpm_label.grid(row=3, column=0, columnspan=1, padx=10, pady=10, ipady=10)
            
            wpm = ttk.Label(self.content, text='{:.1f}'.format(self.word_count_correct / self.time_elapsed * 60), font='Helvetica 14')
            wpm.grid(row=3, column=1, columnspan=1, padx=10, pady=10, ipady=10)            
        
        
        #Time typed for (if not an activity with a time limit)
        replay_button = ttk.Button(self.content, text='Replay', command= lambda: self.back_screen())
        replay_button.grid(row=4, column=0, padx=10, pady=10, ipady=10, sticky='E')
        self.replay_button = replay_button
        
        home_button = ttk.Button(self.content, text='Home', command=self.home_reset)
        home_button.grid(row=4, column=1, padx=10, pady=10, ipady=10, sticky='W')
        self.home_button = home_button        

        self.set_ipadx(self.replay_button, 150)
        self.set_ipadx(self.home_button, 150)   
        self.centre_widget(self.content)     
                                 
#-------------------------------------------------------------------------------
#       Screen Manipulation
#-------------------------------------------------------------------------------
        
    def change_screens(self, screen, back_screen=False):
        '''changes the content in the window'''        
        #Get name of previous Frame from the children of the window
        widget_name = list(self.window.children.values())[0]        
        previous_screen = self.window.winfo_atom(widget_name)
        
        widget_name.destroy()
        
        self.timer_isRunning = False
        
        if not back_screen:
            self.previous_screens.append(previous_screen)
        screen()
    
    def window_buttons(self, screen):
        '''creates the home and back buttons'''
        window_buttons = ttk.Frame(screen)
        window_buttons.grid(sticky='NE')
        
        back_button = ttk.Button(window_buttons, text='Back', command=self.back_screen)
        back_button.pack(padx=10, pady=10)
        
        home_button = ttk.Button(window_buttons, text='Home', command=self.home_reset)
        home_button.pack(padx=10)        
        
        
    def back_screen(self):
        '''destroys current screen, creates previous screen'''
        try:
            #Get the function of the previous screen using its id
            screen = self.screen_dict[self.previous_screens.pop()]
            
            #Change to previous screen
            self.change_screens(screen, True)
        except IndexError:
            #This covers the case that the back button is pressed on the home screen,
            #since the self.previous_screens is empty
            pass
            
            
    def home_reset(self):
        ''''''
        self.change_screens(self.home_screen)
        self.previous_screens = []
        
    
    def add_to_screen_dict(self, screen_func):
        '''adds the screen to screen_dict if not already in it'''
        if screen_func not in self.screen_dict.values():
            widget_name = list(self.window.children.values())[0]
            self.screen_dict[self.window.winfo_atom(widget_name)] = screen_func
                 
#-------------------------------------------------------------------------------
#       Word Functions
#-------------------------------------------------------------------------------  

    def file_to_list(self):
        '''takes a file of line separated words and creates a list'''
        filename = self.language_dict[self.language][0]
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
        
        
    def file_to_list_letters(self):
        filename = self.language_dict[self.language][1]
        word_freq_list = []
        
        with open(filename, 'r', encoding='utf-8-sig') as infile:
            letter_list = infile.read().split('\n')
        letter_list.pop()
        return letter_list, len(letter_list)


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

    
    def get_single_letter(self):
        '''return a random single word from a word list'''
        language_alphabet, total = self.language_alphabet_info[0], self.language_alphabet_info[1]       
        num = random.randint(1, total - 1)
        new_letter = language_alphabet[num]
        return new_letter
    

    def get_items(self, sub_item_list, game_type):
        '''generates a list of words from the main word list of no more than 50chars and 10 words'''
        game_type_dict = {'words': self.get_single_word,
                          'alphabet': self.get_single_letter}
        test_length = ''.join(sub_item_list)
        
        while len(sub_item_list) < 10:
            
            new_item = game_type_dict[game_type]()
                
            if len(sub_item_list) > 0:
                if len(new_item) > 10 or new_item == sub_item_list[-1]:
                    continue            
            
            test_length += new_item
            if len(test_length) > 50:
                break
            sub_item_list.append(new_item)
            
        return sub_item_list


    def get_words(self, sub_word_list, _):
        '''generates a list of words from the main word list of no more than 50chars and 10 words'''
        test_length = ''.join(sub_word_list)
        
        while len(sub_word_list) < 10:
            
            new_word = self.get_single_word()
                
            if len(new_word) > 10:
                continue
            
            test_length += new_word
            if len(test_length) > 50:
                break
            sub_word_list.append(new_word)
            
        return sub_word_list
     

    def get_letters(self, sub_letter_list, _):
        '''generates a list of words from the main word list of no more than 50chars and 10 words'''
        while len(sub_letter_list) < 10:
            
            new_letter = self.get_single_letter()
            
            if len(sub_letter_list) > 0:
                if new_letter == sub_letter_list[-1]:
                    continue

            sub_letter_list.append(new_letter)
            
        return sub_letter_list   

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
    
    def submit_word(self, _):
        ''''''
        word_list = self.words
        word_displayed = self.word_to_type['text']
        word_typed = self.words_entry.get()
        
        if word_typed == '':
            return 'break'            
        
        if word_displayed == word_typed:
            self.word_count_correct += 1
            self.flash_set('#00bb00', self.words_entry)
        else:
            self.flash_set('#dd0000', self.words_entry)
        self.word_count += 1
        word_list.pop(0)
        word_list = self.get_words(word_list, '')
        
        self.word_to_type['text'] = word_list[0]
        self.next_words['text'] = word_list[1:]
        self.words_entry.delete(0, 'end')

        self.centre_widget(self.content)        
        return 'break'
    
    
    def submit_letter(self, event_info):
        ''''''
        letter_list = self.words
        letter_displayed = self.word_to_type['text']
        letter_typed = event_info.char

        if letter_typed == '':
            return 'break'
        
        if letter_displayed == letter_typed:
            self.word_count_correct += 1
            self.flash_set('#00bb00', self.words_display)
        else:
            self.flash_set('#dd0000', self.words_display)
        self.word_count += 1
        letter_list.pop(0)
        letter_list = self.get_letters(letter_list, '')
        
        self.word_to_type['text'] = letter_list[0]
        self.next_words['text'] = ' '+'   '.join(letter_list[1:])
        
        self.centre_widget(self.content)
        
    
    def apply_settings(self, back=False):
        '''Settings Screen Support Function
        apply changes to settings'''
        if self.language != self.language_choice.get():
            self.language = self.language_choice.get()
            
            language_word_list, total = self.file_to_list()
            self.language_list_info = (language_word_list, total)
    
            language_alphabet, total = self.file_to_list_letters()
            self.language_alphabet_info = (language_alphabet, total)      
            
    
    def run_timer(self, input_time):
        '''calls the resursive function update_timer as long as the timer is not already running'''
        if not self.timer_isRunning:
            self.timer_isRunning = True
            self.start_time = time.time()
            self.update_timer(input_time)

                
    def update_timer(self, input_time):
        '''recursively updates the timer'''
        self.time_elapsed = time.time() - self.start_time
        time_to_display = input_time - self.time_elapsed
        options_dict = {60: ['{:.2f}', time_to_display],
                        0: ['{:.1f}', self.time_elapsed]}
        self.time_display['text'] = options_dict[input_time][0].format(options_dict[input_time][1])
        self.time_display.update_idletasks()
        if float(self.time_display['text']) >= 0:
            self.time_display.after(10, lambda: self.update_timer(input_time))
        else:
            self.time_display['text'] = '0.00'
            game = list(self.window.children.values())[0]
            if self.type_dict[str(game)[1:]][0] == 'words':
                self.words_entry.delete(0, 'end')
                self.words_entry.configure(state=tk.DISABLED)
            self.content.focus()
            
            
    def flash_set(self, colour, item):
        background_colour = '#f0f0f0' #item.cget('background')
        bg_colour = [int(background_colour[1:3], 16),
                     int(background_colour[3:5], 16),
                     int(background_colour[5:7], 16)]
        rgb = [int(colour[1:3], 16),
               int(colour[3:5], 16),
               int(colour[5:7], 16)]
        self.flash(rgb, bg_colour, item)
        item.configure(bg=background_colour)
        item.update_idletasks()
        for widget in item.children.values():
            widget.configure(bg=background_colour)
            widget.update_idletasks()           
        
    
    def flash(self, rgb, bg_colour, item):
    
        for i in range(len(rgb)):
            num = rgb[i]
            diff = num - bg_colour[i]
            if diff < 0:
                rgb[i] =  int(format(num - (diff // 10), 'x'), 16)
        colour = ('#' + 
            '{:0>2}'.format(format(rgb[0], 'x')) +
            '{:0>2}'.format(format(rgb[1], 'x')) +
            '{:0>2}'.format(format(rgb[2], 'x'))
            )
        
        item.configure(bg=colour)
        item.update_idletasks()
        for widget in item.children.values():
            widget.configure(bg=colour)
            widget.update_idletasks()            
        loop = False
        for i in range(len(rgb)):
            if rgb[i] != bg_colour[i]:
                loop = True
                break
        if loop:
            self.window.after(15, lambda: self.flash(rgb, bg_colour, item))

#-------------------------------------------------------------------------------
#       Deprecated Functions
#-------------------------------------------------------------------------------   
        
    def grid_full_size(self, widget_name):
        '''takes the name of a widget and centres it horizontally within its master window
        Deprecated as not in current use'''
        widget_name.update_idletasks()
        
        current_width = 0#widget_name.winfo_width()
        master_width = widget_name.master.winfo_width()
        ipadx_width = (master_width - current_width) / 2
        
        current_height = 0#widget_name.winfo_height()
        master_height = widget_name.master.winfo_width()
        ipady_height = (master_height - current_height) / 2
        
        widget_name.grid_configure(ipadx=ipadx_width, ipady=ipady_height)


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
    language_dict = {'English': ['english_word_frequency_counts.txt', 'english_alphabet.txt'],
                     'Korean': ['korean word list.txt', 'korean_alphabet.txt']}
    window = tk.Tk()
    typingGui = TypingGame(window, language_dict)
    window.mainloop()
import re, os

def word_frequency_dict_per_file(filename, word_count_dict={}):
    '''parse a file and return a frequency dictionary of words using latin characters.
    '''
    delimiters = [", ", "; ", ". ", ": "," ", "(", ")", "/", "\n", "-"]
    regexPattern = r'[^a-zA-Z0-9\']+'#'|'.join(map(re.escape, delimiters))
    
    with open(filename, encoding='utf8') as infile:
        words = re.split(regexPattern, infile.read())
        words_list = [x.lower() for x in words if x.isalpha()]
    for word in words_list:
        word_count_dict[word] = word_count_dict.get(word, 0) + 1
    return word_count_dict


def word_frequency_dict():
    '''return a frequency dictionary of words in files in a folder
    '''
    word_dict = {}
    word_list = []
    for file in os.listdir('Texts\English'):
        print('Texts\English\\'+file)
        word_dict = word_frequency_dict_per_file('Texts\English\\'+file, word_dict)
    key_list = list(word_dict.keys())
    for key in key_list:
        word_list.append((word_dict[key], key))
    with open('D:\Daniel Davis\Documents\Coding\Python\Typing Project\\english_word_frequency_counts.txt', 'w', encoding='utf-8-sig') as file:
        for count, word in reversed(sorted(word_list)):
            file.write('{},{}\n'.format(word, count))

if __name__ == '__main__':
    word_frequency_dict()


'''
Some Random testing shit for the word dict


top_10 = [''] * 10
bottom_list = []
one_letters = []
longest_word = ''
for key in word_dict:
    for i in range(10):
        if word_dict.get(top_10[i], 0) < word_dict[key]:
            top_10[i] = key
            break
    if word_dict[key] <= 2:
        bottom_list.append(key)
    if len(key) == 1:
        one_letters.append((key, word_dict[key]))
    if len(key) > len(longest_word):
        longest_word = key
    
[print(top_10[i], word_dict[top_10[i]]) for i in range(10)]
print('Number of words with 2 or less occurances:', len(bottom_list))
[print(i[0], i[1]) for i in one_letters]
print(sum(word_dict.values()))
print(longest_word)
'''
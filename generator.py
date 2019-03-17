import re
import random

def count_entry(word, dictionary):
    '''Подсчитывает количество вхождений слова word в словарь dictionary'''

    if word in dictionary:
        dictionary[word] += 1
    else:
        dictionary[word] = 1
    return dictionary    

def make_markov(order, data):
    '''Создаёт структуру для цепи Маркова,
    order - порядок цепи Маркова, 
    data - массив входных слов'''

    markov_model = dict()
    
    for i in range(0, len(data)-order):
        window = tuple(data[i:i+order])
        #window - "окно" значений в звене цепи Маркова
        word = data[i + order]
        #word - слово, для которого будет подсчитана частота использования с данным "окном"

        if window not in markov_model:
            markov_model[window] = dict()
        count_entry(word, markov_model[window])
    return markov_model

def get_word(markov_model, window):
    '''Получает следующее слово для предложения'''
    
    dic = markov_model[window]
    count = len(dic)
    list_of_keys = dic.keys()
    index = 0
    summ = 0
    for key in list_of_keys: 
        summ += int(dic[key]) 

    random_int = random.randint(0, summ-1)

    for i in list_of_keys:
        index += dic[i]
        if (index > random_int):
            return i 


def gen_lines(filename):
    '''Считывает построчно файл и перекодирует строки в utf-8'''

    data = open(filename)
    for line in data:
        yield line.lower()

def gen_tokens(lines):
    '''Делит строку на последовательность слов и символов'''

    r_alphabet = re.compile(u'[а-яА-Я0-9-]+|[.,:;?!]+')
    for line in lines:
        for token in r_alphabet.findall(line):
            yield token

def generate_markov(markov_model, order, window, number_of_words=100):
    '''Генератор предложений на основании цепи Маркова ранга order
    number_of_words - количество сгенерированных слов 
    window - первое окно для генерации'''

    if order == 1:
        phrase = window[0].title()
    elif order == 2:
        phrase = window[0].title() + ' ' + window[1]
    elif order == 3:
        phrase = window[0].title() + ' ' + window[1] + ' ' + window[2]
    elif order == 4:
        phrase = window[0].title() + ' ' + window[1] + ' ' + window[2] + ' ' + window[3]
    count = 0
    big = False
    
    while True:
        new_word = get_word(markov_model, window)
        if new_word in '.!?':
            big = True
            phrase = phrase + new_word
        elif new_word in ',:;-':
            phrase = phrase + new_word
        else:
            if big:
                phrase = phrase + ' ' + new_word.title()
                big = False
            else:
                phrase = phrase + ' ' + new_word 
        if count > number_of_words:
            phrase +='.'
            return phrase
        if order == 1:
            new_window = new_word,
        elif order == 2:
            new_window = window[1], new_word 
        elif order == 3:
            new_window = window[1], window[2], new_word
        elif order == 4:
            new_window = window[1], window[2], window[3], new_word
        window = new_window
        count += 1

lines = gen_lines('podrostki.txt')
tokens = gen_tokens(lines)
str = []
for a in tokens:
    str.append(a)

mark = make_markov(1, str)
window, d = random.choice(list(mark.items()))
print(window)
print(generate_markov(mark, 1, window))

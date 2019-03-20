import re
import os
import pickle
import random
from mudved_sql import *

def show_progress(value, count_of_data):
    print('{0} of {1}'.format(value, count_of_data), end = '\r')

def count_entry(word, dictionary):
    '''Подсчитывает количество вхождений слова word в словарь dictionary'''

    if word in dictionary:
        dictionary[word] += 1
    else:
        dictionary[word] = 1
    return dictionary    

def make_markov(order, data, markov_model):
    '''Создаёт структуру для цепи Маркова,
    order - порядок цепи Маркова, 
    data - список входных слов
    markov_model - модель цепи Маркова'''

    
    for i in range(0, len(data)-order):
        window = tuple(data[i:i+order])
        #window - "окно" значений в звене цепи Маркова
        word = data[i + order]
        #word - слово, для которого будет подсчитана частота использования с данным "окном"

        if window not in markov_model:
            markov_model[window] = dict()
        count_entry(word, markov_model[window])
    return markov_model

def make_markov_db(order, data):
    '''Создаёт структуру для цепи Маркова в базе данных,
    order - порядок цепи Маркова, 
    data - список входных слов'''

    #name_db = 'markovdb_order' + str(order) 
    #if not os.path.exists(name_db):
    #    print("Not found BD in current directory.")
    #    print("Create DB ", name_db, " in current directory")
    #    create_db(order)

    #conn = sqlite3.connect(name_db)
    conn = create_db_ozu()
    print("In progress ", str(len(data)-order), " words.")

    for i in range(0, len(data)-order):
        window = ' '.join(data[i:i+order])
        #window - "окно" значений в звене цепи Маркова
        word = data[i + order]
        #word - слово, для которого будет подсчитана частота использования с данным "окном"
        window_id = input_db(conn, 'window', window)
        word_id = input_db(conn, 'word', word)
        window_word_id = input_window_word(conn, window_id, word_id)
        show_progress(i, len(data))

    conn.close()
    return True

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

def save_markov(data):
    '''Сохраняет модель Маркова в файл data.pickle'''

    with open('data.pickle', 'wb') as f:
        pickle.dump(data, f)
    print("Data is save in pickle")

def load_markov():
    '''Загружает модель Маркова из файла data.pickle'''

    with open('data.pickle', 'rb') as f:
        data = pickle.load(f)
    print("Data load from pickle")
    return data

def read_file(filename):
    '''Читает входной файл с текстами и загружает в список'''

    if not os.path.exists(filename):
        print("Not found file ", filename)
        return False

    lines = gen_lines(filename)
    tokens = gen_tokens(lines)
    data = []
    for a in tokens:
        data.append(a)
    return data

if __name__=='__main__':
    data = read_file('podrostki.txt')
    markov_model = dict()
    mark = make_markov(3, data, markov_model)
    save_markov(mark)
    new_mark = load_markov()

    window, d = random.choice(list(mark.items()))
    print(window)
    print(generate_markov(mark, 3, window))

    #make_markov_db(3, data)

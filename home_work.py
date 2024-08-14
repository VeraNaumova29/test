import math

def exersise_1():
    print('#Задание 1.')

    dict_1 = {'a': 'яблоко', 'v': 20, 'h': 5}
    dict_2 = {'title': 'хлеб', 'price': 15, 'count': 3}

    def join_dict(dict_1, dict_2):
        result_dict = {}
        result_dict.update(dict_1)
        result_dict.update(dict_2)

        return result_dict

    print(join_dict(dict_1, dict_2))

def exersise_2():
    print('#Задание 2.')

    dict_stud = {'name': 'lox', 'marks': [1, 2, 5 ,5]}

    def avg_metric(a):
        return sum(a['marks'])/len(a['marks'])

    print(avg_metric(dict_stud))

def exersise_3():
    print('#Задание 3.')

    spisok_dict = [{'title': 'яблоко', 'price': 20, 'count': 8}, {'title': 'банан', 'price': 30, 'count': 7}, {'title': 'хлеб', 'price': 15, 'count': 3}]
    
    def create_new_list(a):
        new_spisok_dict = []
        for value in a:
            if value['count'] > 5:
                new_spisok_dict.append({
                    'title': value['title'],
                    'price': value['price']
                })
        return new_spisok_dict
    
    print(create_new_list(spisok_dict))

def exersise_4():
    print('#Задание 4.')

    list_products = [
        {'title': 'яблоко', 'cathegory': 'food'},
        {'title': 'банан', 'cathegory': 'food'},
        {'title': 'сидр', 'cathegory': 'drinks'}
    ]

    def get_cathegories(lst):
        new_dict = {}

        for value in lst:
            if value['cathegory'] not in new_dict:
                new_dict[value['cathegory']] = []
            new_dict[value['cathegory']].append(value)
        return new_dict

    print(get_cathegories(list_products))

def exersise_5():
    print('#Задание 5.')

    spisok_dict = [
        {'id': 0, 'title': 'яблоко', 'price': 20, 'count': 5},
        {'id': 1, 'title': 'груша', 'price': 10, 'count': 10},
        {'id': 2, 'title': 'куй', 'price': 5, 'count': 34},
        {'id': 3, 'title': 'куй', 'price': 70, 'count': 1},
    ]

    def new_list(m_dict, m_key, m_value):
        l = []
        for my_dict in m_dict:
            if m_key in my_dict and my_dict[m_key] == m_value:
                l.append(my_dict)
        return l

    print(new_list(spisok_dict, 'title', 'яблоко'))
    print(new_list(spisok_dict, 'title', 'ytyt'))
    print(new_list(spisok_dict, 'title', 'куй'))

if __name__== '__main__':
    exersise_1()
    exersise_2()
    exersise_3()
    exersise_4()
    exersise_5()




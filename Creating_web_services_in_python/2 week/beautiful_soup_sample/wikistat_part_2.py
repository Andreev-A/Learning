"""
Практическое задание по Beautiful Soup
Часть 2:
В этом задании продолжаем работать со страницами из wikipedia. Необходимо реализовать механизм сбора статистики по
нескольким страницам. Сложность задачи состоит в том, что сначала нужно будет определить страницы, с которых
необходимо собирать статистику. В качестве входных данных служат названия двух статей(страниц). Гарантируется, что
файлы обеих статей есть в папке wiki и из первой статьи можно попасть в последнюю, переходя по ссылкам только на те
статьи, копии которых есть в папке wiki.
Например, на вход подаются страницы: Stone_Age и Python_(programming_language). В статье Stone_Age есть ссылка на
Brain, в ней на Artificial_intelligence, а в ней на Python_(programming_language) и это кратчайший путь от Stone_Age
до Python_(programming_language). Ваша задача — найти самый короткий путь (гарантируется, что существует только один
путь минимальной длины), а затем с помощью функции parse из предыдущего задания собрать статистику по всем статьям в
найденном пути.
Результат нужно вернуть в виде словаря, ключами которого являются имена статей, а значениями списки со статистикой.
Для нашего примера правильный результат будет :
{ 'Stone_Age': [13, 10, 12, 40],
  'Brain': [19, 5, 25, 11],
  'Artificial_intelligence': [8, 19, 13, 198],
  'Python_(programming_language)': [2, 5, 17, 41]
}
Вам необходимо реализовать две функции:  build_bridge и get_statistics.
def build_bridge(path, start_page, end_page):
    '''возвращает список страниц, по которым можно перейти по ссылкам со start_page на
    end_page, начальная и конечная страницы включаются в результирующий список'''
    # напишите вашу реализацию логики по вычисления кратчайшего пути здесь


def get_statistics(path, start_page, end_page):
    '''собирает статистику со страниц, возвращает словарь, где ключ - название страницы,
    значение - список со статистикой страницы'''
    # получаем список страниц, с которых необходимо собрать статистику
    pages = build_bridge(path, start_page, end_page)
    # напишите вашу реализацию логики по сбору статистики здесь
    return statistic

Обе функции принимают на вход три параметра:path - путь до директории с сохраненными файлами из wikipedia,start_page
- название начальной страницы,end_page - название конечной страницы.
Функция build_bridge вычисляет кратчайший путь и возвращает список страниц в том порядке, в котором происходят
переходы. Начальная и конечная страницы включаются в результирующий список. В случае, если название стартовой и
конечной страницы совпадают, то результирующий список должен содержать только стартовую страницу. Получить все ссылки
на странице можно разными способами, в том числе и с помощью регулярных выражений, например так:
with open(os.path.join(path, page), encoding="utf-8") as file:
    links = re.findall(r"(?<=/wiki/)[\w()]+", file.read())
Обратите внимание, что что на страницах wikipedia могут встречаться ссылки на страницы, которых нет в директории wiki,
такие ссылки должны игнорироваться.
Пример работы функции build_bridge:
# >>> result = build_bridge('wiki/', 'The_New_York_Times', 'Stone_Age')
# >>> print(result)
['The_New_York_Times', 'London', 'Woolwich', 'Iron_Age', 'Stone_Age']
Функция get_statistics использует функцию parse и собирает статистику по страницам, найденным с помощью функции
build_bridge. Пример работы функции get_statistics:
# >>> from pprint import pprint
# >>> result = get_statistics('wiki/', 'The_New_York_Times', "Binyamina_train_station_suicide_bombing")
# >>> pprint(result)
{'Binyamina_train_station_suicide_bombing': [1, 3, 6, 21],
 'Haifa_bus_16_suicide_bombing': [1, 4, 15, 23],
 'Second_Intifada': [9, 13, 14, 84],
 'The_New_York_Times': [5, 9, 8, 42]}
Ваше решение должно содержать реализацию функций get_statistics, build_bridge и parse. Вы можете дополнительно объявить
в коде другие функции, если этого требует логика вашего решения.
"""

import os
import re
from bs4 import BeautifulSoup


def parse(path_to_file):
    with open(path_to_file, encoding='utf-8') as data:
        soup = BeautifulSoup(data, 'html.parser')
    body = soup.find(id="bodyContent")

    imgs = len((body.find_all('img', width=lambda x: int(x or 0) > 199)))

    headers = len([i.text for i in body.find_all(name=re.compile(r'[hH1-6]{2}')) if i.text[0] in 'ETC'])

    linkslen = 0
    all_links = body.find_all('a')
    for link in all_links:
        current_count = 1
        siblings = link.find_next_siblings()
        for sibling in siblings:
            if sibling.name == 'a':
                current_count += 1
                linkslen = max(current_count, linkslen)
            else:
                current_count = 0

    lists = 0
    html_lists = body.find_all(['ul', 'ol'])
    for html_list in html_lists:
        if not html_list.find_parents(['ul', 'ol']):
            lists += 1

    return [imgs, headers, linkslen, lists]


def get_backlinks(path, end_page, unchecked_pages, checked_pages, backlinks):
    if end_page in checked_pages or not checked_pages:
        return backlinks

    new_checked_pages = set()

    for checked_page in checked_pages:
        unchecked_pages.remove(checked_page)
        with open(os.path.join(path, checked_page), encoding="utf-8") as file:
            links = set(re.findall(r"(?<=/wiki/)[\w()]+", file.read()))
            if checked_page in links:
                links.remove(checked_page)
        linked_pages = links & unchecked_pages

        for linked_page in linked_pages:
            backlinks[linked_page] = backlinks.get(linked_page, checked_page)
            new_checked_pages.add(linked_page)

    checked_pages = new_checked_pages & unchecked_pages

    return get_backlinks(path, end_page, unchecked_pages, checked_pages, backlinks)


def build_bridge(path, start_page, end_page):
    backlinks = \
        get_backlinks(path, end_page, set(os.listdir(path)), {start_page, }, dict())

    current_page, bridge = end_page, [end_page]

    while current_page != start_page:
        current_page = backlinks.get(current_page)
        bridge.append(current_page)

    return bridge[::-1]


def get_statistics(path, start_page, end_page):
    pages = build_bridge(path, start_page, end_page)
    statistic = {}
    for file in pages:
        statistic[file] = parse(os.path.join(path, file))

    return statistic

######################################################################################################################
# Решение задания от преподавателей по Beautiful Soup часть 2
######################################################################################################################
# import os
# import re
#
# from bs4 import BeautifulSoup
#
#
# def parse(path_to_file):
#     with open(path_to_file, encoding="utf-8") as file:
#         soup = BeautifulSoup(file, "lxml")
#         body = soup.find(id="bodyContent")
#
#     imgs = len(body.find_all('img', width=lambda x: int(x or 0) > 199))
#
#     headers = sum(1 for tag in body.find_all(
#         ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) if tag.get_text()[0] in "ETC")
#
#     lists = sum(
#         1 for tag in body.find_all(['ol', 'ul']) if not tag.find_parent(['ol', 'ul']))
#
#     linkslen = 0
#
#     for a in body.find_all('a'):
#         current_streak = 1
#
#         for tag in a.find_next_siblings():
#             if tag.name == 'a':
#                 current_streak += 1
#             else:
#                 break
#
#         linkslen = current_streak if current_streak > linkslen else linkslen
#
#     return [imgs, headers, linkslen, lists]
#
#
# def get_statistics(path, start_page, end_page):
#     """собирает статистику со страниц, возвращает словарь, где ключ - название страницы,
#     значение - список со статистикой страницы"""
#     pages = build_bridge(path, start_page, end_page)
#     statistic = {}
#
#     for page in pages:
#         statistic[page] = parse(os.path.join(path, page))
#
#     return statistic
#
#
# def get_links(path, page):
#     """возвращает множество названий страниц, ссылки на которые содержатся в файле page"""
#
#     with open(os.path.join(path, page), encoding="utf-8") as file:
#         links = set(re.findall(r"(?<=/wiki/)[\w()]+", file.read()))
#         if page in links:
#             links.remove(page)
#     return links
#
#
# def get_backlinks(path, end_page, unchecked_pages, checked_pages, backlinks):
#     """возвращает словарь обратных ссылок (ключ - страница, значение - страница
#     с которой возможен переход по ссылке на страницу, указанную в ключе)"""
#
#     if end_page in checked_pages or not checked_pages:
#         return backlinks
#
#     new_checked_pages = set()
#
#     for checked_page in checked_pages:
#         unchecked_pages.remove(checked_page)
#         linked_pages = get_links(path, checked_page) & unchecked_pages
#
#         for linked_page in linked_pages:
#             backlinks[linked_page] = backlinks.get(linked_page, checked_page)
#             new_checked_pages.add(linked_page)
#
#     checked_pages = new_checked_pages & unchecked_pages
#
#     return get_backlinks(path, end_page, unchecked_pages, checked_pages, backlinks)
#
#
# def build_bridge(path, start_page, end_page):
#     """возвращает список страниц, по которым можно перейти по ссылкам со start_page на
#     end_page, начальная и конечная страницы включаются в результирующий список"""
#
#     backlinks = \
#         get_backlinks(path, end_page, set(os.listdir(path)), {start_page, }, dict())
#
#     current_page, bridge = end_page, [end_page]
#
#     while current_page != start_page:
#         current_page = backlinks.get(current_page)
#         bridge.append(current_page)
#
#     return bridge[::-1]

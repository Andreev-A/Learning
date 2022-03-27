"""
Практическое задание по Beautiful Soup
Часть 1:
В этом задании вам необходимо реализовать парсер для сбора статистики со страниц Википедии. Чтобы упростить вашу
задачу, необходимые страницы уже скачаны и сохранены на файловой системе в директории wiki/ (Например, страница
https://en.wikipedia.org/wiki/Stone_Age сохранена файле wiki/Stone_Age).
Парсер реализован в виде функции parse, которая принимает на вход один параметр: path_to_file — путь до файла,
содержащий html код страницы википедии. Гарантируется, что такой путь существует. Ваша задача — прочитать файл,
пройтись Beautiful Soup по статье, найти её тело (это <div id="bodyContent">) и внутри него подсчитать:
Количество картинок (img) с шириной (width) не меньше 200. Например: <img width="200">, но не <img> и не
<img width="199">
Количество заголовков (h1, h2, h3, h4, h5, h6), первая буква текста внутри которых соответствует заглавной букве
E, T или C. Например: <h1>End</h1> или <h5><span>Contents</span></h5>, но не <h1>About</h1> и не <h2>end</h2> и не
<h3><span>1</span><span>End</span></h3>
Длину максимальной последовательности ссылок, между которыми нет других тегов, открывающихся или закрывающихся.
Например: <p><span><a></a></span>, <a></a>, <a></a></p> - тут 2 ссылки подряд, т.к. закрывающийся span прерывает
последовательность. <p><a><span></span></a>, <a></a>, <a></a></p> - а тут 3 ссылки подряд, т.к. span находится внутри
ссылки, а не между ссылками.
Количество списков (ul, ol), не вложенных в другие списки. Например: <ol><li></li></ol>,
<ul><li><ol><li></li></ol></li></ul> - два не вложенных списка (и один вложенный)
Результатом работы функции parse будет список четырех чисел, посчитанных по формулам выше.
В пункте про последовательность ссылок вы можете ошибиться с результатом, если решите использовать метод find_next().
Обратите внимание, что хотя find_next находит тег, идущий сразу за текущим, этот тег может оказаться вложенным в
текущий, а не быть его следующим соседом. Возможно, нужно использовать другой метод или алгоритм.
Так же, не упустите момент, что данные во всех пунктах нужно искать внутри <div id="bodyContent">, а не по всей
странице.
"""

from bs4 import BeautifulSoup
import unittest
import re


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


class TestParse(unittest.TestCase):
    def test_parse(self):
        test_cases = (
            ('wiki/Stone_Age', [13, 10, 12, 40]),
            ('wiki/Brain', [19, 5, 25, 11]),
            ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
            ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
            ('wiki/Spectrogram', [1, 2, 4, 7]),)

        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                self.assertEqual(parse(path), expected)


if __name__ == '__main__':
    unittest.main()


######################################################################################################################
# Решение задания от преподавателей по Beautiful Soup часть 1
######################################################################################################################
# import unittest
#
# from bs4 import BeautifulSoup
#
#
# def parse(path_to_file):
#     with open(path_to_file, encoding="utf-8") as file:
#         soup = BeautifulSoup(file, "lxml")
#         body = soup.find(id="bodyContent")
#
#     # количество картинок (img) с шириной (width) не меньше 200
#     imgs = len(body.find_all('img', width=lambda x: int(x or 0) > 199))
#
#     # количество заголовков (h1, h2, h3, h4, h5, h6), первая буква текста внутри которых
#     # соответствует заглавной букве E, T или C
#     headers = sum(1 for tag in body.find_all(
#         ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) if tag.get_text()[0] in "ETC")
#
#     # количество списков (ul, ol), не вложенных в другие списки
#     lists = sum(
#         1 for tag in body.find_all(['ol', 'ul']) if not tag.find_parent(['ol', 'ul']))
#
#     # Длину максимальной последовательности ссылок, между которыми нет других тегов
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
# class TestParse(unittest.TestCase):
#     def test_parse(self):
#         test_cases = (
#             ('wiki/Stone_Age', [13, 10, 12, 40]),
#             ('wiki/Brain', [19, 5, 25, 11]),
#             ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
#             ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
#             ('wiki/Spectrogram', [1, 2, 4, 7]),)
#
#         for path, expected in test_cases:
#             with self.subTest(path=path, expected=expected):
#                 self.assertEqual(parse(path), expected)
#
#
# if __name__ == '__main__':
#     unittest.main()

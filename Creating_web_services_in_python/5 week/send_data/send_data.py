"""
В этом задании требуется отправить POST запрос на следующий https://datasend.webpython.graders.eldf.ru/submissions/1/
В запросе должен содержаться заголовок Authorization со способом аутентификации Basic логином alladin и паролем
opensesame закодированными в base64. -> Authorization: Basic YWxsYWRpbjpvcGVuc2VzYW1l
Запрос можно отправить любым удобным для вас способом, но мы рекомендуем использовать библиотеку requests, так как она
понадобится вам при выполнении последующих заданий.
В ответе на запрос вы получите инструкции для последующего запроса который приведет вас к специальному коду который
является ответом на это задание.
"""

import requests
import base64

url = 'https://datasend.webpython.graders.eldf.ru/submissions/1/'
headers = {'Authorization': 'Basic YWxsYWRpbjpvcGVuc2VzYW1l'}  # b'alladin:opensesame' -> base64.b64decode
r = requests.post(url, headers=headers)
print(r.status_code)  # 201
print(r.json())  # {'login': 'alibaba', 'password': '40razboinikov', 'path': 'submissions/secretlocation/',
# 'instructions': 'Сделайте PUT запрос на тот же хост, но на path указанный в этом документе c логином и паролем из
# этого документа. Логин и пароль также передайте в заголовке Authorization.'}

url1 = 'https://datasend.webpython.graders.eldf.ru/submissions/secretlocation/'
print(base64.b64encode(b'alibaba:40razboinikov'))
header1 = {'Authorization': 'Basic YWxpYmFiYTo0MHJhemJvaW5pa292'}
r1 = requests.put(url1, headers=header1)
print(r1.status_code)  # 202
print(r1.json())  # {'answer': 'w3lc0m370ch4p73r4.2'}
with open('answer.txt', 'w') as f:
    f.write(r1.json()['answer'])

######################################################################################################################
# Решение задания по отправке данных от преподавателей
######################################################################################################################
# Решение задания по отправке данных
# Для решения этого задания достаточно библиотеки requests и консоли python.
# Python 3.6.6 (default, Aug  9 2018, 19:58:47)
# [GCC 6.3.0 20170516] on linux
# Type "help", "copyright", "credits" or "license" for more information.
# >>> import requests
# >>> import json
# >>> headers = {'Authorization': 'Basic YWxsYWRpbjpvcGVuc2VzYW1l'}
# >>> response = requests.post('https://datasend.webpython.graders.eldf.ru/submissions/1/', headers=headers)
# >>> json.loads(response.content.decode('utf-8'))
# {'login': 'alibaba', 'password': '40razboinikov', 'path': 'submissions/secretlocation/', 'instructions': 'Сделайте
# PUT запрос на тот же хост, но на path указанный в этом документе c логином и паролем из этого документа. Логин и
# пароль также передайте в заголовке Authorization.'}
# >>>

# Далее кодируем новый логин и пароль в base64.
# >>> import base64
# >>> base64.b64encode(b'alibaba:40razboinikov')
# b'YWxpYmFiYTo0MHJhemJvaW5pa292'

# После этого делаем еще один запрос на новую точку API.
# >>> headers = {'Authorization': 'Basic YWxpYmFiYTo0MHJhemJvaW5pa292'}
# >>> response = requests.put('https://datasend.webpython.graders.eldf.ru/submissions/secretlocation/', headers=headers)
# >>> json.loads(response.content.decode('utf-8'))
# {'answer': 'w3lc0m370ch4p73r4.2'}
# >>>
# И получаем ответ на задание.
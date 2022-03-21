# В процессе импорта модуля, он исполняется целиком. А те имена, которые останутся в пространстве имен, связанные с
# исполнением этого модуля, мы затем сможем использовать. Они доступны в качестве атрибутов импортируемого модуля.
# Внутри модуля всегда доступно глобальное имя __name__. Оно показывает текущее имя модуля.
# Когда модуль запускается с помощью интерпретатора, он носит имя __main__
# Если же модуль импортируется, то __name__ будет содержать название самого модуля.
# def fib(k):
#     if k ==0 or k ==1:
#         return 1
#     else:
#         return fib(k - 1) + fib(k - 2)
# if __name__ == '__main__':
#     print(__name__)
#     print(fib(31))
# если запускать модуль - выполнится все. Если импортировать - выполнится до if __name__ == '__main__'
# Исполнения модуля происходит только при первом его импорте. Если повторно вызвать импорт этого модуля, то он не будет
# заново исполнен, а будут переиспользованы старые объекты нашего модуля.
# Имена модулей хранятся в словаре sys.modules
# Если интерпретатор не находит запрашиваемого модуля в словаре sys.modules, он будет искать его в папках, указанных
# в списке sys.path
# import sys
# print(type(sys.modules))
# print(sys.modules)
# Если интерпретатор не находит запрашиваемого модуля в словаре sys.modules, он будет искать его в папках, указанных в
# списке sys.path
# import sys
# for path in sys.path:
#     print(path)
# Сначала он ищет в локальной директории модуля. Затем перебирает внешние библиотеки.
# В PyCharm мы можем тоже увидеть все библиотеки Python:
# В библиотеке Python39 содержатся модули, которые являются стандартной библиотекой языка Python.
# В свою очередь, библиотека site-packages содержит в себе модули, которые являются дополнительно установленными.
# Внутри библиотеки почти все модули представлены папками. Они называются пакеты.
# Пакет - это удобный способ представления некоторого числа файлов в качестве одного модуля. Пакеты тоже могут вести себя
# как модули, которые тоже можно импортировать.
# Интерпретатор умеет определять по папке является ли она пакетом по наличию файла __init__.py внутри: Именно этот файл
# исполняется при импорте.  в папке-пакете может быть больше модулей, чем указано в ините, например незавершённые
# разработки. и они не импортируются. при импорте интерпретатор прочтет файл инит и возьмёт только то, что указано в
# нем, а остальное пропустит.
# Также мы можем импортировать не весь модуль целиком, а только определенные имена из него
# Если в данном модуле уже существует функция с аналогичным именем, произойдет следующее (пример на скрине ниже):
# ●	сначала мы в локальное имя greet записываем функцию из модуля exceptions
# ●	затем, когда мы определяем функцию greet() внутри своего файла, то мы перезаписываем это локальное имя
# Таким образом, мы теряем ссылку на функцию из модуля exceptions
# from exception import BadName, greet
# def greet();
#     pass
# greet()
# Для того, чтобы это избежать, мы можем явно указать то локальное имя, которое мы бы хотели использовать. Мы можем даже
# импортировать целиком модуль, используя для него другое локальное имя:
# from exception import BadName as bad, greet as exc_greet
# import exception as exc
# def greet();
#     pass
# greet()
# В языке Python возможно импортировать все имена из какого-либо модуля. Для этого достаточно использовать *
# Однако, такая практика не рекомендуется. Так как если модуль большой и в нем много имен, то какие-то из них могут
# пересекаться с теми, которые вы используете.
# При этом в самом модуле с помощью конструкции __all__ можно явно указать какие имена будут импортироваться, если
# использовать *
# GREETING = 'Hello'
# class BadName(Exception):
#     pass
# def greet(name):
#     if name[0].isupper():
#         return GREETING + name
#     else:
#         raise BadName(name + ' error')
# __all__ = ['BadName', 'greet']
# Также не будут импортироваться любые имена, начинающиеся с нижнего подчеркивания _ - _GREETING
# Python Package Index
# https://pypi.org/
# https://docs.python.org/3.5/distutils/packageindex.html

# Значит при втором и последующих импортах не удастся произвести импорт других функций этого модуля, т.к. sys.modules уже
# будет содержаться наш импортируемый модуль после первого импорта?
# Не совсем. Если второй импорт делать вида "import mymodule",  то код модуля выполнен не будет и все НЕ импортированные
# до этого функции действительно не будут импортированы, однако если второй импорт будет иметь вид
# "from mymodule import bar", тогда bar станет доступна, хотя код всего модуля исполнен так же не будет.

# Подскажите пожалуйста, чем отличается import exceptions от from exceptions import * ?
# Да ничем по сути, единственное что когда вы импортируете всё со звёздочкой - у вас импортируются все имена из модуля
# (который импортируете) и это может приводить к конфликтам: ну например у вас есть функция с именем input_file, в
# модуле есть
# одноименная функция - возникает путаница. В общем лучше import module_name или module_name as mn (или что-то похожее)
# и потом пользоваться через точку ну или from module_name import f1, f2, f3 - то есть что-то конкретное, вообще вопрос
# вкуса/удобства, но на мой взгляд - так читабельнее и меньше потенциальных багов

######################################################################################################################
# Где взять отсутствующий пакет?
# Необходимость в установке дополнительного пакета возникнет очень быстро, если вы решите поработать над задачей, за
# рамками базового функционала, который предоставляет Python. Например: работа с web, обработка изображений,
# криптография и т.п. В этом случае, необходимо узнать, какой пакет содержит функционал, который вам необходим, найти
# его, скачать, разместить в нужном каталоге и начать использовать. Все эти действия можно сделать вручную, но этот
# процесс поддается автоматизации. К тому же скачивать пакеты с неизвестных сайтов может быть довольно опасно.
#
# К счастью для нас, в рамках Python, все эти задачи решены. Существует так называемый Python Package Index (PyPI) – это
# репозиторий, открытый для всех Python разработчиков, в нем вы можете найти пакеты для решения практически любых задач.
# Там также есть возможность выкладывать свои пакеты. Для скачивания и установки используется специальная утилита,
# которая называется pip.
#
# Менеджер пакетов в Python – pip
# Pip – это консольная утилита (без графического интерфейса). После того, как вы ее скачаете и установите, она
# пропишется в PATH и будет доступна для использования.
#
# Эту утилиту можно запускать как самостоятельно:
#
# > pip <аргументы>
# так и через интерпретатор Python:
#
# > python -m pip <аргументы>
# Ключ -m означает, что мы хотим запустить модуль (в данном случае pip). Более подробно о том, как использовать pip, вы
# сможете прочитать ниже.
#
# Установка pip
# При развертывании современной версии Python (начиная с Python 2.7.9 и Python 3.4),
# pip устанавливается автоматически. Но если, по какой-то причине, pip не установлен на вашем ПК, то сделать это можно
# вручную. Существует несколько способов.
#
# Универсальный способ
#
# Будем считать, что Python у вас уже установлен, теперь необходимо установить pip. Для того, чтобы это сделать,
# скачайте скрипт get-pip.py
#
# > curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# и выполните его.
#
# > python get-pip.py
# При этом, вместе с pip будут установлены setuptools и wheels. Setuptools  – это набор инструментов для построения
# пакетов Python. Wheels – это формат дистрибутива для пакета Python. Обсуждение этих составляющих выходит за рамки
# урока, поэтому мы не будем на них останавливаться.
#
# Способ для Linux
#
# Если вы используете Linux, то для установки pip можно воспользоваться имеющимся в вашем дистрибутиве пакетным
# менеджером. Ниже будут перечислены команды для ряда Linux систем, запускающие установку pip (будем рассматривать
# только Python 3, т.к. Python 2 уже морально устарел, а его поддержка и развитие будут прекращены после 2020 года).
#
# Fedora
#
# Fedora 21:
#
# > sudo yum install python3 python3-wheel
# Fedora 22:
#
# > sudo dnf install python3 python3-wheel
# openSUSE
#
# > sudo zypper install python3-pip python3-setuptools python3-wheel
# Debian/Ubuntu
#
# > sudo apt install python3-venv python3-pip
# Arch Linux
#
# > sudo pacman -S python-pip
# Обновление pip
# Если вы работаете с Linux, то для обновления pip запустите следующую команду.
#
# > pip install -U pip
# Для Windows команда будет следующей:
#
# > python -m pip install -U pip
# Использование pip
# Далее рассмотрим основные варианты использования pip: установка пакетов, удаление и обновление пакетов.
#
# Установка пакета
# Pip позволяет установить самую последнюю версию пакета, конкретную версию или воспользоваться логическим выражением,
# через которое можно определить, что вам, например, нужна версия не ниже указанной. Также есть поддержка установки
# пакетов из репозитория. Рассмотрим, как использовать эти варианты.
#
# Установка последней версии пакета
#
# > pip install ProjectName
# Установка определенной версии
#
# > pip install ProjectName==3.2
# Установка пакета с версией не ниже 3.1
#
# > pip install ProjectName>=3.1
# Установка Python пакета из git репозитория
#
# > pip install -e git+https://gitrepo.com/ProjectName.git
# Установка из альтернативного индекса
#
# > pip install --index-url http://pypackage.com/ ProjectName
# Установка пакета из локальной директории
#
# > pip install ./dist/ProjectName.tar.gz
# Удаление пакета
# Для того, чтобы удалить пакет воспользуйтесь командой
#
# > pip uninstall ProjectName
# Обновление пакетов
# Для обновления пакета используйте ключ –upgrade.
#
# > pip install --upgrade ProjectName
# Просмотр установленных пакетов
# Для вывода списка всех установленных пакетов применяется команда pip list.
#
# > pip list
# Если вы хотите получить более подробную информацию о конкретном пакете, то используйте аргумент show.
#
# > pip show ProjectName
# Поиск пакета в репозитории
# Если вы не знаете точное название пакета, или хотите посмотреть на пакеты, содержащие конкретное слово, то вы можете
# это сделать, используя аргумент search.
#
# > pip search "test"

# python -m pip install имя_пакета
# Пора запустить pip в Python и начать устанавливать пакеты короткой командой из консоли:
# pip install имя_пакета
# При установке в Windows, перед pip  нужно добавить "python -m".
# Обновить пакет не сложнее:
# pip install имя_пакета -U
# Если у вас последняя версия пакета, но вы хотите принудительно переустановить его:
# pip install --force-reinstall
# Посмотреть список установленных пакетов Python можно с помощью команды:
# pip list
##########################################################################################
# pip install pipenv
# Установите зависимости проекта, включая зависимости для разработки
# pipenv install --dev
# Активируйте virtualenv проекта
# pipenv shell
# Запустите миграции
# python manage.py migrate

# he "task" is no longer in version 5.x You can use version 4.x
# pip3 uninstall celery
# pip3 install celery==4.4.0
# Edited the spaces

##########################################################################################
# Для Windows.
# Установите ту версию python, которую хотите использовать в виртуальном пространстве. ВАЖНО! Если у вас есть основаная
# версия и вы не хотите конфликтов, то на моменте установки снимите галочку с опции Add python 3.6 to PATH
# Далее введите (при условии, что у вас установлен python)
# py -3.6 -m venv env
# И вы получите виртуально пространство с python 3.6, которое будет лежать в папке env
#
# Настройка виртуального окружения
# Создание
# Для создания виртуального окружения, перейдите в директорию своего проекта и выполните:
#
# python -m venv venv
# Флаг -m указывает Python-у запустить venv как исполняемый модуль.
# venv/ — название виртуального окружения (где будут храниться ваши библиотеки).
#
# В результате будет создан каталог venv/ содержащий копию интерпретатора Python, стандартную библиотеку и другие
# вспомогательные файлы.
#
# Новые пакеты будут устанавливаться в venv/lib/python3.x/site-packages/
#
# Активация
# Чтобы начать пользоваться виртуальным окружением, необходимо его активировать:
#
# venv\Scripts\activate.bat - для Windows;  ".\\env\Scripts\activate.bat"
# source venv/bin/activate - для Linux и MacOS.
# source выполняет bash-скрипт без запуска дополнительного bash-процесса.
#
# Проверить успешность активации можно по приглашению оболочки. Она будет выглядеть так:
#
# (venv) root@purplegate:/var/test#
# Также новый путь до библиотек можно увидеть выполнив команду:
#
# python -c "import site; print(site.getsitepackages())"
# Интересный факт: в виртуальном окружении вместо команды python3 и pip3, можно использовать python и pip
#
# Автоматическая активация
# В некоторых случаях, процесс активации виртуального окружения может показаться неудобным (про него можно банально
# забыть 🤷‍♀️).
#
# На практике, для автоматической активации перед запуском скрипта, создают скрипт-обертку на bash:
#
# #!/usr/bin/env bash
#
# source $BASEDIR/venv/bin/activate
# python $BASEDIR/my_app.py

# Теперь можно установить права на исполнение и запустить нашу обертку:
#
# chmod +x myapp/run.sh
# ./myapp/run.sh
# Деактивация
# Закончив работу в виртуальной среде, вы можете отключить ее, выполнив консольную команду:
#
# deactivate

###################################################################################################################

# Алиса зашифровала свою информацию с помощью библиотеки simple-crypt. Она представила информацию в виде строки,
# и затем записала в бинарный файл результат работы метода simplecrypt.encrypt.
# Вам необходимо установить библиотеку simple-crypt при установке - внизу поставить галочку options с "--no-deps" (для
# работы этого модуля установите модуль pycryptodome), и с помощью метода simplecrypt.decrypt узнать, какой из паролей
# служит ключом для расшифровки файла с интересной информацией.
#
# from simplecrypt import decrypt, DecryptionException
#
# with open("D:\\encrypted.bin", "rb") as inp:
#     encrypted = inp.read().strip()
# with open("D:\\passwords.txt", "r") as inf:
#     passwords = inf.read().strip().split('\n_test')
#
# for password in passwords:
#     try:
#         print(decrypt(password, encrypted).decode('utf8'))
#         break
#     except DecryptionException:
#         continue
#
# encrypted = open("encrypted.bin", "rb").read()
# passwords = open("passwords.txt").readlines()
# for p in passwords:
#     p = p.strip()
#     try:
#         s = simplecrypt.decrypt(p, encrypted)
#     except simplecrypt.DecryptionException:
#         continue
#     print(s.decode("utf-8"))
#
# import os
# import urllib.request
# from multiprocessing import Process
#
# import simplecrypt
#
# def decryptor(passw,text):
#     try:
#         print("Пробуем " + passw)
#         result_dict = simplecrypt.decrypt(passw.strip(), text)
#         proc = os.getpid()
#         print('Пароль {0} подошел. Результат: {1}. id процесса: {2}'.format(
#             passw, result_dict, proc))
#     except:
#         print(passw + " Не подошел :(")
#
# urllib.request.urlretrieve('https://stepik.org/media/attachments/lesson/24466/encrypted.bin', 'encrypted.bin')
# urllib.request.urlretrieve("https://stepik.org/media/attachments/lesson/24466/passwords.txt", 'passwords.txt')
#
# if __name__ == '__main__':
#     encrypted = ""
#     with open("encrypted.bin", "rb") as inp:
#         encrypted = inp.read()
#
#     with open('passwords.txt') as input_file:
#         lineList = input_file.readlines()
#         procs = []
#
#         for i in lineList:
#             proc = Process(target=decryptor, args=(i.strip(), encrypted,))
#             procs.append(proc)
#             proc.start()
#
#         for proc in procs:
#             proc.join()

# bkl = urllib.request.urlopen('https://stepic.org/media/attachments/lesson/24466/encrypted.bin').read()
# passwords = urllib.request.urlopen('https://stepic.org/media/attachments/lesson/24466/passwords.txt').read().strip().split()
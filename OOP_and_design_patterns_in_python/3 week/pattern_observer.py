"""
Продолжая работу над игрой, вы добрались до системы достижений. Иногда по сценарию игры требуется наградить игрока за
то, что он достигает определенного результата в игре. Это может быть, например: прохождение всех заданий в игре,
достижение определенного уровня, совершение какого-то сложного действия и т.д.
У каждой игры есть движок и интерфейс пользователя. Эти два компонента работают параллельно и взаимодействуют друг с
другом. Достижения генерируются движком игры, а отображаются пользовательским интерфейсом. Кроме того, на современных
игровых площадках, таких как Steam, Google Play, также отображаются достижения, полученные игроком. Реализуется это с
помощью паттерна Наблюдатель.
В реализации нашей игры есть движок Engine, который может создавать уведомления о достижениях. Пример достижения,
которое генерирует движок:
{"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"}
Вам необходимо написать обертку над движком, которая будет иметь возможность подписывать наблюдателей и рассылать им
уведомления. Вы так же должны написать реализацию классов иерархии наблюдателей.
Иерархия наблюдателей включает в себя AbstractObserver (абстрактный наблюдатель) от которого унаследованы два
наблюдателя ShortNotificationPrinter и FullNotificationPrinter. В атрибуте achievements у ShortNotificationPrinter
хранится множество названий полученных достижений, а у FullNotificationPrinter - список достижений в том порядке, в
котором они генерируются Engine. Обратите внимание, что каждое достижение должно быть уникальным (то есть учтено
только один раз).
Метод update не должен возвращать никаких значений, он должен только изменять значение атрибута achievements.
Важно!  На проверку необходимо сдать фрагмент кода, содержащий только реализацию 4 классов: ObservableEngine,
AbstractObserver , ShortNotificationPrinter, FullNotificationPrinter. Описывать класс Engine и импортировать его в коде
НЕ НУЖНО (он уже реализован и будет импортирован тестовой системой).
"""

from abc import ABC, abstractmethod


class ObservableEngine(Engine):  # Наблюдаемая система
    def __init__(self):
        self.__subscribers = set()  # При инициализации множество подписчиков задается пустым

    def subscribe(self, subscriber):
        self.__subscribers.add(
            subscriber)  # Для того чтобы подписать пользователя, он добавляется во множество подписчиков

    def unsubscribe(self, subscriber):
        self.__subscribers.remove(subscriber)  # Удаление подписчика из списка

    def notify(self, message):
        for subscriber in self.__subscribers:
            subscriber.update(message)  # Отправка уведомления всем подписчикам


class AbstractObserver(ABC):
    @abstractmethod
    def update(self, message):  # Абстрактный наблюдатель задает метод update
        pass


class ShortNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = set()

    def update(self, message):  # Конкретная реализация метода update
        self.achievements.add(message['title'])


class FullNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = list()

    def update(self, message):  # Конкретная реализация метода update
        if message not in self.achievements:
            self.achievements.append(message)

# short_notifier = ShortNotificationPrinter()
# full_notifier = FullNotificationPrinter()
#
# manager = ObservableEngine()
#
# manager.subscribe(short_notifier)
# manager.subscribe(full_notifier)
#
# manager.notify({"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"})
# manager.notify({"title": "Покоритель1", "text": "Дается при выполнении всех заданий в игре"})
# manager.notify({"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"})
#
# print(short_notifier.achievements)
# print(full_notifier.achievements)

######################################################################################################################
# Паттерн Наблюдатель — решение от преподавателей
######################################################################################################################
# # Опишем наблюдаемую систему
# class ObservableEngine(Engine):
#     def __init__(self):
#         # Объявим пустое множество подписчиков
#         self.subscribers = set()
#
#     def subscribe(self, subscriber):
#         # Добавим пользователя во множество подписчиков
#         self.subscribers.add(subscriber)
#
#     def unsubscribe(self, subscriber):
#         # Если данный подписчик присутствует в списке подписчиков, его можно удалить
#         if subscriber in self.subscribers:
#             self.subscribers.remove(subscriber)
#
#     def notify(self, message):
#         # Отправка уведомления всем подписчикам
#         for subscriber in self.subscribers:
#             subscriber.update(message)
#
#
# # Определим абстрактного наблюдателя
# class AbstractObserver(ABC):
#
#     # Каждый конкретный наблюдатель должен будет реализовать метод update
#     @abstractmethod
#     def update(self, message):
#         pass
#
#
# # Определим конкретных наблюдателей
# class ShortNotificationPrinter(AbstractObserver):
#     def __init__(self):
#         # Объявим множество всех полученных достижений
#         self.achievements = set()
#
#     def update(self, message):
#         # Добавим название достижения во множество достижений
#         self.achievements.add(message["title"])
#
#
# class FullNotificationPrinter(AbstractObserver):
#     def __init__(self):
#         # Объявим список всех полученных достижений
#         self.achievements = list()
#
#     def update(self, message):
#         # Если подобного достижения не было в списке, добавим его
#         if message not in self.achievements:
#             self.achievements.append(message)
"""
В этом задании вам необходимо сделать рефакторинг уже реализованной программы - заставки для скринсейвера. Исходный код
программы в модуле screen_the_task.
Для работы программы необходима библиотека PyGame.
Программа запускается из консоли, как обычный Python скрипт:
$ python3 screen.py
В открывшемся окне программы доступны следующие команды управления:
<F1>  - показать справку по командам
<R>  - рестарт
<P>  - пауза, снять/поставить
<num+>  - увеличить количество точек «сглаживания»
<num->  - уменьшить количество точек «сглаживания»
<mouse left>  - добавить «опорную» точку
По умолчанию при старте программы «опорные» точки отсутствуют и программа находится в состоянии паузы (движение кривой
выключено). Для добавления точек сделайте несколько кликов левой клавишей мыши в любом месте окна программы. Отрисовка
кривой произойдет, когда точек на экране станет больше двух. Нажмите клавишу <P>, чтобы включить движение кривой.
Ваша задача:
1. Изучить документацию к библиотеке pygame и код программы. Понять механизм работы программы (как происходит отрисовка
кривой, перерасчет точек сглаживания и другие нюансы реализации программы)
2. Провести рефакторниг кода, переписать программу в ООП стиле с использованием классов и наследования.
- Реализовать класс 2-мерных векторов Vec2d [1]. В классе следует определить методы для основных математических
операций, необходимых для работы с вектором: Vec2d.__add__ (сумма), Vec2d.__sub__ (разность), Vec2d.__mul__
(произведение на число). А также добавить возможность вычислять длину вектора с использованием функции len(a) и метод
int_pair, который возвращает кортеж из двух целых чисел (текущие координаты вектора).
- Реализовать класс замкнутых ломаных Polyline с методами отвечающими за добавление в ломаную точки (Vec2d) c её
скоростью, пересчёт координат точек (set_points) и отрисовку ломаной (draw_points). Арифметические действия с векторами
должны быть реализованы с помощью операторов, а не через вызовы соответствующих методов.
- Реализовать класс Knot (наследник класса Polyline), в котором добавление и пересчёт координат инициируют вызов функции
get_knot для расчёта точек кривой по добавляемым «опорным» точкам [2].
- Все классы должны быть самостоятельными и не использовать внешние функции.
- Реализовать дополнительный функционал (выполнение требований этого пункта предоставляет возможность потренировать свои
навыки программирования и позволяет получить дополнительные баллы в этом задании). К дополнительным задачам относятся:
реализовать возможность удаления «опорной» точки из кривой, реализовать возможность отрисовки на экране нескольких
кривых, реализовать возможность ускорения/замедления скорости движения кривой(-ых).
"""

import pygame
import random

SCREEN_DIM = (800, 600)


class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)

    def __mul__(self, k):
        return Vec2d(self.x * k, self.y * k)

    @staticmethod
    def len(a):
        return (a.x ** 2 + a.y ** 2) ** 0.5

    def int_pair(self):
        return int(self.x), int(self.y)


class Polyline:
    def __init__(self):
        self.points = []
        self.speeds = []
        self.factor_speed = 1

    def add_point(self, x, y):
        point = Vec2d(x, y)
        speed = Vec2d(random.random() * 2, random.random() * 2)
        self.points.append(point)
        self.speeds.append(speed * self.factor_speed)

    def del_point(self):
        if len(self.points):
            self.points.pop()
            self.speeds.pop()

    def change_speed(self, k):
        if k > 1 and self.factor_speed < 6:
            self.factor_speed *= k
        elif k < 1 and self.factor_speed > 0.17:
            self.factor_speed *= k
        if 0.17 < self.factor_speed < 6:
            self.speeds = list(map(lambda pair: pair * k, self.speeds))

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] += self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(- self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)

    def draw_points(self, points, style="points", width=3,
                    color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color,
                                 points[p_n].int_pair(),
                                 points[p_n + 1].int_pair(), width)
        elif style == "points":
            for p in points:
                pygame.draw.circle(gameDisplay, color,
                                   p.int_pair(), width)


class Knot(Polyline):
    def __init__(self):
        super().__init__()
        self.count = 35

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha,
                                                    deg - 1) * (1 - alpha)

    def get_points(self, base_points):
        alpha = 1 / self.count
        res = []
        for i in range(self.count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
            res.extend(self.get_points(ptn))
        return res


def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["Сommon", ""])
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play (in pause the screens are separate)"])
    data.append(["Q", "First/Second (key toggle screens)"])
    data.append(["", ""])
    data.append([screen_name, ""])
    data.append([str(steps), "Current points"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(round(speed, 2)), "Current speed"])
    data.append(["Num8", "Speed is higher"])
    data.append(["Num2", "Speed is lower"])
    data.append(["", ""])
    data.append(["DELETE", "Delete supporting point"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 50 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (230, 50 + 30 * i))


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    working = True
    show_help = False
    pause = True
    screen = True
    hue = 0
    color = pygame.Color(0)

    knot_1 = Knot()
    knot_2 = Knot()

    while working:

        if screen:
            knot, screen_name = knot_1, 'First screen'
        else:
            knot, screen_name = knot_2, 'Second screen'
        steps, speed = knot.count, knot.factor_speed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_r:
                    knot_1 = Knot()
                    knot_2 = Knot()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                if event.key == pygame.K_DELETE:
                    knot.del_point()
                if event.key == pygame.K_q:
                    screen = not screen
                if event.key == pygame.K_KP8:
                    knot.change_speed(1.2)
                if event.key == pygame.K_KP2:
                    knot.change_speed(0.83333)

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                knot.add_point(x, y)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        if not pause or screen:
            knot_1.draw_points(knot_1.points)
            knot_1.draw_points(knot_1.get_knot(), "line", 3, color)
        if not pause or not screen:
            knot_2.draw_points(knot_2.points)
            knot_2.draw_points(knot_2.get_knot(), "line", 3, color)
        knot.count = steps
        if not pause:
            knot_1.set_points()
            knot_2.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)

import pygame
import collections

colors = {
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255),
    "red": (255, 0, 0, 255),
    "green": (0, 255, 0, 255),
    "blue": (0, 0, 255, 255),
    "wooden": (153, 92, 0, 255),
}


class ScreenHandle(pygame.Surface):

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            self.successor = args[-1]
            self.next_coord = args[-2]
            args = args[:-2]
        else:
            self.successor = None
            self.next_coord = (0, 0)
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def draw(self, GD):
        if self.successor is not None:
            GD.blit(self.successor, self.next_coord)
            self.successor.draw(GD)

    def connect_engine(self, engine):
        if self.successor is not None:
            return self.successor.connect_engine(engine)


class GameSurface(ScreenHandle):

    def connect_engine(self, engine):
        self.game_engine = engine
        if self.successor is not None:
            return self.successor.connect_engine(engine)

    def draw_hero(self):
        self.game_engine.hero.draw(self)

    def draw_map(self):
        size = self.game_engine.sprite_size
        screen_size = list(self.get_size())
        hero_pos = self.game_engine.hero.position
        self.min_x = int(max(0, hero_pos[0] - screen_size[0] / size + 3))
        self.min_y = int(max(0, hero_pos[1] - screen_size[1] / size + 3))

        if self.game_engine.map:
            for i in range(len(self.game_engine.map[0]) - self.min_x):
                for j in range(len(self.game_engine.map) - self.min_y):
                    self.blit(self.game_engine.map[self.min_y + j][
                                  self.min_x + i][0], (i * size, j * size))
        else:
            self.fill(colors["white"])

    def draw_object(self, sprite, coord):
        size = self.game_engine.sprite_size

        self.blit(sprite, ((coord[0] - self.min_x) * size,
                           (coord[1] - self.min_y) * size))

    def draw(self, GD):
        size = self.game_engine.sprite_size

        self.draw_map()
        for obj in self.game_engine.objects:
            self.blit(obj.sprite[0], ((obj.position[0] - self.min_x) * size,
                                      (obj.position[1] - self.min_y) * size))
        self.draw_hero()

        if self.successor is not None:
            GD.blit(self.successor, self.next_coord)
            return self.successor.draw(GD)


class ProgressBar(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def connect_engine(self, engine):
        self.engine = engine
        if self.successor is not None:
            return self.successor.connect_engine(engine)

    def draw(self, GD):
        self.fill(colors["wooden"])
        pygame.draw.rect(self, colors["black"], (50, 30, 200, 30), 2)
        pygame.draw.rect(self, colors["black"], (50, 70, 200, 30), 2)

        pygame.draw.rect(self, colors[
            "red"], (50, 30, 200 * min(self.engine.hero.hp /
                                       self.engine.hero.max_hp, 1), 30))
        pygame.draw.rect(self, colors[
            "green"], (50, 70, 200 * self.engine.hero.exp / (
                100 * (2 ** (self.engine.hero.level - 1))), 30))

        font = pygame.font.SysFont("comicsansms", 20)
        self.blit(font.render(
            f'Hero at {self.engine.hero.position}', True, colors["black"]),
            (250, 0))

        self.blit(font.render(
            f'{self.engine.level} floor', True, colors["black"]),
            (10, 0))

        self.blit(font.render(f'HP', True, colors["black"]),
                  (10, 30))
        self.blit(font.render(f'Exp', True, colors["black"]),
                  (10, 70))

        self.blit(font.render(
            f'{self.engine.hero.hp}/{self.engine.hero.max_hp}', True,
            colors["black"]),
            (60, 30))
        self.blit(font.render(
            f'{self.engine.hero.exp}/'
            f'{(100 * (2 ** (self.engine.hero.level - 1)))}', True,
            colors["black"]),
            (60, 70))

        self.blit(font.render(f'Level', True, colors["black"]),
                  (280, 30))
        self.blit(font.render(f'Gold', True, colors["black"]),
                  (280, 70))

        self.blit(font.render(
            f'{self.engine.hero.level}', True, colors["black"]),
            (360, 30))
        self.blit(font.render(
            f'{self.engine.hero.gold}', True, colors["black"]),
            (340, 70))

        self.blit(font.render(f'Str', True, colors["black"]),
                  (420, 30))
        self.blit(font.render(f'Luck', True, colors["black"]),
                  (420, 70))

        self.blit(font.render(
            f'{self.engine.hero.stats["strength"]}', True, colors["black"]),
            (480, 30))
        self.blit(font.render(
            f'{self.engine.hero.stats["luck"]}', True, colors["black"]),
            (480, 70))

        self.blit(font.render(f'SCORE', True, colors["black"]),
                  (550, 30))
        self.blit(font.render
                  (f'{self.engine.score:.4f}', True, colors["black"]),
                  (550, 70))
        if self.successor is not None:
            GD.blit(self.successor, self.next_coord)
            return self.successor.draw(GD)


class InfoWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 16
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)

    def update(self, value):
        self.data.append(f"> {str(value)}")

    def draw(self, GD):
        self.fill(colors["wooden"])
        size = self.get_size()

        font = pygame.font.SysFont("comicsansms", 10)
        for i, text in enumerate(self.data):
            self.blit(font.render(text, True, colors["black"]),
                      (5, 20 + 18 * i))

        if self.successor is not None:
            GD.blit(self.successor, self.next_coord)
            return self.successor.draw(GD)

    def connect_engine(self, engine):
        self.engine = engine
        engine.subscribe(self)
        if self.successor is not None:
            return self.successor.connect_engine(engine)


class HelpWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)
        self.data.append([" →", "Move Right"])
        self.data.append([" ←", "Move Left"])
        self.data.append([" ↑ ", "Move Top"])
        self.data.append([" ↓ ", "Move Bottom"])
        self.data.append([" H ", "Show Help"])
        self.data.append(["Num+", "Zoom +"])
        self.data.append(["Num-", "Zoom -"])
        self.data.append([" R ", "Restart Game"])
        self.data.append([" Q ", "Minimap Drawing"])

    def connect_engine(self, engine):
        self.engine = engine
        if self.successor is not None:
            return self.successor.connect_engine(engine)

    def draw(self, GD):
        alpha = 0
        if self.engine.show_help:
            alpha = 128
        self.fill((0, 0, 0, alpha))
        size = self.get_size()
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        if self.engine.show_help:
            pygame.draw.lines(self, (255, 0, 0, 255), True, [
                (0, 0), (700, 0), (700, 500), (0, 500)], 5)
            for i, text in enumerate(self.data):
                self.blit(font1.render(text[0], True, ((128, 128, 255))),
                          (50, 50 + 30 * i))
                self.blit(font2.render(text[1], True, ((128, 128, 255))),
                          (150, 50 + 30 * i))
        if self.successor is not None:
            GD.blit(self.successor, self.next_coord)
            return self.successor.draw(GD)

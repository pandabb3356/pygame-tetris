import pygame as pg


class Game:
    """Main game process"""

    WIN_SIZE = (1000, 800)

    _surface: pg.Surface

    def __init__(self):
        self.set_surface(pg.display.set_mode(self.WIN_SIZE))

    def set_surface(self, surface: pg.Surface):
        self._surface = surface

    def init(self):
        pass

    def run(self):
        pg.init()
        clock = pg.time.Clock()
        clock.tick()

        self.init()

        done = 0

        while not done:
            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
                    done = 1
                    break

        pg.quit()

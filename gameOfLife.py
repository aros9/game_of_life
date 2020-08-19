import pygame
import pygame.locals

class Board(object):
    def __init__(self, width, height): # constructor that will make board
        self.surface = pygame.display.set_mode((width, height), 0 ,32)
        pygame.display.set_caption("Game of Life")

    def draw(self, *args): # method responsible for drawing window
        background = (0, 0, 0)
        self.surface.fill(background)
        for element in args:
            element.draw_on(self.surface)

        pygame.display.update()

class Game(object):
    def __init__(self, width, height, cell_size = 10):

        pygame.init()

        self.board = Board(width * cell_size, height * cell_size)

        self.fps_clock = pygame.time.Clock()

    def run(self): # main loop of the game
        while not self.handle_events():
            self.board.draw()
            self.fps_clock.tick(15)

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                return True
        
if __name__ == "__main__":
    game = Game(80, 40)
    game.run()


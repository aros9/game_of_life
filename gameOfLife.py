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
    
DEAD = 0
ALIVE = 1

class Population(object):

    def __init__(self, width, height, cell_size = 10):
        self.box_size = cell_size
        self.height = height
        self.width = width
        self.generation = self.reset_generation()

    def reset_generation(self):
        # creates and returns an matrix of population
        return [[DEAD for y in range(self.height)] for x in range(self.width)]
    def handle_mouse(self):
        buttons = pygame.mouse.get_pressed()

        if not any(buttons): # ignore when no button is pressed
            return 

        alive = True if buttons[0] else False # add alive cell when first mouse button is pressed

        x, y = pygame.mouse.get_pos() # get coursor's position
        
        # convert coursor position from pixels to co-ordinates
        x /= self.box_size
        y /= self.box_size

        #


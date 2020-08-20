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

class GameOfLife(object): # main class
    def __init__(self, width, height, cell_size = 10):

        pygame.init()

        self.board = Board(width * cell_size, height * cell_size)

        self.fps_clock = pygame.time.Clock()
        self.population = Population(width, height, cell_size)

    def run(self): # main loop of the game
        while not self.handle_events():
            self.board.draw(self.population)
            if getattr(self, "started", None):
                self.population.cycle_generation()
            self.fps_clock.tick(10)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                return True
            from pygame.locals import MOUSEMOTION, MOUSEBUTTONDOWN
            if event.type == MOUSEMOTION or event.type == MOUSEBUTTONDOWN:
                self.population.handle_mouse()
            
            from pygame.locals import KEYDOWN, K_RETURN
            if event.type == KEYDOWN and event.key == K_RETURN:
                self.started = True
        


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

        # set state of cell in matrix
        self.generation[int(x)][int(y)] = ALIVE if alive else DEAD

    def draw_on(self, surface): # method used to draw cells
            for x, y in self.alive_cells():
                size = (self.box_size, self.box_size)
                position = (x * self.box_size, y * self.box_size)
                color = (46, 240, 161)
                thickness = 2
                pygame.draw.rect(surface, color, pygame.locals.Rect(position, size), thickness)
        
    def alive_cells(self): # returns co-ordinates of alive cells
        for x in range(len(self.generation)):
            column = self.generation[x]
            for y in range(len(column)):
                 if column[y] == ALIVE:
                    yield x, y

    def neighbours(self, x, y):
        for nx in range(x-1, x+2):
            for ny in range(y-1, y+2):
                if nx == x and ny == y: # ignore center
                    continue
                if nx >= self.width:
                    nx = 0
                elif nx < 0:
                    nx = self.width -1
                if ny >= self.height:
                    ny = 0
                elif ny < 0:
                    ny = self.height - 1
                yield self.generation[nx][ny]
    def cycle_generation(self): #generates another population of cells
        next_gen = self.reset_generation()
        for x in range(len(self.generation)):
            column = self.generation[x]
            for y in range(len(column)):
                count = sum(self.neighbours(x, y))
                if count == 3:
                    next_gen[x][y] = ALIVE # spreading
                elif count == 2: # moving on to another generation
                    next_gen[x][y] = column[y]
                else: # too many or too little neighbours to survive
                    next_gen[x][y] = DEAD

        self.generation = next_gen 

if __name__ == "__main__":
    game = GameOfLife(80, 40)
    game.run()
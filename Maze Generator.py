
import pygame
import time
import random
import os

# set up pygame window
WIDTH = 435
HEIGHT = 600

# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
LIME=(180,255,100)
RED=(255,0,0)
PURPLE=(240,0,255)

# initalise Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Maze Generator")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 36)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def redrawWindow():
    screen.fill((255, 255, 255))
    greenButton.draw(screen, (0, 0, 0))
    redButton.draw(screen, (0, 0, 255))


def redrawWindow1():
    limebutton.draw(screen, (0, 0, 0))
    bredbutton.draw(screen, (0, 0, 0))



greenButton = button((0, 255, 0), 85, 225, 250, 100, 'Play')
redButton = button((0, 0, 255), 85, 325, 250, 100, 'Quit')
limebutton=button(BLUE,200,450,75,40,'Play')
bredbutton=button(BLUE,200,500,75,40,'Hint')

def gamealgo():
    # setup maze variables
    x = 0  # x axis
    y = 0  # y axis
    w = 20  # width of cell
    FPS = 60

    grid = []
    visited = []
    stack = []
    solution = {}

    def build_grid(x, y, w):
        for i in range(1, 21):
            x = 20
            y = y + 20
            for j in range(1, 21):
                pygame.draw.line(screen, WHITE, [x, y], [x + w, y])
                pygame.draw.line(screen, WHITE, [x + w, y], [x + w, y + w])
                pygame.draw.line(screen, WHITE, [x + w, y + w], [x, y + w])
                pygame.draw.line(screen, WHITE, [x, y + w], [x, y])
                grid.append((x, y))
                x = x + 20

    def text(text, x, y, col1):
        screen_text = font.render(text, True, col1, )
        screen.blit(screen_text, [x, y])

    x, y = 20, 20
    build_grid(40, 0, 20)
    running = True
    while running:

        def push_up(x, y):
            pygame.draw.rect(screen, RED, (x + 1, y - w + 1, 19, 39), 0)
            pygame.display.update()

        def push_down(x, y):
            pygame.draw.rect(screen, RED, (x + 1, y + 1, 19, 39), 0)
            pygame.display.update()

        def push_left(x, y):
            pygame.draw.rect(screen, RED, (x - w + 1, y + 1, 39, 19), 0)
            pygame.display.update()

        def push_right(x, y):
            pygame.draw.rect(screen, RED, (x + 1, y + 1, 39, 19), 0)
            pygame.display.update()

        def single_cell(x, y):
            pygame.draw.rect(screen, LIME, (x + 1, y + 1, 18, 18), 0)
            pygame.display.update()

        def backtracking_cell(x, y):
            pygame.draw.rect(screen, RED, (x + 1, y + 1, 18, 18), 0)
            pygame.display.update()

        def solution_cell(x, y):
            pygame.draw.rect(screen, YELLOW, (x + 8, y + 8, 5, 5), 0)
            pygame.display.update()

        def carve_out_maze(x, y):
            single_cell(x, y)
            stack.append((x, y))
            visited.append((x, y))
            while len(stack) > 0:
                time.sleep(.005)
                cell = []
                if (x + w, y) not in visited and (x + w, y) in grid:
                    cell.append("right")

                if (x - w, y) not in visited and (x - w, y) in grid:
                    cell.append("left")

                if (x, y + w) not in visited and (x, y + w) in grid:
                    cell.append("down")

                if (x, y - w) not in visited and (x, y - w) in grid:
                    cell.append("up")

                if len(cell) > 0:
                    cell_chosen = (random.choice(cell))

                    if cell_chosen == "right":
                        push_right(x, y)
                        solution[(x + w, y)] = x, y
                        x = x + w
                        visited.append((x, y))
                        stack.append((x, y))

                    elif cell_chosen == "left":
                        push_left(x, y)
                        solution[(x - w, y)] = x, y
                        x = x - w
                        visited.append((x, y))
                        stack.append((x, y))

                    elif cell_chosen == "down":
                        push_down(x, y)
                        solution[(x, y + w)] = x, y
                        y = y + w
                        visited.append((x, y))
                        stack.append((x, y))

                    elif cell_chosen == "up":
                        push_up(x, y)
                        solution[(x, y - w)] = x, y
                        y = y - w
                        visited.append((x, y))
                        stack.append((x, y))
                else:
                    x, y = stack.pop()
                    single_cell(x, y)
                    time.sleep(.005)
                    backtracking_cell(x, y)

        def plot_hint_back(x, y):
            solution_cell(x, y)  # solution list contains all the coordinates to route back to start
            i = 0
            while i <= 50:  # loop until cell position == start position
                x, y = solution[x, y]  # "key value" now becomes the new key
                solution_cell(x, y)  # animate route back
                time.sleep(.3)
                i = i + 1

        def plot_route_back(x, y):
            solution_cell(x, y)
            while (x, y) != (20, 20):
                x, y = solution[x, y]
                solution_cell(x, y)
                time.sleep(.2)

        carve_out_maze(x, y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            redrawWindow1()
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if limebutton.isOver(pos):
                    plot_route_back(400, 400)
                if bredbutton.isOver(pos):
                    plot_hint_back(400, 400)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    x = x + 20
                if event.key == pygame.K_LEFT:
                    x = x - 20
                if event.key == pygame.K_UP:
                    y = y - 20
                if event.key == pygame.K_DOWN:
                    y = y + 20

                # def hint():
                #     pygame.draw.rect(screen, YELLOW, (0, 540, 120, 60))
                #     text("Hint", 38, 560, BLACK)
                #     if event.type == pygame.MOUSEBUTTONDOWN:
                #         plot_route_back(400, 400)
                #
                # hint()

                if x == 400 and y == 400:
                    screen.fill((0, 0, 0))
                    text("CONGO, MAZE SOLVED", 125, 250,WHITE)
                    text("press enter to play again", 120, 280,WHITE)
                    if event.key == pygame.K_RETURN:
                        screen.fill((0, 0, 0))
                        solve()


                    pygame.display.update()


            pygame.display.update()
            clock.tick(FPS)

    pygame.quit()
    quit()





def solve():
    FPS=60
    running=True
    while running:
        # keep running at the at the right speed
        redrawWindow()
        pygame.display.update()
        clock.tick(FPS)
        # process input (events)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            pos = pygame.mouse.get_pos()
            # check for closing the window
            if event.type == pygame.QUIT:
                os.system("taskkill /IM \"python.exe\" /F")
            if event.type == pygame.MOUSEBUTTONDOWN:

                if greenButton.isOver(pos):

                    screen.fill((0, 0, 0))
                    redrawWindow1()
                    x, y = 20, 20  # starting position of grid
                    # build_grid(40, 0, 20)  # 1st argument = x value, 2nd argument = y value, 3rd argument = width of cell
                    # carve_out_maze(x, y)  # call build the maze  function
                    # plot_route_back(900, 900)
                    gamealgo()
                    if limebutton.isOver(pos):
                        plot_route_back(400, 400)
                    if bredbutton.isOver(pos):
                        plot_hint_back(400, 400)
                if redButton.isOver(pos):
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEMOTION:
                if greenButton.isOver(pos):
                    greenButton.color = (255, 0, 0)
                else:
                    greenButton.color = (0, 255, 0)
                if redButton.isOver(pos):
                    redButton.color = (0, 0, 255)
                else:
                    redButton.color = (0, 255, 0)

solve()











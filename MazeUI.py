import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys

# Draw maze
def draw_maze(screen, cellList):
    height, width = len(cellList), len(cellList[0])

    # Draw UI
    pygame.font.init()
    mazeFont = pygame.font.SysFont('arial', 20)
    startText = mazeFont.render("Start", False, (0, 0, 0))
    goalText = mazeFont.render("Goal", False, (0, 0, 0))
    screen.blit(startText, (18, 0))
    screen.blit(goalText, (width * 50 - 15, 15 + height * 50))

    # Draw borders
    pygame.draw.line(screen, pygame.Color('black'), (20, 20), (20 + width * 50, 20))
    pygame.draw.line(screen, pygame.Color('black'), (20, 20 + height * 50), (20 + width * 50, 20 + height * 50))
    pygame.draw.line(screen, pygame.Color('black'), (20, 20), (20, 20 + height * 50))
    pygame.draw.line(screen, pygame.Color('black'), (20 + width * 50, 20), (20 + width * 50, 20 + height * 50))

    # Draw walls
    for i in range(height):
        for j in range(width):
            for wall in cellList[i][j].walls:
                if not wall.open:
                    wall_side_y = wall.parent_one.location[0] - wall.parent_two.location[0]
                    wall_side_x = wall.parent_one.location[1] - wall.parent_two.location[1]

                    if wall_side_y == 1:
                        pygame.draw.line(screen, pygame.Color('black'), (20 + j * 50, 20 + i * 50), (20 + (j + 1) * 50, 20 + i * 50))
                    elif wall_side_y == -1:
                        pygame.draw.line(screen, pygame.Color('black'), (20 + j * 50, 20 + (i + 1) * 50), (20 + (j + 1) * 50, 20 + (i + 1) * 50))
                    elif wall_side_x == -1:
                        pygame.draw.line(screen, pygame.Color('black'), (20 + (j + 1) * 50, 20 + i * 50), (20 + (j + 1) * 50, 20 + (i + 1) * 50))
                    elif wall_side_x == 1:
                        pygame.draw.line(screen, pygame.Color('black'), (20 + j * 50, 20 + i * 50), (20 + j * 50, 20 + (i + 1) * 50))
                    else:
                        print("Error in drawing wall!")
                        sys.exit()

# Draw solution on top of maze
def draw_solution():
    pass

def draw(cellList, command):
    height, width = len(cellList), len(cellList[0])
    SCREEN_WIDTH, SCREEN_HEIGHT = 40 + width * 50, 40 + height * 50

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption('Maze')
    screen.fill((255, 255, 255))
    # button = pygame.Rect(100, 100, 50, 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     mouse_pos = event.pos
            #     if button.collidepoint(mouse_pos):
            #         #do stuff
            #         pygame.draw.rect(screen, [255, 0, 0], pygame.Rect(200, 200, 50, 50))
        draw_maze(screen, cellList)

        pygame.display.flip()
    pygame.quit()

    # if command == "maze":
    #     draw_maze()
    # elif command == "solve":
    #     draw_solution()

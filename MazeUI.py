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
def draw_solution(screen, path):
    for cell in path:
        pygame.draw.rect(screen, pygame.Color('green'), pygame.Rect(20 + cell.location[1] * 50, 20 + cell.location[0] * 50, 50, 50))

def draw(cellList, command, path):
    height, width = len(cellList), len(cellList[0])
    SCREEN_WIDTH, SCREEN_HEIGHT = 40 + width * 50, 40 + height * 50

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption('Maze')
    screen.fill((255, 255, 255))
    button = pygame.Rect(SCREEN_WIDTH / 2, 0, 60, 20)

    pygame.font.init()
    mazeFont = pygame.font.SysFont('arial', 20)
    buttonText = mazeFont.render("Solve!", False, (0, 0, 0))

    running = True
    while running:
        draw_maze(screen, cellList)
        pygame.draw.rect(screen, [200, 200, 200], button)
        screen.blit(buttonText, (SCREEN_WIDTH / 2, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button.collidepoint(mouse_pos):
                    draw_solution(screen, path)
                    pygame.display.flip()

        pygame.display.flip()
    pygame.quit()

    # if command == "maze":
    #     draw_maze()
    # elif command == "solve":
    #     draw_solution()

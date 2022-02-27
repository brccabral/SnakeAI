import sys
import pygame

from snake_game import SnakeGameAI


pygame.init()


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CLOCK_SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('SnakeAI')
clock = pygame.time.Clock()


games = [SnakeGameAI()]

while True:

    action = [0, 0, 0, 0]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            action = [event.key == pygame.K_LEFT, event.key == pygame.K_UP,
                      event.key == pygame.K_RIGHT, event.key == pygame.K_DOWN]

    for game in games:
        game.play_step(action)
        screen.blit(game.display, (0, 0))

    clock.tick(CLOCK_SPEED)

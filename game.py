import pygame
import numpy as np

# create window with preferred dimensions
WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode( (WIDTH, HEIGHT) )

# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 200, 200)
YELLOW = (255, 255, 0)
COLORS = [WHITE, RED, GREEN, BLUE, PINK, YELLOW]

# number - color mapping
COLOR_MAP = {i: x for i, x in enumerate(COLORS)}

ALLOWED_KEYS = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]

FPS = 60
rng = np.random.RandomState()
grid_width = 300
grid_height = 300

grid = rng.randint(0, 6, size=(6, 6))

pygame.display.set_caption("Fillzone")

my_color = BLUE

def draw_grid(grid, n):
  # size of the block
  blockSize = grid_height // n

  # draw each block
  for x in range(100, grid_width + 100, blockSize):
    for y in range(100, grid_height + 100, blockSize):
      rect = pygame.Rect(x, y, blockSize, blockSize)
      pygame.draw.rect(WIN, COLOR_MAP[grid[(x - 100) // blockSize, (y - 100) // blockSize]], rect, 0)
      
  pygame.display.update()

def process(key):
  pass
  # tengo que modificar de cierta manera el state, la matriz

def main():
  clock = pygame.time.Clock()
  running = True

  while running:
    clock.tick(FPS)

    # aca tenes el entry point para checkear los eventos, toque de teclas, click lo que sea
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

    draw_grid(grid, 5)
    

  pygame.quit()

if __name__ == "__main__":
  main()
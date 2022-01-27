import os
import sys

import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[1] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 50

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), (
                        self.left + x * self.cell_size, self.top + y * self.cell_size, self.cell_size,
                        self.cell_size), 0)
                    pygame.draw.rect(screen, (255, 255, 255), (
                        self.left + x * self.cell_size, self.top + y * self.cell_size, self.cell_size,
                        self.cell_size), 1)

    def get_cell(self, pos):
        x, y = pos
        x = (x - self.left) // self.cell_size
        y = (y - self.top) // self.cell_size
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return None
        return x, y

    def change(self):
        x, y = coords
        if self.board[y][x] == 1:
            self.board[y][x] = 0



pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
image = load_image("Harry Potter.jpg")
image = pygame.transform.scale(image, (0.45 * width, 0.9 * height))
background_image = pygame.image.load("data/background.jpg")
board = Board(7, 10)
board.left = int(0.5 * width)
board.top = int(0.05 * height)
running = True
circle_or_x = False
coords = (0,0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            coords = board.get_cell(event.pos)
            board.change()
    screen.fill((255, 255, 255))
    screen.blit(background_image, [0, 0])
    screen.blit(image, (0.5 * width, 0.05 * height))
    board.render(screen)
    pygame.display.flip()

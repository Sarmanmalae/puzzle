import os
import sys

import pygame


class HomeButton:
    def __init__(self, image_name, bg_color, scr):
        self.sc = scr
        self.color = bg_color
        self.image = pygame.image.load(f'data/{image_name}')
        self.image = pygame.transform.scale(self.image, (0.055 * width, 0.055 * width))
        self.center_x = 0.075 * width
        self.center_y = 0.9 * height
        self.r = 30
        self.im_rect = self.image.get_rect()
        self.x = self.center_x - self.im_rect.w // 2
        self.y = self.center_y - self.im_rect.h // 2 - 2

    def render(self):
        pygame.draw.circle(self.sc, self.color, (self.center_x, self.center_y), self.r)
        self.sc.blit(self.image, (self.x, self.y))

    def click(self, coords):
        return (self.center_x - coords[0]) ** 2 + (self.center_y - coords[1]) ** 2 <= self.r ** 2


def right_ratio():
    global image
    w, h = image.get_rect()[2:]
    coeff = h / w
    ans_h = 0.9 * height
    ans_w = ans_h // coeff
    image = pygame.transform.scale(image, (ans_w, ans_h))


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
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
    def __init__(self, rows, cols, w, y):
        self.rows = rows
        self.cols = cols
        self.board = [[1] * w for _ in range(cols)]
        self.left = int(0.5 * width - image.get_width() // 2)
        self.top = int(0.05 * height)
        self.cell_x = w / rows
        self.cell_y = y / cols
        self.font = pygame.font.SysFont('britannic', 25)

    def render(self, screen):
        for y in range(self.cols):
            for x in range(self.rows):
                if self.board[y][x] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), (
                        self.left + x * self.cell_x, self.top + y * self.cell_y, self.cell_x,
                        self.cell_y), 0)
                    pygame.draw.rect(screen, (255, 255, 255), (
                        self.left + x * self.cell_x, self.top + y * self.cell_y, self.cell_x,
                        self.cell_y), 1)
                    num = x + 1 + self.rows * y
                    num = self.font.render(str(num), True, pygame.Color('red'))
                    _x = self.left + x * self.cell_x + self.cell_x // 2 - num.get_width() // 2
                    _y = self.top + y * self.cell_y + self.cell_y // 2 - num.get_height() // 2
                    screen.blit(num, (_x, _y))

    def get_cell(self, pos):
        x, y = pos
        x = (x - self.left) // self.cell_x
        y = (y - self.top) // self.cell_y
        if x < 0 or y < 0 or x >= self.rows or y >= self.cols:
            return None
        return x, y

    def change(self, coords):
        coords = self.get_cell(coords)
        if coords:
            x, y = map(int, coords)
            if self.board[y][x] == 1:
                self.board[y][x] = 0


pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
image = load_image("kiralik ask.jfif")
right_ratio()
home_btn = HomeButton('home.png', pygame.Color('dark red'), screen)
background_image = pygame.image.load("data/background.jpg")
board = Board(4, 5, image.get_width(), image.get_height())
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.change(event.pos)
            if home_btn.click(event.pos):
                print('Выход')
    screen.fill((255, 255, 255))
    screen.blit(background_image, [0, 0])
    screen.blit(image, (0.5 * width - image.get_width() // 2, 0.05 * height))
    board.render(screen)
    home_btn.render()
    pygame.display.flip()

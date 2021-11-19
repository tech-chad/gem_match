# gem match
import random
from time import sleep

from typing import Tuple

import pygame

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650
LIGHT_PURPLE = (130, 30, 255)
BG_COLOR = (40, 40, 40)
WHITE = (255, 255, 255)
SELECTED_CELL_COLOR = (255, 200, 20)
RED = (255, 0, 0)


class Score:
    def __init__(self):
        self.score = 0
        self.bonus = 0

    def add_score(self):
        self.score += 10 + self.bonus * 5
        self.bonus += 1

    def get_score(self):
        return self.score

    def reset_bonus(self):
        self.bonus = 0


class Images:
    def __init__(self):
        self.bg = pygame.image.load("images/background.jpeg")
        self.gem_images = []
        self._load_gem_images()

    def background(self):
        return self.bg

    def get_gem_image(self, gem_number: int):
        return self.gem_images[gem_number - 1]

    def _load_gem_images(self):
        gem1 = pygame.image.load("images/gem1.png")
        gem2 = pygame.image.load("images/gem2.png")
        gem3 = pygame.image.load("images/gem3.png")
        gem4 = pygame.image.load("images/gem4.png")
        gem5 = pygame.image.load("images/gem5.png")
        gem6 = pygame.image.load("images/gem6.png")
        gem7 = pygame.image.load("images/gem7.png")
        gem8 = pygame.image.load("images/gem8.png")
        self.gem_images = [gem1, gem2, gem3, gem4, gem5, gem6, gem7, gem8]




class GameBoard:
    def __init__(self, start_level: int, game_score):
        self.level = start_level
        self.game_score = game_score
        self.number_of_gems = 7
        self.game_board = [[0 for _ in range(8)] for _ in range(8)]
        self._init_game_board()

    def get_game_board(self) -> list:
        return self.game_board

    def add_random_gem(self, x: int, y: int):
        self.game_board[y][x] = random.randint(1, self.number_of_gems)

    def get_single_gem(self, x: int, y: int) -> int:
        return self.game_board[y][x]

    def flip_cells(self, x1: int, y1: int, x2: int, y2: int):
        self.game_board[y1][x1], self.game_board[y2][x2] = \
            self.game_board[y2][x2], self.game_board[y1][x1]

    def move_cell1_to_cell2(self, x1: int, y1: int, x2: int, y2: int):
        self.game_board[y2][x2] = self.game_board[y1][x1]

    def remove_single_cell(self, x: int, y: int):
        self.game_board[y][x] = 0

    def check_if_valid_flip(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        if self.game_board[y1][x1] == self.game_board[y2][x2]:
            return False
        self.game_board[y1][x1], self.game_board[y2][x2] = \
            self.game_board[y2][x2], self.game_board[y1][x1]
        item_1 = self.game_board[y1][x1]
        item_2 = self.game_board[y2][x2]
        result = False

        if x1 <= 6 and self.game_board[y1][x1 + 1] == item_1:
            if x1 <= 5 and self.game_board[y1][x1 + 2] == item_1:
                result = True
            if x1 >= 1 and self.game_board[y1][x1 - 1] == item_1:
                result = True
        # left
        if x1 >= 1 and self.game_board[y1][x1 - 1] == item_1:
            if x1 >= 2 and self.game_board[y1][x1 - 2] == item_1:
                result = True
        # down
        if y1 <= 6 and self.game_board[y1 + 1][x1] == item_1:
            if y1 <= 5 and self.game_board[y1 + 2][x1] == item_1:
                result = True
            if y1 >= 1 and self.game_board[y1 - 1][x1] == item_1:
                result = True
        # up
        if y1 >= 1 and self.game_board[y1 - 1][x1] == item_1:
            if y1 >= 2 and self.game_board[y1 - 2][x1] == item_1:
                result = True

        if x2 <= 6 and self.game_board[y2][x2 + 1] == item_2:
            if x2 <= 5 and self.game_board[y2][x2 + 2] == item_2:
                result = True
            if x2 >= 1 and self.game_board[y2][x2 - 1] == item_2:
                result = True
        # left
        if x2 >= 1 and self.game_board[y2][x2 - 1] == item_2:
            if x2 >= 2 and self.game_board[y2][x2 - 2] == item_2:
                result = True
        # down
        if y2 <= 6 and self.game_board[y2 + 1][x2] == item_2:
            if y2 <= 5 and self.game_board[y2 + 2][x2] == item_2:
                result = True
            if y2 >= 1 and self.game_board[y2 - 1][x2] == item_2:
                result = True
        # up
        if y2 >= 1 and self.game_board[y2 - 1][x2] == item_2:
            if y2 >= 2 and self.game_board[y2 - 2][x2] == item_2:
                result = True

        self.game_board[y1][x1], self.game_board[y2][x2] = \
            self.game_board[y2][x2], self.game_board[y1][x1]
        return result

    def _init_game_board(self):
        # this could be more efficient
        for y in range(8):
            for x in range(8):
                while True:
                    gem = random.randint(1, self.number_of_gems)
                    # right
                    if x <= 6 and self.game_board[y][x + 1] == gem:
                        if x <= 5 and self.game_board[y][x + 2] == gem:
                            continue
                        if x >= 1 and self.game_board[y][x - 1] == gem:
                            if x >= 2 and self.game_board[y][x - 2] == gem:
                                continue
                    # left
                    if x >= 1 and self.game_board[y][x - 1] == gem:
                        if x >= 2 and self.game_board[y][x - 2] == gem:
                            continue
                    # down
                    if y <= 6 and self.game_board[y + 1][x] == gem:
                        if y <= 5 and self.game_board[y + 2][x] == gem:
                            continue
                        if y >= 1 and self.game_board[y - 1][x] == gem:
                            if y >= 2 and self.game_board[y - 2][x] == gem:
                                continue
                    # up
                    if y >= 1 and self.game_board[y - 1][x] == gem:
                        if y >= 2 and self.game_board[y - 2][x] == gem:
                            continue
                    self.game_board[y][x] = gem
                    break

    def remove_matches(self) -> bool:
        h_remove_list = []
        v_remove_list = []
        for y in range(8):
            for x in range(7):
                if self.game_board[y][x] == 0 or (x, y) in h_remove_list:
                    continue
                temp_list = []
                g = self.game_board[y][x]
                g_count = 1
                temp_list.append((x, y))
                for x2 in range(x + 1, 8):
                    if self.game_board[y][x2] == g:
                        g_count += 1
                        temp_list.append((x2, y))
                        if x2 == 7 and g_count >= 3:
                            h_remove_list += temp_list
                            self.game_score.add_score()
                            break
                    elif g_count >= 3:
                        h_remove_list += temp_list
                        self.game_score.add_score()
                        break
                    else:
                        break
        for x in range(8):
            for y in range(7):
                if self.game_board[y][x] == 0 or (x, y) in v_remove_list:
                    continue
                temp_list = []
                g = self.game_board[y][x]
                g_count = 1
                temp_list.append((x, y))
                for y2 in range(y + 1, 8):
                    if self.game_board[y2][x] == g:
                        g_count += 1
                        temp_list.append((x, y2))
                        if y2 == 7 and g_count >= 3:
                            v_remove_list += temp_list
                            self.game_score.add_score()
                            break
                    elif g_count >= 3:
                        v_remove_list += temp_list
                        self.game_score.add_score()
                        break
                    else:
                        break
        remove_list = set(h_remove_list + v_remove_list)
        if len(remove_list) == 0:
            return False
        else:
            for rem in remove_list:
                self.game_board[rem[1]][rem[0]] = 0
            return True

    def are_there_valid_moves(self) -> bool:
        for x in range(8):
            for y in range(8):
                if x >= 1 and self.check_if_valid_flip(x, y, x - 1, y):
                    return True
                elif x <= 6 and self.check_if_valid_flip(x, y, x + 1, y):
                    return True
                elif y >= 1 and self.check_if_valid_flip(x, y, x, y - 1):
                    return True
                elif y <= 6 and self.check_if_valid_flip(x, y, x, y + 1):
                    return True
        return False


class Display:
    def __init__(self, win: pygame.Surface, game_score, game_board):
        self.win = win
        self.game_score = game_score
        self.game_board = game_board
        self.font_70 = pygame.font.SysFont("comicsans", 70, bold=True)
        self.font_44 = pygame.font.SysFont("comicsans", 44)
        self.images = Images()
        self.selected_cell_1 = ()
        self.selected_cell_2 = ()

    def _display(self, gb: list):
        self.win.fill(color=BG_COLOR)
        self.win.blit(self.images.background(), (0, 0))
        row = col = 0
        for y in range(len(gb)):
            for x in range(len(gb[y])):
                if gb[y][x] == 0:
                    continue
                if y == 0:
                    row = 2
                elif y == 1:
                    row = 77
                elif y == 2:
                    row = 152
                elif y == 3:
                    row = 227
                elif y == 4:
                    row = 302
                elif y == 5:
                    row = 377
                elif y == 6:
                    row = 452
                elif y == 7:
                    row = 527
                if x == 0:
                    col = 2
                elif x == 1:
                    col = 77
                elif x == 2:
                    col = 152
                elif x == 3:
                    col = 227
                elif x == 4:
                    col = 302
                elif x == 5:
                    col = 377
                elif x == 6:
                    col = 452
                elif x == 7:
                    col = 527
                gem = gb[y][x]
                self.win.blit(self.images.get_gem_image(gem), (col, row))
        text = f"Score: {self.game_score.get_score()}"
        score_text = self.font_44.render(text, True, WHITE)
        self.win.blit(score_text, (5, 610))
        pygame.display.update()

    def reset_display(self):
        self.win.fill(color=BG_COLOR)
        self.win.blit(self.images.background(), (0, 0))
        gb = self.game_board.get_game_board()
        row = col = 0
        for y in range(8):
            for x in range(8):
                if gb[y][x] == 0:
                    continue
                if y == 0:
                    row = 2
                elif y == 1:
                    row = 77
                elif y == 2:
                    row = 152
                elif y == 3:
                    row = 227
                elif y == 4:
                    row = 302
                elif y == 5:
                    row = 377
                elif y == 6:
                    row = 452
                elif y == 7:
                    row = 527
                if x == 0:
                    col = 2
                elif x == 1:
                    col = 77
                elif x == 2:
                    col = 152
                elif x == 3:
                    col = 227
                elif x == 4:
                    col = 302
                elif x == 5:
                    col = 377
                elif x == 6:
                    col = 452
                elif x == 7:
                    col = 527
                gem = gb[y][x]
                self.win.blit(self.images.get_gem_image(gem), (col, row))
        self._highlight_selected_cells()
        text = f"Score: {self.game_score.get_score()}"
        score_text = self.font_44.render(text, True, WHITE)
        self.win.blit(score_text, (5, 610))
        pygame.display.update()

    def _highlight_selected_cells(self):
        # grid_x = self.selected_cell_1[0]
        # grid_y = self.selected_cell_1[1]
        for cell in [self.selected_cell_1, self.selected_cell_2]:
            if cell == ():
                continue
            grid_x = cell[0]
            grid_y = cell[1]
            if grid_x == 0:
                x = 0
            elif grid_x == 1:
                x = 75
            elif grid_x == 2:
                x = 150
            elif grid_x == 3:
                x = 225
            elif grid_x == 4:
                x = 300
            elif grid_x == 5:
                x = 375
            elif grid_x == 6:
                x = 450
            elif grid_x == 7:
                x = 525
            else:
                continue
            if grid_y == 0:
                y = 0
            elif grid_y == 1:
                y = 75
            elif grid_y == 2:
                y = 150
            elif grid_y == 3:
                y = 225
            elif grid_y == 4:
                y = 300
            elif grid_y == 5:
                y = 375
            elif grid_y == 6:
                y = 450
            elif grid_y == 7:
                y = 525
            else:
                continue
            pygame.draw.rect(self.win, SELECTED_CELL_COLOR, (x, y, 75, 75), width=5)

    def display_full_fill_2(self):
        gb = self.game_board.get_game_board()
        fill_gb = []
        for fill_y in range(7, -1, -1):
            fill_gb.insert(0, [])
            for x in range(8):
                fill_gb[0].append(gb[fill_y][x])
                self._display(fill_gb)
                sleep(0.02)
            sleep(0.01)

    def set_selected_cell(self, x: int, y: int, selected_num: int):
        if selected_num == 1:
            self.selected_cell_1 = (x, y)
        elif selected_num == 2:
            self.selected_cell_2 = (x, y)

    def selected_cell_reset(self):
        self.selected_cell_1 = ()
        self.selected_cell_2 = ()

    def fill_in_game_board(self):
        self.reset_display()
        for y in range(7, -1, -1):
            for x in range(8):
                if y == 0 and self.game_board.get_single_gem(x, y) == 0:
                    self.game_board.add_random_gem(x, y)
                elif self.game_board.get_single_gem(x, y) == 0:
                    for y2 in range(y - 1, -1, -1):
                        if y2 == 0 and self.game_board.get_single_gem(x, y2) == 0:
                            self.game_board.add_random_gem(x, y)
                            break
                        elif self.game_board.get_single_gem(x, y2) != 0:
                            self.game_board.move_cell1_to_cell2(x, y2, x, y)
                            self.game_board.remove_single_cell(x, y2)
                            break
                else:
                    continue
            self.reset_display()
            sleep(0.1)

    def show_game_over(self):
        text1 = self.font_70.render("No more valid moves", True, RED)
        text2 = self.font_70.render("Game Over", True, RED)
        self.win.blit(text2, (150, 200))
        self.win.blit(text1, (22, 275))
        pygame.display.update()


def get_grid_location(mouse_x: int, mouse_y: int) -> Tuple[int, int]:
    # returns the game_board x,y location
    col = row = -1
    if 0 < mouse_x < 75:
        col = 0
    elif 75 < mouse_x < 150:
        col = 1
    elif 150 < mouse_x < 225:
        col = 2
    elif 225 < mouse_x < 300:
        col = 3
    elif 300 < mouse_x < 375:
        col = 4
    elif 375 < mouse_x < 450:
        col = 5
    elif 450 < mouse_x < 525:
        col = 6
    elif 525 < mouse_x < 600:
        col = 7
    if 0 < mouse_y < 75:
        row = 0
    elif 75 < mouse_y < 150:
        row = 1
    elif 150 < mouse_y < 225:
        row = 2
    elif 225 < mouse_y < 300:
        row = 3
    elif 300 < mouse_y < 375:
        row = 4
    elif 375 < mouse_y < 450:
        row = 5
    elif 450 < mouse_y < 525:
        row = 6
    elif 525 < mouse_y < 600:
        row = 7
    if col == -1 or row == -1:
        col = row = -1
    return col, row


def check_if_adjacent(x1: int, y1: int, x2: int, y2: int) -> bool:
    if y1 == y2 and abs(x1 - x2) == 1:
        return True
    elif x1 == x2 and abs(y1 - y2) == 1:
        return True
    else:
        return False


def main_game(win: pygame.Surface) -> None:
    # clock = pygame.time.Clock()
    # clock.tick(50)
    game_score = Score()
    game_board = GameBoard(1, game_score)
    display = Display(win, game_score, game_board)
    display.display_full_fill_2()
    first_selected = (-1, -1)
    play = True
    game_over = False
    while play:
        display.reset_display()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_y >= 600:
                    pass
                elif first_selected == (-1, -1):
                    loc_x, loc_y = get_grid_location(mouse_x, mouse_y)
                    if loc_x == -1 or loc_y == -1:
                        pass  # invalid selection
                    first_selected = (loc_x, loc_y)
                    display.set_selected_cell(loc_x, loc_y, 1)
                else:
                    loc_x, loc_y = get_grid_location(mouse_x, mouse_y)
                    if check_if_adjacent(*first_selected, loc_x, loc_y):
                        display.set_selected_cell(loc_x, loc_y, 2)
                        sleep(0.05)
                        if game_board.check_if_valid_flip(*first_selected, loc_x, loc_y):
                            game_board.flip_cells(*first_selected, loc_x, loc_y)
                            display.reset_display()
                            sleep(0.3)
                            display.selected_cell_reset()
                            first_selected = (-1, -1)
                            while game_board.remove_matches():
                                display.fill_in_game_board()
                                sleep(0.1)
                            for event2 in pygame.event.get():
                                if event2.type == pygame.MOUSEBUTTONDOWN:
                                    pass
                            game_score.reset_bonus()
                            if not game_board.are_there_valid_moves():
                                play = False
                                game_over = True
                        else:
                            game_board.flip_cells(*first_selected, loc_x, loc_y)
                            display.reset_display()
                            sleep(0.3)
                            game_board.flip_cells(*first_selected, loc_x, loc_y)
                            display.selected_cell_reset()
                            display.reset_display()
                    elif loc_x == -1 or loc_y == -1:
                        pass  # invalid selection
                    else:
                        first_selected = (loc_x, loc_y)
                        display.set_selected_cell(loc_x, loc_y, 1)
    if game_over:
        display.show_game_over()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False


def welcome_screen(win: pygame.Surface) -> bool:
    # return True - Play
    # return False - Quit
    font_50 = pygame.font.SysFont("comicsans", 50)
    font_30 = pygame.font.SysFont("comicsans", 30, False)
    welcome_text = font_50.render("Welcome to Gem Match", True, LIGHT_PURPLE)
    start_text = font_30.render("Click anywhere to start", True, WHITE)
    win.fill(color=BG_COLOR)
    win.blit(welcome_text, (100, 50))
    win.blit(start_text, (180, 200))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return True

def main() -> None:
    pygame.init()
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Gem Match")
    if welcome_screen(win):
        main_game(win)


if __name__ == "__main__":
    main()

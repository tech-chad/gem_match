# gem match
import os
import random
from time import sleep

from typing import Tuple

import pygame

HERE = os.path.dirname(os.path.abspath(__file__))

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650
LIGHT_PURPLE = (130, 30, 255)
BG_COLOR = (40, 40, 40)
WHITE = (255, 255, 255)
SELECTED_CELL_COLOR = (255, 200, 20)
HINT_CELL_COLOR = (0, 255, 90)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
DARK_GRAY = (100, 100, 100)
TIME_FOR_HINT = 10000


class Score:
    def __init__(self, game_level):
        self.score = 0
        self.bonus = 0
        self.game_level = game_level
        self.level_score = 0

    def add_score(self):
        # True if level up else False
        self.score += 10 + self.bonus * 5 + self.game_level.point_modifier
        self.level_score += 10 + self.bonus * 5
        self.bonus += 1
        if self.level_score >= self.game_level.score_next_level:
            self.game_level.increase_level()
            self.level_score = 0

    def get_score(self):
        return self.score

    def reset_bonus(self):
        self.bonus = 0

    def reset_score(self) -> None:
        self.score = 0
        self.bonus = 0
        self.level_score = 0


class Levels:
    def __init__(self):
        self.level = 1
        # self.max_level = 20  # not set
        self.number_of_gems = 7
        self.max_number_of_gems = 15
        self.point_modifier = 0
        self.score_next_level = 300
        self.num_gems_remove = 2
        self.new_level = False

    def increase_level(self) -> None:
        self.level += 1
        if self.level % 2 != 0 and self.number_of_gems < self.max_number_of_gems:
            self.number_of_gems += 1
        self.point_modifier += 10
        self.score_next_level *= self.level
        self.num_gems_remove += 1
        self.new_level = True

    def reset_level(self) -> None:
        self.level = 1
        self.number_of_gems = 7
        self.point_modifier = 0
        self.num_gems_remove = 2
        self.score_next_level = 300

    def moved_to_new_level(self) -> bool:
        if self.new_level:
            self.new_level = False
            return True
        else:
            return False


class Images:
    def __init__(self):
        self.bg = pygame.image.load(os.path.join(HERE, "images/background.jpeg"))
        self.gem_images = []
        self.gem_flash = None
        self._load_gem_images()

    def background(self):
        return self.bg

    def get_gem_image(self, gem_number: int):
        return self.gem_images[gem_number - 1]

    def _load_gem_images(self):
        gem1 = pygame.image.load(os.path.join(HERE, "images/gem1.png"))
        gem2 = pygame.image.load(os.path.join(HERE, "images/gem2.png"))
        gem3 = pygame.image.load(os.path.join(HERE, "images/gem3.png"))
        gem4 = pygame.image.load(os.path.join(HERE, "images/gem4.png"))
        gem5 = pygame.image.load(os.path.join(HERE, "images/gem5.png"))
        gem6 = pygame.image.load(os.path.join(HERE, "images/gem6.png"))
        gem7 = pygame.image.load(os.path.join(HERE, "images/gem7.png"))
        gem8 = pygame.image.load(os.path.join(HERE, "images/gem8.png"))
        gem9 = pygame.image.load(os.path.join(HERE, "images/gem9.png"))
        gem10 = pygame.image.load(os.path.join(HERE, "images/gem10.png"))
        gem11 = pygame.image.load(os.path.join(HERE, "images/gem11.png"))
        gem12 = pygame.image.load(os.path.join(HERE, "images/gem12.png"))
        gem13 = pygame.image.load(os.path.join(HERE, "images/gem13.png"))
        gem14 = pygame.image.load(os.path.join(HERE, "images/gem14.png"))
        gem15 = pygame.image.load(os.path.join(HERE, "images/gem15.png"))
        self.gem_flash = pygame.image.load(os.path.join(HERE, "images/gem_flash2.png"))

        self.gem_images = [gem1, gem2, gem3, gem4, gem5, gem6, gem7, gem8,
                           gem9, gem10, gem11, gem12, gem13, gem14, gem15]


class GameBoard:
    def __init__(self, start_level: int, game_score, game_level):
        self.level = start_level
        self.game_score = game_score
        self.game_level = game_level
        self.game_board = [[0 for _ in range(8)] for _ in range(8)]
        self._init_game_board()

    def get_game_board(self) -> list:
        return self.game_board

    def reset_game_board(self) -> None:
        self.game_board = [[0 for _ in range(8)] for _ in range(8)]
        self._init_game_board()

    def add_random_gem(self, x: int, y: int):
        self.game_board[y][x] = random.randint(1, self.game_level.number_of_gems)

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
                    gem = random.randint(1, self.game_level.number_of_gems)
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

    def remove_random_gems(self):
        random_list = []
        for _ in range(self.game_level.num_gems_remove):
            while True:
                loc = (random.randint(0, 7), random.randint(0, 7))
                if loc not in random_list:
                    random_list.append(loc)
                    break
        for loc in random_list:
            self.game_board[loc[1]][loc[0]] = 0

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

    def get_hint(self) -> Tuple[int, int]:
        for x in range(8):
            for y in range(8):
                if x >= 1 and self.check_if_valid_hint(x, y, x - 1, y):
                    return x, y
                elif x <= 6 and self.check_if_valid_hint(x, y, x + 1, y):
                    return x, y
                elif y >= 1 and self.check_if_valid_hint(x, y, x, y - 1):
                    return x, y
                elif y <= 6 and self.check_if_valid_hint(x, y, x, y + 1):
                    return x, y

    def check_if_valid_hint(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        if self.game_board[y1][x1] == self.game_board[y2][x2]:
            return False
        self.game_board[y1][x1], self.game_board[y2][x2] = \
            self.game_board[y2][x2], self.game_board[y1][x1]
        item_2 = self.game_board[y2][x2]
        result = False

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


class Display:
    def __init__(self, win: pygame.Surface, game_score, game_board, game_level):
        self.win = win
        self.game_score = game_score
        self.game_board = game_board
        self.game_level = game_level
        self.font_70 = pygame.font.SysFont("comicsans", 70, bold=True)
        self.font_44 = pygame.font.SysFont("comicsans", 44)
        self.font_24 = pygame.font.SysFont("comicsans", 24)
        self.images = Images()
        self.selected_cell_1 = ()
        self.selected_cell_2 = ()
        self.display_hint = False
        self.hint = (0, 0)

    def _display(self, gb: list):
        self.win.fill(color=BG_COLOR)
        self.win.blit(self.images.background(), (0, 0))
        for y in range(len(gb)):
            for x in range(len(gb[y])):
                if gb[y][x] == 0:
                    continue
                row = get_grid(y)
                col = get_grid(x)
                gem = gb[y][x]
                self.win.blit(self.images.get_gem_image(gem), (col, row))
        text = f"Score: {self.game_score.get_score()}"
        score_text = self.font_44.render(text, True, WHITE)
        self.win.blit(score_text, (5, 610))
        pygame.display.update()

    def display_gem_remove_flash(self):
        gb = self.game_board.get_game_board()
        for y in range(8):
            for x in range(8):
                if gb[y][x] == 0:
                    row = get_grid(y)
                    col = get_grid(x)
                    self.win.blit(self.images.gem_flash, (col, row))
        pygame.display.update()

    def reset_display(self):
        self.win.fill(color=BG_COLOR)
        self.win.blit(self.images.background(), (0, 0))
        gb = self.game_board.get_game_board()
        for y in range(8):
            for x in range(8):
                if gb[y][x] == 0:
                    continue
                row = get_grid(y)
                col = get_grid(x)

                gem = gb[y][x]
                self.win.blit(self.images.get_gem_image(gem), (col, row))
        self._highlight_selected_cells()
        text = f"Score: {self.game_score.get_score()}"
        score_text = self.font_44.render(text, True, WHITE)
        self.win.blit(score_text, (5, 610))
        self.level_bar()
        if self.display_hint:
            self.display_hint_on_screen()
        pygame.display.update()

    def level_bar(self):
        start_x = int(SCREEN_WIDTH / 2)
        start_y = 610
        empty = pygame.rect.Rect((start_x, start_y, int(SCREEN_WIDTH / 2), 30))
        pygame.draw.rect(self.win, (180, 180, 180), empty, border_radius=4)
        score = self.game_score.level_score / self.game_level.score_next_level
        filled = pygame.rect.Rect((start_x, start_y, int(SCREEN_WIDTH / 2) * score, 30))
        level_txt = self.font_24.render(f"Level {self.game_level.level}", True, WHITE)
        pygame.draw.rect(self.win, (0, 50, 200), filled, border_radius=4)
        txt_x = start_x + int(start_x / 2) - int(level_txt.get_width() / 2)
        txt_y = start_y + int(level_txt.get_height() / 2)
        self.win.blit(level_txt, (txt_x, txt_y))

    def display_hint_on_screen(self) -> None:
        grid_x, grid_y = self.hint
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
            x = -100
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
            y = -100
        pygame.draw.rect(self.win, HINT_CELL_COLOR, (x, y, 75, 75), width=5)
        pygame.display.update()

    def _highlight_selected_cells(self):
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
        self.win.blit(text2, (150, 125))
        self.win.blit(text1, (22, 200))
        pygame.display.update()


def get_grid(a: int) -> int:
    if a == 0:
        return 2
    elif a == 1:
        return 77
    elif a == 2:
        return 152
    elif a == 3:
        return 227
    elif a == 4:
        return 302
    elif a == 5:
        return 377
    elif a == 6:
        return 452
    elif a == 7:
        return 527
    else:
        return 0


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


def quit_confirm() -> bool:
    win = pygame.display.get_surface()
    size = (int(SCREEN_WIDTH / 2) - 200, int(SCREEN_HEIGHT / 2) - 100, 400, 200)
    font_30 = pygame.font.SysFont("comicsans", 30, False)
    font_50 = pygame.font.SysFont("comicsans", 50)
    message = font_50.render("Confirm Quit?", True, BLACK)
    yes = font_30.render("YES", True, BLACK)
    no = font_30.render("NO", True, BLACK)
    button1 = pygame.rect.Rect((size[0] + 50, size[1] + 100, 75, 50))
    button2 = pygame.rect.Rect((size[0] + size[2] - 125, size[1] + 100, 75, 50))
    pygame.draw.rect(win, DARK_GRAY, size, border_radius=4)
    pygame.draw.rect(win, BLACK, size, width=3, border_radius=4)
    message_pos = (int(SCREEN_WIDTH / 2) - int(message.get_width() / 2), size[1] + 20)
    win.blit(message, message_pos)
    pygame.draw.rect(win, WHITE, button1, border_radius=8)
    pygame.draw.rect(win, WHITE, button2, border_radius=8)
    yes_pos_x = (button1.x + int(button1.width / 2) - int(yes.get_width() / 2))
    yes_pos_y = (button1.y + int(button1.height / 2) - int(yes.get_height() / 2))
    win.blit(yes, (yes_pos_x, yes_pos_y))
    no_pos_x = (button2.x + int(button2.width / 2) - int(no.get_width() / 2))
    no_pos_y = (button2.y + int(button2.height / 2) - int(no.get_height() / 2))
    win.blit(no, (no_pos_x, no_pos_y))
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button1.collidepoint(mouse_x, mouse_y):
                    return True
                elif button2.collidepoint(mouse_x, mouse_y):
                    return False


def play_again():
    win = pygame.display.get_surface()
    size = (int(SCREEN_WIDTH / 2) - 200, int(SCREEN_HEIGHT / 2), 400, 200)
    font_30 = pygame.font.SysFont("comicsans", 30, False)
    font_50 = pygame.font.SysFont("comicsans", 50)
    message = font_50.render("Play Again?", True, BLACK)
    yes = font_30.render("YES", True, LIGHT_PURPLE)
    no = font_30.render("NO", True, LIGHT_PURPLE)
    button1 = pygame.rect.Rect((size[0] + 50, size[1] + 100, 75, 50))
    button2 = pygame.rect.Rect((size[0] + size[2] - 125, size[1] + 100, 75, 50))
    pygame.draw.rect(win, DARK_GRAY, size, border_radius=4)
    pygame.draw.rect(win, BLACK, size, width=3, border_radius=4)
    message_pos = (int(SCREEN_WIDTH / 2) - int(message.get_width() / 2), size[1] + 20)
    win.blit(message, message_pos)
    pygame.draw.rect(win, WHITE, button1, border_radius=8)
    pygame.draw.rect(win, WHITE, button2, border_radius=8)
    yes_pos_x = (button1.x + int(button1.width / 2) - int(yes.get_width() / 2))
    yes_pos_y = (button1.y + int(button1.height / 2) - int(yes.get_height() / 2))
    win.blit(yes, (yes_pos_x, yes_pos_y))
    no_pos_x = (button2.x + int(button2.width / 2) - int(no.get_width() / 2))
    no_pos_y = (button2.y + int(button2.height / 2) - int(no.get_height() / 2))
    win.blit(no, (no_pos_x, no_pos_y))
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button1.collidepoint(mouse_x, mouse_y):
                    return True
                elif button2.collidepoint(mouse_x, mouse_y):
                    return False


def main_game(win: pygame.Surface) -> None:
    game_level = Levels()
    game_score = Score(game_level)
    game_board = GameBoard(1, game_score, game_level)
    display = Display(win, game_score, game_board, game_level)
    display.display_full_fill_2()
    first_selected = (-1, -1)
    pygame.time.set_timer(1, TIME_FOR_HINT)
    play = True
    while play:
        display.reset_display()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if quit_confirm():
                    play = False
            if event.type == 1:
                display.display_hint = True
                display.hint = game_board.get_hint()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                if quit_confirm():
                    play = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                display.display_hint = False
                pygame.time.set_timer(1, 0)
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
                            sleep(0.07)
                            display.selected_cell_reset()
                            first_selected = (-1, -1)
                            while game_board.remove_matches():
                                display.display_gem_remove_flash()
                                sleep(0.07)
                                display.fill_in_game_board()
                                sleep(0.07)
                            if game_level.moved_to_new_level():
                                game_board.remove_random_gems()
                                display.display_gem_remove_flash()
                                sleep(0.07)
                                display.fill_in_game_board()
                                while game_board.remove_matches():
                                    display.display_gem_remove_flash()
                                    sleep(0.07)
                                    display.fill_in_game_board()
                                    sleep(0.07)
                            for event2 in pygame.event.get():
                                if event2.type == pygame.MOUSEBUTTONDOWN:
                                    pass
                            game_score.reset_bonus()
                            if not game_board.are_there_valid_moves():
                                display.show_game_over()
                                sleep(0.3)
                                if play_again():
                                    game_level.reset_level()
                                    game_board.reset_game_board()
                                    game_score.reset_score()
                                    display.display_full_fill_2()
                                else:
                                    play = False
                            pygame.time.set_timer(1, TIME_FOR_HINT)
                        else:
                            game_board.flip_cells(*first_selected, loc_x, loc_y)
                            display.reset_display()
                            sleep(0.3)
                            game_board.flip_cells(*first_selected, loc_x, loc_y)
                            display.selected_cell_reset()
                            display.reset_display()
                            pygame.time.set_timer(1, TIME_FOR_HINT)
                    elif loc_x == -1 or loc_y == -1:
                        pass  # invalid selection
                    else:
                        first_selected = (loc_x, loc_y)
                        display.set_selected_cell(loc_x, loc_y, 1)


def welcome_screen(win: pygame.Surface) -> bool:
    # return True - Play and False - Quit
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

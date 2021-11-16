# gem match

import pygame

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650
LIGHT_PURPLE = (130, 30, 255)
BG_COLOR = (40, 40, 60)
WHITE = (255, 255, 255)

def welcome_screen(win: pygame.Surface) -> bool:
    # return True - Play
    # return False - Quit
    font_50 = pygame.font.SysFont("comicsans", 50, False)
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
    if welcome_screen(win):
        pass


if __name__ == "__main__":
    main()

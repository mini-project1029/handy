"""Modal-style popups (game over screen, etc.)."""

import sys
import time

import cv2
import pygame

from config import WINDOW_WIDTH, WINDOW_HEIGHT


def show_game_over_popup(screen, cap, message):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    font_big = pygame.font.SysFont("Segoe UI", 48, bold=True)
    font_small = pygame.font.SysFont("Segoe UI", 28)

    text = font_big.render(message, True, (255, 255, 255))
    rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
    screen.blit(text, rect)

    sub = font_small.render("Press any key or click to exit", True, (200, 200, 200))
    rect2 = sub.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
    screen.blit(sub, rect2)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.QUIT):
                waiting = False
                break
        time.sleep(0.05)

    cap.release()
    pygame.quit()
    cv2.destroyAllWindows()
    sys.exit()

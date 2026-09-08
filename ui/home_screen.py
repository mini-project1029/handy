"""Start screen shown before the main game loop begins."""

import sys

import cv2
import pygame

from config import WINDOW_WIDTH, WINDOW_HEIGHT


def show_home_screen(screen, cap):
    """Returns 'ai' or 'two_player' depending on which mode button is clicked."""
    screen.fill((15, 15, 15))

    title_font = pygame.font.SysFont("Segoe UI", 52, bold=True)
    button_font = pygame.font.SysFont("Segoe UI", 28)

    title = title_font.render("Handy Chess", True, (230, 230, 230))
    t_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
    screen.blit(title, t_rect)

    btn_width, btn_height = 280, 70
    gap = 24

    ai_rect = pygame.Rect(WINDOW_WIDTH // 2 - btn_width // 2, WINDOW_HEIGHT // 2 - 20, btn_width, btn_height)
    two_p_rect = pygame.Rect(WINDOW_WIDTH // 2 - btn_width // 2, WINDOW_HEIGHT // 2 - 20 + btn_height + gap, btn_width, btn_height)

    for rect, label in [(ai_rect, "Play vs AI"), (two_p_rect, "Two Player")]:
        pygame.draw.rect(screen, (230, 230, 230), rect, border_radius=12)
        btn_text = button_font.render(label, True, (20, 20, 20))
        screen.blit(btn_text, btn_text.get_rect(center=rect.center))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                cv2.destroyAllWindows()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if ai_rect.collidepoint(event.pos):
                    return "ai"
                if two_p_rect.collidepoint(event.pos):
                    return "two_player"

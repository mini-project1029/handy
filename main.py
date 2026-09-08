"""sip_chess entry point. Hand-gesture controlled chess.

Run with: python main.py
"""

import sys
import time

import cv2
import pygame

from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, CAMERA_WIDTH, CAMERA_HEIGHT, BOARD_SIZE,
    SELECTED_COLOR, HOVER_COLOR, INVALID_FLASH_COLOR,
    STARTUP_HINT_DURATION, INVALID_FLASH_DURATION, POST_MOVE_COOLDOWN,
)
from core.hand_tracker import HandTracker, INDEX_FINGER_TIP, FINGERTIP_IDS
from core.gesture import DwellClickDetector
from game.state import GameState
from game.engine import Engine
from game.player_model import PlayerModel
from ui.board_view import load_piece_images, draw_board, get_square_from_pos, square_center_pixels
from ui.home_screen import show_home_screen
from ui.popups import show_game_over_popup

import chess

PLAYER_COLOR = chess.WHITE  # human always plays white in AI mode


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("sip_chess")

    piece_images = load_piece_images()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not found.")
        sys.exit()

    mode = show_home_screen(screen, cap)  # 'ai' or 'two_player'

    tracker = HandTracker(max_hands=1)
    dwell = DwellClickDetector()
    state = GameState()

    player_model = PlayerModel() if mode == "ai" else None
    engine = Engine(depth=3, player_model=player_model) if mode == "ai" else None

    show_hands = True
    show_startup_hint = True
    hint_start_time = time.time()

    font = pygame.font.SysFont("Segoe UI", 20)

    while True:
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)
        h, w, _ = img.shape

        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (10, 10, 10), 20)
        img = cv2.addWeighted(overlay, 0.1, img, 0.9, 0)

        landmarks = tracker.process(img)
        raw_pos = None

        if landmarks:
            if show_hands:
                for tip_id in FINGERTIP_IDS:
                    x, y = landmarks[tip_id]
                    color = (0, 255, 0) if tip_id == INDEX_FINGER_TIP else (255, 50, 50)
                    cv2.circle(img, (x, y), 6, color, -1)
            raw_pos = landmarks[INDEX_FINGER_TIP]

        cursor_pos, valid_cursor, clicked = dwell.update(raw_pos, w, h)

        if cursor_pos:
            cv2.circle(img, cursor_pos, 8, (0, 255, 0), 2)

        now = time.time()
        # In AI mode, only accept clicks when it's the human's turn
        human_turn = mode != "ai" or state.board.turn == PLAYER_COLOR

        if clicked and valid_cursor and human_turn:
            bx = CAMERA_WIDTH + (cursor_pos[0] / w) * BOARD_SIZE
            by = (cursor_pos[1] / h) * BOARD_SIZE
            sq = get_square_from_pos(bx, by)
            if sq is not None:
                board_before = state.board.copy() if mode == "ai" else None
                from_sq = state.selected_square
                result = state.try_select_or_move(sq, POST_MOVE_COOLDOWN, now)

                if result == "moved":
                    if mode == "ai" and player_model is not None:
                        player_model.record_player_move(board_before, state.last_move, PLAYER_COLOR)

                    over = state.is_game_over()
                    if over:
                        if mode == "ai":
                            player_model.record_game_end()
                        draw_board(screen, state.board, state.last_move, piece_images)
                        pygame.display.flip()
                        show_game_over_popup(screen, cap, over)

        # AI's turn: pick and play a move (runs once, fast, between frames)
        if mode == "ai" and state.board.turn != PLAYER_COLOR and not state.board.is_game_over():
            ai_move = engine.select_move(state.board)
            if ai_move is not None:
                state.board.push(ai_move)
                state.last_move = ai_move
                state.last_move_time = time.time()

                over = state.is_game_over()
                if over:
                    player_model.record_game_end()
                    draw_board(screen, state.board, state.last_move, piece_images)
                    pygame.display.flip()
                    show_game_over_popup(screen, cap, over)

        cam_surface = pygame.surfarray.make_surface(cv2.cvtColor(img, cv2.COLOR_BGR2RGB).swapaxes(0, 1))
        screen.blit(cam_surface, (0, 0))
        draw_board(screen, state.board, state.last_move, piece_images)

        if state.selected_square is not None:
            col = chess.square_file(state.selected_square)
            row = chess.square_rank(state.selected_square)
            pygame.draw.rect(
                screen, SELECTED_COLOR,
                pygame.Rect(CAMERA_WIDTH + col * 80, (7 - row) * 80, 80, 80), 3,
            )

        if cursor_pos and valid_cursor:
            bx = CAMERA_WIDTH + (cursor_pos[0] / w) * BOARD_SIZE
            by = (cursor_pos[1] / h) * BOARD_SIZE
            hover_square = get_square_from_pos(bx, by)
            if hover_square is not None:
                cx, cy = square_center_pixels(hover_square)
                pygame.draw.circle(screen, HOVER_COLOR, (cx, cy), 6)

        if time.time() - state.invalid_flash_time < INVALID_FLASH_DURATION:
            pygame.draw.rect(screen, INVALID_FLASH_COLOR, (CAMERA_WIDTH, 0, BOARD_SIZE, BOARD_SIZE), 5)

        if show_startup_hint and time.time() - hint_start_time < STARTUP_HINT_DURATION:
            hint_font = pygame.font.SysFont("Segoe UI", 22)
            text = hint_font.render("Hold index steady to select, then hold again to move.", True, (200, 200, 200))
            screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 10))

        label = font.render("Hand Tracking Active  |  Press H to toggle hand overlay", True, (200, 200, 200))
        screen.blit(label, (20, WINDOW_HEIGHT - 30))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                cv2.destroyAllWindows()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    show_hands = not show_hands

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    tracker.close()
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()


if __name__ == "__main__":
    main()

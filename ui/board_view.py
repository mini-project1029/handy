"""Drawing the chessboard, pieces, and coordinate conversions."""

import os

import chess
import pygame

from config import (
    SQUARE_SIZE, CAMERA_WIDTH, LIGHT_SQUARE, DARK_SQUARE,
    FROM_SQUARE_COLOR, TO_SQUARE_COLOR, PIECES_DIR,
)


def load_piece_images():
    images = {}
    for color in ["w", "b"]:
        for piece in ["p", "n", "b", "r", "q", "k"]:
            path = os.path.join(PIECES_DIR, f"{color}{piece}.png")
            if os.path.exists(path):
                img = pygame.image.load(path)
                img = pygame.transform.smoothscale(img, (SQUARE_SIZE, SQUARE_SIZE))
                images[f"{color}{piece}"] = img
    return images


def draw_board(screen, board, last_move, piece_images):
    colors = [LIGHT_SQUARE, DARK_SQUARE]
    for r in range(8):
        for c in range(8):
            color = colors[(r + c) % 2]
            pygame.draw.rect(
                screen, color,
                pygame.Rect(CAMERA_WIDTH + c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            )

    if last_move:
        for sq, color in [(last_move.from_square, FROM_SQUARE_COLOR), (last_move.to_square, TO_SQUARE_COLOR)]:
            col = chess.square_file(sq)
            row = chess.square_rank(sq)
            pygame.draw.rect(
                screen, color,
                pygame.Rect(CAMERA_WIDTH + col * SQUARE_SIZE, (7 - row) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                4,
            )

    for r in range(8):
        for c in range(8):
            piece = board.piece_at(chess.square(c, 7 - r))
            if piece:
                key = f"{'w' if piece.color else 'b'}{piece.symbol().lower()}"
                screen.blit(piece_images[key], (CAMERA_WIDTH + c * SQUARE_SIZE, r * SQUARE_SIZE))


def get_square_from_pos(x, y):
    col = int((x - CAMERA_WIDTH) // SQUARE_SIZE)
    row = int(y // SQUARE_SIZE)
    if 0 <= col < 8 and 0 <= row < 8:
        return chess.square(col, 7 - row)
    return None


def square_center_pixels(sq):
    col = chess.square_file(sq)
    row = chess.square_rank(sq)
    cx = CAMERA_WIDTH + (col + 0.5) * SQUARE_SIZE
    cy = (7 - row + 0.5) * SQUARE_SIZE
    return int(cx), int(cy)

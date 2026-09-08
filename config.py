"""Central configuration constants for sip_chess."""

# Board / window
SQUARE_SIZE = 80
BOARD_SIZE = SQUARE_SIZE * 8
CAMERA_WIDTH, CAMERA_HEIGHT = 640, 480
WINDOW_WIDTH = BOARD_SIZE + CAMERA_WIDTH
WINDOW_HEIGHT = max(BOARD_SIZE, CAMERA_HEIGHT)

# Colors
LIGHT_SQUARE = (245, 245, 245)
DARK_SQUARE = (60, 60, 60)
FROM_SQUARE_COLOR = (90, 160, 255)
TO_SQUARE_COLOR = (255, 220, 70)
SELECTED_COLOR = (0, 255, 0)
HOVER_COLOR = (0, 200, 0)
INVALID_FLASH_COLOR = (255, 0, 0)

# Gesture / dwell-click tuning
HOLD_THRESHOLD = 30      # frames of stillness required to register a "click"
HOLD_DISTANCE = 20       # px movement tolerance while holding
SMOOTHING_ALPHA = 0.20   # cursor smoothing factor
MARGIN = 15              # dead-zone margin from camera frame edge
POST_MOVE_COOLDOWN = 1 # seconds before another click can register after a move

# Misc
PIECES_DIR = "pieces"
STARTUP_HINT_DURATION = 2.0
INVALID_FLASH_DURATION = 0.25

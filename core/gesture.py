"""Dwell-to-click gesture detection: hold the fingertip still to register a click."""

import math

from config import HOLD_THRESHOLD, HOLD_DISTANCE, SMOOTHING_ALPHA, MARGIN


class DwellClickDetector:
    """Tracks a smoothed cursor position and emits a 'click' when the
    fingertip has been held still for enough frames."""

    def __init__(self):
        self.smooth_x = 0.0
        self.smooth_y = 0.0
        self.last_pos = None
        self.hold_frames = 0

    def update(self, raw_pos, frame_w, frame_h):
        """raw_pos: (x, y) fingertip pixel position, or None if no hand.
        Returns (cursor_pos, valid, clicked).
        """
        if raw_pos is None:
            self.hold_frames = 0
            self.last_pos = None
            return None, False, False

        ix, iy = raw_pos
        self.smooth_x = SMOOTHING_ALPHA * ix + (1 - SMOOTHING_ALPHA) * self.smooth_x
        self.smooth_y = SMOOTHING_ALPHA * iy + (1 - SMOOTHING_ALPHA) * self.smooth_y
        cursor_pos = (int(self.smooth_x), int(self.smooth_y))

        valid = (MARGIN < cursor_pos[0] < frame_w - MARGIN and
                 MARGIN < cursor_pos[1] < frame_h - MARGIN)

        clicked = False
        if valid:
            if self.last_pos is None:
                self.last_pos = cursor_pos
                self.hold_frames = 0
            else:
                dist = math.dist(cursor_pos, self.last_pos)
                if dist < HOLD_DISTANCE:
                    self.hold_frames += 1
                    if self.hold_frames >= HOLD_THRESHOLD:
                        clicked = True
                        self.hold_frames = 0
                        self.last_pos = None
                else:
                    self.hold_frames = 0
                    self.last_pos = cursor_pos
        else:
            self.hold_frames = 0
            self.last_pos = None

        return cursor_pos, valid, clicked

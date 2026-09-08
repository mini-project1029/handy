"""Wraps MediaPipe Hands to give clean landmark data per frame."""

import cv2
import mediapipe as mp


class HandTracker:
    def __init__(self, max_hands=1, detection_confidence=0.5, tracking_confidence=0.5):
        self._mp_hands = mp.solutions.hands
        self._hands = self._mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )

    def process(self, bgr_frame):
        """Run hand detection on a BGR frame. Returns list of (x, y) pixel
        landmarks for the first detected hand, or None if no hand found."""
        h, w, _ = bgr_frame.shape
        rgb = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        results = self._hands.process(rgb)

        if not results.multi_hand_landmarks:
            return None

        hand = results.multi_hand_landmarks[0]
        return [(int(lm.x * w), int(lm.y * h)) for lm in hand.landmark]

    def close(self):
        self._hands.close()


# Landmark indices used elsewhere (index fingertip, etc.)
INDEX_FINGER_TIP = 8
FINGERTIP_IDS = [4, 8, 12, 16, 20]

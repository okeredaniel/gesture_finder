import cv2
import mediapipe as mp


class HandTracker:
    """
    Wraps MediaPipe Hands to detect a hand in a webcam frame
    and return its landmark positions.
    """

    def __init__(self, max_hands=1, detection_confidence=0.7, tracking_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, frame, draw=True):
        """
        Detects hands in the given BGR frame.
        Returns the (possibly annotated) frame and the raw results object.
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks and draw:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )

        return frame, results

    def get_landmark_positions(self, frame, results):
        """
        Converts normalized landmark coordinates (0-1) into pixel coordinates
        for the first detected hand. Returns a list of [id, x, y] or [] if none.
        """
        landmark_list = []

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            h, w, _ = frame.shape
            for idx, lm in enumerate(hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmark_list.append([idx, cx, cy])

        return landmark_list
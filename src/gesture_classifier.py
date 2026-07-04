import math


class GestureClassifier:
    """
    Takes a list of hand landmarks (from HandTracker) and classifies
    them into a named gesture based on finger positions.
    """

    TIP_IDS = [4, 8, 12, 16, 20]  # thumb, index, middle, ring, pinky

    def _fingers_up(self, points):
        """Returns [thumb, index, middle, ring, pinky] as 1 (up) or 0 (curled)."""
        fingers = []

        # Thumb: sideways comparison (mirrored webcam view)
        fingers.append(1 if points[4][0] < points[3][0] else 0)

        # Other 4 fingers: tip above the joint two below it = extended
        for tip_id in self.TIP_IDS[1:]:
            fingers.append(1 if points[tip_id][1] < points[tip_id - 2][1] else 0)

        return fingers

    def _distance(self, p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def classify(self, landmark_list):
        if not landmark_list:
            return None

        points = {idx: (x, y) for idx, x, y in landmark_list}
        thumb, index, middle, ring, pinky = self._fingers_up(points)
        pattern = (thumb, index, middle, ring, pinky)

        # OK sign: thumb tip and index tip close together, other 3 fingers up
        thumb_index_dist = self._distance(points[4], points[8])
        hand_span = self._distance(points[0], points[9])  # wrist to middle knuckle, for scale
        if hand_span > 0 and (thumb_index_dist / hand_span) < 0.35 and middle and ring and pinky:
            return "ok_sign"

        gestures = {
            (0, 0, 0, 0, 0): "fist",
            (1, 1, 1, 1, 1): "open_palm",
            (1, 0, 0, 0, 0): "thumbs_up",
            (0, 1, 1, 0, 0): "peace",
            (1, 1, 1, 0, 0): "peace",       # peace with thumb out too
            (0, 1, 0, 0, 0): "pointing",
            (0, 1, 0, 0, 1): "rock_on",
            (1, 1, 0, 0, 1): "rock_on",     # rock on with thumb out too
            (1, 0, 0, 0, 1): "call_me",
            (0, 1, 1, 1, 0): "three",
            (1, 1, 1, 1, 0): "three",       # three with thumb out too
            (0, 1, 1, 1, 1): "four",
            (1, 1, 0, 0, 0): "gun",
            (0, 0, 0, 0, 1): "pinky_promise",
        }

        return gestures.get(pattern, "unknown")
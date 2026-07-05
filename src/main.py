import cv2
import os
import time

from hand_tracker import HandTracker
from gesture_classifier import GestureClassifier

ASSETS_DIR = "../assets"
REACTION_SIZE = (200, 200)  # width, height of the reaction pic on screen
VALID_EXTENSIONS = (".png", ".webp", ".jpg", ".jpeg")


def load_reaction_images():
    """
    Auto-scans assets/ and loads any image whose filename (minus extension)
    matches a gesture name the classifier can produce, e.g. fist.webp -> "fist".
    No manual mapping needed — just drop matching files in the folder.
    """
    images = {}

    if not os.path.exists(ASSETS_DIR):
        return images

    for filename in os.listdir(ASSETS_DIR):
        name, ext = os.path.splitext(filename)
        if ext.lower() not in VALID_EXTENSIONS:
            continue

        path = os.path.join(ASSETS_DIR, filename)
        img = cv2.imread(path)

        if img is None:
            print(f"Warning: couldn't load {filename} (unsupported format or corrupt file)")
            continue

        img = cv2.resize(img, REACTION_SIZE)
        images[name] = img

    return images


def overlay_image(background, overlay, x, y):
    """Places overlay image onto background at position (x, y), clipped to frame bounds."""
    h, w = overlay.shape[:2]
    bg_h, bg_w = background.shape[:2]

    if x + w > bg_w or y + h > bg_h:
        return background

    background[y:y + h, x:x + w] = overlay
    return background


def main():
    print("Opening camera...")
    cap = cv2.VideoCapture(0)
    print("Camera opened:", cap.isOpened())

    tracker = HandTracker()
    classifier = GestureClassifier()
    reactions = load_reaction_images()
    print("Loaded reaction images:", list(reactions.keys()))

    prev_time = 0

    while True:
        success, frame = cap.read()

        if not success:
            print("Could not read from webcam.")
            break

        frame = cv2.flip(frame, 1)  # mirror so it feels natural

        frame, results = tracker.find_hands(frame)
        landmark_list = tracker.get_landmark_positions(frame, results)
        gesture = classifier.classify(landmark_list)

        # Show gesture label
        label = gesture if gesture else "No hand detected"
        cv2.putText(frame, label, (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2)

        # Overlay matching reaction image, if we have one
        if gesture and gesture in reactions:
            frame = overlay_image(frame, reactions[gesture], 20, 80)
        elif gesture and gesture not in reactions:
            cv2.putText(frame, "(no pic yet for this gesture)", (20, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 1)

        # FPS counter
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time else 0
        prev_time = curr_time
        cv2.putText(frame, f"FPS: {int(fps)}", (frame.shape[1] - 150, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        cv2.imshow("Gesture Pic Finder", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Quit key pressed.")
            break

    print("Releasing camera...")
    cap.release()
    cv2.destroyAllWindows()
    print("Done.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("Press Enter to close...")
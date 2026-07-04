# ✋ Gesture Pic Finder

A real-time hand gesture recognition app built with Python, OpenCV, and MediaPipe. It tracks your hand through your webcam, classifies the gesture you're making, and displays a matching reaction image on screen — all live, no ML training required.

Built by **NullVerse**.

<!-- Add your demo gif/screenshot here — this is the first thing people see -->
<!-- ![demo](assets/demo.gif) -->

## Features

- Real-time hand tracking via webcam using MediaPipe's 21-point hand landmark model
- Recognizes **12 distinct gestures**:
  - 👍 Thumbs Up
  - ✌️ Peace Sign
  - ✊ Fist
  - 🖐️ Open Palm
  - 👉 Pointing
  - 👌 OK Sign
  - 🤘 Rock On
  - 🤙 Call Me
  - Three Fingers
  - Four Fingers
  - 👉👍 Gun
  - Pinky Promise
- Auto-loads reaction images from the `assets/` folder — drop in a file named after a gesture (e.g. `fist.webp`) and it's picked up automatically, no code changes needed
- Live FPS counter and hand skeleton overlay
- Clean, modular codebase split across hand tracking, gesture classification, and the main app loop

## How It Works

1. **Hand tracking** (`hand_tracker.py`) — MediaPipe detects 21 landmark points on your hand from each webcam frame (fingertips, knuckles, wrist, etc.)
2. **Gesture classification** (`gesture_classifier.py`) — checks which fingers are extended vs. curled by comparing landmark positions, then matches the resulting pattern against known gestures. The OK sign is detected differently, using the pixel distance between the thumb and index fingertip.
3. **Reaction display** (`main.py`) — once a gesture is classified, the matching image from `assets/` is overlaid on the live video feed in real time.

## Project Structure

```
gesture-finder/
├── src/
│   ├── main.py                 # Webcam loop, display, and reaction overlay
│   ├── hand_tracker.py         # MediaPipe hand detection wrapper
│   └── gesture_classifier.py   # Finger-pattern -> gesture logic
├── assets/                     # Drop reaction images here (named after gestures)
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

**Requirements:** Python 3.11 (MediaPipe's legacy `solutions` API used here does not currently support Python 3.14+)

```bash
# Clone the repo
git clone https://github.com/okeredaniel/gesture_finder.git
cd gesture_finder

# Create and activate a virtual environment
python -m venv venv
source venv/Scripts/activate     # Windows (Git Bash)
# source venv/bin/activate       # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

## Usage

Add reaction images to the `assets/` folder, named to match a gesture (supports `.png`, `.webp`, `.jpg`, `.jpeg`):

```
assets/
├── thumbs_up.webp
├── peace.webp
├── fist.webp
├── open_palm.webp
└── ...
```

Then run:

```bash
cd src
python main.py
```

Press **`q`** to quit.

## Tech Stack

- **Python 3.11**
- **OpenCV** — webcam capture, image display, drawing
- **MediaPipe** — hand landmark detection
- **NumPy** — supporting numerical operations

## Notes

This project was built and tested against **MediaPipe 0.10.14**. Newer MediaPipe releases have removed the legacy `mp.solutions.hands` API in favor of a new Tasks-based interface, so pinning this version is intentional — check `requirements.txt` for the full working dependency set.

## Future Improvements

- Package as a standalone executable for non-technical users
- Add two-hand gesture combinations
- Support custom gesture training instead of hardcoded finger patterns
- Add sound effects alongside reaction images

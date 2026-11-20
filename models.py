"""Tải các file .task cho MediaPipe Tasks API (bản 1.x)."""
from __future__ import annotations

import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODEL_DIR = ROOT / "models"

MODELS = {
    "hand_landmarker.task": (
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
        "hand_landmarker/float16/1/hand_landmarker.task"
    ),
    "pose_landmarker_lite.task": (
        "https://storage.googleapis.com/mediapipe-models/pose_landmarker/"
        "pose_landmarker_lite/float16/1/pose_landmarker_lite.task"
    ),
    "face_landmarker.task": (
        "https://storage.googleapis.com/mediapipe-models/face_landmarker/"
        "face_landmarker/float16/1/face_landmarker.task"
    ),
}


def model_path(name: str) -> Path:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    dest = MODEL_DIR / name
    if dest.is_file():
        return dest
    url = MODELS[name]
    print(f"Dang tai model {name}...")
    urllib.request.urlretrieve(url, dest)
    print(f"Da luu: {dest}")
    return dest


def ensure_all() -> dict[str, Path]:
    return {name: model_path(name) for name in MODELS}
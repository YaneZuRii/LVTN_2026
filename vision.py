from __future__ import annotations

import cv2
import numpy as np
from mediapipe import Image, ImageFormat
from mediapipe.tasks.python.core.base_options import BaseOptions
from mediapipe.tasks.python.vision import (
    FaceLandmarker,
    FaceLandmarkerOptions,
    HandLandmarker,
    HandLandmarkerOptions,
    HandLandmarksConnections,
    PoseLandmarker,
    PoseLandmarkerOptions,
    PoseLandmark,
    RunningMode,
    drawing_styles,
    drawing_utils,
)

from models import ensure_all

MOUTH_LEFT = 61
MOUTH_RIGHT = 291
MOUTH_TOP = 13
MOUTH_BOTTOM = 14

POSE_POINTS = (
    PoseLandmark.LEFT_SHOULDER,
    PoseLandmark.RIGHT_SHOULDER,
    PoseLandmark.LEFT_ELBOW,
    PoseLandmark.RIGHT_ELBOW,
)


def _mp_image_from_rgb(rgb: np.ndarray) -> Image:
    return Image(image_format=ImageFormat.SRGB, data=np.ascontiguousarray(rgb))


class LandmarkProcessor:
    def __init__(self) -> None:
        paths = ensure_all()
        hand_opts = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=str(paths["hand_landmarker.task"])),
            running_mode=RunningMode.VIDEO,
            num_hands=2,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        pose_opts = PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=str(paths["pose_landmarker_lite.task"])),
            running_mode=RunningMode.VIDEO,
            min_pose_detection_confidence=0.5,
            min_pose_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        face_opts = FaceLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=str(paths["face_landmarker.task"])),
            running_mode=RunningMode.VIDEO,
            num_faces=1,
            min_face_detection_confidence=0.5,
            min_face_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self._hands = HandLandmarker.create_from_options(hand_opts)
        self._pose = PoseLandmarker.create_from_options(pose_opts)
        self._face = FaceLandmarker.create_from_options(face_opts)
        self._ts_ms = 0

    def close(self) -> None:
        self._hands.close()
        self._pose.close()
        self._face.close()

    def process(self, frame_bgr: np.ndarray) -> np.ndarray:
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        h, w = frame_bgr.shape[:2]
        mp_img = _mp_image_from_rgb(rgb)
        self._ts_ms += 33

        hand_result = self._hands.detect_for_video(mp_img, self._ts_ms)
        pose_result = self._pose.detect_for_video(mp_img, self._ts_ms)
        face_result = self._face.detect_for_video(mp_img, self._ts_ms)

        out = frame_bgr.copy()

        if hand_result.hand_landmarks:
            for hand_lm in hand_result.hand_landmarks:
                drawing_utils.draw_landmarks(
                    out,
                    hand_lm,
                    HandLandmarksConnections.HAND_CONNECTIONS,
                    drawing_styles.get_default_hand_landmarks_style(),
                    drawing_styles.get_default_hand_connections_style(),
                )
        if pose_result.pose_landmarks:
            pose_lm = pose_result.pose_landmarks[0]
            for idx in POSE_POINTS:
                if idx >= len(pose_lm):
                    continue
                pt = pose_lm[idx]
                vis = pt.visibility if pt.visibility is not None else 1.0
                if vis < 0.5:
                    continue
                cx, cy = int(pt.x * w), int(pt.y * h)
                cv2.circle(out, (cx, cy), 8, (0, 255, 255), -1)
                cv2.circle(out, (cx, cy), 10, (255, 255, 255), 2)
        if face_result.face_landmarks:
            flm = face_result.face_landmarks[0]
            for idx in (MOUTH_LEFT, MOUTH_RIGHT, MOUTH_TOP, MOUTH_BOTTOM):
                if idx >= len(flm):
                    continue
                pt = flm[idx]
                cx, cy = int(pt.x * w), int(pt.y * h)
                cv2.circle(out, (cx, cy), 5, (255, 0, 255), -1)
        return out
from __future__ import annotations

import functools
from pathlib import Path
from typing import List, Tuple

import cv2
import numpy as np
import torch


RIGHT_LOWER_EYELID = [33, 7, 163, 144, 145, 153, 154, 155, 133]
LEFT_LOWER_EYELID = [263, 249, 390, 373, 374, 380, 381, 382, 362]
RIGHT_IRIS = [469, 470, 471, 472]
LEFT_IRIS = [474, 475, 476, 477]


def _unit(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v)
    if n < 1e-8:
        return np.array([0.0, 1.0], dtype=np.float32)
    return (v / n).astype(np.float32)


def _resample_polyline(points: np.ndarray, n_points: int = 25) -> np.ndarray:
    if len(points) < 2:
        return points.copy()
    seg = np.linalg.norm(points[1:] - points[:-1], axis=1)
    seg = np.maximum(seg, 1e-6)
    arc = np.concatenate([[0.0], np.cumsum(seg)])
    target = np.linspace(0.0, arc[-1], n_points)
    x = np.interp(target, arc, points[:, 0])
    y = np.interp(target, arc, points[:, 1])
    return np.stack([x, y], axis=1).astype(np.float32)


def _largest_face(landmarks_list: List) -> List:
    best = None
    best_area = -1.0
    for face in landmarks_list:
        xs = [lm.x for lm in face]
        ys = [lm.y for lm in face]
        area = (max(xs) - min(xs)) * (max(ys) - min(ys))
        if area > best_area:
            best = face
            best_area = area
    return best


def _build_under_eye_polygon(
    pts_xy: np.ndarray,
    eyelid_indices: List[int],
    iris_indices: List[int],
    depth_ratio: float,
    width_padding_ratio: float,
) -> np.ndarray:
    eyelid = pts_xy[np.array(eyelid_indices), :]
    iris_center = pts_xy[np.array(iris_indices), :].mean(axis=0)

    upper = _resample_polyline(eyelid.astype(np.float32), 25)
    eye_width = float(np.linalg.norm(upper[-1] - upper[0]))
    if eye_width < 1.0:
        eye_width = 1.0

    # Direction points away from iris center, which naturally pushes the mask
    # from lower eyelid toward tear trough / upper cheek.
    raw_dirs = upper - iris_center[None, :]
    norms = np.linalg.norm(raw_dirs, axis=1, keepdims=True)
    norms = np.maximum(norms, 1e-6)
    dirs = raw_dirs / norms

    # Blend with image down direction for extra stability.
    down = np.array([0.0, 1.0], dtype=np.float32)[None, :]
    dirs = dirs * 0.75 + down * 0.25
    dirs = dirs / np.maximum(np.linalg.norm(dirs, axis=1, keepdims=True), 1e-6)

    t = np.linspace(0.0, 1.0, len(upper), dtype=np.float32)
    center_boost = 0.82 + 0.28 * np.sin(np.pi * t)
    depths = eye_width * depth_ratio * center_boost
    lower = upper + dirs * depths[:, None]

    tangent_start = _unit(upper[1] - upper[0])
    tangent_end = _unit(upper[-1] - upper[-2])

    pad = eye_width * width_padding_ratio
    start_upper = upper[0] - tangent_start * (pad * 0.60)
    end_upper = upper[-1] + tangent_end * (pad * 0.95)
    start_lower = lower[0] - tangent_start * (pad * 0.35) + dirs[0] * (eye_width * 0.04)
    end_lower = lower[-1] + tangent_end * (pad * 0.55) + dirs[-1] * (eye_width * 0.06)

    poly = np.vstack([
        start_upper[None, :],
        upper,
        end_upper[None, :],
        end_lower[None, :],
        lower[::-1],
        start_lower[None, :],
    ])
    return poly.astype(np.float32)


def _overlay_mask(image_rgb: np.ndarray, mask: np.ndarray, opacity: float) -> np.ndarray:
    color = np.array([1.0, 0.15, 0.15], dtype=np.float32)
    mask3 = mask[..., None]
    out = image_rgb * (1.0 - mask3 * opacity) + color[None, None, :] * (mask3 * opacity)
    return np.clip(out, 0.0, 1.0).astype(np.float32)


@functools.lru_cache(maxsize=4)
def _get_landmarker(
    model_path: str,
    min_face_detection_confidence: float,
    min_face_presence_confidence: float,
    min_tracking_confidence: float,
):
    try:
        import mediapipe as mp
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision
    except Exception as e:
        raise RuntimeError(
            "未安装 mediapipe。先运行: pip install -r custom_nodes/ComfyUI_UnderEyeMask/requirements.txt"
        ) from e

    resolved = Path(model_path)
    if not resolved.is_absolute():
        # .../ComfyUI/custom_nodes/ComfyUI_UnderEyeMask/under_eye_mask_node.py
        comfy_root = Path(__file__).resolve().parents[2]
        resolved = comfy_root / resolved

    if not resolved.exists():
        raise FileNotFoundError(
            f"找不到 MediaPipe Face Landmarker 模型: {resolved}\n"
            "把 face_landmarker.task 放到 ComfyUI/models/mediapipe/face_landmarker.task"
        )

    options = vision.FaceLandmarkerOptions(
        base_options=python.BaseOptions(model_asset_path=str(resolved)),
        running_mode=vision.RunningMode.IMAGE,
        num_faces=1,
        min_face_detection_confidence=float(min_face_detection_confidence),
        min_face_presence_confidence=float(min_face_presence_confidence),
        min_tracking_confidence=float(min_tracking_confidence),
        output_face_blendshapes=False,
        output_facial_transformation_matrixes=False,
    )
    return mp, vision.FaceLandmarker.create_from_options(options)


def _tensor_to_uint8_rgb(image_tensor: torch.Tensor) -> np.ndarray:
    arr = image_tensor.detach().cpu().numpy()
    arr = np.clip(arr, 0.0, 1.0)
    return (arr * 255.0).round().astype(np.uint8)


class MediaPipeUnderEyeMask:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "model_path": ("STRING", {
                    "default": "models/mediapipe/face_landmarker.task",
                    "multiline": False
                }),
                "depth_ratio": ("FLOAT", {
                    "default": 0.22, "min": 0.08, "max": 0.45, "step": 0.01
                }),
                "width_padding_ratio": ("FLOAT", {
                    "default": 0.08, "min": 0.00, "max": 0.25, "step": 0.01
                }),
                "dilate_px": ("INT", {
                    "default": 12, "min": 0, "max": 256, "step": 1
                }),
                "feather_px": ("INT", {
                    "default": 18, "min": 0, "max": 256, "step": 1
                }),
                "overlay_opacity": ("FLOAT", {
                    "default": 0.35, "min": 0.0, "max": 1.0, "step": 0.01
                }),
                "min_face_detection_confidence": ("FLOAT", {
                    "default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01
                }),
                "min_face_presence_confidence": ("FLOAT", {
                    "default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01
                }),
                "min_tracking_confidence": ("FLOAT", {
                    "default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01
                }),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "IMAGE")
    RETURN_NAMES = ("image", "mask", "preview")
    FUNCTION = "generate"
    CATEGORY = "Face/Mask"

    def generate(
        self,
        image,
        model_path,
        depth_ratio,
        width_padding_ratio,
        dilate_px,
        feather_px,
        overlay_opacity,
        min_face_detection_confidence,
        min_face_presence_confidence,
        min_tracking_confidence,
    ):
        mp, landmarker = _get_landmarker(
            model_path,
            float(min_face_detection_confidence),
            float(min_face_presence_confidence),
            float(min_tracking_confidence),
        )

        if image.ndim == 3:
            image = image.unsqueeze(0)

        batch_images = []
        batch_masks = []
        batch_previews = []

        for i in range(image.shape[0]):
            img_float = image[i]
            img_rgb_u8 = _tensor_to_uint8_rgb(img_float)
            h, w = img_rgb_u8.shape[:2]

            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb_u8)
            result = landmarker.detect(mp_image)
            if not result.face_landmarks:
                raise RuntimeError("MediaPipe 没检测到人脸，无法自动生成下眼睑术区 mask。")

            face = _largest_face(result.face_landmarks)
            pts_xy = np.array([[lm.x * w, lm.y * h] for lm in face], dtype=np.float32)

            left_poly = _build_under_eye_polygon(
                pts_xy, LEFT_LOWER_EYELID, LEFT_IRIS,
                float(depth_ratio), float(width_padding_ratio)
            )
            right_poly = _build_under_eye_polygon(
                pts_xy, RIGHT_LOWER_EYELID, RIGHT_IRIS,
                float(depth_ratio), float(width_padding_ratio)
            )

            mask_u8 = np.zeros((h, w), dtype=np.uint8)
            for poly in (left_poly, right_poly):
                poly_i = np.round(poly).astype(np.int32)
                poly_i[:, 0] = np.clip(poly_i[:, 0], 0, w - 1)
                poly_i[:, 1] = np.clip(poly_i[:, 1], 0, h - 1)
                cv2.fillPoly(mask_u8, [poly_i], 255)

            if int(dilate_px) > 0:
                k = int(dilate_px) * 2 + 1
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
                mask_u8 = cv2.dilate(mask_u8, kernel, iterations=1)

            if int(feather_px) > 0:
                k = int(feather_px) * 2 + 1
                mask_u8 = cv2.GaussianBlur(mask_u8, (k, k), 0)

            mask = np.clip(mask_u8.astype(np.float32) / 255.0, 0.0, 1.0)
            preview = _overlay_mask(img_float.detach().cpu().numpy().astype(np.float32), mask, float(overlay_opacity))

            batch_images.append(img_float.detach().cpu())
            batch_masks.append(torch.from_numpy(mask.astype(np.float32)))
            batch_previews.append(torch.from_numpy(preview.astype(np.float32)))

        images_out = torch.stack(batch_images, dim=0)
        previews_out = torch.stack(batch_previews, dim=0)

        if len(batch_masks) == 1:
            masks_out = batch_masks[0]
        else:
            masks_out = torch.stack(batch_masks, dim=0)

        return (images_out, masks_out, previews_out)


NODE_CLASS_MAPPINGS = {
    "MediaPipeUnderEyeMask": MediaPipeUnderEyeMask,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MediaPipeUnderEyeMask": "MediaPipe Under-Eye Mask",
}

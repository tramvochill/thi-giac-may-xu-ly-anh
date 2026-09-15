import math
import os
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs"
OUT_DIR.mkdir(exist_ok=True)


def clip_uint8(arr):
    return np.clip(arr, 0, 255).astype(np.uint8)


def save_gray(arr, name):
    path = OUT_DIR / name
    Image.fromarray(clip_uint8(arr), "L").save(path)
    return path


def save_rgb(arr, name):
    path = OUT_DIR / name
    Image.fromarray(clip_uint8(arr), "RGB").save(path)
    return path


def make_gray_sample(size=256):
    y, x = np.mgrid[0:size, 0:size]
    base = 35 + 0.55 * x + 0.18 * y
    circle = ((x - 92) ** 2 + (y - 110) ** 2) < 42 ** 2
    ellipse = (((x - 170) / 36) ** 2 + ((y - 145) / 60) ** 2) < 1
    base[circle] += 85
    base[ellipse] -= 55
    base += 14 * np.sin(x / 13.0) + 10 * np.cos(y / 19.0)
    return clip_uint8(base)


def make_low_contrast_sample(size=256):
    gray = make_gray_sample(size).astype(np.float32)
    return clip_uint8(82 + (gray - gray.min()) * 70 / max(1, gray.max() - gray.min()))


def make_dark_sample(size=256):
    gray = make_gray_sample(size).astype(np.float32)
    return clip_uint8(gray * 0.42)


def make_noisy_sample(size=256):
    rng = np.random.default_rng(7)
    gray = make_gray_sample(size).astype(np.float32)
    noise_mask = rng.random((size, size))
    gray[noise_mask < 0.035] = 0
    gray[(noise_mask >= 0.035) & (noise_mask < 0.07)] = 255
    return clip_uint8(gray)


def make_color_sample(size=256):
    y, x = np.mgrid[0:size, 0:size]
    img = np.zeros((size, size, 3), dtype=np.uint8)
    img[..., 0] = clip_uint8(50 + 170 * x / (size - 1))
    img[..., 1] = clip_uint8(45 + 165 * y / (size - 1))
    img[..., 2] = clip_uint8(140 + 70 * np.sin((x + y) / 30.0))
    red_obj = (x - 82) ** 2 + (y - 96) ** 2 < 38 ** 2
    yellow_obj = ((x - 170) ** 2 / 42 ** 2 + (y - 155) ** 2 / 30 ** 2) < 1
    img[red_obj] = [225, 35, 35]
    img[yellow_obj] = [230, 210, 40]
    return img


def convolve2d(gray, kernel):
    img = gray.astype(np.float32)
    k = np.array(kernel, dtype=np.float32)
    pad_y, pad_x = k.shape[0] // 2, k.shape[1] // 2
    padded = np.pad(img, ((pad_y, pad_y), (pad_x, pad_x)), mode="edge")
    out = np.zeros_like(img)
    for y in range(out.shape[0]):
        for x in range(out.shape[1]):
            out[y, x] = np.sum(padded[y:y + k.shape[0], x:x + k.shape[1]] * k)
    return out


def box_filter(gray, ksize=5):
    kernel = np.ones((ksize, ksize), dtype=np.float32) / (ksize * ksize)
    return clip_uint8(convolve2d(gray, kernel))


def median_filter(gray, ksize=3):
    pad = ksize // 2
    padded = np.pad(gray, pad, mode="edge")
    out = np.zeros_like(gray)
    for y in range(gray.shape[0]):
        for x in range(gray.shape[1]):
            out[y, x] = np.median(padded[y:y + ksize, x:x + ksize])
    return out


def normalize_to_uint8(arr):
    arr = arr.astype(np.float32)
    mn, mx = float(arr.min()), float(arr.max())
    if abs(mx - mn) < 1e-6:
        return np.zeros_like(arr, dtype=np.uint8)
    return clip_uint8((arr - mn) * 255.0 / (mx - mn))


def rgb_to_gray(rgb):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    return clip_uint8(0.299 * r + 0.587 * g + 0.114 * b)


def rgb_to_hsi(rgb):
    arr = rgb.astype(np.float32) / 255.0
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    num = 0.5 * ((r - g) + (r - b))
    den = np.sqrt((r - g) ** 2 + (r - b) * (g - b)) + 1e-8
    theta = np.degrees(np.arccos(np.clip(num / den, -1, 1)))
    h = np.where(b <= g, theta, 360 - theta) / 360.0
    s = 1 - 3 * np.minimum(np.minimum(r, g), b) / (r + g + b + 1e-8)
    i = (r + g + b) / 3
    return np.dstack([h, s, i])


def pseudo_colormap(gray):
    v = gray.astype(np.float32) / 255.0
    r = clip_uint8(255 * np.clip(1.5 * v - 0.25, 0, 1))
    g = clip_uint8(255 * np.clip(1.5 - np.abs(3 * v - 1.5), 0, 1))
    b = clip_uint8(255 * np.clip(1.25 - 1.5 * v, 0, 1))
    return np.dstack([r, g, b])


def add_title_strip(img, label):
    arr = clip_uint8(img)
    pil = Image.fromarray(arr if arr.ndim == 3 else np.dstack([arr] * 3))
    strip = Image.new("RGB", (pil.width, 24), "white")
    draw = ImageDraw.Draw(strip)
    draw.text((6, 5), label, fill=(0, 0, 0))
    canvas = Image.new("RGB", (pil.width, pil.height + 24), "white")
    canvas.paste(strip, (0, 0))
    canvas.paste(pil.convert("RGB"), (0, 24))
    return np.array(canvas)


def save_comparison(original, processed, name, left="Input", right="Output"):
    left_img = add_title_strip(original, left)
    right_img = add_title_strip(processed, right)
    h = max(left_img.shape[0], right_img.shape[0])
    canvas = np.full((h, left_img.shape[1] + right_img.shape[1] + 12, 3), 255, dtype=np.uint8)
    canvas[:left_img.shape[0], :left_img.shape[1]] = left_img
    x0 = left_img.shape[1] + 12
    canvas[:right_img.shape[0], x0:x0 + right_img.shape[1]] = right_img
    return save_rgb(canvas, name)


def print_saved(path):
    print(f"saved: {path}")
    if os.environ.get("SHOW_RESULT", "1") == "1":
        os.startfile(str(path))

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "examples"))

import numpy as np
from common import make_color_sample, median_filter, rgb_to_hsi, save_comparison, print_saved


img = make_color_sample()
hsi = rgb_to_hsi(img)
hue = hsi[..., 0]
sat = hsi[..., 1]
intensity = (hsi[..., 2] * 255).astype("uint8")

# Method 1: color slicing in HSI space for red objects.
red_mask = ((hue < 0.05) | (hue > 0.94)) & (sat > 0.45)

# Method 2: median filtering removes isolated mask noise.
mask_img = (red_mask.astype("uint8") * 255)
mask_clean = median_filter(mask_img, 3) > 0

# Method 3: thresholding on intensity removes very dark false positives.
mask_final = mask_clean & (intensity > 55)

out = np.zeros_like(img)
out[mask_final] = [255, 0, 0]
out[~mask_final] = (img[~mask_final] * 0.30).astype("uint8")

print_saved(save_comparison(img, out, "21_red_object_detection.png", "Input", "Detected red object"))

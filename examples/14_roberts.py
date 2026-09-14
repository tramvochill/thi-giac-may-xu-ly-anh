import numpy as np
from common import make_gray_sample, normalize_to_uint8, save_comparison, print_saved


img = make_gray_sample().astype("float32")
gx = img[1:, 1:] - img[:-1, :-1]
gy = img[1:, :-1] - img[:-1, 1:]
mag = np.zeros_like(img)
mag[:-1, :-1] = np.abs(gx) + np.abs(gy)
out = normalize_to_uint8(mag)
print_saved(save_comparison(img, out, "14_roberts.png", "Input", "Roberts edges"))

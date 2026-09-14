import numpy as np
from common import make_low_contrast_sample, clip_uint8, save_comparison, print_saved


img = make_low_contrast_sample()
pad = 8
padded = np.pad(img, pad, mode="edge")
out = np.zeros_like(img)
for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        block = padded[y:y + 2 * pad + 1, x:x + 2 * pad + 1]
        rank = (block <= img[y, x]).sum()
        out[y, x] = 255 * rank / block.size
print_saved(save_comparison(img, clip_uint8(out), "08_local_histogram_equalization.png", "Input", "Local hist eq"))

import numpy as np
from common import make_color_sample, save_comparison, print_saved


img = make_color_sample()
r, g, b = img[..., 0], img[..., 1], img[..., 2]
mask = (r > 170) & (g < 90) & (b < 90)
out = np.zeros_like(img)
out[mask] = [255, 0, 0]
out[~mask] = (img[~mask] * 0.25).astype("uint8")
print_saved(save_comparison(img, out, "20_color_slicing.png", "RGB input", "Red slice"))

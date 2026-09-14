import numpy as np
from common import make_low_contrast_sample, save_comparison, print_saved


img = make_low_contrast_sample()
hist = np.bincount(img.ravel(), minlength=256)
cdf = hist.cumsum()
cdf = (cdf - cdf[cdf > 0][0]) * 255 / (cdf[-1] - cdf[cdf > 0][0])
lut = np.clip(cdf, 0, 255).astype("uint8")
out = lut[img]
print_saved(save_comparison(img, out, "07_histogram_equalization.png", "Low contrast", "Histogram equalized"))

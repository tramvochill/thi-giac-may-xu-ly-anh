import numpy as np
from common import make_gray_sample, convolve2d, normalize_to_uint8, save_comparison, print_saved


img = make_gray_sample()
kx = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
ky = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
gx = convolve2d(img, kx)
gy = convolve2d(img, ky)
out = normalize_to_uint8(np.abs(gx) + np.abs(gy))
print_saved(save_comparison(img, out, "15_sobel.png", "Input", "Sobel edges"))

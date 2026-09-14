from common import make_gray_sample, convolve2d, clip_uint8, save_comparison, print_saved


img = make_gray_sample()
kernel = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]
lap = convolve2d(img, kernel)
out = clip_uint8(img.astype("float32") - lap)
print_saved(save_comparison(img, out, "12_laplacian_sharpening.png", "Input", "Sharpened"))

from common import make_gray_sample, save_comparison, print_saved


img = make_gray_sample()
out = 255 - img
print_saved(save_comparison(img, out, "01_negative.png", "Original", "Negative"))

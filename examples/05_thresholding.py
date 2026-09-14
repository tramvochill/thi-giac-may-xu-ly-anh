from common import make_gray_sample, save_comparison, print_saved


img = make_gray_sample()
threshold = 128
out = (img >= threshold).astype("uint8") * 255
print_saved(save_comparison(img, out, "05_thresholding.png", "Input", "Threshold >= 128"))

from common import make_gray_sample, box_filter, save_comparison, print_saved


img = make_gray_sample()
out = box_filter(img, 9)
print_saved(save_comparison(img, out, "09_averaging.png", "Input", "9x9 average"))

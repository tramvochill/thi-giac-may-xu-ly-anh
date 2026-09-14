from common import make_noisy_sample, median_filter, save_comparison, print_saved


img = make_noisy_sample()
out = median_filter(img, 3)
print_saved(save_comparison(img, out, "10_median_filter.png", "Salt-pepper noise", "3x3 median"))

from common import make_color_sample, rgb_to_gray, save_comparison, print_saved


img = make_color_sample()
out = rgb_to_gray(img)
print_saved(save_comparison(img, out, "16_rgb.png", "RGB input", "Luminosity gray"))

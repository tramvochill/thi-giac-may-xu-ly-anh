from common import make_color_sample, rgb_to_hsi, clip_uint8, save_comparison, print_saved


rgb = make_color_sample()
hsi = rgb_to_hsi(rgb)
preview = clip_uint8(hsi * 255)
print_saved(save_comparison(rgb, preview, "18_hsi_model.png", "RGB", "HSI as image"))

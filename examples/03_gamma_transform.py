from common import make_dark_sample, clip_uint8, save_comparison, print_saved


img = make_dark_sample().astype("float32") / 255.0
gamma = 0.45
out = clip_uint8(255 * (img ** gamma))
print_saved(save_comparison((img * 255), out, "03_gamma_transform.png", "Dark input", "Gamma 0.45"))

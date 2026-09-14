from common import make_low_contrast_sample, clip_uint8, save_comparison, print_saved


img = make_low_contrast_sample().astype("float32")
r1, r2 = img.min(), img.max()
out = clip_uint8((img - r1) * 255 / max(1, r2 - r1))
print_saved(save_comparison(img, out, "04_contrast_stretching.png", "Low contrast", "Stretched"))

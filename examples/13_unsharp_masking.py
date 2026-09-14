from common import make_gray_sample, box_filter, clip_uint8, save_comparison, print_saved


img = make_gray_sample()
blur = box_filter(img, 9).astype("float32")
mask = img.astype("float32") - blur
out = clip_uint8(img.astype("float32") + 1.5 * mask)
print_saved(save_comparison(img, out, "13_unsharp_masking.png", "Input", "Unsharp mask"))

from common import make_gray_sample, save_comparison, print_saved


img = make_gray_sample()
bit = 7
out = ((img >> bit) & 1) * 255
print_saved(save_comparison(img, out, "06_bit_plane_slicing.png", "Input", "Bit plane 7"))

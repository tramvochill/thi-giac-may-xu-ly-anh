from common import make_gray_sample, pseudo_colormap, save_comparison, print_saved


gray = make_gray_sample()
out = pseudo_colormap(gray)
print_saved(save_comparison(gray, out, "19_pseudocolor.png", "Gray input", "Pseudocolor"))

import numpy as np
from common import make_color_sample, clip_uint8, save_comparison, print_saved


rgb = make_color_sample().astype("float32") / 255.0
cmy = 1 - rgb
k = np.min(cmy, axis=2)
cmy_preview = clip_uint8(cmy * 255)
print("K channel mean:", float(k.mean()))
print_saved(save_comparison(rgb * 255, cmy_preview, "17_cmy_cmyk.png", "RGB", "CMY preview"))

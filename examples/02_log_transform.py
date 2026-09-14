import numpy as np
from common import make_dark_sample, normalize_to_uint8, save_comparison, print_saved


img = make_dark_sample()
c = 255 / np.log(1 + 255)
out = c * np.log(1 + img.astype(np.float32))
print_saved(save_comparison(img, out, "02_log_transform.png", "Dark input", "Log transform"))

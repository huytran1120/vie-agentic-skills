"""Key a flat #FF00FF background out of a mascot image -> RGBA PNG (soft edge + magenta despill)."""
import sys
import numpy as np
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
im = np.asarray(Image.open(src).convert('RGB')).astype(np.float32) / 255
r, g, b = im[..., 0], im[..., 1], im[..., 2]
# magenta-ness: strong red and blue, weak green
m = np.clip(np.minimum(r, b) - g, 0, 1)
d = np.sqrt((1 - r) ** 2 + g ** 2 + (1 - b) ** 2)  # distance to pure magenta
alpha = np.clip((d - 0.18) / 0.32, 0, 1)
alpha = np.minimum(alpha, np.clip(1 - (m - 0.35) / 0.4, 0, 1))
# despill: remove the magenta cast that is left on edge pixels
spill = np.clip(np.minimum(r, b) - g, 0, 1) * (1 - alpha * 0.85)
out = np.stack([r - spill, g, b - spill, alpha], -1)
img = Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), 'RGBA')
if '--nocrop' in sys.argv:
    img = img.resize((768, 768), Image.LANCZOS)
    img.save(dst)
    print(dst, img.size)
    sys.exit(0)
bbox = img.getbbox()
if bbox:
    pad = 12
    img = img.crop((max(0, bbox[0] - pad), max(0, bbox[1] - pad), min(img.width, bbox[2] + pad), min(img.height, bbox[3] + pad)))
img.save(dst)
print(dst, img.size)

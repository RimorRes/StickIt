import stickit
from PIL import Image, ImageDraw
import numpy as np
import math


img = stickit.convert_to_rgb(Image.open('./res/images/petitprince_sj_crop.png'))
pal = stickit.Palette()
pal.from_file('./res/palettes/postit', mode='hex')

post_it_img = stickit.convert_to_palette(img, pal).convert('RGB')
post_it_img.save('./test/design.jpg')
print('- Converted image to Palette + to RGB')

img_arr = np.asarray(post_it_img)
print('- Grabbed image array')

h, w = img_arr.shape[:2]

used_colors = {}

for y in range(h):
    for x in range(w):
        col = tuple(img_arr[y][x])
        if col in used_colors:
            used_colors[col] += 1
        else:
            used_colors[col] = 1

print('- Counted colors used')


phys_w, phys_h = (5, 7.5)  # 5x7.5 m
post_w, post_h = (76e-3, 76e-3)  # 76x76 mm
surf = phys_w * phys_h
p_surf = post_w * post_h

post_cov = surf / p_surf
print(f'- Need {post_cov} Post-Its to cover area')

pix_cov = w * h
print(f'- Image contains {pix_cov} pixels')

ratio = pix_cov / post_cov
print(f'- pixel to Post-It ratio: {ratio}')


post_its = {key: used_colors[key]//ratio for key in used_colors if used_colors[key]//ratio > 0}


print('- Drawing swatch')

size = 64
swatch_width = 5
margin = 0.50  # 50% overhead for number of post-its

n = len(post_its)
swatch = Image.new('RGB', (size*swatch_width, size*math.ceil(n/swatch_width)))
drawer = ImageDraw.Draw(swatch)

i = 0
for key in post_its:
    x0 = (i % swatch_width)*size
    x1 = x0 + size
    y0 = (i//swatch_width)*size
    y1 = y0 + size
    drawer.rectangle((x0, y0, x1, y1), fill=key)
    num = post_its[key] * (margin + 1)
    drawer.text((x0+size//4, (y0 + y1)//2), str(math.ceil(num)), fill=(0, 0, 0))
    i += 1

swatch.save('test/swatch.jpg')

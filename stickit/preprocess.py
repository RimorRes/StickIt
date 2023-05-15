from PIL import Image


def convert_to_rgb(image):
    background = Image.new('RGBA', image.size, (0, 0, 0))
    new = Image.alpha_composite(background, image).convert('RGB')

    return new


def reduce_colors(image, num_colors):
    return image.convert('P', palette=Image.ADAPTIVE, colors=num_colors+1)

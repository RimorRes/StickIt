from PIL import Image
import colorsys


def hex_to_rgb(hexcode):
    h = hexcode.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


class Palette:

    def __init__(self, colors=()):
        self.colors = list(colors)

    def from_file(self, path: str, mode: str='rgb'):
        """
        Builds color palette from file containing the colors to add.
        Will append new colors to those already present.

        :param path: path to file
        :param mode: color code format. Either 'hex', 'rgb', or 'hsv'. Defaults to RGB.
        :return: None
        """

        with open(path, 'r') as file:

            lines = file.readlines()

            for line in lines:

                col_str = line.strip()  # Remove trailing new-line

                if mode == 'rgb':
                    # If there are parenthesis, remove them
                    col_str = col_str.replace('(', '')
                    col_str = col_str.replace(')', '')
                    # Reconstitute RGB tuple
                    col = tuple(int(val) for val in col_str.split(','))

                elif mode == 'hex':
                    # Convert to RGB
                    col = hex_to_rgb(col_str)

                elif mode == 'hsv':
                    # If there are parenthesis, remove them
                    col_str = col_str.replace('(', '')
                    col_str = col_str.replace(')', '')
                    # If there are '%', remove them
                    col_str = col_str.replace('%', '')
                    # Get H,S,V values
                    h, s, v = [int(val) for val in tuple(col_str.split(','))]

                    # Convert to RGB
                    col = colorsys.hsv_to_rgb(h, s, v)

                self.colors.append(col)

    def to_sequence(self):
        """
        Converts the palette to an integer sequence.
        The palette sequence contains 256 colors,
        made up of one integer value for each channel in the raw mode (768 values total).
        Used in conjunction with PIL.Image.putpalette

        :return: list: RGB integer sequence
        """

        seq = []
        for col in self.colors:
            seq += col

        seq += (0, 0, 0) * (256 - len(self.colors))  # Fill remaining space with (0, 0, 0)

        return seq


def convert_to_palette(img: Image.Image, palette: Palette, dither=False):
    """
    Converts an image to the specified color palette.

    :param img: image to convert.
    :param palette: Palette object to use
    :return: image
    """
    pal_image = Image.new('P', (1, 1))
    pal_image.putpalette(palette.to_sequence())

    d = 1 if dither else 0

    return img.convert("RGB").quantize(palette=pal_image, dither=d)

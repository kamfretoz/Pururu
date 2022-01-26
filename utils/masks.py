# Portions were taken from https://github.com/Supersebi3/pilutils/blob/master/pilutils/masks.py

from PIL import Image, ImageDraw

def ellipse(size, invert=False):
    """Returns an alpha mask in the shape of an ellipse."""
    fg, bg = (0, 255) if invert else (255, 0)
    mask = Image.new("L", size, bg)
    d = ImageDraw.Draw(mask)
    d.ellipse((0, 0, *size), fill=fg)
    return mask

def rectangle(size, invert=False):
    """Returns a rectangular alpha mask."""
    fg = 0 if invert else 255
    mask = Image.new("L", size, fg)
    return mask
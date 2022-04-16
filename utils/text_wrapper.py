###
# CREDIT TO KING NORI
# LONG LIVE THE KING!
##

import math

def wrap_text(font, text: str, max_width: int, max_height: int):
    _, height = font.getsize(text)
    width = 0
    max_row = math.ceil(max_height / height)
    current_text = ""
    remainder = text
    ret = ""
    row = 0

    while remainder:
        if width < max_width:
            current_text = f"{current_text}{remainder[0]}"
            remainder = remainder[1:]
        else:
            if remainder:
                remainder = f"{current_text[-1]}{remainder}"
                if not current_text[-1].isspace() and not current_text[-2].isspace():
                    current_text = f"{current_text[:-1]}-"
                else:
                    current_text = f"{current_text[:-1]}"

                if row == max_row - 1:
                    current_text = f"{current_text[:-2]}..."

            ret = f"{ret}{current_text.strip()}\n"
            row += 1

            if row == max_row:
                break

            current_text = ""

        width, _ = font.getsize(current_text)
    else:
        ret = f"{ret}{current_text.strip()}"

    return ("\n".join(ret.split("\n")[:max_row])).strip()
"""Flat silhouette people (SVG paths, 1000x1200 box, facing right) rendered with cairosvg."""
import io
import cairosvg
from PIL import Image

WOMAN = ("M 150 1200 C 160 1000, 250 935, 360 905 C 320 900, 275 880, 255 835 "
         "C 232 760, 270 640, 312 560 C 300 520, 300 482, 330 456 "
         "C 322 335, 385 228, 505 214 C 640 195, 722 290, 730 380 "
         "C 735 412, 742 432, 762 462 L 800 530 C 806 546, 792 556, 770 556 "
         "C 776 574, 786 586, 778 600 C 770 610, 760 612, 770 625 "
         "C 778 642, 765 662, 745 672 C 735 690, 720 700, 690 705 "
         "C 645 712, 622 742, 622 792 C 622 852, 642 900, 702 940 "
         "C 800 1000, 860 1080, 870 1200 Z")
# small hair bun detail for the ponytail tie
MAN = ("M 110 1200 C 120 990, 250 930, 400 905 C 440 890, 442 805, 432 725 "
       "C 380 668, 348 590, 348 470 C 348 330, 425 248, 545 240 "
       "C 600 238, 640 248, 668 262 C 730 252, 762 300, 748 362 C 744 400, 756 440, 774 470 L 808 538 "
       "C 814 556, 800 566, 778 566 C 782 584, 790 596, 782 610 "
       "C 774 620, 764 622, 774 636 C 782 654, 772 680, 752 694 "
       "C 742 712, 722 726, 682 730 C 640 734, 628 762, 630 805 "
       "C 632 860, 652 905, 720 940 C 830 1000, 890 1080, 900 1200 Z")
ARM = ("M 360 1200 C 372 1000, 382 820, 392 640 C 360 600, 345 540, 352 470 "
       "C 330 455, 318 420, 330 390 C 345 352, 380 345, 405 360 "
       "C 400 300, 420 268, 465 265 C 490 238, 535 235, 560 258 "
       "C 590 238, 635 245, 650 280 C 690 280, 712 318, 700 360 "
       "C 712 420, 700 500, 668 560 C 650 600, 640 620, 628 650 "
       "C 632 820, 640 1000, 652 1200 Z")


def silhouette(path, fill="#1d1f24", w=1000, h=1200, scale=1.0, mirror=False):
    t = f'transform="translate(1000,0) scale(-1,1)"' if mirror else ""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{int(w*scale)}" height="{int(h*scale)}" viewBox="0 0 {w} {h}">'
           f'<path {t} d="{path}" fill="{fill}"/></svg>')
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert("RGBA")


if __name__ == "__main__":
    S = Image.new("RGB", (3000, 1200), (255, 200, 60))
    for i, p in enumerate([WOMAN, MAN, ARM]):
        im = silhouette(p); S.paste(im, (i * 1000, 0), im)
    S.resize((1500, 600)).save("/tmp/shapes.jpg")

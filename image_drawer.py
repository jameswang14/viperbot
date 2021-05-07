import os
import random
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from viper_rnn import load_pretrained_model


def _pick_font_with_size(image_size, txt, font_path, img_fraction=0.85):
    fontsize = 12
    font = ImageFont.truetype(font_path, fontsize)
    while font.getsize(txt)[0] < img_fraction * image_size[0]:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype(font_path, fontsize)
    return font


def _horz_center(image_width, text_width):
    return (image_width - text_width) / 2


# def get_avg_color(x, y, dx, dy):


def draw_text(
    top_text, bottom_text, img_file_path, font_color, font_path, outfile_name
):
    img = Image.open(img_file_path)
    draw = ImageDraw.Draw(img)

    font = _pick_font_with_size(img.size, top_text, font_path)
    horz_center = _horz_center(img.width, font.getsize(top_text)[0])
    top_coor = (horz_center, 0)
    draw.text(top_coor, top_text, fill=font_color, font=font)

    font = _pick_font_with_size(img.size, bottom_text, font_path)
    horz_center = _horz_center(img.width, font.getsize(bottom_text)[0])
    bottom_coor = (horz_center, img.height - font.getsize(bottom_text)[1] - 5)
    draw.text(bottom_coor, bottom_text, fill=font_color, font=font)

    img.save(outfile_name)


def select_random_font():
    font_folder = random.choice([x[0] for x in os.walk("./fonts")])

    for x in next(os.walk(font_folder))[2]:
        if ".ttf" in x:
            return os.path.join(font_folder, x)
    return ""


def random_color():
    rgbl = [255, 0, 0]
    random.shuffle(rgbl)
    return tuple(rgbl)


n = 10
rnn = load_pretrained_model("./weights/viper_v2.hdf5")
bottom_texts = rnn.generate(temperature=0.9, n=n, return_as_list=True)
for x in range(0, n):
    draw_text(
        "Viper the Rapper",
        bottom_texts[x],
        "matt.jpg",
        random_color(),
        select_random_font(),
        "./img/sample_{}.jpg".format(x),
    )

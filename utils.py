import os
import random
import traceback

from fontTools.ttLib import TTFont
from PIL import ImageFont, ImageDraw, Image

import config


# Convert string to list character-wise
def convert_string_to_list(string):
    character_list = string.split("\n")
    if "\n" in character_list:
        character_list.remove("\n")
    if "" in character_list:
        character_list.remove("")
    if "" in character_list or "\n" in character_list:
        if "" in character_list:
            print("None in character list")
        if "\n" in character_list:
            print("\n in character list")
        exit()
    for ch in character_list:
        if character_list.count(ch) != 1:
            print(f"Character duplicate {ch}")
            exit()
    if " " not in character_list:
        print("Space not in character list")
        exit()
    return character_list


# create String from data
def choose_string(s, size, index_character, language="en"):
    # check error
    assert size >= 1 and len(" ".join(s.split()).strip()) > 0

    # if len(s) <= size:
    #     return " ".join(s.split()).strip()
    if len(s) <= size:
        return s.strip()
    # initialize an empty string
    str1 = ""

    # get start and end of index for cut string
    start_cut = random.randint(max(0, index_character - size), index_character)
    end_cut = min(start_cut + size, len(s) - 1)

    # cut string
    for x in range(start_cut, end_cut):
        str1 += s[x]

    # format string
    # str1 = " ".join(str1.split())
    str1 = str1.strip()

    # remove space in japanese
    # if language == "ja":
    #     str1 = str1.replace(" ", "")
    return str1


# for random color background and text
def random_color(prop, dis_color):
    prop_color = random.uniform(0, 1)
    if prop_color >= prop:
        background_color = random.randint(dis_color + 1, 255)
        text_color = max(0, background_color - random.randint(dis_color, background_color))
    else:
        background_color = random.randint(0, 255 - dis_color - 21)
        text_color = min(255, background_color + random.randint(dis_color, 255 - background_color) + 20)
    return background_color, text_color


# for check font
def has_glyph(font, glyph):
    for table in font['cmap'].tables:
        if ord(glyph) in table.cmap.keys():
            return True
    return False


# Choose random font
def choose_random_font(fonts_directory, str1, font_size_text):
    import warnings
    warnings.filterwarnings("ignore")
    while True:
        try:
            ft = random.choice([x for x in os.listdir(os.getcwd() + "/" + fonts_directory) if
                                os.path.isfile(os.path.join(os.getcwd() + "/" + fonts_directory, x)) and (
                                        x.endswith(".ttf") or x.endswith(".otf") or x.endswith(".TTF")) or x.endswith(
                                    ".ttc")])
            font_check = TTFont(os.getcwd() + "/" + fonts_directory + "/" + ft)
            while not all(has_glyph(font_check, x) for x in str1):
                # print("loop font")
                ft = random.choice([x for x in os.listdir(os.getcwd() + "/" + fonts_directory) if
                                    os.path.isfile(os.path.join(os.getcwd() + "/" + fonts_directory, x))])
                font_check = TTFont(os.getcwd() + "/" + fonts_directory + "/" + ft)
            font = ImageFont.truetype(os.getcwd() + "/" + fonts_directory + "/" + ft, font_size_text)
            break
        except Exception as e:
            print(f"Font is error: ", os.getcwd() + "/" + fonts_directory + "/" + ft)
            print(e)
    return font


# Draw Image
def create_image(str1, font, background_color, text_color):
    start_text_position = (
        random.randint(
            int(config.point_start_text),
            int(
                config.range_start_text_width +
                config.point_start_text
            )
        ),
        random.randint(
            int(config.point_start_text),
            int(
                config.range_start_text_height +
                config.point_start_text
            )
        )
    )
    line = random.randint(2, 9)
    img_save = convert_string_image(str1, font, background_color, text_color,
                                    start_text_position, line)
    return img_save


def set_height_width_image(str1, font, start_text_position, line, max_length_splitted):
    # print("******")
    # print(line)
    # print(str1)

    height = int(font.getsize(str1)[1] + start_text_position[1] +
                 random.randint(0, config.redundancy_letters_height)) * line  # merge-height
    # print(height)
    width = int(font.getsize(max_length_splitted.replace("\n", ""))[0] + start_text_position[0] +
                random.randint(0, config.redundancy_letters_width))

    return height, width


# (random.randint(0,9))

# convert string to image
def convert_string_image(str1, font, background_color, text_color,
                         start_text_position, line):
    # height, width = set_height_width_image(str1, font, start_text_position, line, str1)

    splitted = []
    prev = 0
    while True:
        splitted.append(str1[prev:prev + line])
        prev = prev + line
        if prev >= len(str1) - 1:
            break
    splitted = [ch + "\n" for ch in splitted]
    line = len(splitted)
    max_length_splitted = max(splitted, key=len)
    splitted = "".join(splitted)
    splitted = splitted[:len(splitted) - 1]


    height, width = set_height_width_image(splitted, font, start_text_position, line, max_length_splitted)
    # print("font.getsize(str1)", font.getsize(str1))
    img_save = Image.new('L', (width, height), color=background_color)

    d = ImageDraw.Draw(img_save)

    d.text(start_text_position, splitted, font=font, fill=text_color)

    return img_save

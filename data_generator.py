import json
import random

import numpy

import config
import utils


class CreateDataFromWiki:
    def __init__(self, length_text=30, wikipedia=config.ja_wikipedia_file,
                 characters_list=config.ja_chars_list_file,
                 characters_indexing=config.ja_chars_indexing,
                 font_directory=config.font_directory):
        """

        :param length_text:
        :param wikipedia:
        :param characters_list:
        :param characters_indexing:
        :param font_directory:
        """
        assert length_text >= 1 # check điều kiện

        self.length_text = length_text

        with open(characters_list) as file_chars_list:
            self.characters_list = utils.convert_string_to_list(file_chars_list.read())  # [1,4,6,3,4]

        self.list_sequence = []
        with open(wikipedia) as file_wikipedia:
            self.list_sequence = file_wikipedia.read().splitlines() # into string, slipt by \n

        with open(characters_indexing) as file_character_indexing:
            self.character_indexing = json.load(file_character_indexing) # convert from json format to python format...

        self.font_directory = font_directory
        self.characters_list_before_replace = self.characters_list

    def create_image(self):
        string_output = ""
        # 50

        # get sting
        while 1:
            size = random.randint(1, self.length_text)
            character = random.choice(self.characters_list)

            if character == "" or character is None:
                print("character is \"\" or None")
                continue
            while character == " ":
                character = random.choice(self.characters_list) # chọn tiếp nếu random ra " "

            list_id_sequence = self.character_indexing.get(character)

            if not list_id_sequence or size == 1 or len(list_id_sequence) == 0:
                # string_output = character
                continue
            # if character in indexing, find string has character
            else:
                # get id sequence
                ind_sequence_choose = random.choice(list_id_sequence)

                # get index character
                index_character = random.choice(
                    [i for i, ltr in enumerate(self.list_sequence[ind_sequence_choose]) if ltr == character])

                # get string
                string_output = utils.choose_string(self.list_sequence[ind_sequence_choose], size, index_character)

                # check character in character_list or not
                for ch in string_output:
                    if ch not in self.characters_list:
                        string_output = string_output.replace(ch, "")

                if (" ".join(string_output.split()).strip() == "" or string_output is None or string_output.rstrip(
                        "\n") == ""
                        or string_output == "" or len("".join(string_output.split()).strip()) == 1 or len(string_output.rstrip("\n"))==1):
                    continue
            break
        image = self.create_image_by_string(string_output)
        return string_output, image

    def create_image_by_string(self, string_output):
        background_color, text_color = utils.random_color(config.property_choose_color,
                                                          config.distance_color)
        font_size_text = random.randint(config.range_font_size_text[0],
                                        config.range_font_size_text[1])

        # choose font
        font = utils.choose_random_font(self.font_directory, string_output, font_size_text)

        image = utils.create_image(string_output, font, background_color, text_color)
        return numpy.asarray(image)

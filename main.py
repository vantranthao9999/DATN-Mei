import os
import cv2
from PIL import Image

import config
from data_generator import CreateDataFromWiki


def delete_all_files(folder_path):
    for file in os.listdir(folder_path):
        os.remove(os.path.join(folder_path, file))


if __name__ == "__main__":
    print("Create or remove file in folder")
    os.makedirs(f'{config.folder_image_output_generator}', exist_ok=True)
    delete_all_files(f'{config.folder_image_output_generator}')

    # Create file ground if not exist or clean file if file exist
    file = open(config.file_label, "w")
    file.close()

    create_image_from_wiki = CreateDataFromWiki(length_text=30, wikipedia=config.ja_wikipedia_file,
                                                characters_list=config.ja_chars_list_file,
                                                characters_indexing=config.ja_chars_indexing,
                                                font_directory=config.font_directory)

    for number_image in range(0, config.total_image_gen): # 50
        label, img = create_image_from_wiki.create_image()
        path_image = os.path.join(config.folder_image_output_generator, f"{config.name_image}_{number_image}.png")
        try:
            cv2.imwrite(path_image, img)
        except Exception as e:
            print(e)

        file = open(config.file_label, "a+") # ghi thêm vào file output
        file.write(f"{path_image}:{label}\n")
        file.close()

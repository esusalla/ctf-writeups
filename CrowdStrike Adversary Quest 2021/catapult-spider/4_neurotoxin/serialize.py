import base64
import os
import sys

import tensorflow


def load_and_serialize_picture(path):
    img_unprepared = tensorflow.keras.preprocessing.image.load_img(path)
    img = tensorflow.keras.preprocessing.image.img_to_array(img_unprepared) / 255.0

    assert img.shape == (180, 180, 3)

    return base64.b64encode(tensorflow.io.serialize_tensor(img).numpy()).decode()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    target_dir = sys.argv[1]

    # Serialize images
    for img in os.listdir(target_dir):
        if img.endswith(".png"):
            data = load_and_serialize_picture(target_dir + img)
            with open(target_dir + img.replace(".png", ".dat"), "w") as outfile:
                outfile.write(data)


#!/usr/bin/env python3

""" Example Conversion

This script converts an image (e.g. png) into the format that is expected
by the remote classification service.
"""

# disable tensorflow logging:
import logging
import os

logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import argparse
import base64
import tensorflow

def load_and_serialize_picture(path):
    """ Reads an image from given path and encodes it. """

    img_unprepared = tensorflow.keras.preprocessing.image.load_img(path)
    img = tensorflow.keras.preprocessing.image.img_to_array(img_unprepared) / 255.0

    assert img.shape == (180, 180, 3)

    return base64.b64encode(tensorflow.io.serialize_tensor(img).numpy()).decode()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dst")
    parser.add_argument("src")
    args = parser.parse_args()

    img = load_and_serialize_picture(args.src)

    with open(args.dst, "w") as writer:
        writer.write(img)

if __name__ == "__main__":
    main()

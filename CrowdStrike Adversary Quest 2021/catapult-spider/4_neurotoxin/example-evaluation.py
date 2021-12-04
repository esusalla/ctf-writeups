#!/usr/bin/env python3

""" Example Evaluation.

This script is provided to you to verify your solution locally. It expects the encoded raw
image data (please take a look at example-conversion.py).

Example:
--------

    $ python3 example-conversion.py /tmp/cat1.dat ./my-cat-pictures/cat1.png
    $ ... do your modifications $ python3 example-evaluation.py --original ./my-cat-pictures/cat1.png /tmp/cat1.dat ...

Your solution is fine if and only if:

    1) the differences between the original picture and your modification is small enough
    2) the modified picture is classified as a doge
"""


import logging
import os

logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import argparse
import base64
import matplotlib.pyplot
import numpy
import tensorflow

def load_image(path):
    img = tensorflow.keras.preprocessing.image.load_img(path)
    img_prepared = tensorflow.keras.preprocessing.image.img_to_array(img) / 255.0
    assert img_prepared.shape == (180, 180, 3)
    return img_prepared

def load_and_deserialize_picture(path):
    with open(path, "rb") as reader:
        data = reader.read()

    return tensorflow.io.parse_tensor(base64.b64decode(data), out_type=tensorflow.float32)

def predict(batch):
    labels = {0: "Cat", 1: "Cow", 2: "Elephant", 3: "Doge", 4: "Squirrel"}
    model = tensorflow.keras.models.load_model("./tf-model")

    prediction = model.predict(batch)
    score = tensorflow.nn.softmax(prediction[0])
    print(score)
    classification = labels[numpy.argmax(score)]

    print(f"[*] prediction result (classified as {classification}):")

    for class_index, class_confidence in enumerate(score):
        percent = round(float(class_confidence * 100), 2)
        print(f"    class #{class_index} => {percent:02.02f}% ({labels[class_index]})")

    if score[3] < 0.95:
        print("[!] picture will be encrypted :(")
    else:
        print("[+] picture won't be encrypted \\o/")

    return classification

def verify_difference(img_a, img_b):
    accepted_offset = 0.025

    difference = img_a - img_b
    max_value = round(difference.numpy().max(), 6)
    min_value = round(abs(difference.numpy().min()), 6)
    print(min_value, max_value)

    if max_value <= accepted_offset and min_value <= accepted_offset:
        print("[+] both images are close enough")
    else:
        print("[!] both images are not close enough")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--original")
    parser.add_argument("--show", action="store_true")
    parser.add_argument("input_file")
    args = parser.parse_args()

    image = load_and_deserialize_picture(args.input_file)

    # check if the modification is small enough:
    if args.original:
        verify_difference(load_image(args.original), image)

    # classify the image with the given model:
    batch = tensorflow.expand_dims(image, 0)
    classification = predict(batch)

    # plot image if requested:
    if args.show:
        matplotlib.pyplot.figure()
        matplotlib.pyplot.imshow(image)
        matplotlib.pyplot.title(f"My favorite {classification}")
        matplotlib.pyplot.show()

if __name__ == "__main__":
    main()

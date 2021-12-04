import base64

import numpy
import tensorflow
from PIL import Image


def load_and_deserialize_picture(path):
    with open(path, "rb") as reader:
        data = reader.read()

    return tensorflow.io.parse_tensor(base64.b64decode(data), out_type=tensorflow.float32)


if __name__ == "__main__":
    flag = load_and_deserialize_picture("flag.dat")
    flag = flag.numpy()[0].clip(0, 1) * 255

    img = Image.fromarray(flag.astype(numpy.uint8))
    img.save("flag.png")


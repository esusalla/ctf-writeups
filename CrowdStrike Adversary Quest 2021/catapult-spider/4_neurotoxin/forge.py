# Reference: https://medium.com/@ageitgey/machine-learning-is-fun-part-8-how-to-intentionally-trick-neural-networks-b55da32b7196

import os

import numpy
import tensorflow
from keras.preprocessing import image
from keras import backend
from PIL import Image


def forge_image(path, target_class):
    # Load the image to modify
    img = image.load_img(path, target_size=(180, 180))
    original_img = image.img_to_array(img)

    # Normalize values so that all pixels are between [0, 1] as the model expects
    original_img /= 255.0

    # Add a 4th dimension for batch size (as Keras expects)
    original_img = numpy.expand_dims(original_img, axis=0)

    # Pre-calculate the maximum changes allowed
    max_change_above = original_img + 0.02
    max_change_below = original_img - 0.02

    # Create copy of input image to modify
    forged_img = numpy.copy(original_img)

    # How much to update image in each iteration
    learning_rate = 0.1

    # Likelihood the image is the target class according to the pre-trained model
    cost_func = output_layer[0, target_class]

    # Calculate gradient based on input image and currently predicted class
    # Referring to "input_layer" gives back image being forged
    gradient_func = backend.gradients(cost_func, input_layer)[0]

    # Calculates current cost and gradients
    get_cost_and_gradients = backend.function([input_layer, backend.learning_phase()], [cost_func, gradient_func])

    cost = 0.0
    count = 0

    while cost < 17.5 and count < 2000:
        # Grab the costs and gradients to push forged image in right direction
        cost, gradients = get_cost_and_gradients([forged_img, 0])
        
        # Move the forged image one step further towards the target class
        forged_img += gradients * learning_rate

        # Ensure the image doesn't fall outside the allowed ranges
        forged_img = numpy.clip(forged_img, max_change_below, max_change_above)
        forged_img = numpy.clip(forged_img, 0.0, 1.0)

        count += 1

    img = forged_img[0]
    img *= 255.0

    img_out = Image.fromarray(img.astype(numpy.uint8))
    outpath = path.replace("my-cat-pictures", "forged-pictures").replace("cat", "forged")
    img_out.save(outpath)
    print(path, "forged")



if __name__ == "__main__":
    tensorflow.compat.v1.disable_eager_execution()

    # Load image recognition model
    model = tensorflow.keras.models.load_model("./tf-model")

    # Grab references to the first and last layer
    input_layer = model.layers[0].input
    output_layer = model.layers[-1].output

    # labels = {0: "Cat", 1: "Cow", 2: "Elephant", 3: "Doge", 4: "Squirrel"}
    target_class = 3 # trying to forge doge pictures
    
    cat_dir = "./my-cat-pictures/"
    forge_dir = "./forged-pictures/"

    # Forge images
    for img in os.listdir(cat_dir):
        if img.endswith(".png"):
            forge_image(cat_dir + img, target_class)


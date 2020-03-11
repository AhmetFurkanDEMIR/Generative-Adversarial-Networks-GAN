import math
import numpy as np


def combine_images(generated_images):
    total,width,height = generated_images.shape[:-1]
    cols = int(math.sqrt(total))
    rows = math.ceil(float(total)/cols)
    combined_image = np.zeros((height*rows, width*cols),
                              dtype=generated_images.dtype)

    for index, image in enumerate(generated_images):
        i = int(index/cols)
        j = index % cols
        combined_image[width*i:width*(i+1), height*j:height*(j+1)] = image[:, :, 0]
    return combined_image


def show_progress(epoch, batch, g_loss, d_loss, g_acc, d_acc):
    msg = "epoch: {}, batch: {}, g_loss: {}, d_loss: {}, g_accuracy: {}, d_accuracy: {}"
    print(msg.format(epoch, batch, g_loss, d_loss, g_acc, d_acc))

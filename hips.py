import os
import numpy as np
import matplotlib.pyplot as plt


def read_header(fname):

    """
    :param fname:
    :return:

    header_length, bands, res_x, res_y, fmt
    """

    # grab header info
    header_length = open(fname).read().find('\n.')
    header = open(fname).read()[:header_length].split()
    bands = int(header[1])
    res_x = int(header[2])
    res_y = int(header[3])
    fmt = int(header[4])

    return header_length, bands, res_x, res_y, fmt

def read_hips(fname):

    header_length, bands, res_x, res_y, fmt = read_header(fname)

    # extract image from hips
    hips = np.fromfile(fname, np.float32)
    hips_length = len(hips)
    img = hips[hips_length - (bands * res_x * res_y):].reshape(bands, res_x, res_y)
    img = np.rot90(img.T, 3)

    return img, bands, res_x, res_y, fmt


def hipstats(fname):

    img, bands, res_x, res_y, fmt = read_hips(fname)
    return img.min(), img.max(), img.mean(), img.std()


def hips2img(fname, order=[0,1,2], stretch=True, imshow=True,
             image_save=False, ax=None):
    
    img, bands, res_x, res_y, fmt = read_hips(fname)
    
    #stretch
    for b in range(bands):
        arr_b = img[:, :, b]
        if stretch:
            arr_b = ((arr_b - np.percentile(arr_b, 2.5)) / np.percentile(arr_b, 97.5))
            arr_b[arr_b < 0] = 0
            arr_b[arr_b > 1] = 1
        img[:, :, b] = arr_b

    # display image
    if not ax:
        fig, ax = plt.subplots(figsize=(10, 10))

    if len(order) == 1 or bands == 1:
        order = order[0]
        cmap = 'gray'
    else:
        cmap = 'spectral'
    ax.axis('off')
    ax.imshow(img[:, :, order], cmap=cmap, interpolation='none')

    # save image
    if image_save:
        plt.imsave(os.path.splitext(fname)[0] + '.png', img)

    # plot image to screen
    if imshow:
        plt.show()

    return ax
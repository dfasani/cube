# import the necessary packages
import numpy as np
import logging
import argparse
import cv2
import glob, os

MAX_SIZE = 800  # taille maximale de l’image en pixels

# version BGR
'''
colors = dict(
    {
        "R": (60, 50, 105),
        "O": (60, 70, 170),
        "G": (50, 100, 70),
        "B": (100, 60, 0),
        "Y": (80, 120, 160),
        "W": (150, 150, 130)
    }
)
'''

# version HSV
colors = dict(
    {
        "R ": (170, 195, 100),
        "O1": (60, 160, 145),
        "O2": (7, 160, 150),
        "O3": (170, 170, 170),
        "O4": (1, 160, 170),
        "O5": (22, 165, 140),
        "Y1": (15, 150, 170),
        "Y2": (15, 156, 154),
        "G ": (70, 120, 100),
        "B ": (100, 240, 100),
        "W ": (100, 25, 150)
    }
)

# logging.basicConfig(level=logging.DEBUG)

for file in glob.glob("square*.jpg"):
    # load the image
    image = cv2.imread(file)
    logging.info("Résolution de l'image  {2}: '{0}x{1}'".format(image.shape[1], image.shape[0], file))

    # On vérifie si l'image est trop grande et si c'est le cas on calcule un ratio pour la réduire
    ratio = 1
    if image.shape[1] > MAX_SIZE or image.shape[0] > MAX_SIZE:
        if image.shape[1] / MAX_SIZE > image.shape[0] / MAX_SIZE:
            ratio = float(image.shape[1]) / MAX_SIZE
        else:
            ratio = float(image.shape[0]) / MAX_SIZE

    ## Si l'image est trop grande, on la retaille
    if ratio != 1:
        newsize = (int(image.shape[1] / ratio), int(image.shape[0] / ratio))
        logging.info("Redimensionnement de l'image en : {0}".format(newsize))
        image = cv2.resize(image, newsize)

    for numcolonne in range(3):
        for numligne in range(3):
            x1 = 230 + 150 * numligne
            y1 = 40 + 150 * numcolonne
            x2 = 280 + 150 * numligne
            y2 = 90 + 150 * numcolonne

            crop_img = image[y1:y2, x1:x2]

            crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)

            average_color_per_row = np.average(crop_img, axis=0)
            average_color = np.average(average_color_per_row, axis=0)

            # initialize the minimum distance found thus far
            minDist = 255 + 255 + 255
            couleur = None

            # loop over the known color values
            for nom, brg in colors.items():

                # compute euclidian distance
                d = abs(brg[0] - average_color[0]) + abs(brg[1] - average_color[1]) + abs(brg[2] - average_color[2])

                # if the distance is smaller than the current distance,
                # then update the bookkeeping variable
                if d < minDist:
                    minDist = d
                    couleur = nom

            if numligne == 2 :
                print(couleur[0])
            else:
                print(couleur[0] + '|', end='')
            #print(average_color, "-->", couleur)

            # un petit carré vert
            cv2.rectangle(image, (x1 - 1, y1 - 1), (x2 + 1, y2 + 1), (0, 255, 0), 1)

    print()

    cv2.imshow("images", image)
    cv2.waitKey(0)

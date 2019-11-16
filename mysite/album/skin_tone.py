import numpy as np
import cv2
from sklearn.cluster import KMeans
from collections import Counter
import imutils
import pprint

def extractSkin(image):
    # Taking a copy of the image
    img = image.copy()
    img_bgra = cv2.cvtColor(img,cv2.COLOR_BGR2BGRA)

    # BGRA
    skin_mask_bgra = np.zeros((img_bgra.shape[0],img_bgra.shape[1]),np.uint8)

    for y in range(img_bgra.shape[0]):
        for x in range(img_bgra.shape[1]):
            b = img_bgra.item(y,x,0)
            g = img_bgra.item(y,x,1)
            r = img_bgra.item(y,x,2)
            a = img_bgra.item(y,x,3)
            if (r > 95) & (g > 40) & (b > 20) & (r > b) & (r - g > 15) & (a > 15):
                skin_mask_bgra[y,x] = 1

    # YCrCb
    YCrCb = cv2.cvtColor(img,cv2.COLOR_BGR2YCrCb) 
    lower_threshold = np.array([0, 130, 100], dtype=np.uint8)
    upper_threshold = np.array([255, 175, 127], dtype=np.uint8)
    skin_mask_ycrcb = cv2.inRange(YCrCb, lower_threshold, upper_threshold)

    # HSV
    #HSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #lower_threshold = np.array([0, 48, 80], dtype=np.uint8)
    #upper_threshold = np.array([20, 255, 255], dtype=np.uint8)
    #skin_mask_hsv = cv2.inRange(HSV, lower_threshold, upper_threshold)

    skin_mask = cv2.bitwise_and(skin_mask_bgra, skin_mask_ycrcb)
    skin_mask = cv2.GaussianBlur(skin_mask, (3, 3), 0)

    # Extracting skin from the threshold mask
    skin = cv2.bitwise_and(img, img, mask=skin_mask)

    # Return the Skin image
    return skin


def removeBlack(estimator_labels, estimator_cluster):

    # Check for black
    hasBlack = False

    # Get the total number of occurance for each color
    occurance_counter = Counter(estimator_labels)

    # Quick lambda function to compare to lists
    def compare(x, y): return Counter(x) == Counter(y)

    # Loop through the most common occuring color
    for x in occurance_counter.most_common(len(estimator_cluster)):

        # Quick List comprehension to convert each of RBG Numbers to int
        color = [int(i) for i in estimator_cluster[x[0]].tolist()]

        # Check if the color is [0,0,0] that if it is black
        if compare(color, [0, 0, 0]) == True:
            # delete the occurance
            del occurance_counter[x[0]]
            # remove the cluster
            hasBlack = True
            estimator_cluster = np.delete(estimator_cluster, x[0], 0)
            break

    return (occurance_counter, estimator_cluster, hasBlack)


def getColorInformation(estimator_labels, estimator_cluster, hasThresholding=False):

    # Variable to keep count of the occurance of each color predicted
    occurance_counter = None

    # Output list variable to return
    colorInformation = []

    # Check for Black
    hasBlack = False

    # If a mask has be applied, remove th black
    if hasThresholding == True:

        (occurance, cluster, black) = removeBlack(
            estimator_labels, estimator_cluster)
        occurance_counter = occurance
        estimator_cluster = cluster
        hasBlack = black

    else:
        occurance_counter = Counter(estimator_labels)

    # Get the total sum of all the predicted occurances
    totalOccurance = sum(occurance_counter.values())

    # Loop through all the predicted colors
    for x in occurance_counter.most_common(len(estimator_cluster)):

        index = (int(x[0]))

        # Quick fix for index out of bound when there is no threshold
        index = (index-1) if ((hasThresholding & hasBlack)
                              & (int(index) != 0)) else index

        # Get the color number into a list
        color = estimator_cluster[index].tolist()

        # Get the percentage of each color
        color_percentage = (x[1]/totalOccurance)

        # make the dictionay of the information
        colorInfo = {"cluster_index": index, "color": color,
                     "color_percentage": color_percentage}

        # Add the dictionary to the list
        colorInformation.append(colorInfo)

    return colorInformation


def extractDominantColor(image, number_of_colors=5, hasThresholding=False):

    # Quick Fix Increase cluster counter to neglect the black(Read Article)
    if hasThresholding == True:
        number_of_colors += 1

    # Taking Copy of the image
    img = image.copy()

    # Convert Image into RGB Colours Space
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Reshape Image
    img = img.reshape((img.shape[0]*img.shape[1]), 3)

    # Initiate KMeans Object
    estimator = KMeans(n_clusters=number_of_colors, random_state=0)

    # Fit the image
    estimator.fit(img)

    # Get Colour Information
    colorInformation = getColorInformation(
        estimator.labels_, estimator.cluster_centers_, hasThresholding)
    return colorInformation


def plotColorBar(colorInformation):
    # Create a 500x100 black image
    color_bar = np.zeros((100, 500, 3), dtype="uint8")

    top_x = 0
    for x in colorInformation:
        bottom_x = top_x + (x["color_percentage"] * color_bar.shape[1])

        color = tuple(map(int, (x['color'])))

        cv2.rectangle(color_bar, (int(top_x), 0),
                      (int(bottom_x), color_bar.shape[0]), color, -1)
        top_x = bottom_x
    return color_bar


"""## Section Two.4.2 : Putting it All together: Pretty Print

The function makes print out the color information in a readable manner
"""


def prety_print_data(color_info):
    for x in color_info:
        print(pprint.pformat(x))
        print()

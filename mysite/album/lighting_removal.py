import numpy as np
import cv2

def clahe(image):
    #LAB = cv2.cvtColor(image,cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(image)
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    l_clahe = clahe.apply(l)
    
    result_lab = cv2.merge((l_clahe,a,b))
    result = cv2.cvtColor(result_lab,cv2.COLOR_LAB2BGR)
    return result

def histogram(image):
    #LAB = cv2.cvtColor(image,cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(image)
    #hist, bins = np.histogram(l.ravel(), 256, [0,256])
    hist, bins = np.histogram(l.ravel(), 256, [1,256])
    cdf = hist.cumsum()

    cdf_m = np.ma.masked_equal(cdf,0)
    cdf_m = (cdf_m-cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
    cdf = np.ma.filled(cdf_m, 0).astype('uint8')
    l_he = cdf[l]
    
    result_lab = cv2.merge((l_he,a,b))
    result = cv2.cvtColor(result_lab,cv2.COLOR_LAB2BGR)
    #cv2.imshow("he", result)
    return result

def normalize_lighting(image, norm):
    l, a, b = cv2.split(image)
    mean = 0
    count = 0
    for y in range(l.shape[0]):
        for x in range(l.shape[1]):
            if l.item(y,x) != 0:
                mean += l.item(y,x)
                count = count + 1
    mean = mean / count
    print("====")
    print(mean)
    diff = norm - mean
    
    for y in range(l.shape[0]):
        for x in range(l.shape[1]):
            if l.item(y,x) == 0:
                l.itemset(y,x,0)
            elif l.item(y,x)+diff > 255:
                l.itemset(y,x,255)
            elif l.item(y,x)+diff < 0:
                l.itemset(y,x,0)
            else:
                l.itemset(y,x,l.item(y,x)+diff)
    result_lab = cv2.merge((l,a,b))
    return cv2.cvtColor(result_lab,cv2.COLOR_LAB2BGR)

def lighting_removal(image, norm):
    img = image.copy()
    cv2.imshow("1",img)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    #image_he = histogram(lab)
    image_he = clahe(lab)
    cv2.imshow("2", cv2.cvtColor(image_he,cv2.COLOR_LAB2BGR))
    image_norm = normalize_lighting(image_he, norm)
    cv2.imshow("3", image_norm)
    return image_norm

def normalize(image, norm):
    LAB = cv2.cvtColor(image,cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(LAB)
    
    for y in range(l.shape[0]):
        for x in range(l.shape[1]):
            if l.item(y,x) != 0:
                l.itemset(y,x,norm)
    #return normalize_lighting(LAB, norm)
    
    result_lab = cv2.merge((l,a,b))
    return cv2.cvtColor(result_lab,cv2.COLOR_LAB2BGR)

"""fname = 'img/test3.png'

img = cv2.imread(fname, cv2.IMREAD_COLOR)
img2 = histogram(cv2.cvtColor(img,cv2.COLOR_BGR2LAB))
cv2.imshow("original image", img)
cv2.imshow("after image", img2)
#cv2.imshow("norm image", img3)
cv2.waitKey(0)
cv2.destroyAllWindows()"""
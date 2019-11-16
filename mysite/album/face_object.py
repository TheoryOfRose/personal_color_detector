from django.conf import settings
import numpy as np
import cv2
import os

HAAR_DIR = os.path.join(settings.BASE_DIR, 'mysite/album/haar_cascade/')

def extractFaceSkin(image):

    # Convert image to gray image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Take face haar cascade
    face_cascade = cv2.CascadeClassifier(os.path.join(HAAR_DIR,'Face.xml'))
    faces = face_cascade.detectMultiScale(gray, 1.1, 6)

    # Make mask
    face = np.zeros(shape=image.shape[:2], dtype=np.uint8)
    for (x,y,w,h) in faces:
        cv2.rectangle(img=face, pt1=(x,y), pt2=(x+w,y+h), color=(255,255,255), thickness=-1)
        face = removeEye(gray, face)
        face = removeNose(gray, face)
        face = removeMouth(gray, face)
        face = removeEar(gray, face)
    face_skin = cv2.bitwise_and(image, image, mask=face)

    return face_skin

def removeEye(roi_gray, mask):

    # Take eye haar cascade
    eye_cascade = cv2.CascadeClassifier(os.path.join(HAAR_DIR,'Eye.xml'))
    eyes = eye_cascade.detectMultiScale(roi_gray)

    for (x,y,w,h) in eyes:
        cv2.rectangle(img=mask, pt1=(x,y), pt2=(x+w,y+h), color=(0,0,0), thickness=-1)
    
    return mask

def removeNose(roi_gray, mask):

    # Take nose haar cascade
    nose_cascade = cv2.CascadeClassifier(os.path.join(HAAR_DIR,'Nose.xml'))
    noses = nose_cascade.detectMultiScale(roi_gray)

    for (x,y,w,h) in noses:
        cv2.rectangle(img=mask, pt1=(x,y), pt2=(x+w,y+h), color=(0,0,0), thickness=-1)
    
    return mask

def removeMouth(roi_gray, mask):

    # Take mouth haar cascade
    mouth_cascade = cv2.CascadeClassifier(os.path.join(HAAR_DIR,'Mouth.xml'))
    mouths = mouth_cascade.detectMultiScale(roi_gray)

    for (x,y,w,h) in mouths:
        cv2.rectangle(img=mask, pt1=(x,y), pt2=(x+w,y+h), color=(0,0,0), thickness=-1)
    
    return mask

def removeEar(roi_gray, mask):

    # Take ear haar cascade
    left_cascade = cv2.CascadeClassifier(os.path.join(HAAR_DIR,'LeftEar.xml'))
    lefts = left_cascade.detectMultiScale(roi_gray)
    right_cascade = cv2.CascadeClassifier(os.path.join(HAAR_DIR,'RightEar.xml'))
    rights = right_cascade.detectMultiScale(roi_gray)

    for (x,y,w,h) in lefts:
        cv2.rectangle(img=mask, pt1=(x,y), pt2=(x+w,y+h), color=(0,0,0), thickness=-1)
    for (x,y,w,h) in rights:
        cv2.rectangle(img=mask, pt1=(x,y), pt2=(x+w,y+h), color=(0,0,0), thickness=-1)
    
    return mask

# Just for debugging
def detectFace(image):
    face_cascade = cv2.CascadeClassifier(os.path.join(HAAR_DIR,'Face.xml'))
    eye_cascade = cv2.CascadeClassifier(os.path.join(HAAR_DIR,'Eye.xml'))
    nose_cascade = cv2.CascadeClassifier(os.path.join(HAAR_DIR,'Nose.xml'))
    mouth_cascade = cv2.CascadeClassifier(os.path.join(HAAR_DIR,'Mouth.xml'))
    left_ear_cascade = cv2.CascadeClassifier(os.path.join(HAAR_DIR,'LeftEar.xml'))
    right_ear_cascade = cv2.CascadeClassifier(os.path.join(HAAR_DIR,'RightEar.xml'))

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
 
    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = image[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        nose = nose_cascade.detectMultiScale(roi_gray)
        mouth = mouth_cascade.detectMultiScale(roi_gray)
        left_ear = left_ear_cascade.detectMultiScale(roi_gray)
        right_ear = right_ear_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        for (nx,ny,nw,nh) in nose:
            cv2.rectangle(roi_color,(nx,ny),(nx+nw,ny+nh),(0,0,255),2)
        for (mx,my,mw,mh) in mouth:
            cv2.rectangle(roi_color,(mx,my),(mx+mw,my+mh),(0,255,255),2)
        for (lx,ly,lw,lh) in left_ear:
            cv2.rectangle(roi_color,(lx,ly),(lx+lw,ly+lh),(255,255,0),2)
        for (rx,ry,rw,rh) in right_ear:
            cv2.rectangle(roi_color,(rx,ry),(rx+rw,ry+rh),(0,255,255),2)

    return image
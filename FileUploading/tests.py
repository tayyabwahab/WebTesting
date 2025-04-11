import cv2 
import numpy as np 
  

def image_set(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    equ = cv2.equalizeHist(gray) 
    blurred = cv2.GaussianBlur(src=equ, ksize=(3, 5), sigmaX=0.5) 
    edges = cv2.Canny(blurred, 70, 135) 
    return edges
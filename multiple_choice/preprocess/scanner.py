import cv2
import numpy as np
from imutils.perspective import four_point_transform

def resize_img(img, width = 500):
    h, w, _ = img.shape
    height = int((h/w) * width)
    size = (width, height)
    image = cv2.resize(img, size)
    return image, size

def document_scannner(img):
    resized_img, size = resize_img(img)
    
    #Find edges
    detail = cv2.detailEnhance(resized_img,sigma_s = 20, sigma_r = 0.15)
    gray = cv2.cvtColor(detail,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    edge_image = cv2.Canny(blur,75,200)
    
    #Remove edge noises
    kernel = np.ones((5,5),np.uint8)
    dilate = cv2.dilate(edge_image,kernel,iterations=1)
    closing = cv2.morphologyEx(dilate,cv2.MORPH_CLOSE,kernel)
    
    #Find contours
    contours , _ = cv2.findContours(closing,
                                    cv2.RETR_LIST,
                                    cv2.CHAIN_APPROX_SIMPLE)
    
    #Find largest contour that can be approximated to a rectangle
    contours = sorted(contours,key=cv2.contourArea,reverse=True)
    for contour in contours:
        peri = cv2.arcLength(contour,True)
        approx = cv2.approxPolyDP(contour,0.02*peri, True)

        if len(approx) == 4:
            four_points = np.squeeze(approx)
            break
    
    cv2.drawContours(resized_img,[four_points],-1,(0,255,0),3)
    
    #Convert to original shape
    multiplier = img.shape[1] / size[0]
    four_points_orig = four_points * multiplier
    four_points_orig = four_points_orig.astype(int)
    
    wrap_image = four_point_transform(img, four_points_orig)
    return wrap_image


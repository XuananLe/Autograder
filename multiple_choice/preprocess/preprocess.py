import cv2
import os
from .scanner import document_scannner

class Preprocess():
    def __init__(self, config):
        self.config = config
    
    
    def __call__(self, img):
        DEBUG_DIR = self.config['PREP_DEBUG_DIR']
        PAPER_SIZE = self.config['IMAGE_SIZE_DEFAULT']
        if self.config["PREP_VISUALIZE"]:
            os.makedirs(DEBUG_DIR, exist_ok=True)
            
        if self.config["PREP_VISUALIZE"]:
            cv2.imwrite(DEBUG_DIR + "/1_original.jpg", img)
        scanned_img = document_scannner(img)
        if self.config["PREP_VISUALIZE"]:
            cv2.imwrite(DEBUG_DIR + "/2_scanned.jpg", scanned_img)
        
        final = scanned_img
        return cv2.resize(final, PAPER_SIZE)

        
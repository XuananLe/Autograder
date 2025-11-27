
import cv2
import sys
import os

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '..')))

from end2end import Pipeline

img = cv2.imread(r"data/answer_sheet/test_moi2.jpg")
pipeline = Pipeline()
extract_output = pipeline.process(img)
print(extract_output)
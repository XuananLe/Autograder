import cv2
import os

from .grid import scale_new_grid, grid_visualize
from .contrast import process_img

class AnswerExtract():
    def __init__(self, config):
        self.config = config

    def __call__(self, img):
        ANSWER = self.config['ANSWER']
        PIXEL_THRESHOLD = self.config['PIXEL_THRESHOLD']
        DEBUG_DIR = self.config['ANSWER_DEBUG_DIR']
        
        if self.config['ANSWER_VISUALIZE']:
            os.makedirs(DEBUG_DIR, exist_ok=True)
            os.makedirs(os.path.join(DEBUG_DIR, "slice"), exist_ok=True)

        # Crop answer area
        h = img.shape[0]
        img = img[int(h * 0.2): int(h * 0.95), :]

        blur_img = process_img(img)
        
        # Apply canny edge detection algorithm
        canny_img = cv2.Canny(blur_img, 125, 200)
        if self.config['ANSWER_VISUALIZE']:
            cv2.imwrite(DEBUG_DIR + "4_canny.jpg", canny_img)
            
        canny_img = cv2.dilate(canny_img, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
        if self.config['ANSWER_VISUALIZE']:
            cv2.imwrite(DEBUG_DIR + "5_dilate_canny.jpg", canny_img)

        # Finding contours for the detected edges.
        contours, hierarchy = cv2.findContours(
            canny_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        # Contour of 4 columns (4 largest contours)
        boxes_cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:4]
        boxes_img = cv2.drawContours(
            img.copy(), boxes_cnts, -1, (0, 0, 255), 3)
        if self.config['ANSWER_VISUALIZE']:
            cv2.imwrite(DEBUG_DIR + "6_boxes.jpg", boxes_img)

        columns = []
        if len(boxes_cnts) > 0:
            for cnt in boxes_cnts:
                x, y, w, h = cv2.boundingRect(cnt)
                columns.append((x, y, w, h))

        # Sort left to right
        columns = sorted(columns, key=lambda x: x[0])
        result = {}

        for column_index, col in enumerate(columns):
            x, y, col_w, col_h = col
            x += 5
            y += 5
            col_w -= 10
            col_h -= 10

            column_img = img.copy()[y:y + col_h, x:x + col_w]
            grid = scale_new_grid((x, y, col_w, col_h), self.config)
            
            _img_with_box = column_img.copy()
            
            if self.config['ANSWER_VISUALIZE']:
                cv2.imwrite(DEBUG_DIR + f"4_{column_index}.jpg", grid_visualize(column_img, grid))

            # Iterate through boxes in the column
            for box_index, box_grid in enumerate(grid):
                # Iterate through questions in the box
                for qindex, qgrid in enumerate(box_grid):
                    question_id = column_index * 30 + box_index * 5 + qindex + 1
                    result[question_id] = []

                    max_pixels = 0
                    best_ans_idx = -1
                    best_bb = None

                    # Iterate through bubbles (A, B, C, D)
                    for answer_index, bb in enumerate(qgrid):
                        choice_img = column_img.copy()[bb[0][1]:bb[3][1], bb[0][0]:bb[2][0]]
                        
                        # Process bubble image
                        bubble_choice = cv2.cvtColor(choice_img, cv2.COLOR_BGR2GRAY)
                        bubble_choice = cv2.threshold(
                            bubble_choice, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                        
                        # Remove noise
                        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                        bubble_choice = cv2.morphologyEx(
                            bubble_choice, cv2.MORPH_OPEN, kernel, iterations=2)

                        if self.config['ANSWER_VISUALIZE']:
                            cv2.imwrite(os.path.join(
                                DEBUG_DIR, "slice", f"{question_id}_{answer_index}.jpg"), bubble_choice)

                        # Calculate non-zero pixels
                        pixel_count = cv2.countNonZero(bubble_choice)

                        # Check if this bubble is the "darkest" so far for this question
                        if pixel_count > max_pixels:
                            max_pixels = pixel_count
                            best_ans_idx = answer_index
                            best_bb = bb

                    # --- DECISION BLOCK ---
                    # Only accept the best answer if it meets the minimum threshold
                    if max_pixels > PIXEL_THRESHOLD and best_ans_idx != -1:
                        result[question_id].append(ANSWER[best_ans_idx])
                        
                        # Draw the rectangle only for the selected answer
                        if best_bb is not None:
                            cv2.rectangle(_img_with_box, 
                                        (best_bb[0][0], best_bb[0][1]), 
                                        (best_bb[2][0], best_bb[2][1]), 
                                        (0, 255, 0), 2)
                            
     
            if self.config['ANSWER_VISUALIZE']:
                cv2.imwrite(DEBUG_DIR + f"result_col_{column_index}.jpg", _img_with_box)

        return result
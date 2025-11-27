from extraction import StudentIDExtract
from extraction import AnswerExtract
from extraction import ExamCodeExtract
from preprocess import Preprocess
import yaml
import cv2




class Pipeline():
    def __init__(self, config_path="config.yaml"):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        self.paperExt = Preprocess(self.config)
        self.answerExt = AnswerExtract(self.config)
        self.ECExt = ExamCodeExtract(self.config)
        self.SIDExt = StudentIDExtract(self.config)

    def process(self, img):
        if img.shape[0] < img.shape[1]:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

        processed_img = self.paperExt(img)
        return {
            "studentID": self.SIDExt(processed_img),
            "examCode": self.ECExt(processed_img),
            "answer": self.answerExt(processed_img)
        }


if __name__ == "__main__":
    pass

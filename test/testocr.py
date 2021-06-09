# -*- coding: utf-8 -*-
import cv2
import pytesseract
import numpy as np
import sys
import pdb
from cnocr import CnOcr

#path = 'rect/23_98.jpg'
# path = 'rect/451_448.jpg'
path = 'rect/2.png'
# img = cv2.imread(path)
# pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
# tessdata_dir_config = '--tessdata-dir "C:/Program Files (x86)/Tesseract-OCR/tessdata/"'
# text1 = pytesseract.image_to_string(img, config=tessdata_dir_config, lang='chi_sim')

ocr = CnOcr()
text1 = ocr.ocr(path)
text1 = ocr.ocr_for_single_line(path)
print(text1)



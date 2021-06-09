# -*- coding: utf-8 -*-
import cv2
import pytesseract
import numpy as np
import sys
import pdb
from RectDetect import RectDetector
from RectOcr import RectOCR
from XLSor import XLsor
# from XlsBorder import XLSBorder

class ImageTableOCR(object):

    def __init__(self, ImagePath):

        self.image = cv2.imread(ImagePath, 1)

        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('gray', self.gray)
        #cv2.waitKey(0)

    def HorizontalLineDetect(self, minstart, maxend):

        ret, thresh1 = cv2.threshold(self.gray, 240, 255, cv2.THRESH_BINARY)
        cv2.imshow('thresh1', thresh1)
        cv2.waitKey(0)
        minlength = 40

        blur = cv2.medianBlur(thresh1, 1)
        blur = cv2.medianBlur(blur, 1)
        # cv2.imshow('blur', blur)
        # cv2.waitKey(0)
        h, w = self.gray.shape

        horizontal_lines = []
        ppinum = w * 255.0
        for i in range(h - 1):
            start = 0
            end = 0
            if i < minstart or i > maxend:
                continue
            ratio = np.sum(blur[i, :])/ppinum
            if ratio > 0.8:
                #print(np.sum(blur[:, i]), ppinum, ratio)
                continue
            #从竖着d第一个像素开始搜索，如果m能够直接加，那就容易了
            for m in range(w - 1):
                if m <= end:
                    continue
                # if m >= 224 and blur[m, i] < 2:
                #     print(blur[m, i], m)
                    #pdb.set_trace()
                #查到第一个黑点，开始往后搜索
                if blur[i, m] < 2 and np.mean(blur[i, m:m+minlength]) < 2:
                    start = m
                    for tt in range(w - m -minlength):
                        if blur[i, m + minlength + tt] < 2:
                            continue
                        else:
                            end = m+minlength+tt - 1
                            #pdb.set_trace()
                            break
                    if len(horizontal_lines) == 0:
                        horizontal_lines.append([start, i, end, i])
                        cv2.line(self.image, (start, i), (end, i), (0, 0, 255), 2)
                        #print(ratio, i, start, end)
                        fft = i
                    #elif i - vertical_lines[-1][1] > 2 or i == vertical_lines[-1][1]:
                    elif i - horizontal_lines[-1][1] > 2 or i == horizontal_lines[-1][1]:
                        #fft = i
                        #print(ratio, i, start, end)
                        horizontal_lines.append([start, i, end, i])
                        cv2.line(self.image, (start, i), (end, i), (0, 0, 255), 2)

        return horizontal_lines

    def VerticalLineDetect(self):
        ret, thresh1 = cv2.threshold(self.gray, 240, 255, cv2.THRESH_BINARY)
        cv2.imshow('thresh1', thresh1)
        cv2.waitKey(0)
        minlength = 40

        blur = cv2.medianBlur(thresh1, 1)
        blur = cv2.medianBlur(blur, 1)
        # cv2.imshow('blur', blur)
        # cv2.waitKey(0)
        h, w = self.gray.shape

        vertical_lines = []
        fft = 20
        ppinum = h * 255.0
        for i in range(w - 1):
            start = 0
            end = 0
            #if i < fft:
            # if i != 451:
            #     continue
            ratio = np.sum(blur[:, i])/ppinum
            if ratio > 0.9:
                #print(np.sum(blur[:, i]), ppinum, ratio)
                continue
            #从竖着d第一个像素开始搜索，如果m能够直接加，那就容易了
            for m in range(h - 1):
                if m <= end:
                    continue
                # if m >= 224 and blur[m, i] < 2:
                #     print(blur[m, i], m)
                    #pdb.set_trace()
                #查到第一个黑点，开始往后搜索
                if blur[m, i] < 2 and np.mean(blur[m:m+minlength, i]) < 2:
                    start = m
                    for tt in range(h - m -minlength):
                        if blur[m + minlength + tt, i] < 2:
                            continue
                        else:
                            end = m+minlength+tt - 1
                            #pdb.set_trace()
                            break
                    if len(vertical_lines) == 0:
                        vertical_lines.append([i, start, i, end])
                        cv2.line(self.image, (i, start), (i, end), (0, 0, 255), 2)
                        #print(ratio, i, start, end)
                        fft = i
                    #elif i - vertical_lines[-1][1] > 2 or i == vertical_lines[-1][1]:
                    elif i - vertical_lines[-1][0] > 2 or i == vertical_lines[-1][0]:
                        fft = i
                        #print(ratio, i, start, end)
                        vertical_lines.append([i, start, i, end])
                        cv2.line(self.image, (i, start), (i, end), (0, 0, 255), 2)

        return vertical_lines

    def VerticalLineDetect1(self):
        edges = cv2.Canny(self.gray, 30, 240)
        #cv2.imshow('edges', edges)
        minLineLength = 50
        maxLineGap = 0
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength, maxLineGap).tolist()
        #lines.append([[13, 937, 13, 102]])
        #lines.append([[756, 937, 756, 102]])
        sorted_lines = sorted(lines, key=lambda x: (x[0][0], x[0][2]))

        vertical_lines = []
        for line in sorted_lines:
            for x1, y1, x2, y2 in line:

                if x1 == x2 and abs(y1 - y2) > 30:
                    print(line)
                    vertical_lines.append((x1, y1, x2, y2))
                    cv2.line(self.image, (x1, y1), (x2, y2), (0, 0, 255), 2)
                if abs(x1 - x2) > 30 and y1 == y2:
                    print(line)
                    vertical_lines.append((x1, y1, x2, y2))
                    cv2.line(self.image, (x1, y1), (x2, y2), (0, 0, 255), 2)

        return vertical_lines


    def VertexDetect(self):
        vertical_lines = self.VerticalLineDetect()
        horizontal_lines = self.HorizontalLineDetect()
        cv2.imshow('imshow', self.image)
        cv2.waitKey(0)

        vertex = []
        for v_line in vertical_lines:
            for h_line in horizontal_lines:
                vertex.append((v_line[0], h_line[1]))

        #print(vertex)

        for point in vertex:
            cv2.circle(self.image, point, 1, (255, 0, 0), 2)

        return vertex

    def CellDetect(self):
        print('vertical:')
        vertical_lines = self.VerticalLineDetect()
        minstart, maxend = 999, 0
        #minstart, maxend用来去除不必要的白线
        for line in vertical_lines:
            minstart = min(minstart, line[1])
            maxend = max(maxend, line[3])
            print(line)
        print('horizontal:')
        horizontal_lines = self.HorizontalLineDetect(minstart, maxend)

        for line in horizontal_lines:
            print(line)
        cv2.imshow('imshow', self.image)
        # cv2.imwrite('cat2.jpg', self.image)
        cv2.waitKey(0)
        return horizontal_lines, vertical_lines

    def OCR(self):
        hlines, vlines = self.CellDetect()
        rectDetector = RectDetector(hlines, vlines, self.gray)
        rectDetector.getCell()
        # pdb.set_trace()
        # print(rectDetector.rect_list)
        rectOCR = RectOCR(rectDetector.rect_lst, rectDetector.gray)
        rectOCR.OcrPic()
        print(rectOCR.rectText)
        xlsOr = XLsor(rectDetector.rect_lst, vlines, hlines, rectOCR.rectText)
        xlsOr.genXls(rectDetector.hline)

    def ShowImage(self):
        cv2.imshow('AI', self.image)
        cv2.waitKey(0)
        # cv2.imwrite('E://Horizontal.png', self.image)

ImagePath = '2.png'
imageOCR = ImageTableOCR(ImagePath)
imageOCR.OCR()

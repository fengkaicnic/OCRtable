# -*- coding: utf-8 -*-
#这个代码是把文字切出来，而后ocr
import cv2
import numpy as np
import sys
import pdb
from cnocr import CnOcr
import os

class RectOCR(object):

    def __init__(self, rect_lst, gray):

        self.gray = gray
        self.rect_lst = rect_lst
        self.rectText = {}

        self.ocr = CnOcr()

    def cutH(self, img, rect):
        shape = img.shape
        # print(shape)
        x = shape[0]
        y = shape[1]
        h_lst = []
        start, end = 0, 0
        for i in range(y):
            # print(np.mean(img[:, i]))
            if not start:
                if np.mean(img[:, i]) > 254.98:
                    continue
                start = max(i-1, 0)
            elif not end:
                if np.mean(img[:, i]) < 254.7:
                    continue
                end = i
            else:
                if len(h_lst) > 0:
                    if abs(h_lst[-1][1]-start) < 20:
                        h_lst[-1][1] = end
                    else:
                        h_lst.append([start, end])
                else:
                    h_lst.append([start, end])
                start = 0
                end = 0
        # print (h_lst)
        for j in range(len(h_lst)):
            stend = h_lst[j]
            if stend[1] - stend[0] < 5:
                continue
            tmp = img[:, h_lst[j][0]:h_lst[j][1]]
            tmp = np.array(tmp)
            # text1 = ocr.ocr_for_single_line(tmp)
            text1 = self.ocr.ocr(tmp)

            print(text1)
            if len(text1) > 0:
                self.rectText.setdefault(rect, [])
                # texts = map(lambda x:''.join(x), text1)
                if j:
                    self.rectText[rect].append('     ')
                self.rectText[rect].append(''.join(text1[0]))
            # cv2.imwrite('rect/cut/'+str(stend[0])+'_'+str(stend[1])+'.jpg', tmp)
            # cv2.imshow('tmp', tmp)
            # cv2.waitKey(0)

    def cutV(self, img, rect):
        # img = cv2.imread(path)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = img[1:, 1:]
        # cv2.imshow('img', img)
        # cv2.waitKey(0)
        shape = img.shape
        # print(shape)
        x = shape[0]
        y = shape[1]
        h_lst = []
        start, end = 0, 0
        for i in range(x):
            # print(np.mean(img[i, :]))
            if not start:
                if np.mean(img[i, :]) > 254.98:
                    continue
                start = max(i-1, 0)
            elif not end:
                if np.mean(img[i, :]) < 254.7:
                    continue
                end = i
            else:
                h_lst.append((start, end))
                start = 0
                end = 0
        # print (h_lst)
        for j in range(len(h_lst)):
            stend = h_lst[j]
            if stend[1] - stend[0] < 5:
                continue
            tmp = img[h_lst[j][0]:h_lst[j][1], :]
            # cv2.imshow('tmp', tmp)
            # cv2.waitKey(0)
            if j:
                self.rectText[rect].append('\n\n')
            self.cutH(tmp, rect)
        # cv2.imshow('testimg', testimg)
        cv2.waitKey(5)

    # path = 'rect/451_98.jpg'
    # cutV(path)
    def OcrPic(self):
        for rect in self.rect_lst:
            v1 = rect[0]
            v2 = rect[1]
            v3 = rect[2]
            v4 = rect[3]

            img = self.gray[v1[1]+1:v4[1]-1, v1[0]+1:v2[0]-1]
            self.cutV(img, rect)
        # for name in os.listdir(path):
        #     imgpath = path+name
        #     self.cutV(imgpath)



# -*- coding: utf-8 -*-
#这个代码是把文字切出来，而后ocr
import cv2
import numpy as np
import sys
import pdb
from cnocr import CnOcr

ocr = CnOcr()

def cutH(img):
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
    print (h_lst)
    for j in range(len(h_lst)):
        stend = h_lst[j]
        if stend[1] - stend[0] < 5:
            continue
        tmp = img[:, h_lst[j][0]:h_lst[j][1]]
        tmp = np.array(tmp)
        # text1 = ocr.ocr_for_single_line(tmp)
        text1 = ocr.ocr(tmp)
        print(text1)
        # cv2.imwrite('rect/cut/'+str(stend[0])+'_'+str(stend[1])+'.jpg', tmp)
        # cv2.imshow('tmp', tmp)
        # cv2.waitKey(0)

def cutV(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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
    print (h_lst)
    for j in range(len(h_lst)):
        stend = h_lst[j]
        if stend[1] - stend[0] < 5:
            continue
        tmp = img[h_lst[j][0]:h_lst[j][1], :]
        cv2.imshow('tmp', tmp)
        cv2.waitKey(0)
        cutH(tmp)
    # cv2.imshow('testimg', testimg)
    cv2.waitKey(5)

import os

# path = 'rect/451_98.jpg'
# cutV(path)

path = 'rect/'
for name in os.listdir(path):
    imgpath = path+name
    cutV(imgpath)



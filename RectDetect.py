# -*- coding: utf-8 -*-
#这个代码是把矩阵块切出的代码
import cv2
import pytesseract
import numpy as np
import sys
import pdb

class RectDetector(object):

    def __init__(self, h_lines, v_lines, gray):

        self.hlines = h_lines
        self.vlines = v_lines
        self.hline = []
        self.gray = gray
        self.rectv_dct = {}
        self.rect_lst = []


    #v1(98, 451), 代表纵坐标98，横坐标451
    def testRectByH(self, v1, v2, v3, v4):
        v1flag = 0
        v2flag = 0
        #横线的四个坐标， x1和x2是横坐标，相同的，y1和y2则是纵坐标，不同
        for x1, y1, x2, y2 in self.vlines:
            if x1 == v1[0]:#横坐标不同，则不在一条横线上，过
                if y2 <= v1[1] or y1 >= v3[1]:
                    continue
                else:
                    v1flag = 1
            elif x1 == v2[0]:#横坐标不同，则不在一条横线上，过
                if y2 <= v2[1] or y1 >= v4[1]:
                    continue
                else:
                    v2flag = 1

        return v1flag and v2flag

    #根据顶点判断是否已经确定了方块
    def testL(self, volst):
        flag = 1
        for i in range(len(volst) -1 ):
            if not self.rectv_dct.get((volst[i], volst[i+1]), None):
                flag = 0
        return flag

    #两条线上的顶点，判断是否是方块，主要是按照顶点的位置
    def detectRect(self, volst, vtlst):

        # pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
        # tessdata_dir_config = '--tessdata-dir "C:/Program Files (x86)/Tesseract-OCR/tessdata/"'

        # ocr = CnOcr()
        vox, voy = 0, 1
        vtx, vty = 0, 1
        #从该线段的最左边两个顶点搜索
        while voy < len(volst) and vty < len(vtlst):
            #pdb.set_trace()
            v1 = volst[vox]
            v2 = volst[voy]
            v3 = vtlst[vtx]
            v4 = vtlst[vty]
            #已经确定方块的话，第一行顶点往后移动
            if self.rectv_dct.get((v1, v2), None):
                vox += 1
                voy += 1
                continue
            #如果左边两个顶点相同
            if v1[0] == v3[0]:
                #如果右边两个顶点相同
                if v2[0] == v4[0]:
                    # if (v1, v2) == ((451, 292), (578, 292)):
                    #     pdb.set_trace()
                    self.rectv_dct[(v1, v2)] = 1
                    #根据四个顶点和竖线判断是否是方块
                    if self.testRectByH(v1, v2, v3, v4):
                        #这里是先纵坐标，然后横坐标
                        testimg = self.gray[v1[1]+1:v4[1]-1, v1[0]+1:v2[0]-1]
                        testimg = np.array(testimg)
                        # pdb.set_trace()
                        # cv2.imshow('testimg', testimg)
                        # cv2.waitKey(0)
                        cv2.imwrite('recttest/'+ str(v1[0])+'_'+str(v1[1]) + '.jpg', testimg )
                        self.rect_lst.append((v1, v2, v3, v4))
                        # pred = ocr.ocr(testimg)
                        # text1 = pytesseract.image_to_string(testimg, config=tessdata_dir_config, lang='chi_sim')
                        print(v1, v2, v3, v4)
                        # self.rect.append((v1, v2, v3, v4))
                        # print(text1)
                    else:
                        self.rectv_dct[(volst[voy], volst[voy+1])] = 1
                        voy += 1
                        vty += 1
                    continue

                elif v2[0] > v4[0]:
                    vty += 1
                    continue
                    #return 'v4r'
            elif v1[0] < v3[0]:
                vox += 1
                voy += 1
                continue
                #return 'v1r'
            else:
                vtx += 1
                vty += 1
                continue
                #return 'v3r'

    #[(23, 292), (451, 292), (578, 292), (704, 292)]
    #[(23, 332), (451, 332), (578, 332), (704, 332)]
    #[x1, y1, x2, y2] x is h, y is v
    def getCell(self):
        vertex_lst = []
        for hl in self.hlines:
            h_lst = []
            for vl in self.vlines:
                if hl[0]<=vl[0]<= hl[2]:
                    if vl[1]<=hl[1]<=vl[3]:
                        #h_lst.append((hl[1], vl[0]))
                        h_lst.append((vl[0], hl[1]))
            print(h_lst)
            vertex_lst.append(h_lst)#每一行都是一个列表，所有顶点存入
        # pdb.set_trace()
        h1 = (23, 0)
        h2 = (vertex_lst[0][-1][0],0 )
        h3 = (23, vertex_lst[0][0][1])
        h4 = vertex_lst[0][-1]
        self.rect_lst.append((h1, h2, h3, h4))
        self.hline = (h1, h2)
        for i in range(len(vertex_lst) - 1):
            volst = vertex_lst[i]
            vtnum = 1
            while(not self.testL(volst)): #检查该条横线，是否所有的顶点都已经利用上
                vtlst = vertex_lst[i+vtnum]
                self.detectRect(volst, vtlst)
                vtnum += 1 #如果没利用，往下搜

        # print(len(rect_lst))
        # for vetxt in rect_lst:
        #     print(vetxt)

__author__ = 'hamdiahmadi'

import pywt
import cv2
import numpy
import os
import pylab
import xlwt
import xlrd
import matplotlib.cm as cm
import copy as cpy
import Image
import matplotlib.pyplot as plt
import copy
from xlutils.copy import copy as copys


class file:
     def __init__(self):
         pass

     def readFolder(self,path):
         return os.listdir(path)

class image:
    def __init__(self):
        pass

    def toBinary(self,image):
        return cv2.threshold(image,127,255,cv2.THRESH_BINARY)[1]/255

    def toGrayScale(self,image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def readImage(self,path):
        return cv2.imread(path)

    def showImage(self,image):
        while 1:
            cv2.imshow('image',image)
            cv2.waitKey(1)
        return

    def toHSV(self,image):
        return cv2.cvtColor(image,cv2.COLOR_RGB2HSV)

class processing(file):

    def __init__(self):
        pass

    def getFractal(self,image,size):
        listRes = []
        for x in range  (0,size*size+1):
            listRes.append(0)
        for y in range(0,len(image)-(size-1)):
            for x in range(0,len(image[y])-(size-1)):
                tmpImage = copy.copy(image)
                tmpImage = numpy.array(tmpImage[y:y+size,x:x+size])
                cnt = len(numpy.where(tmpImage > 0)[0])
                listRes[cnt]+=1
        sums = numpy.sum(listRes)
        z1 = 0
        z2 = 0
        for x in range(0,len(listRes)):
            z1+=(float(x)*float(listRes[x])/float(sums))
            z2+=(float(x)*float(x)*float(listRes[x])/float(sums))
        if z1 == 0:
            z1 = 1
        return float(z2)/(float(z1)*float(z1))

    def doInitList(self,ranges,chunks):
        lists = []
        res = float(ranges)/float(chunks)
        length = 1
        while res*length <= ranges:
            lists.append(res*length)
            length+=1
        lists[length-2] = ranges
        return lists

    def getIndex(self,lists,val):
        for x in range(0,len(lists)):
            if lists[x] >= val:
                return x

    def getHSVFeature(self,image):
        H = self.doInitList(360,8)
        S = self.doInitList(1,3)
        V = self.doInitList(1,3)

        lists = [[[0 for k in xrange(len(V))] for j in xrange(len(S))]for i in xrange(len(H))]

        for y in range(0,len(image)):
            for x in range(0,len(image[y])):
                tmp = image[y][x]
                tmpH,tmpS,tmpV = float(tmp[0])*float(2),float(tmp[1])/float(255),float(tmp[2])/float(255)
                indexH = self.getIndex(H,tmpH)
                indexS = self.getIndex(S,tmpS)
                indexV = self.getIndex(V,tmpV)
                lists[indexH][indexS][indexV]+=1
        return lists

    def getListFractal(self,image):
        lists = [3,5,7,9,11]
        res = []
        for x in lists:
            res.append(self.getFractal(image,x))
        return res

    def getFeature(self,binaryImage,imageHSV):
        fractalList = self.getListFractal(binaryImage)
        HSVList = self.getHSVFeature(imageHSV)
        res = []
        for x in fractalList:
            res.append(x)
        for x in xrange(len(HSVList)):
            for y in xrange(len(HSVList[x])):
                for z in range(len(HSVList[x][y])):
                    res.append(HSVList[x][y][z])
        return res

    def getCanberra(self,data1,data2):
        res = 0
        for x in range(0,len(data1)):
            try:
                res+=(abs((data2[x]-data1[x]))/(abs(data1[x])+abs(data2[x])))
            except :
                res+=0
        return float(res)

    def getRetrieve(self,data,dataset):
        lists = []
        for x in dataset:
            lists.append((str(x[77]),self.getCanberra(data,x[0:77])))
        return lists

    def getSort(self,lists):
        dtype = [('name','S101'),('val', float)]
        lists = numpy.array(lists,dtype=dtype)
        lists = numpy.sort(lists,order='val')
        return lists

    def getRecallPrecission(self,original,list,path):
        original = original.split('_')[0]
        tp = 0
        fp = 0
        fn = 0
        for x in list:
            res = str(x)
            if original == res.split('_')[0]:
                tp+=1
            else:
                fp+=1
        for x in file.readFolder(self,path):
            if x.split('_')[0] == original:
                fn+=1
        fn-=tp
        fn-=2
        return [float(tp)/(float(tp)+float(fn)),float(tp)/(float(tp)+float(fp))]

class excel:
     def __init__(self):
         pass

     def write(self,path,content):
        wb = xlrd.open_workbook(filename=path)
        data = wb.sheet_by_index(0)
        wb2 = copys(wb)
        data2 = wb2.get_sheet(0)
        col = 0

        for x in content :
            data2.write(data.nrows,col,x)
            col+=1
        wb2.save(path)

     def readDataSet(self,path):
        wb = xlrd.open_workbook(filename=path)
        data = wb.sheet_by_index(0)
        dataSets = []
        for x in range(0,data.nrows):
            content = data.row(x)
            tmp = []
            for idx,cell_obj in enumerate(content):
                tmp.append(cell_obj.value)
            dataSets.append(tmp)
        return dataSets


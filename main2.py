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
from xlutils.copy import copy

class wavelet:

    def __init__(self):
        pass

    def toWavelet(self,image):
        return pywt.dwt2(image,'db4')

class file:

     def __init__(self):
         pass

     def readFolder(self,path):
         return os.listdir(path)

class image:

    def __init__(self):
        pass

    def toGrayScale(self,image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def readImage(self,path):
        return cv2.imread(path)

    def showImage(self,imageName,order):
        path = 'Data Batik/'+imageName
        images = self.readImage(path)
        while len(images) < 200:
            images = cv2.pyrUp(images)
        cv2.imshow(str(order)+" - "+imageName,images)

class data:

    def __init__(self):
        pass

    def calMean(self,image):
        return numpy.mean(image)

    def calDev(self,image):
        return numpy.std(image)

    def euclid(self,data1,data2):
        res = 0
        for x in range(0,len(data1)):
            res+=pow((data2[x]-data1[x]),2)
        return numpy.sqrt(res)

    def canberra(self,data1,data2):
        res = 0
        bawah = 0
        for x in range(0,len(data1)):
            res+=(abs((data2[x]-data1[x]))/(abs(data1[x])+abs(data2[x])))
        return float(res)

    def getRecallPrecission(self,original, list, path):
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

class excell:
     def __init__(self):
         pass

     def write(self,path,content):
        wb = xlrd.open_workbook(filename=path)
        data = wb.sheet_by_index(0)
        wb2 = copy(wb)
        data2 = wb2.get_sheet(0)
        row = 0

        for x in content :
            col = 0
            for y in x:
                data2.write(data.nrows+row,col,y)
                col+=1
            row+=1
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

class main(wavelet,image,data,file,excell):

    def __init__(self):
        pass

    def do(self,path):
        img = image.readImage(self,path)
        images = (image.toGrayScale(self,img))
        arr = []
        for x in range(0,5):
            img,(cH,cV,cD) = wavelet.toWavelet(self,cpy.copy(images))

            arr.append(data.calMean(self,abs(img)))
            arr.append(data.calDev(self,(img)))
            arr.append(data.calMean(self,abs(cH)))
            arr.append(data.calDev(self,(cH)))
            arr.append(data.calMean(self,abs(cV)))
            arr.append(data.calDev(self,(cV)))
            arr.append(data.calMean(self,abs(cD)))
            arr.append(data.calDev(self,(cD)))
            images = cpy.copy(img)
        return arr

    def getBatik(self,path,datasetPath,total,option,datasetImage):
        srch = self.do(path)
        dataset = excell.readDataSet(self,datasetPath)
        res = []
        for x in dataset:
            if (option == 'euclidean' or option == '1'):
                result = data.euclid(self,srch,x)
            else :
                result = data.canberra(self,srch,x)
            res.append((result,x[40]))

        dtype = [('val', float),('name','S101')]
        res = numpy.array(res,dtype=dtype)
        res = numpy.sort(res,order='val')
        for x in res:
            print x

        path = path.split('/')[1]
        f = plt.figure()
        original = path
        results = []

        for x in range(0,total):
            results.append(res[x][1])
        print results
        print data.getRecallPrecission(self, original, results, datasetImage)

        image.showImage(self,path,"Original")
        for x in range(0,total):
            paths = 'Data Batik/'+res[total - 1 - x][1]
            img = image.readImage(self,paths)
            arr=numpy.asarray(img)
            f.add_subplot(2, 2, total - x)  # this line outputs images on top of each other
            plt.imshow(arr,cmap=cm.cool)
        plt.show()

    def getBatikAll(self,path,datasetPath,total,dataSetImage):
        dataset = excell.readDataSet(self,datasetPath)
        cnt = 0
        results = []
        for x in file.readFolder(self,path):
            x = str(x)
            length = len(x)
            num = (x[length-5])
            fitur = []
            fitur.append('')
            if (x.split('.')[1] == 'jpg'):
                res = []
                tmp = []
                if (num == '5' or num == '6'):
                    res.append(x)
                    srch = self.do(path+'/'+x)
                    for y in dataset:
                        if (cnt == 0):
                            fitur.append(y[40])
                        hasil = data.euclid(self,srch,y)
                        tmp.append((hasil,y[40]))
                        res.append(hasil)

                    dtype = [('val', float),('name','S101')]
                    tmp = numpy.array(tmp,dtype=dtype)
                    tmp = numpy.sort(tmp,order='val')

                    res.append('-')
                    fitur.append('')
                    res_sort = []
                    for z in range(0,total):
                        fitur.append('')
                        res.append(tmp[z][1])
                        res_sort.append(tmp[z][1])
                    recall,precission = data.getRecallPrecission(self, x, res_sort, dataSetImage)

                    if (cnt == 0):
                        cnt+=1
                        fitur.append('Recall')
                        fitur.append('Precission')
                        results.append(fitur)

                    res.append(recall)
                    res.append(precission)
                    results.append(res)
        path = '100 data uji - euclid.xls'
        excell.write(self,path,results)

    def getDataSet(self,path):
        data = []
        for x in file.readFolder(self,path):
            x = str(x)
            length = len(x)
            num = (x[length-5])
            if (x.split('.')[1] == 'jpg'):
                if (num == '5' or num == '6'):
                    pass
                else:
                    tmp = self.do(path+'/'+x)
                    tmp.append(x)
                    data.append(tmp)
        path = 'dataset.xls'
        excell.write(self,path,data)


if __name__ == '__main__':

    mainmain = main()

    # mengambil dataset
    # path = 'Data Batik'
    # mainmain.getDataSet(path)

    # path = 'Data Batik/B44_6.jpg'
    # print "Option : "
    # option = raw_input()
    # path = 'Data Batik/'+raw_input()
    datasetPath = 'dataset.xls'
    total = 4
    # mainmain.getBatik(path,datasetPath,total,option,'Data Batik')

    path = 'Data Batik'
    mainmain.getBatikAll(path,datasetPath,total,'Data Batik')

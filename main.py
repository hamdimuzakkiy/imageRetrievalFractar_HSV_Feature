__author__ = 'hamdiahmadi'

import processing
import os
import numpy

def getDataSet():
    cImage = processing.image()
    cProcess = processing.processing()
    cExcel = processing.excel()
    cFile = processing.file()
    files = cFile.readFolder('Data Batik')
    for x in files:
        length = len(x)
        num = (x[length-5])

        extension = x.split('.')[1]
        if extension != 'jpg':
            continue
        if int(num) == 5 or int(num) == 6 :
            continue
        else:
            path = 'Data Batik/'+x
            image = cImage.readImage(path)
            imageGray = cImage.toGrayScale(image)
            imageHSV = cImage.toHSV(image)
            imageBinary = cImage.toBinary(imageGray)
            data = cProcess.getFeature(imageBinary,imageHSV)
            path = x
            data.append(path)
            cExcel.write('dataset.xls',data)


def getRetrieve(input):
    cImage = processing.image()
    cProcess = processing.processing()
    cExcel = processing.excel()
    dataset = cExcel.readDataSet('dataset.xls')
    image = cImage.readImage(input)
    imageGray = cImage.toGrayScale(image)
    imageHSV = cImage.toHSV(image)
    imageBinary = cImage.toBinary(imageGray)
    data = cProcess.getFeature(imageBinary,imageHSV)
    res = cProcess.getRetrieve(data,dataset)
    for x in range(0,4):
        print res[x]

def getRetrieveAll():
    cImage = processing.image()
    cProcess = processing.processing()
    cExcel = processing.excel()
    cFile = processing.file()
    files = cFile.readFolder('Data Batik')
    dataset = cExcel.readDataSet('dataset.xls')
    counter = 0
    for x in files:
        length = len(x)
        num = (x[length-5])
        extension = x.split('.')[1]
        if extension != 'jpg':
            continue
        if int(num) == 5 or int(num) == 6 :
            path = 'Data Batik/'+x
            image = cImage.readImage(path)
            imageGray = cImage.toGrayScale(image)
            imageHSV = cImage.toHSV(image)
            imageBinary = cImage.toBinary(imageGray)
            data = cProcess.getFeature(imageBinary,imageHSV)
            res = cProcess.getRetrieve(data,dataset)
            if counter == 0:
                name = []
                name.append('')
                for y in res:
                    name.append(y[0])
                name.append('')
                name.append('')
                name.append('')
                name.append('')
                name.append('')
                name.append('recall')
                name.append('precission')
                cExcel.write('hasil.xls',name)
                counter+=1
            inp = []
            inp.append(x)
            for y in res :
                inp.append(y[1])
            res = cProcess.getSort(res)
            inp.append('')
            listHasil = []
            for y in range(0,4) :
                inp.append(res[y][0])
                listHasil.append(res[y][0])
            path = 'Data Batik/'
            rec,pres = cProcess.getRecallPrecission(x,listHasil,path)
            inp.append(rec)
            inp.append(pres)
            cExcel.write('hasil.xls',inp)

if __name__ == '__main__':
    # getDataSet()
    # getRetrieve('Data Batik/B42_5.jpg')
    getRetrieveAll()
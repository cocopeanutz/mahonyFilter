from DataHandler import DataHandler
import time



def dataAccumulator(dataHandler):
    start = time.time()
    dataAverage = None
    numOfData = 0
    while True:
        measurementData = dataHandler.readFromPort()
        if measurementData != None :
            gyro = [measurementData.rawWx, measurementData.rawWy, measurementData.rawWz]
            numOfData = numOfData + 1
            if dataAverage == None:
                dataAverage = gyro
            else:
                for x in range(3):
                    dataAverage[x] = dataAverage[x] + (gyro[x]-dataAverage[x])/numOfData
            print(dataAverage)
        curtime = time.time()
        print('iteration ' + str(numOfData))
        if curtime-start > 4:
            return dataAverage

dataHandler = DataHandler('/dev/ttyACM0', 115200)
# print('Start Accumulating Data:')
data = dataAccumulator(dataHandler)
print(data)

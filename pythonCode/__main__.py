from DataHandler import DataHandler
import time
import mahonieBinding
import showQuaternion
import threading


dataHandler = DataHandler('/dev/ttyACM0', 115200)
mahonieBinding.mahonyInit()
def procThread():
    while(True):
        measurementData = dataHandler.readFromPort()
        if measurementData != None :
            # print(measurementData)
            mahonieBinding.mahonyUpdateFull(measurementData.rawAx, measurementData.rawAy, measurementData.rawAz,
                                        measurementData.rawWx, measurementData.rawWy, measurementData.rawWz,
                                        measurementData.rawMx, measurementData.rawMy, measurementData.rawMz)
            quaternion = mahonieBinding.mahonyGetQuaternion()
            # plot
            # print('q0 ' + str(quaternion.q0)
            #       + ' q1 ' + str(quaternion.q1)
            #       + ' q2 ' + str(quaternion.q2)
            #       + ' q3 ' + str(quaternion.q3))

thread = threading.Thread(target=procThread)
thread.start()
showQuaternion.startPlot()

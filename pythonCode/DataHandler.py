from collections import namedtuple
import serial

G_CONS = 9.80665;

MeasData = namedtuple("MeasData", "rawPosi rawPosj rawPosk rawMx rawMy rawMz rawMAvail rawAx rawAy rawAz rawAAvail rawWx rawWy rawWz rawWAvail")


def moveStreamToStruct(buff):
    s=buff.decode('ascii')
    try:
        dataList = list(map(float,s.split(',')))
        measRaw = MeasData(*dataList)
        gyroBias = [-0.11245064113451089, 2.614698548247849, -0.3286168195199276]
        meas = MeasData(
            measRaw.rawPosi,
            measRaw.rawPosj,
            measRaw.rawPosk,

            measRaw.rawMx*0.15,
            measRaw.rawMy*0.15,
            measRaw.rawMz*0.15,
            measRaw.rawMAvail,

            measRaw.rawAx/16384*G_CONS,
            measRaw.rawAy/16384*G_CONS,
            measRaw.rawAz/16384*G_CONS,
            measRaw.rawAAvail,

            measRaw.rawWx/16384*125-gyroBias[0],
            measRaw.rawWy/16384*125-gyroBias[1],
            measRaw.rawWz/16384*125-gyroBias[2],
            measRaw.rawWAvail

        )
        return meas
    except Exception as e:
        print(e)
    return None
class DataHandler:
    serialPort = None
    buff=bytearray()
    def __init__(self, port, baudrate):
        try:
            self.serialPort = serial.Serial(port, baudrate, timeout=0)
        except Exception as e:
            print(e)
            print ('Serial port cannot open!')
            pass
    def readFromPort(self):
        connected = True
        retval = None
        # while self.serialPort.inWaiting():
        while True:
            # time.sleep(0.1)
            #reading = serial_port.read().decode('ascii')
            reading = self.serialPort.read()
            # if(reading!=b''):
            #      print(reading)
            if(reading == b'<'):
                self.buff=bytearray()
            elif(reading==b'>'):
                retval = moveStreamToStruct(self.buff)
                self.buff=bytearray()
                return retval
            else:
                self.buff+=reading
        return retval
    def flush(self):
        self.serialPort.flushInput()

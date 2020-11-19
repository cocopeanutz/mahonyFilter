from ctypes import *
import os
import math
from pyquaternion import Quaternion


G_CONS = 9.80665;

wrapperDll= cdll.LoadLibrary("/home/edo/SIPA/projects/mahonieFilter/cCode/mahonieFilter.so")
quaternionMahony = Quaternion()

def mahonyInit():
    wrapperDll.mahony_init()
def mahonyUpdate(ax, ay, az, gx, gy, gz):
    # void mahony_updateIMU(float gx, float gy, float gz, float ax, float ay, float az);
    # gyroscope in rad/s, acc in g
    mahonyGx = c_float(gx*math.pi/180)
    mahonyGy = c_float(gy*math.pi/180)
    mahonyGz = c_float(gz*math.pi/180)

    mahonyAx = c_float(ax/G_CONS)
    mahonyAy = c_float(ay/G_CONS)
    mahonyAz = c_float(az/G_CONS)
    wrapperDll.mahony_updateIMU(mahonyGx, mahonyGy, mahonyGz, mahonyAx, mahonyAy, mahonyAz)
def mahonyUpdateFull(ax, ay, az, gx, gy, gz, mx, my, mz):
    # void mahony_updateIMU(float gx, float gy, float gz, float ax, float ay, float az);
    # gyroscope in rad/s, acc in g
    mahonyGx = c_float(gx*math.pi/180)
    mahonyGy = c_float(gy*math.pi/180)
    mahonyGz = c_float(gz*math.pi/180)

    mahonyAx = c_float(-ax/G_CONS)
    mahonyAy = c_float(-ay/G_CONS)
    mahonyAz = c_float(-az/G_CONS)

    mahonyMx = c_float(-mx)
    mahonyMy = c_float(-my)
    mahonyMz = c_float(-mz)
    wrapperDll.mahony_update_full(mahonyGx, mahonyGy, mahonyGz,
                                mahonyAx, mahonyAy, mahonyAz,
                                mahonyMx, mahonyMy, mahonyMz)


def mahonyGetQuaternion():
    q0 = c_float()
    q1 = c_float()
    q2 = c_float()
    q3 = c_float()
    wrapperDll.fusion_read(byref(q0), byref(q1), byref(q2), byref(q3))
    global quaternionMahony
    quaternionMahony = Quaternion(
    q0.value,
    q1.value,
    q2.value,
    q3.value
    )
    # print('q0: ', q0.value)
    # print (quaternionMahony)
    return quaternionMahony
def getQuaternionStep2():
    # So doesn't need to think about the complexity of multi-threading with c
    return quaternionMahony

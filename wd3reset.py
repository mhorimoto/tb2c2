#! /usr/bin/python3
#coding: utf-8
#
#  WD-3のリセット
#
#    (1) WD-3の電源をOFF
#    (2) WD-3の電源をON
#
#  正常にリセットが出来ると True を返す。
#
#  On/Offに関わるPortは、PD14(GPIO110)として、
#  WD3SWを追加されているものとする。
#  OSはArmbian Version=5.25以降を必要とする。
#
import time
import os
#
def wd3reset():
    wd3initok = True
    GPIOD = "/sys/class/gpio"
    GPIO110 = GPIOD + "/gpio110"
    g = open(GPIOD+"/export","a")
    c = 3

    while not os.path.isdir(GPIO110):
        if (c==0) :
            print("CAN NOT CREATE gpio110")
            return(False)
        g.write("110")
        g.flush()
        time.sleep(0.1)
        c = c-1
    gp = open(GPIO110+"/direction","a")
    gp.write("out")
    gp.flush()
    gp.close()
    gp = open(GPIO110+"/value","a")
    gp.write("0")
    gp.flush()
    time.sleep(1)
    gp.write("1")
    gp.flush()
    gp.close()
    return(True)
# end of def wd3reset()

if __name__ == '__main__':

    wd3reset()
    

#! /usr/bin/python3
#coding: utf-8
#
#  WD-3の初期化
#
#    (1) WD-3の電源をOFF
#    (2) WD-3の電源をON
#    (3) コマンドPを送出
#    (4) パスワードARP.を送出
#    (5) コマンドMを送出
#
#  On/Offに関わるPortは、PD14(GPIO110)として、
#  WD3SWを追加されているものとする。
#  OSはArmbian Version=5.25以降を必要とする。
#
import time
import os
import serial
import wd3reset as w
#
def wd3init():
    wd3initok = True
    rc = w.wd3reset()
    if rc:
        pass
    else:
        print("::WD-3 POWER RESET FAIL.")
        return(False)
    time.sleep(1)
    try:
        serwd3 = serial.Serial('/dev/ttyS3',9600,timeout=2)
    except serial.serialutil.SerialException:
        print("NO SERIAL ttyS3 for WD-3")
        wd3initok = False
    if wd3initok:
        print("SERIAL AVAILABLE")
        serwd3.write("P".encode('UTF-8'))
        time.sleep(2)  # Wait for 2Sec
        res = serwd3.read(2).decode()
        print("RES1={0}".format(res))
        if res != 'PO':
            print("No present WD-3 via ttyS3")
            return(False)
        else:
            serwd3.write("ARP.".encode('UTF-8'))
            res = serwd3.read(5).decode()
            print("RES2={0}".format(res))
            if res != 'ARP.O':
                print("Password fail.")
                return(False)
            else:
                serwd3.write("M".encode('UTF-8'))
                res = serwd3.read(2).decode()
                print("RES3={0}".format(res))
                if res != 'MO':
                    print("set Mode fail.")
                    return(False)
        return serwd3
    else:
        return(False)
# end of def wd3init()

if __name__ == '__main__':
    c = 3
    while( c>0 ):
        ss = wd3init()
        if ( ss != False ):
            break
        else:
            c = c-1
    else:
        print("ERROR END\n")
        quit()
    print("NORMAL END\n")
    quit()
    

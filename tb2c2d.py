#! /usr/bin/python3
#coding: utf-8
import signal
import lcd_i2c as lcd
import datetime
import time
import serial
import configparser
import netifaces
from wd3init import wd3init
from socket import *

tb2initok = True
tb2ok     = True
wd3initok = True
wd3ok     = True

i_tb2v = 0
i_vwc  = 0
i_ec   = 0
i_tp   = 0

HOST = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
ADDRESS = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['broadcast']
PORT = 16520

def send_UECSdata(typename,data,ip):
    room     = config[typename]['room']
    region   = config[typename]['region']
    order    = config[typename]['order']
    priority = config[typename]['priority']
    s = socket(AF_INET,SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
    s.bind((HOST,PORT))
    ut = "<?xml version=\"1.0\"?><UECS ver=\"1.00-E10\"><DATA type=\"{0}\" "\
         "room=\"{1}\" region=\"{2}\" order=\"{3}\" priority=\"{4}\">{5}</DATA>"\
         "<IP>{6}</IP></UECS>".format(typename,room,region,order,priority,data,ip)
    s.sendto(ut.encode(),(ADDRESS,PORT))
    s.close()

###################################################

config = configparser.ConfigParser()
config.read('/etc/uecs/config.ini')

lcd.lcd_init()
prevsec = 0
ip = HOST

#
#  TB2 port initialize
#
try:
    tb2 = serial.Serial('/dev/ttyS1',19200,timeout=0.1)
except serial.serialutil.SerialException:
    print("NO SERIAL ttyS1 for TB2")
    tb2 = False
    tb2initok = False

#
#  WD-3 port initilize
#
wd3 = wd3init()
    
while(True):
    a=datetime.datetime.now()
    d="{0:2d}{1:02d}{2:02d}".format(a.year-2000,a.month,a.day)
    t=int("{0:2d}{1:02d}{2:02d}".format(a.hour,a.minute,a.second))
    s="{0:6s} {1:6d}".format(d,t)
    if (prevsec > a.second):
        ##################################################################
        #
        # Read data from TB2
        #
        if tb2initok:
            for i in range(20):
                print("IN FOR")
                tb2.write("a".encode())
                time.sleep(0.05)  # Wait for 50mSec
                ans = tb2.readline().decode()
                if ans != "":
                    tb2ok = True
                    break         # exit for-loop
                else:
                    tb2ok = False
            print("EXIT FOR")
            if tb2ok:
                try:
                    f_ans = float(ans)
                    i_tb2v = int(f_ans * 10)
                    print("TB2 VAL={0}".format(f_ans))
                except ValueError:
                    print("TB2 Value error")
        else:
            print("tb2init NG")
            pass

        #
        # Read data from WD-3
        #
        print("ENTER WD3")
        if wd3initok:
            wd3.write("D".encode())
            ans = wd3.readline().decode()
            chkans = ans[0:2]
            if chkans=='DW':
                wd3ok = True
            else:
                wd3ok = False
                print(chkans)

            if wd3ok:
                # DW=1.000,E=0.009,T=0.482E1 <== Responsed TEXT

                #
                # Calculate for WD-3 VWC
                #
                wv = ans[3:8]
                wf = float(wv)
                vwc = wf * 100
                i_vwc = int((vwc+0.05)*10)
                #
                # Calculate for WD-3 EC
                #
                ev = ans[11:16]
                ef = float(ev)
                ec = ef / 0.1428
                i_ec = int((ec+0.005)*100)
                #
                # Calculate for WD-3 Temperature
                #
                tv = ans[19:24]
                tf = float(tv)
                tp = tf / 0.02 - 10.0
                i_tp = int((tp+0.05)*10)
            else:
                i_vwc = -100
                i_tp = 990
                i_ec = 9999
        else:
            print("WD3 ERROR")
            #i_vwc = -99
            #i_tp = 998
            #i_ec = 9998

        send_UECSdata("FLOW.mNB",i_tb2v,HOST)
        send_UECSdata("VWC.mNB",i_vwc,HOST)
        send_UECSdata("EC.mNB",i_ec,HOST)
        send_UECSdata("TEMP.mNB",i_tp,HOST)

#######################################################        
    if (a.second>50):
        lcd.lcd_string(ip,lcd.LCD_LINE_2)
    elif (a.second>40):
        msg = "UECS TB2C2 V1.0"
        lcd.lcd_string(msg,lcd.LCD_LINE_2)
    elif (a.second>30):
        lcd.lcd_string(ip,lcd.LCD_LINE_2)
    elif (a.second>20):
        msg = "UECS TB2C2 V1.0"
        lcd.lcd_string(msg,lcd.LCD_LINE_2)
    elif (a.second>10):
        lcd.lcd_string(ip,lcd.LCD_LINE_2)
    else:
        l = lcd.LCD_LINE_1
        a1 = i_tb2v/10.0
        a2 = i_vwc/10.0 
        u = "TB:{0:4.1f} VWC:{1:4.1f}".format(a1,a2)
        lcd.lcd_string(u,l)
        l = lcd.LCD_LINE_2
        a1 = i_ec/100.0
        a2 = i_tp/10.0 
        u = "EC:{0:4.2f} TP:{1:4.1f}".format(a1,a2)
        lcd.lcd_string(u,l)
        
    prevsec = a.second
    time.sleep(1)

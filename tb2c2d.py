#! /usr/bin/python3
#coding: utf-8
#
#  Version 1.42
#
import os
import signal
import lcd_i2c as lcd
import datetime
import time
import serial
import configparser
import netifaces
from wd3init import wd3init
from socket import *
import ambient

tb2initok = True
tb2ok     = True
wd3initok = True
wd3ok     = True

i_tb2v = 0
f_ans  = 0.0
i_vwc  = 0
vwc    = 0.0
i_ec   = 0
ec     = 0.0
i_tp   = 0
tp     = 0.0

#HOST = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
#ADDRESS = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['broadcast']
HOST = netifaces.ifaddresses('tun0')[netifaces.AF_INET][0]['addr']
ADDRESS = netifaces.ifaddresses('tun0')[netifaces.AF_INET][0]['peer']
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
config.read('/etc/uecs/config.ini',encoding="utf-8")

ambflag = False
if 'Ambient' in config:
    if ('chid' in config['Ambient']) and ('wrkey' in config['Ambient']):
        ambflag = True

lcd.lcd_init()
prevsec = 0
ip = HOST

#
#  D2,D3 initialize
#
GPIO="/sys/class/gpio"
GPIOEXPORT=GPIO+"/export"
GPIO10="/sys/class/gpio/gpio10"
GPIO20="/sys/class/gpio/gpio20"

DOUT = open(GPIOEXPORT,"w")
if os.path.isdir(GPIO10):
    pass
else:
    DOUT.write("10")
    DOUT.flush()
if os.path.isdir(GPIO20):
    pass
else:
    DOUT.write("20")
    DOUT.flush()
DOUT.close()

DOUT = open(GPIO10+"/direction","w")
DOUT.write("out")
DOUT.close()
DOUT = open(GPIO20+"/direction","w")
DOUT.write("out")
DOUT.close()

D2 = open(GPIO10+"/value","w")
D3 = open(GPIO20+"/value","w")

#
#  TB2 port initialize
#
try:
    tb2 = serial.Serial('/dev/ttyS1',19200,timeout=0.1)
except serial.serialutil.SerialException:
    print("NO SERIAL ttyS1 for TB2")
    lcd.lcd_string("NO ttyS1 for TB2",lcd.LCD_LINE_1)
    D2.write("1")
    D2.flush()
    tb2 = False
    tb2initok = False

#
#  WD-3 port initilize
#
wd3 = wd3init()

#
#  Ambient initilize
#
if ambflag:
    am = ambient.Ambient(config['Ambient']['chid'],config['Ambient']['wrkey'])

while(True):
    a=datetime.datetime.now()
    if (prevsec > a.second):    # 59秒から0秒で逆転することから1分経過を意味する
        ##################################################################
        #
        # Read data from TB2
        #
        if tb2initok:
            D2.write("1")
            D2.flush()
            for i in range(20):
                tb2.write("a".encode())
                time.sleep(0.05)  # Wait for 50mSec
                ans = tb2.readline().decode()
                if ans != "":
                    tb2ok = True
                    D2.write("0")
                    D2.flush()
                    break         # exit for-loop
                else:
                    tb2ok = False
            if tb2ok:
                try:
                    f_ans = float(ans)
                    i_tb2v = int(f_ans * 10)
                    #print("TB2 VAL={0}".format(f_ans))
                except ValueError:
                    f_ans = 0.0
                    i_tb2v = 0
                    print("TB2 Value error")
                    lcd.lcd_string("TB2 Value error",lcd.LCD_LINE_1)
                    D2.write("1")
                    D2.flush()
            if os.path.isfile("/tmp/tb2-zero"):
                os.remove("/tmp/tb2-zero")
                tb2.write("b".encode())
                time.sleep(0.05)  # Wait for 50mSec
                tb2.write("b".encode())
                time.sleep(0.05)  # Wait for 50mSec
                                
        else:
            print("tb2init NG")
            lcd.lcd_string("tb2init NG",lcd.LCD_LINE_1)
            D2.write("1")
            D2.flush()
        #
        # Read data from WD-3
        #
        if wd3initok:
            D2.write("1")
            D2.flush()
            wd3.write("D".encode())
            ans = wd3.readline().decode()
            chkans = ans[0:2]
            if chkans=='DW':
                wd3ok = True
                D2.write("0")
                D2.flush()
            else:
                wd3ok = False
                print(chkans)
                emsg = "WD3init ERR {0}".format(chkans)
                lcd.lcd_string(emsg,lcd.LCD_LINE_1)
                D2.write("1")
                D2.flush()
            if wd3ok:
                D2.write("0")
                D2.flush()
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
            D2.write("1")
            D2.flush()
            emsg = "WD3 ERROR"
            print(emsg)
            lcd.lcd_string(emsg,lcd.LCD_LINE_1)

        D3.write("1")
        D3.flush()
        send_UECSdata("FLOW.mNB",i_tb2v,HOST)
        send_UECSdata("VWC.mNB",i_vwc,HOST)
        send_UECSdata("EC.mNB",i_ec,HOST)
        send_UECSdata("TEMP.mNB",i_tp,HOST)
        if ambflag:
            amr = am.send({'d1': f_ans, 'd2': vwc, 'd3': ec, 'd4': tp})
        D3.write("0")
        D3.flush()

#######################################################        
    if (a.second>50):
        lcd.lcd_string(ip,lcd.LCD_LINE_2)
    elif (a.second>40):
        msg = "UECS TB2C2 V1.42"
        lcd.lcd_string(msg,lcd.LCD_LINE_2)
    elif (a.second>30):
        lcd.lcd_string(ip,lcd.LCD_LINE_2)
    elif (a.second>20):
        l = lcd.LCD_LINE_1
        a1 = f_ans
        a2 = vwc
        u = "TB:{0:4.1f} VWC:{1:4.1f}".format(a1,a2)
        lcd.lcd_string(u,l)
        l = lcd.LCD_LINE_2
        a1 = ec
        a2 = tp
        u = "EC:{0:4.2f} TP:{1:4.1f}".format(a1,a2)
        lcd.lcd_string(u,l)
    elif (a.second>10):
        lcd.lcd_string(ip,lcd.LCD_LINE_2)
    else:
        l = lcd.LCD_LINE_1
        a1 = f_ans
        a2 = vwc
        u = "TB:{0:4.1f} VWC:{1:4.1f}".format(a1,a2)
        lcd.lcd_string(u,l)
        l = lcd.LCD_LINE_2
        a1 = ec
        a2 = tp
        u = "EC:{0:4.2f} TP:{1:4.1f}".format(a1,a2)
        lcd.lcd_string(u,l)
        
    prevsec = a.second
    time.sleep(1)
    send_UECSdata("cnd.mNB",0,HOST)

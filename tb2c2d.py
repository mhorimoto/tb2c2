#! /usr/bin/python3
#coding: utf-8
import lcd_i2c as lcd
import datetime
import time
import configparser
import netifaces
from socket import *

HOST = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
ADDRESS = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['broadcast']
PORT = 16520

def send_UECSdata(typename,room,region,order,priority,data,ip):
    s = socket(AF_INET,SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
    s.bind((HOST,PORT))
    ut = "<?xml version=\"1.0\"?><UECS ver=\"1.00-E10\"><DATA type=\"{0}\" room=\"{1}\" region=\"{2}\" order=\"{3}\" priority=\"{4}\">{5}</DATA><IP>{6}</IP></UECS>".format(typename,room,region,order,priority,data,ip)
    s.sendto(ut.encode(),(ADDRESS,PORT))
    s.close()


###################################################

config = configparser.ConfigParser()
config.read('/etc/uecs/config.ini')

lcd.lcd_init()
prevsec = 0
ip = HOST

while(True):
    a=datetime.datetime.now()
    d="{0:2d}{1:02d}{2:02d}".format(a.year-2000,a.month,a.day)
    t=int("{0:2d}{1:02d}{2:02d}".format(a.hour,a.minute,a.second))
    s="{0:6s} {1:6d}".format(d,t)
    if (prevsec > a.second):
        l = lcd.LCD_LINE_2
        u = "U:{0}".format(s)
        lcd.lcd_string(u,l)
        tn = "Time"
        send_UECSdata(tn,config[tn]['room'],config[tn]['region'],config[tn]['order'],config[tn]['priority'],t,HOST)
        tn = "Date"
        send_UECSdata(tn,config[tn]['room'],config[tn]['region'],config[tn]['order'],config[tn]['priority'],d,HOST)
    l = lcd.LCD_LINE_1
    lcd.lcd_string(s,l)
    if (a.second>50):
        lcd.lcd_string(ip,lcd.LCD_LINE_2)
    elif (a.second>40):
        msg = "UECS todtalker.."
        lcd.lcd_string(msg,lcd.LCD_LINE_2)
    elif (a.second>30):
        lcd.lcd_string(ip,lcd.LCD_LINE_2)
    elif (a.second>20):
        msg = "UECS todtalker.."
        lcd.lcd_string(msg,lcd.LCD_LINE_2)
    elif (a.second>10):
        lcd.lcd_string(ip,lcd.LCD_LINE_2)
    prevsec = a.second
    time.sleep(1)

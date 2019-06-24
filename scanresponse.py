#! /usr/bin/python3
#coding: utf-8
import datetime
import time
import configparser
import netifaces
import threading
import xml.etree.ElementTree as ET
import uuid
from socket import *

XML_HEADER  = "<?xml version=\"1.0\"?>"
UECS_HEADER = "<UECS ver=\"1.00-E10\">"
HOST = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
ADDRESS = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['broadcast']
PORT = 16529
config = configparser.ConfigParser()
config.read('/etc/uecs/config.ini')

class ServerThread(threading.Thread):
    def __init__(self, PORT):
        threading.Thread.__init__(self)
        self.data = 'hoge'
        self.kill_flag = False
        # line information
        self.HOST = ""
        self.PORT = PORT
        self.BUFSIZE = 512
        self.ADDR = (gethostbyname(self.HOST), self.PORT)
        # bind
        self.udpServSock = socket(AF_INET, SOCK_DGRAM)
        self.udpServSock.setsockopt(SOL_SOCKET,SO_REUSEADDR|SO_BROADCAST,1)
        self.udpServSock.bind(self.ADDR) # HOST, PORTでbinding
        # Get Network information by myself
        self.ipaddress = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
        self.node = uuid.getnode()
        self.mac = uuid.UUID(int=self.node)
        self.macaddr = self.mac.hex[-12:].upper()

    def send_cnd(self):
        ccm = ET.parse(config['NODE']['xmlfile'])
        self.sdata = "{0}{1}<DATA type=\"cnd.mXX\" room=\"0\" region=\"0\" order=\"0\" priority=\"29\">"\
                     "0</DATA><IP>{2}</IP></UECS>".\
                     format(XML_HEADER,UECS_HEADER,self.ipaddress)
        self.broadaddress = (ADDRESS,PORT)
        self.udpServSock.sendto(self.sdata.encode('utf-8'),self.broadaddress)
        


    def run(self):
        while True:
#            try:
                data, self.addr = self.udpServSock.recvfrom(self.BUFSIZE) # データ受信
                self.data = data.decode('utf-8').rstrip("\n")
                root = ET.fromstring(self.data)
                for c1 in root:
                    sp = c1.tag
#                    print("SPd=:{0}:".format(sp))

                if ( sp == 'NODESCAN' ):
                    self.sdata = "{0}{1}<NODE><NAME>{2}</NAME><VENDER>{3}</VENDER>"\
                                 "<UECSID>{4}</UECSID><IP>{5}</IP><MAC>{6}</MAC></UECS>".\
                                 format(XML_HEADER,UECS_HEADER,config['NODE']['name'],config['NODE']['vender'],\
                                        config['NODE']['uecsid'],self.ipaddress,self.macaddr)
                    self.udpServSock.sendto(self.sdata.encode('utf-8'),self.addr)

                # CCMSCAN
                elif ( sp == 'CCMSCAN' ):
                    ccm = ET.parse(config['NODE']['xmlfile'])
                    ccmroot = ccm.getroot()
                    maxx    = len(ccmroot)
                    maxy    = int((maxx+1)/2)
                    cpag    = int(c1.attrib['page'])
                    curx    = int(cpag-1)*2
                    ccmt    = ccmroot[curx]
                    ccmnum  = curx+1
                    if (ccmnum < maxx):
                        ccmcount = 2
                    else:
                        ccmcount = 1
                    ccmtt   = config[ccmt.text]
                    ccmdata = "{0}{1}<CCMNUM page=\"{2}\" total=\"{3}\">{4}</CCMNUM>"\
                              "<CCM No=\"{5}\" room=\"{6}\" region=\"{7}\" order=\"{8}\" "\
                              "priority=\"{9}\" cast=\"{10}\" unit=\"{11}\" SR=\"{12}\" "\
                              "LV=\"{13}\">{14}</CCM>"\
                              .format(XML_HEADER,UECS_HEADER,cpag,maxy,ccmcount,
                                      ccmnum,ccmtt['room'],ccmtt['region'],ccmtt['order'],
                                      ccmtt['priority'],ccmt.attrib['cast'],ccmt.attrib['unit'],ccmt.attrib['SR'],
                                      ccmt.attrib['LV'],ccmt.text)
                    curx   += 1
                    ccmnum  = curx+1
                    if (curx < maxx):
                        if (ccmroot[curx]!=""):
                            ccmt  = ccmroot[curx]
                            ccmtt = config[ccmt.text]
                            ccmdata += "<CCM No=\"{0}\" room=\"{1}\" region=\"{2}\" order=\"{3}\" "\
                                       "priority=\"{4}\" cast=\"{5}\" unit=\"{6}\" SR=\"{7}\" "\
                                       "LV=\"{8}\">{9}</CCM>"\
                                       .format(ccmnum,ccmtt['room'],ccmtt['region'],ccmtt['order'],
                                               ccmtt['priority'],ccmt.attrib['cast'],ccmt.attrib['unit'],ccmt.attrib['SR'],
                                               ccmt.attrib['LV'],ccmt.text)
                    ccmdata += "</UECS>"
                    self.udpServSock.sendto(ccmdata.encode('utf-8'),self.addr)
                else:
                    pass
#            except:
#                pass


if __name__ == '__main__':
    th = ServerThread(PORT)
    th.setDaemon(True)
    th.start()
    itv = 0     # Interval Counter

    while True:
        if not th.data:
            pass
        # print(th.data)
        itv += 1
        time.sleep(0.1)
        if (itv>=10):
            th.send_cnd()
            itv = 0
            

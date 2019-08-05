# UECS TB2C2 Talker Daemon

UECSインタフェースを使って排液量データを送出するデーモン


Version 1.20  
horimoto@holly-linux.com

Python3で動作する。

## 必要なモジュール

 * import lcd_i2c as lcd   (RPiSpiを使う)
 * import datetime
 * import time
 * import configparser
 * import netifaces
 * import smbus
 * from socket import *
 * OPi.GPIO (後述する)
 
## CCM

    <?xml version="1.0" encoding="UTF-8"?>
    <UECS>
      <CCM cast="1" unit="L" SR="S" LV="A-1M-0" exp="排液量" detail="">FLOW.mNB</CCM>
      <CCM cast="1" unit="%" SR="S" LV="A-1M-0" exp="VWC" detail="体積含水率">VWC.mNB</CCM>
      <CCM cast="2" unit="mS/cm" SR="S" LV="A-1M-0" exp="EC" detail="電気伝導度">EC.mNB</CCM>
      <CCM cast="1" unit="C" SR="S" LV="A-1M-0" exp="水温" detail="排液水温">TEMP.mNB</CCM>
      <CCM cast="0" unit="" SR="S" LV="A-1S-0" exp="機器動作状態" detail="" >cnd.mNB</CCM>
    </UECS>


## 使い方

### config.iniの変更

config.iniを変更することで、room,region,order,priorityの設定を変更することが出来る。

    [NODE]
    name = TB2C2
    vender = HOLLY
    uecsid = 10100C000002
    xmlfile = /etc/uecs/tb2c2.xml
    
    [FLOW.mNB]
    room = 0
    region = 0
    order = 0
    priority = 1
    
    [VWC.mNB]
    room = 0
    region = 0
    order = 0
    priority = 1
    
    [EC.mNB]
    room = 0
    region = 0
    order = 0
    priority = 1
    
    [TEMP.mNB]
    room = 0
    region = 0
    order = 0
    priority = 1
    
    [cnd.mNB]
    room = 0
    region = 0
    order = 0
    priority = 29

### インストールの方法

    sudo make install

 詳細は、Makefileの中を見る。


### 起動の方法

    systemctl enable tb2c2
    systemctl enable scanresponse
    systemctl start tb2c2
    systemctl start scanresponse
    

## OPi.GPIO

 RPiで使われているRPi.GPIOのOrangePi版。
 [https://github.com/rm-hull/OPi.GPIO]


    $ sudo apt install python-setuptools
    $ sudo apt install python3-pip
    $ sudo pip3 install --upgrade OPi.GPIO

 今のところ、

    import orangepi.one
    from OPi import GPIO
    GPIO.setmode(orangepi.one.BOARD)

 しか有効ではない。BCMを使ってもBOARDになるので注意。
 
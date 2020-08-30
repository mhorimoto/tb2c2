# UECS TB2C2 Talker Daemon

UECSインタフェースを使って排液量データを送出するデーモン


Version 1.53  
horimoto@holly-linux.com

Python3で動作する。

1.42はAmbient対応している。/etc/uecs/config.iniにAmbient設定を書き込むことでAmbientにもデータを送り出す。

1.50から、GIS10に対応している。/etc/uecs/config.iniにgis設定を書き込むことでGIS10サーバにデータを送り出す。

1.53から、ボタンを部分的に有効化した。
左から

 * PICのReset (!MCLR)
 * OPi Reset (SW2-SA6)
 * 予約 (SW3-PC4)
 * OPi Shutdown (SW1-PC7)

## 必要なモジュール

 * import lcd_i2c as lcd   (RPiSpiを使う)
 * import datetime
 * import time
 * import configparser
 * import netifaces
 * import smbus
 * import uuid
 * import urllib.parse
 * import urllib.request
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
    jname = 排液量センサ
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
    
    [Ambient]
    chid = 1***9
    wrkey = 5***55a2***682a7
    
    [gis]
    url = http://farmem.holly-linux.com:9980/rxdata.php
    sensid    = 1
    tb2p      = 61445
    wd3vwc    = 61448
    wd3ec     = 61449
    wd3temp   = 61450

### インストールの方法

以下のパッケージを別途インストールする。

* minicom
* ntp
* comet1
* i2c-tools
* python3-smbus
* python3-serial
* python3-pip
* python3-netifaces
* python3-setuptools
* OPi.GPIO

オペレーションは以下を参照。

     # cd work
     # apt update
     # apt install i2c-tools python3-smbus python3-serial python3-netifaces python3-pip python3-setuptools ntp
     # pip3 install --upgrade OPi.GPIO
     # git clone https://github.com/mhorimoto/tb2c2.git
     # cd tb2c2
     # mkdir /etc/uecs
     # make install

 詳細は、Makefileの中を見る。  
 /etc/uecs/config.iniを編集する。上書きに備えて直ぐにバックアップをconfig.ini-backなどとコピーしておく。

### minicomのインストール

    # apt install minicom
    # cp minirc.* /etc/minicom

 TB2は、ttyS1で192000bps。  
 WD3は、ttyS3で9600bps。

### Ambientのインストール

     # pip3 install git+https://github.com/AmbientDataInc/ambient-python-lib.git

### 起動の方法

     # systemctl enable tb2c2
     # systemctl enable scanresponse
     # systemctl start tb2c2
     # systemctl start scanresponse
    

## OPi.GPIO

 RPiで使われているRPi.GPIOのOrangePi版。
 [https://github.com/rm-hull/OPi.GPIO]


 今のところ、

     import orangepi.one
     from OPi import GPIO
     GPIO.setmode(orangepi.one.BOARD)

 しか有効ではない。BCMを使ってもBOARDになるので注意。

## crontabの設定

TB2のリセットを行うために以下の設定をcrontabに施す。

    MAILTO=""
    0 0 * * * touch /tmp/tb2-zero

## GIS10の設定

要相談

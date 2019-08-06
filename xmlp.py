#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

tree = ET.parse('tb2c2.xml')
root = tree.getroot()
for ccm in root.findall('CCM'):
    detail = ccm.get('detail')
    exp = ccm.get('exp')
    cast = ccm.get('cast')
    unit = ccm.get('unit')
    sr   = ccm.get('SR')
    lv   = ccm.get('LV')
    name = ccm.text
#1    name = ccm.
    print(cast,unit,sr,lv,exp,detail,name)

for cast in root.iter('cast'):
    print(cast.attrib)


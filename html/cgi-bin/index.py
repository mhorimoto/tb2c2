#! /usr/bin/env python3
#coding: utf-8
#

import configparser
import netifaces
import xml.etree.ElementTree as ET

# HTML Source Code
html_head = """
<!doctype html>
<html class="no-js" lang="ja">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <title>{0} {1}</title>
    <meta name="description" content="{1}のUECSパラメータの表示">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  </head>
"""
html_body_node = """
  <body>
    <H1>{0} {1} 設定内容</H1>
    <h2>ノード情報</h2>
    <table border=1>
      <tr><th>Name</th><td>{1}</td></tr>
      <tr><th>Vender</th><td>{2}</td></tr>
      <tr><th>UECS Id</th><td>{3}</td></tr>
      <tr><th>xml file</th><td>{4}</td></tr>
    </table>
"""

html_body_ccm1 = """
    <h2>CCM情報</h2>
    <table border=1>
      <tr><th>Info</th><th>Cast</th><th>Unit</th><th>S/R</th><th>Type</th><th>SR Lev</th><th>Attr</th></tr>
"""

html_body_ccm2 = """
      <tr><td align="center">{0}</td><td align="center">{1}</td><td align="center">{2}</td><td align="center">{3}</td><td>{4}</td><td>{5}</td><td>{6}</td></tr>
"""

html_body_ccm3 = """
    </table>
"""

html_foot = """
  </body>
</html>
"""

# config.ini Data
config = configparser.ConfigParser()
config.read('/etc/uecs/config.ini')


# Output HTML Data
print("Content-type: text/html\n\n")
print(html_head.format(config['NODE']['jname'],config['NODE']['name']))
print(html_body_node.format(config['NODE']['jname'],config['NODE']['name'],
                            config['NODE']['vender'],config['NODE']['uecsid'],
                            config['NODE']['xmlfile']))

print(html_body_ccm1)
# Read XML Data
tree = ET.parse(config['NODE']['xmlfile'])
root = tree.getroot()
for ccm in root.findall('CCM'):
    detail = ccm.get('detail')
    exp = ccm.get('exp')
    cast = ccm.get('cast')
    unit = ccm.get('unit')
    sr   = ccm.get('SR')
    lv   = ccm.get('LV')
    typename = ccm.text
    attr = "{0}-{1}-{2}-{3}".format(config[typename]['room'],config[typename]['region'],config[typename]['order'],config[typename]['priority'])
    print(html_body_ccm2.format(exp,cast,unit,sr,typename,lv,attr))
print(html_body_ccm3)
print(html_foot)

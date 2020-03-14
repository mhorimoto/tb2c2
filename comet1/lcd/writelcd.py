#! /usr/bin/env python3
#coding: utf-8
#
import sys
import lcd_i2c as lcd

s = sys.argv[1]
y = sys.argv[2]
x = sys.argv[3]

if (x=="i"):
    lcd.lcd_init()
if (y=="2"):
    l = lcd.LCD_LINE_2
else:
    l = lcd.LCD_LINE_1

lcd.lcd_string(s,l)

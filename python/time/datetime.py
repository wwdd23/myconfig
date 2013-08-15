#! /usr/bin/env python
#coding=utf-8
#improt datetime mode

import datetime

today = datetime.date.today()

yesterday = today - datetime.timedelta(days = 1)

tomorrow = today + datetime.timedelta(days = 1)

print (yesterday,today,tomorrow)

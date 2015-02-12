#!/bin/bash
###################
# Author:  wudi
# Mail: programmerwudi@gmail.com 
# Description:
# Created Time: 2015-01-31 07:47:32
###################

#while  readline使用案例
#应用范围:
#读取带有转义符号的字符串
#解决使用for x in x 脚本将转义字符换行问题

ls |while read line

cp $line /tmp



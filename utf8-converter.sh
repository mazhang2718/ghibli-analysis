#!/bin/bash

for i in $(find srt-files -name '*.srt')
do
  encoding='ISO-8859-1'
  iconv -f $encoding -t utf-8 $i > $i.tmp #tmp file is created as a workaround for bus error
  mv $i.tmp $i
done

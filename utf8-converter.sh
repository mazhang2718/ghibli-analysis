#!/bin/bash

find srtFiles -iname '*.srt' -exec sh -c 'iconv -f ISO-8859-1 -t UTF-8//TRANSLIT $0 > utf8-${0}' {} \;

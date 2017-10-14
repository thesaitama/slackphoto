#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import time
import json

# PIL Image Info
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def getExifInfo(filePath):
    '''
    Exif 情報の取得
    '''
    i = Image.open(filePath)

    exif = i._getexif()

    # Exif データの存在を確認する
    if (exif is None):
        return 'no Exif data.'

    tagStr = '' # 出力文字列
    date = ''
    maker = ''
    model = ''
    software = ''

    for tag, value in exif.items():
        #  TIFF Tag MakerNote: 37500
        if (tag != 37500): 
            tagName = TAGS.get(tag)
            #if (str(tagName) != 'None'):
            print str(tagName) + ": " + str(value)
            if (tagName == 'DateTimeOriginal'):
                date = "".join(map(str, value))
            elif (tagName == 'Make'):
                maker = str(value).strip()
            elif (tagName == 'Model'):
                model = str(value).strip().strip('\x00')
            elif (tagName == 'Software'):
                software = str(value).strip().strip('\x00')

    # モデル名の整形
    model = model.replace(maker, '').strip()

    tagStr = 'Date: %s\nCamera: %s %s' % (date, maker, model)

    # Software名の整形
    if(software != ''):
        software = software.replace(model, '').strip()
        tagStr += ' (%s)' % software

    return tagStr

if __name__ == '__main__':
    print getExifInfo('test.jpg')
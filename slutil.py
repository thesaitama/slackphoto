#!/usr/bin/env python
# -*- coding: utf-8 -*-

# slutil.py

import os

IMG_EXT_LIST = ['jpg', 'jpe', 'jpeg', 'png', 'bmp']

def checkFilePathExt(filePath):
    '''
    check file extention
    '''
    base_path, ext = os.path.splitext(filePath)
    extlist = IMG_EXT_LIST
    if (ext.lower().lstrip('.') in extlist):
        return True

    return False

def checkFileExt(ext):
    '''
    check image file extention
    '''
    extlist = IMG_EXT_LIST
    if (ext.lower().lstrip('.') in extlist):
        return True
 
    return False

if __name__ == '__main__':
    pass

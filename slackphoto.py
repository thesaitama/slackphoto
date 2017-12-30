#!/usr/bin/env python
# -*- coding: utf-8 -*-

# slackphoto.py

import os
import json
import random

import requests

# external functions
import sexifreader as spexif
import slackoldrm as sloldrm

# setting variables
g_settings = {}
g_settingPath = ''
g_repeatCount = 1

__version__ = '0.1.7.171230'

def slackPhotoMain():
    '''
    main routine
    '''
    paths = []

    global g_settingPath
    g_settingPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'slackphoto.json')

    # load settings
    loadSettings()
 
    # obtain schedule viariable
    for dir in g_settings['dirs']:
        for path in getDirList(dir):
            paths.append(path)

    # check scheduled paths
    if(len(paths) > 0):
        # excute photoPicker
        for i in range(0, g_settings['repeatCount']):
            photoPicker(paths)
    else:
        print 'no paths'

    # remove old file from Slack
    sloldrm.slackOldRmMain()

def checkFilePathExt(filePath):
    '''
    check file extention
    '''
    path, ext = os.path.splitext(filePath)
    extlist = ['jpg', 'jpe', 'jpeg', 'png', 'bmp']
    if (ext.lower().lstrip('.') in extlist):
        return True
    else:
        return False

def photoPicker(paths):
    '''
    photo-picker
    '''
    # pick up from file for upload
    uploadFile = selectTargetFile(paths)

    if(uploadFile != ''):
        # post message to Slack
        fileMsg = ''
        fileMsg = '%s\n%s' % (uploadFile, spexif.getExifInfo(uploadFile))
        sendSlackText(g_settings['slackChannelID'], fileMsg)
        # post photo data to Slack
        sendSlackPhoto(uploadFile, g_settings['slackChannelID'], uploadFile)

def selectTargetFile(paths):
    '''
    select upload target files
    '''
    # retry 10 times
    for var in range(0, 10):
        pivotDir = random.randrange(0, len(paths), 1)
        fileList = getFileList(paths[pivotDir])
        if (len(fileList) >= 1):
            filePivot = random.randrange(0, len(fileList), 1)
            filePath = os.path.join(paths[pivotDir], fileList[filePivot])
            print filePath
            return filePath
        else:
            print 'retry - selectTargetFile'
    return ''

def getFileList(dir):
    '''
    create file list of dir
    '''
    # create file list
    files = os.listdir(dir)
    fileList = [f for f in files
        if os.path.isfile(os.path.join(dir, f))
    ]

    # filter file list
    filteredList = []
    for fileName in fileList:
        if (fileName[0:1] != '.'):
            # ファイル拡張子を確認する
            if(checkFilePathExt(fileName)):
                filteredList.append(fileName)

    return filteredList

def getDirList(path):
    '''
    create directry list (recursive)
    '''
    for root, dirs, files in os.walk(path):
        yield root
        for dir in dirs:
            yield os.path.join(root, dir)

def sendSlackPhoto(filePath, channel, text):
    '''
    post a file to Slack
    '''
    # upload a file
    with open(filePath, 'rb') as f:
        imgParam = {
            'token': g_settings['slackToken'],
            'channels': channel,
            'title': os.path.basename(filePath)
        }
        r = requests.post('https://slack.com/api/files.upload', params=imgParam, files={'file':f})
        print r.status_code

def sendSlackText(channel, text):
    '''
    post a message to Slack
    '''
    # post a message
    sendUrl = 'http://slack.com/api/chat.postMessage?token=%s&channel=%s&text=%s' % (g_settings['slackToken'], g_settings['slackChannelID'], text)
    r = requests.post(sendUrl)
    print r.status_code

def loadSettings():
    '''
    load settings
    '''
    global g_settings

    # check setting file exists
    if (os.path.exists(g_settingPath)):
        settingFile = open(g_settingPath, 'r')
        g_settings = json.load(settingFile)
        return True

    return False

if __name__ == '__main__':
    slackPhotoMain()

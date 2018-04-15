#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" slackphoto.py
"""

import os
import json
import random

import requests

# external functions
import slutil as slutil
import sexifreader as spexif
import slackoldrm as sloldrm

# setting variables
g_settings = {}
g_settingPath = ''
g_repeatCount = 1

__version__ = '0.2.8.180415'

def slackPhotoMain():
    """ main routine
    """

    global g_settingPath
    g_settingPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'slackphoto.json')

    # load settings
    loadSettings()

    paths = createPathList()

    # check scheduled paths
    if(len(paths) > 0):
        # excute photoPicker
        for index in range(0, g_settings['repeatCount']):
            photoPicker(paths)
    else:
        print 'no paths'

    # remove old file from Slack
    sloldrm.slackOldRmMain()

def createPathList():
    """ create Path List
    """
    paths = []
    for dir in g_settings['dirs']:
        for path in getDirList(dir):
            paths.append(path)
    return paths

def photoPicker(paths):
    """ photo-picker
    """
    # pick up from file for upload
    upload_file = selectTargetFile(paths)

    if(upload_file != ''):
        # post message to Slack
        file_msg = '%s\n%s' % (upload_file, spexif.getExifInfo(upload_file))
        sendSlackText(g_settings['slackChannelID'], file_msg)
        # post photo data to Slack
        sendSlackPhoto(upload_file, g_settings['slackChannelID'], upload_file)

def selectTargetFile(paths):
    """ select upload target files
    """
    # retry 10 times
    for index in range(0, 10):
        pivot_dir = random.randrange(0, len(paths), 1)
        file_list = getFileList(paths[pivot_dir])
        if (len(file_list) >= 1):
            file_pivot = random.randrange(0, len(file_list), 1)
            file_path = os.path.join(paths[pivot_dir], file_list[file_pivot])
            if (isIgnoredPath(file_path)):
                print 'ignored: ' + file_path
                continue
            else:
                print file_path
                return file_path
        else:
            print 'retry: selectTargetFile'
    return ''

def getFileList(dir):
    """ create file list of dir
    """
    # create file list
    files = os.listdir(dir)
    file_list = [f for f in files if os.path.isfile(os.path.join(dir, f))]

    # filter file list
    filtered_list = []
    for file_name in file_list:
        if (file_name[0:1] != '.'):
            # check file extention
            if(slutil.checkFilePathExt(file_name)):
                filtered_list.append(file_name)

    return filtered_list

def isIgnoredPath(path):
    """ filiter ignoreed path
    """
    if 'dirsIgnore' in g_settings:
        for ignorePath in g_settings['dirsIgnore']:
            # is ignore
            if path.startswith(ignorePath):
                print ignorePath
                return True
    return False

def getDirList(path):
    """ create directry list (recursive)
    """
    for root, dirs, files in os.walk(path):
        yield root
        for dir in dirs:
            yield os.path.join(root, dir)

def sendSlackPhoto(filePath, channel, text):
    """ post a file to Slack
    """
    # upload a file
    with open(filePath, 'rb') as f:
        img_param = {
            'token': g_settings['slackToken'],
            'channels': channel,
            'title': os.path.basename(filePath)
        }
        r = requests.post('https://slack.com/api/files.upload', params=img_param, files={'file': f})
        print r.status_code

def sendSlackText(channel, text):
    """ post a message to Slack
    """
    # post a message
    send_url = 'http://slack.com/api/chat.postMessage?token=%s&channel=%s&text=%s' % (g_settings['slackToken'], g_settings['slackChannelID'], text)
    r = requests.post(send_url)
    print r.status_code

def loadSettings():
    """ load settings
    """
    global g_settings

    # check setting file exists
    if (os.path.exists(g_settingPath)):
        setting_file = open(g_settingPath, 'r')
        g_settings = json.load(setting_file)
        return True

    return False


if __name__ == '__main__':
    slackPhotoMain()

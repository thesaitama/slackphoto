#!/usr/bin/env python
# -*- coding: utf-8 -*-

# slackoldrm.py

import os
import sys
import json
import time
import calendar
from datetime import datetime, timedelta
import requests

# Slack設定
g_slackDomain = ''
g_slackToken = ''
g_slackBotToken = ''
g_slackChannelID = ''
g_slackRemoveLimitDay = 15

# 設定
g_settings = {}
g_settingPath = ''
g_repeatCount = 1

__version__ = '0.1.5.171021'

def slackOldRmMain():
    '''
    メインルーチン
    '''
    global g_settingPath
    g_settingPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'slackphoto.json')

    # 設定ファイルの読み込み
    loadSettings()

    listData = getSlackOldFileList()
    if(listData != {}):
        deleteSlackOldFile(listData)
    else:
        print 'no old files found.'

def checkImgExt(ext):
    '''
    画像拡張子の確認
    '''
    extlist = ['jpg', 'jpe', 'jpeg', 'png', 'bmp']
    if (ext.lower().lstrip('.') in extlist):
        return True
    else:
        return False

def deleteSlackOldFile(listData):
    '''
    古いファイルを削除する
    '''
    for slackFile in listData:
        # 拡張子の確認
        if(checkImgExt(slackFile['filetype'])):
            print 'deleting file %s (%s)' % (slackFile['name'], slackFile['timestamp'])
            timestamp = str(calendar.timegm(datetime.now().utctimetuple()))
            deleteAPIUrl = 'https://%s.slack.com/api/files.delete?t=%s' % (g_slackDomain, timestamp)
            requests.post(deleteAPIUrl, data = {
                'token': g_slackToken, 'file': slackFile['id'], 
                'set_active': 'true', '_attempts': '1'})

def getSlackOldFileList():
    '''
    古いファイルリストを取得する
    '''
    listAPIUrl = 'https://slack.com/api/files.list'
    date = str(calendar.timegm((datetime.now() + timedelta(-g_slackRemoveLimitDay)).utctimetuple()))
    data = {'token': g_slackToken, 'ts_to': date}
    response = requests.post(listAPIUrl, data = data)
    jsonData = response.json()
    if ('files' in jsonData.keys()):
        if len(jsonData['files']) == 0:
            return {}
        else:
            return jsonData['files']
    else:
        print 'erorr'
        print response.text

def loadSettings():
    ''' 
    設定情報を読み取る
    '''
    global g_settings, g_repeatCount
    global g_slackDomain, g_slackToken, g_slackBotToken, g_slackChannelID, g_slackRemoveLimitDay

    # 設定ファイルの存在を確認する
    if (os.path.exists(g_settingPath)):
        settingFile = open(g_settingPath, 'r') 
        g_settings = json.load(settingFile)

        # Slack設定反映
        if('slackDomain' in g_settings.keys()):
            g_slackDomain = g_settings['slackDomain']
        if('slackToken' in g_settings.keys()):
            g_slackToken = g_settings['slackToken']
        if('slackBotToken' in g_settings.keys()):
            g_slackBotToken = g_settings['slackBotToken']
        if('slackChannelID' in g_settings.keys()):
            g_slackChannelID = g_settings['slackChannelID']
        if('slackRemoveLimitDay' in g_settings.keys()):
            g_slackRemoveLimitDay = g_settings['slackRemoveLimitDay']
        
        # リピート設定の反映
        if('repeatCount' in g_settings.keys()):
            g_repeatCount = g_settings['repeatCount']
        return True
    else:
        return False

if __name__ == '__main__':
    slackOldRmMain()
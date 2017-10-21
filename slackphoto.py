#!/usr/bin/env python
# -*- coding: utf-8 -*-

# slackphoto.py

import os
import sys
import time
import json
import random
import requests

# PIL Image Info
from PIL import Image
from PIL.ExifTags import TAGS

# Slack設定
g_slackDomain = ''
g_slackToken = ''
g_slackBotToken = ''
g_slackChannelID = ''

# 設定
g_settings = {}
g_settingPath = ''
g_repeatCount = 1

__version__ = '0.1.5.171021'

def slackPhotoMain():
    '''
    メインルーチン
    '''
    paths = []

    global g_settingPath
    g_settingPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'slackphoto.json')

    # 設定ファイルの読み込み
    loadSettings()
  
    # 設定データより 候補パスを取り出し
    for dir in g_settings['dirs']:
        for path in getDirList(dir):
            paths.append(path)

    # パスの検査
    if(len(paths) > 0):
        # photoPIcker の実行
        for i in range(0, g_repeatCount):
            photoPicker(paths)
    else:
        print 'no paths'

def checkFilePathExt(filePath):
    '''
    ファイルパスから画像拡張子の確認
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

    # アップロードファイルをピックアップする
    uploadFile = selectTargetFile(paths)

    if(uploadFile != ''):
        # Slack に投稿する
        
        # メッセージの投稿        
        fileMsg = ''
        fileMsg = '%s\n%s' % (uploadFile, getExifInfo(uploadFile))
        sendSlackText(g_slackChannelID, fileMsg)
        
        # 写真本体の投稿
        sendSlackPhoto(uploadFile, g_slackChannelID, uploadFile)

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

def selectTargetFile(paths):
    '''
    ターゲットになるファイルを探す
    '''
    # 有効なファイルが見つかるまで 10回トライする
    for var in range(0, 10):
        pivotDir = random.randrange(0, len(paths), 1)
        fileList = getFileList(paths[pivotDir])
        if (len(fileList) >= 1):
            filePivot = random.randrange(0, len(fileList), 1)
            filePath = os.path.join(paths[pivotDir], fileList[filePivot])
            print filePath
            return filePath
            break
        else:
            print 'retry - selectTargetFile'
    
    return ''

def getFileList(dir):
    '''
    ディレクトリ内の有効ファイルリストを作成する
    '''
    # ファイル一覧の作成
    files = os.listdir(dir)
    fileList = [f for f in files 
        if os.path.isfile(os.path.join(dir, f))
    ]

    # ファイルのフィルタリング
    filteredList = []
    for fileName in fileList:
        if (fileName[0:1] != '.'):
            # ファイル拡張子を確認する
            if(checkFilePathExt(fileName)):
                filteredList.append(fileName)

    return filteredList

def getDirList(path):
    '''
    ディレクトリ内のディレクトリのリストを再帰的に作成する
    '''
    for root, dirs, files in os.walk(path):
        yield root
        for dir in dirs:
            yield os.path.join(root, dir)

def loadSettings():
    ''' 
    設定情報を読み取る
    '''
    global g_settings, g_repeatCount
    global g_slackToken, g_slackBotToken, g_slackChannelID

    # 設定ファイルの存在を確認する
    if (os.path.exists(g_settingPath)):
        settingFile = open(g_settingPath, 'r') 
        g_settings = json.load(settingFile)

        # Token情報を反映
        if('slackToken' in g_settings.keys()):
            g_slackToken = g_settings['slackToken']
        if('slackBotToken' in g_settings.keys()):
            g_slackBotToken = g_settings['slackBotToken']
        if('slackChannelID' in g_settings.keys()):
            g_slackChannelID = g_settings['slackChannelID']
        
        # リピート設定の反映
        if('repeatCount' in g_settings.keys()):
            g_repeatCount = g_settings['repeatCount']
        return True
    else:
        return False

def sendSlackPhoto(filePath, channel, text):
    '''
    Slack に写真を投稿する
    ''' 
    # 画像のアップロード
    with open(filePath, 'rb') as f:
        imgParam = {
            'token': g_slackToken,
            'channels': channel,
            'title': os.path.basename(filePath)
        }
        r = requests.post('https://slack.com/api/files.upload', params=imgParam, files={'file':f})
        print r.status_code

def sendSlackText(channel, text):
    '''
    Slack にテキストを投稿する
    ''' 
    #　テキストメッセージの送信
    sendUrl = 'http://slack.com/api/chat.postMessage?token=%s&channel=%s&text=%s' % (g_slackToken, g_slackChannelID, text)
    #print sendUrl
    r = requests.post(sendUrl)
    print r.status_code

if __name__ == '__main__':
    slackPhotoMain()
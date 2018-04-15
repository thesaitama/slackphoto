#!/usr/bin/env python
# -*- coding: utf-8 -*-

# slackoldrm.py

import os
import json
import calendar

from datetime import datetime, timedelta

import requests

import slutil as slutil

g_settings = {}
g_settingPath = ''

def slackOldRmMain():
    """ main routine
    """
    global g_settingPath
    g_settingPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'slackphoto.json')

    # load configration
    loadSettings()

    if(g_settings['slackRemoveLimitDay'] != 0):
        print 'start: slackoldrm'
        list_data = getSlackOldFileList()
        if(list_data != {}):
            deleteSlackOldFile(list_data)
        else:
            print 'no old files found.'
    else:
        print 'cannceled: slackoldrm'

def deleteSlackOldFile(list_data):
    """ remove old files
    """
    for slack_file in list_data:
        # check image files extension
        if(slutil.checkFileExt(slack_file['filetype'])):
            print 'deleting file %s (%s)' % (slack_file['name'], slack_file['timestamp'])
            timestamp = str(calendar.timegm(datetime.now().utctimetuple()))
            delete_api_url = 'https://slack.com/api/files.delete?t=%s' % (timestamp)
            requests.post(delete_api_url, data={
                'token': g_settings['slackToken'], 'file': slack_file['id'],
                'set_active': 'true', '_attempts': '1'})

def getSlackOldFileList():
    """ obtatin old files list
    """
    list_api_url = 'https://slack.com/api/files.list'
    date = str(calendar.timegm((datetime.now() + timedelta(-g_settings['slackRemoveLimitDay'])).utctimetuple()))
    data = {'token': g_settings['slackToken'], 'ts_to': date}
    response = requests.post(list_api_url, data=data)
    json_data = response.json()
    if ('files' in json_data.keys()):
        if (len(json_data['files']) == 0):
            return {}
        else:
            return json_data['files']
    else:
        print 'erorr'
        print response.text

def loadSettings():
    """ load configration
    """
    global g_settings

    # check configration file exist
    if (os.path.exists(g_settingPath)):
        setting_file = open(g_settingPath, 'r')
        g_settings = json.load(setting_file)
        return True

    return False


if __name__ == '__main__':
    slackOldRmMain()

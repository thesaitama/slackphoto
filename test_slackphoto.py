#!/usr/bin/env python
# -*- coding: utf-8 -*-

# test_slackphoto.py

import slackphoto as slackphoto
import pytest

def test_loadSettings():
    ret = slackphoto.loadSettings('./slackphoto.sample.json')
    assert ret != {}



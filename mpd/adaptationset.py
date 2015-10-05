# coding: utf-8
# Copyright 2014 jeoliva author. All rights reserved.
# Use of this source code is governed by a MIT License
# license that can be found in the LICENSE file.

class AdaptationSet(object):
    TYPE_VIDEO = 0
    TYPE_AUDIO = 1
    TYPE_TEXT = 2
    TYPE_UNKNOWN = -1

    def __init__(self):
        self.id = 0
        self.type = 0
        self.representations = []
        self.contentProtections = []

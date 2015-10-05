# coding: utf-8
# Copyright 2014 jeoliva author. All rights reserved.
# Use of this source code is governed by a MIT License
# license that can be found in the LICENSE file.

class MediaPresentationDescription(object):
    def __init__(self):
        self.availabilityStartTime = 0
        self.duration = 0
        self.minBufferTime = 0
        self.dynamic = False
        self.minUpdatePeriod = 0
        self.timeShiftBufferDepth = 0
        self.location = ""
        self.periods = []
        self.utcTiming = None
        self.maxSegmentDuration = 0
        self.profiles = ""

# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4
#
# flumotion/component/producers/webcam/webcam.py: webcam producer
#
# Flumotion - a streaming media server
# Copyright (C) 2004 Fluendo, S.L. (www.fluendo.com). All rights reserved.

# This file may be distributed and/or modified under the terms of
# the GNU General Public License version 2 as published by
# the Free Software Foundation.
# This file is distributed without any warranty; without even the implied
# warranty of merchantability or fitness for a particular purpose.
# See "LICENSE.GPL" in the source distribution for more information.

# Licensees having purchased or holding a valid Flumotion Advanced
# Streaming Server license may use this file in accordance with the
# Flumotion Advanced Streaming Server Commercial License Agreement.
# See "LICENSE.Flumotion" in the source distribution for more information.

import gst

from flumotion.component import feedcomponent

class WebCamera(feedcomponent.ParseLaunchComponent):
    def __init__(self, name, pipeline):
        feedcomponent.ParseLaunchComponent.__init__(self, name,
                                                    [],
                                                    ['default'],
                                                    pipeline)
                                       
def setProp(struct, dict, name):
    if dict.has_key(name):
        struct[name] = dict[name]
                                                                                
def createComponent(config):
    # Filtered caps
    format = config.get('format', 'video/x-raw-yuv')
    struct = gst.structure_from_string('%s,format=(fourcc)I420' % format)
    setProp(struct, config, 'width')
    setProp(struct, config, 'height')
    setProp(struct, config, 'framerate')
    caps = gst.Caps(struct)
                                                                                
    component = WebCamera(config['name'], 'v4lsrc name=camera autoprobe=false copy-mode=1 ! %s ! videorate ! %s' % (caps, caps))

    return component

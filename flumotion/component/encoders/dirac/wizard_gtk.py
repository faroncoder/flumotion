# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4
#
# Flumotion - a streaming media server
# Copyright (C) 2004,2005,2006,2007,2008 Fluendo, S.L. (www.fluendo.com).
# All rights reserved.

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

# Headers in this file shall remain intact.

import gettext
import os

from zope.interface import implements

from flumotion.admin.assistant.interfaces import IEncoderPlugin
from flumotion.admin.assistant.models import VideoEncoder
from flumotion.admin.gtk.basesteps import VideoEncoderStep

__version__ = "$Rev: 6443 $"
_ = gettext.gettext


class DiracVideoEncoder(VideoEncoder):
    componentType = 'dirac-encoder'

    def __init__(self):
        super(DiracVideoEncoder, self).__init__()

        self.properties.bitrate = 400


class DiracStep(VideoEncoderStep):
    name = 'Dirac encoder'
    title = _('Dirac Encoder')
    sidebarName = _('Dirac')
    icon = 'xiphfish.png'
    gladeFile = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'wizard.glade')
    componentType = 'dirac'
    docSection = 'help-configuration-assistant-encoder-dirac'
    docAnchor = ''
    docVersion = 'local'

    # WizardStep

    def setup(self):
        self.bitrate.data_type = int
        self.add_proxy(self.model.properties,
                       ['bitrate'])

    def workerChanged(self, worker):
        self.model.worker = worker

        self.wizard.debug('running Dirac checks')
        # FIXME: what happens to this deferred ? Does it get fired into the
        # unknown ? Should we wait on it ?
        self.wizard.requireElements(worker, 'schroenc')


class DiracWizardPlugin(object):
    implements(IEncoderPlugin)

    def __init__(self, wizard):
        self.wizard = wizard
        self.model = DiracVideoEncoder()

    def getConversionStep(self):
        return DiracStep(self.wizard, self.model)

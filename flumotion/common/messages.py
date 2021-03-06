# -*- Mode: Python; test-case-name: flumotion.test.test_common_messages -*-
# vi:si:et:sw=4:sts=4:ts=4
#
# Flumotion - a streaming media server
# Copyright (C) 2004,2005,2006,2007 Fluendo, S.L. (www.fluendo.com).
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

"""serializable translatable messages.
support for serializable translatable messages from component/manager to admin
"""

import time

from twisted.spread import pb

from flumotion.common import log
from flumotion.configure import configure
from flumotion.common.i18n import FancyEqMixin, Translatable
from flumotion.common.i18n import *

__version__ = "$Rev$"

(ERROR,
 WARNING,
 INFO) = range(1, 4)


# NOTE: same caveats apply for FancyEqMixin as above
# this might be a little heavy; we could consider only comparing
# on id, once we verify that all id's are unique


class Message(pb.Copyable, pb.RemoteCopy, FancyEqMixin):
    """
    I am a message to be shown in a UI.

    Projects should subclass this base class to provide default project
    and version class attributes.

    @ivar  section: name of the section in which the message is described.
    @type  section: str
    @ivar  anchor:  name of the anchor in which the message is described.
    @type  anchor:  str
    @ivar  description: the link text to show
    @type  description: L{flumotion.common.messages.Translatable}
    """
    project = configure.PACKAGE
    version = configure.version

    # these properties allow linking to the documentation
    section = None
    anchor = None
    description = None

    compareAttributes = ["level", "translatables", "debug", "mid", "priority",
        "timestamp"]

    def __init__(self, level, translatable, debug=None, mid=None, priority=50,
        timestamp=None):
        """
        Create a new message.

        The mid identifies this kind of message, and serves two purposes.

        The first purpose is to serve as a key by which a kind of
        message might be removed from a set of messages. For example, a
        firewire component detecting that a cable has been plugged in
        will remove any message that the cable is unplugged.

        Secondly it serves so that the message viewers that watch the
        'current state' of some object only see the latest message of a
        given type. For example when messages are stored in persistent
        state objects that can be transferred over the network, it
        becomes inefficient to store the whole history of status
        messages. Message stores can keep only the latest message of a
        given ID.

        @param level:        ERROR, WARNING or INFO
        @param translatable: a translatable possibly with markup for
                             linking to documentation or running commands.
        @param debug:        further, untranslated, debug information, not
                             always shown
        @param priority:     priority compared to other messages of the same
                             level
        @param timestamp:    time since epoch at which the message was
                             generated, in seconds.
        @param mid:          A unique id for this kind of message, as
                             discussed above. If not given, will be
                             generated from the contents of the
                             translatable.
        """
        self.level = level
        self.translatables = []
        self.debug = debug

        # FIXME: untranslated is a really poor choice of id
        self.id = mid or translatable.untranslated()
        self.priority = priority
        self.timestamp = timestamp or time.time()
        # -1 is in __init__, -2 is in the subclass __init__,
        # -3 is in the caller
        log.doLog(log.DEBUG, None, 'messages',
            'creating message %r', self, where=-3)
        log.doLog(log.DEBUG, None, 'messages',
            'message debug %s', debug)
        self.add(translatable)

    def __repr__(self):
        return '<Message %r at %r>' % (self.id, id(self))

    def add(self, translatable):
        if not isinstance(translatable, Translatable):
            raise ValueError('%r is not Translatable' % translatable)
        self.translatables.append(translatable)
        log.doLog(log.DEBUG, None, 'messages',
            'message %r: adding %r', (id(self), translatable.untranslated()),
             where=-2)

    def getTimeStamp(self):
        """Get the timestamp for the message
        @returns: the timestamp or None
        @rtype: int
        """
        # F0.4: timestamp was added in 0.4.2
        return getattr(self, 'timestamp', None)

    def getDescription(self):
        """Get the description for the message
        @returns: the description or None
        @rtype: str
        """
        return getattr(self, 'description', None)

pb.setUnjellyableForClass(Message, Message)

# these are implemented as factory functions instead of classes because
# properly proxying to the correct subclass is hard with Copyable/RemoteCopy


def Error(*args, **kwargs):
    """
    Create a L{Message} at ERROR level, indicating a failure that needs
    intervention to be resolved.
    """
    return Message(ERROR, *args, **kwargs)

# FIXME: figure out a way to not be shadowing the Warning builtin without
# breaking all other code
__pychecker__ = 'no-shadowbuiltin'


def Warning(*args, **kwargs):
    """
    Create a L{Message} at WARNING level, indicating a potential problem.
    """
    return Message(WARNING, *args, **kwargs)
__pychecker__ = ''


def Info(*args, **kwargs):
    """
    Create a L{Message} at INFO level.
    """
    return Message(INFO, *args, **kwargs)


class Result(pb.Copyable, pb.RemoteCopy):
    """
    I am used in worker checks to return a result.

    @ivar value:    the result value of the check
    @ivar failed:   whether or not the check failed.  Typically triggered
                    by adding an ERROR message to the result.
    @ivar messages: list of messages
    @type messages: list of L{Message}
    """

    def __init__(self):
        self.messages = []
        self.value = None
        self.failed = False

    def succeed(self, value):
        """
        Make the result be successful, setting the given result value.
        """
        self.value = value

    def add(self, message):
        """
        Add a message to the result.

        @type message: L{Message}
        """
        self.messages.append(message)
        if message.level == ERROR:
            self.failed = True
            self.value = None
pb.setUnjellyableForClass(Result, Result)

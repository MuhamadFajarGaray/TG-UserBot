# TG-UserBot - A modular Telegram UserBot script for Python.
# Copyright (C) 2019  Kandarp <https://github.com/kandnub>
#
# TG-UserBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TG-UserBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TG-UserBot.  If not, see <https://www.gnu.org/licenses/>.


import re
from telethon import events
from telethon.tl import types
from typing import Tuple


@events.common.name_inner_event
class NewMessage(events.NewMessage):
    """Custom NewMessage event inheriting the default Telethon event"""

    def __init__(
        self,
        disable_prefix: bool = None,
        regex: Tuple[str, int] or str = None,
        require_admin: bool = None,
        **kwargs
    ):
        """Overriding the default init to add additional attributes"""
        events.NewMessage.__init__(self, **kwargs)

        if regex:
            if isinstance(regex, tuple):
                exp, flags = regex
                if not isinstance(exp, str):
                    raise TypeError(
                        "Make sure you're using a string for a pattern!"
                    )
                self.regex = (exp, flags)
            elif isinstance(regex, str):
                self.regex = (regex, 0)
            else:
                raise TypeError("Invalid regex type given!")
        else:
            self.regex = regex

        self.disable_prefix = disable_prefix
        self.require_admin = require_admin

    def filter(self, event):
        """Overriding the default filter to check additional values"""
        prefix = re.escape(event._client.prefix)
        tl_event = events.NewMessage.filter(self, event)

        if not tl_event:
            return

        if self.regex:
            exp, flags = self.regex

            if not self.disable_prefix:
                pattern = re.compile("(?i)^" + prefix + exp).finditer
            else:
                pattern = re.compile(exp).finditer

            text = tl_event.message.message or ''
            matches = list(pattern(text)) or None
            if not matches:
                return
            tl_event.matches = matches

        if self.require_admin:
            if not (
                (tl_event.chat.is_private or tl_event.chat.creator) or
                tl_event.chat.admin_rights
            ):
                return

        return tl_event


@events.common.name_inner_event
class MessageEdited(NewMessage):
    """Custom MessageEdited event inheriting the custom NewMessage event"""

    @classmethod
    def build(cls, update, others=None, self_id=None):
        """Required to check if message is edited, double events"""
        if isinstance(update, (types.UpdateEditMessage,
                               types.UpdateEditChannelMessage)):
            return cls.Event(update.message)

    class Event(NewMessage.Event):
        """Overriding the default Event which inherits Telethon's NewMessage"""
        pass  # Required if we want a different name for it

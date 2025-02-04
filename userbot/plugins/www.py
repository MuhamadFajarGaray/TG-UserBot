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


from telethon.tl.functions.help import GetNearestDcRequest

from userbot import client


@client.onMessage(
    command="nearestdc", info="Get your DC information",
    outgoing=True, regex="nearestdc$"
)
async def nearestdc(event):
    """DC function used to get information for .dc"""
    result = await client(GetNearestDcRequest())
    text = (
        f"**Country:** `{result.country}`\n" +
        f"**This DC:** `{result.this_dc}`\n" +
        f"**Nearest DC:** `{result.nearest_dc}`"
    )
    await event.edit(text)

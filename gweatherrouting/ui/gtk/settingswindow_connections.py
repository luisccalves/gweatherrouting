# -*- coding: utf-8 -*-
# Copyright (C) 2017-2021 Davide Gessa
'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

For detail about GNU see <http://www.gnu.org/licenses/>.
'''

import gi
import os
import json
import math
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GObject, Gdk
from threading import Thread


class SettingsWindowConnections:
	def __init__(self, mainWindow, settingsManager):
		self.reloadConnections()

	def reloadConnections(self):
		self.connectionStore = self.builder.get_object("connection-store")
		self.connectionStore.clear()

		# for c in self.mainWindow.conn.connections:
		# 	self.connectionStore.append ([])
		# 	pass 

	def onAddNetworkConnection(self, widget):
		pass

	def onAddDeviceConnection(self, widget):
		pass

	def onConnectionRemove(self, widget):
		pass

	def onConnectionClick(self, widget, event):
		if event.button == 3:
			menu = self.builder.get_object("connection-menu")
			menu.popup (None, None, None, None, event.button, event.time)
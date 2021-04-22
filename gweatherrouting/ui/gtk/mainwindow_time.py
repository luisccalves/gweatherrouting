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

gi.require_version('Gtk', '3.0')
gi.require_version('OsmGpsMap', '1.2')

from gi.repository import Gtk, Gio, GObject, OsmGpsMap, Gdk
from .timepickerdialog import TimePickerDialog


class MainWindowTime:
	play = False

	def __init__(self):
		# self.timeAdjust = self.builder.get_object('time-adjustment')
		self.timeLabel = self.builder.get_object('time-label')
		self.timeControl.connect('time-change', self.onTimeChange)
		self.onTimeChange(self.timeControl.time)

	def onTimeChange(self, t):
		self.timeLabel.set_text("%s" % str(t))
		self.map.queue_draw ()

	def onTimeNow(self, event):
		self.timeControl.now()

	def onPlayClick(self, event):
		self.play = True
		GObject.timeout_add (10, self.onPlayStep)

	def onPlayStep(self):
		self.onFowardClick(None)
		if self.play:
			GObject.timeout_add (1000, self.onPlayStep)

	def onStopClick(self, event):
		self.play = False

	def onFowardClick(self, event):
		self.timeControl.increase(minutes=30)
		self.map.queue_draw ()

	def onBackwardClick(self, event):
		# if self.timeControl.time > 0:
		self.timeControl.decrease(minutes=30)

	def onTimeSelect(self, event):
		tp = TimePickerDialog.create(self.window)
		tp.setFromDateTime(self.timeControl.time)
		response = tp.run()

		if response == Gtk.ResponseType.OK:
			self.timeControl.setTime(tp.getDateTime())
		
		tp.destroy()



	# def updateTimeSlider(self):
	# 	self.timeAdjust.set_value(int(self.timeControl.time))

	def onTimeSlide (self, widget):
		self.timeControl.setTime(int (self.timeAdjust.get_value()))
		self.map.queue_draw ()
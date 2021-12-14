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
import datetime
from threading import Thread
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GObject, Gdk
import cairo
import matplotlib.pyplot as plt
import io
import numpy
import PIL

class MPLWidget(Gtk.DrawingArea):
	def __init__(self, parent):      
		self.par = parent
		super(MPLWidget, self).__init__()
 
		self.plotDrawer = None 

		# self.set_size_request(-1, 30)
		self.connect("draw", self.draw)

	def setPlotDrawer(self, f):
		self.plotDrawer = f	

	def draw(self, area, ctx):      
		if not self.plotDrawer:
			return

		width = self.allocation.width
		height = self.allocation.height
	 
		s = 20
		a = self.get_allocation()
		import matplotlib.pyplot as plt

		plt.style.use('dark_background')
		plt.rcParams.update({'font.size': 8})

		self.plotDrawer(width, height, plt, self)

		buf = io.BytesIO()
		plt.savefig(buf, dpi=100)
		buf.seek(0)
		buf2= PIL.Image.open(buf)
	
		arr = numpy.array(buf2)
		height, width, channels = arr.shape
		surface = cairo.ImageSurface.create_for_data(arr, cairo.FORMAT_RGB24, width, height)

		ctx.save()
		ctx.set_source_surface (surface, 0, 0)
		ctx.paint()
		ctx.restore()

		# fig.clf()
		# plt.close(fig)

	

	   
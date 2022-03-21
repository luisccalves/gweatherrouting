# -*- coding: utf-8 -*-
# Copyright (C) 2017-2022 Davide Gessa
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

gi.require_version('Gtk', '3.0')
gi.require_version('OsmGpsMap', '1.2')

from gi.repository import Gtk, Gdk

import logging

from .gribmanagerwindow import GribFileFilter
from .maplayers import GribMapLayer, AISMapLayer

from .settings import SettingsManager
from ..core import TimeControl
from .chartstack_poi import ChartStackPOI
from .chartstack_track import ChartStackTrack
from .chartstack_routing import ChartStackRouting
from .widgets.timetravel import TimeTravelWidget

logger = logging.getLogger ('gweatherrouting')

class ChartStack(Gtk.Box, ChartStackPOI, ChartStackTrack, ChartStackRouting):
	def __init__(self, parent, chartManager, core):
		Gtk.Widget.__init__(self)

		self.parent = parent
		self.chartManager = chartManager
		self.core = core

		self.timeControl = TimeControl()
		self.settingsManager = SettingsManager()

		self.builder = Gtk.Builder()
		self.builder.add_from_file(os.path.abspath(os.path.dirname(__file__)) + "/chartstack.glade")
		self.builder.connect_signals(self)

		self.pack_start(self.builder.get_object("chartcontent"), True, True, 0)

		self.map = self.builder.get_object("map")
		self.map.set_center_and_zoom (39., 9., 6)

		self.map.layer_add (self.chartManager)

		self.gribMapLayer = GribMapLayer (self.core.gribManager, self.timeControl, self.settingsManager)
		self.map.layer_add (self.gribMapLayer)
		
		# This causes rendering problem
		#self.map.layer_add (OsmGpsMap.MapOsd (show_dpad=True, show_zoom=True, show_crosshair=False))

		self.statusbar = self.builder.get_object("status-bar")

		ChartStackRouting.__init__(self)
		ChartStackTrack.__init__(self)
		ChartStackPOI.__init__(self)

		self.core.connect('boatPosition', self.boatInfoHandler)

		self.timetravelWidget = TimeTravelWidget(self.parent, self.timeControl, self.map)
		self.builder.get_object("timetravelcontainer").pack_start(self.timetravelWidget, True, True, 0)


		# https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/#Z/#Y/#X
		# https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/#Z/#Y/#X
		# https://a.basemaps.cartocdn.com/dark_all/#Z/#X/#Y.png

		# var CartoDB_DarkMatter = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
		# 	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
		# 	subdomains: 'abcd',
		# 	maxZoom: 19
		# });
		# var OpenSeaMap = L.tileLayer('https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png', {
		# 	attribution: 'Map data: &copy; <a href="http://www.openseamap.org">OpenSeaMap</a> contributors'
		# });

		self.show_all()


	def boatInfoHandler(self, bi):
		self.map.gps_add(bi.latitude, bi.longitude, heading=bi.heading)
		self.map.queue_draw ()


	def onMapMouseMove(self, map, event):
		lat, lon = map.convert_screen_to_geographic(event.x, event.y).get_degrees ()
		w = self.core.gribManager.getWindAt(self.timeControl.time, lat, lon)
		
		sstr = ""
		if w:
			sstr += "Wind %.1f°, %.1f kts - " % (w[0], w[1])
		sstr += "Latitude: %f, Longitude: %f" % (lat, lon)

		self.statusbar.push(self.statusbar.get_context_id ('Info'), sstr)

	def onMapClick(self, map, event):
		lat, lon = map.get_event_location (event).get_degrees ()
		self.builder.get_object("track-add-point-lat").set_text (str (lat))
		self.builder.get_object("track-add-point-lon").set_text (str (lon))
		self.statusbar.push(self.statusbar.get_context_id ('Info'), "Clicked on " + str(lat) + " " + str(lon))
		
		if event.button == 3:
			menu = self.builder.get_object("map-context-menu")
			menu.popup (None, None, None, None, event.button, event.time)
		self.map.queue_draw ()


	def onNew (self, widget):
		self.core.trackManager.create()
		self.updateTrack ()
		self.map.queue_draw ()

	def onExport(self, widget):
		menu = self.builder.get_object("export-menu")
		menu.popup_at_widget (widget, Gdk.Gravity.SOUTH_WEST, Gdk.Gravity.NORTH_WEST, None)

	def onImport (self, widget):
		dialog = Gtk.FileChooserDialog ("Please choose a file", self.parent,
					Gtk.FileChooserAction.OPEN,
					(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
			
		filter_gpx = Gtk.FileFilter ()		
		filter_gpx.set_name ("GPX track")
		filter_gpx.add_mime_type ("application/gpx+xml")
		filter_gpx.add_pattern ('*.gpx')
		dialog.add_filter (filter_gpx)

		dialog.add_filter (GribFileFilter)

		response = dialog.run()
		
		if response == Gtk.ResponseType.OK:
			filepath = dialog.get_filename ()
			dialog.destroy ()

			extension = filepath.split('.')[-1]

			if extension in ['gpx']:
				if self.core.importGPX (filepath):
					# self.builder.get_object('header-bar').set_subtitle (filepath)
					self.updateTrack ()
					self.updatePOI()

					edialog = Gtk.MessageDialog (self.parent, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Done")
					edialog.format_secondary_text ("GPX file opened and loaded")
					edialog.run ()
					edialog.destroy ()	
					self.statusbar.push (self.statusbar.get_context_id ('Info'), 'Loaded %s with %d waypoints' % (filepath, len (self.core.trackManager.activeTrack)))					
					
				else:
					edialog = Gtk.MessageDialog (self.parent, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "Error")
					edialog.format_secondary_text ("Cannot open file: %s" % filepath)
					edialog.run ()
					edialog.destroy ()

			elif extension in ['grb', 'grb2', 'grib']:
				if self.core.gribManager.importGrib(filepath):
					edialog = Gtk.MessageDialog (self.parent, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Done")
					edialog.format_secondary_text ("File opened, loaded grib")
					edialog.run ()
					edialog.destroy ()	
					self.statusbar.push (self.statusbar.get_context_id ('Info'), 'Loaded grib %s' % (filepath))					

				else:
					edialog = Gtk.MessageDialog (self.parent, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "Error")
					edialog.format_secondary_text ("Cannot open grib file: %s" % filepath)
					edialog.run ()
					edialog.destroy ()

			else:
				edialog = Gtk.MessageDialog (self.parent, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "Error")
				edialog.format_secondary_text ("Unrecognize file format: %s" % filepath)
				edialog.run ()
				edialog.destroy ()

		else:
			dialog.destroy()

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

gi.require_version('Gtk', '3.0')
gi.require_version('OsmGpsMap', '1.2')
	
from gi.repository import Gtk

from ..core import utils
from .maplayers import POIMapLayer

class ChartStackPOI:
	selectedPOI = None

	def __init__(self):
		self.poiMapLayer = POIMapLayer(self.core.poiManager)
		self.map.layer_add (self.poiMapLayer)

		self.poiStore = self.builder.get_object("poi-store")
		self.updatePOI()


	def onPOINameEdit(self, widget, i, name):
		self.core.poiManager.pois[int(i)].name = utils.uniqueName(name, self.core.poiManager.pois)
		self.updatePOI()

	def onSelectPOI (self, selection):
		store, pathlist = selection.get_selected_rows()
		for path in pathlist:
			tree_iter = store.get_iter(path)
			self.selectedPOI = store.get_value(tree_iter, 0)

	def onPOIRemove(self, widget):
		if self.selectedPOI != None:
			self.core.poiManager.remove(self.core.poiManager.remove(self.selectedPOI))
			self.updatePOI()

	def onPOIToggle(self, widget, i):
		self.core.poiManager.pois[int(i)].visible = not self.core.poiManager.pois[int(i)].visible
		self.updatePOI()

	def onPOIClick(self, item, event):
		if event.button == 3 and len(self.core.poiManager.pois) > 0:
			menu = self.builder.get_object("poi-menu")
			menu.popup (None, None, None, None, event.button, event.time)

	def updatePOI (self):
		self.poiStore.clear()
		for x in self.core.poiManager.pois:
			self.poiStore.append([x.name, x.position[0], x.position[1], x.visible, x.type])
		self.core.poiManager.savePOI()
		self.map.queue_draw ()


	def addPOI (self, widget):
		lat = self.builder.get_object("track-add-point-lat").get_text ()
		lon = self.builder.get_object("track-add-point-lon").get_text ()

		if len (lat) > 1 and len (lon) > 1:
			self.core.poiManager.create([float (lat), float (lon)])
			self.map.queue_draw ()
			self.updatePOI()

	def exportPOIsAsNMEAPFEC(self, widget):
		dialog = Gtk.FileChooserDialog("Export POIs as NMEA PFEC", self.parent, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
		dialog.set_do_overwrite_confirmation(True)

		filter_gpx = Gtk.FileFilter()
		filter_gpx.set_name("NMEA text file")
		filter_gpx.add_mime_type("text/plain")
		filter_gpx.add_pattern ('*.nmea')
		dialog.add_filter(filter_gpx)

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			filename = dialog.get_filename()
			dialog.destroy()
			s = self.core.poiManager.exportAsNMEAPFEC()
			f = open(filename, 'w')
			f.write(s)
			f.close()

			self.statusbar.push(0, "POIs exported as NMEA PFEC to %s" % filename)
		else:
			dialog.destroy()


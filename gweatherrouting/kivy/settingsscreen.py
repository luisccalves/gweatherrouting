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
from kivy.properties import BooleanProperty, ObjectProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import IRightBodyTouch, TwoLineIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox

class SettingsScreen(MDScreen):
	def on_pre_enter(self, *args):
		pass
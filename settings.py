#!/usr/bin/python
from gi.repository import Gtk
import json
import os


config_addr = os.getenv("HOME")+'/.config/wildguppy/config.json'
user_config = json.load(open(config_addr))

samplerate = user_config['samplerate']
max_brightness = user_config['maxbrightness']
min_brightness = user_config['minbrightness']


class mainWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="Autobrightness Settings")
		grid = Gtk.Grid()
		self.add(grid)

		self.button = Gtk.Button(label="Update")
		self.button.connect("clicked", self.on_button_clicked)
		self.entry1 = Gtk.Entry()
		self.entry1.set_text(samplerate)
		self.entry2 = Gtk.Entry()
		self.entry2.set_text(str(max_brightness))
		self.entry3 = Gtk.Entry()
		self.entry3.set_text(str(min_brightness))
		label1 = Gtk.Label("Time interval in seconds")
		label2 = Gtk.Label("Max brightness (1 - 100)")
		label3 = Gtk.Label("Min brightness (0 - 99)")
		self.label4 = Gtk.Label("")
		grid.add(label1)
		grid.attach_next_to(self.entry1, label1, Gtk.PositionType.RIGHT, 2, 1)
		grid.attach_next_to(label2, label1, Gtk.PositionType.BOTTOM, 1, 2)
		grid.attach_next_to(self.entry2, label2, Gtk.PositionType.RIGHT, 1, 2)
		grid.attach_next_to(label3, label2, Gtk.PositionType.BOTTOM, 1, 2)
		grid.attach_next_to(self.entry3, label3, Gtk.PositionType.RIGHT, 1, 2)
		grid.attach_next_to(self.button, self.entry3, Gtk.PositionType.BOTTOM, 1, 2)
		grid.attach_next_to(self.label4, label3, Gtk.PositionType.BOTTOM, 1, 2)
	
	def on_button_clicked(self, widget):
            try:
                int(self.entry1.get_text())
                int(self.entry2.get_text())
                int(self.entry3.get_text())
            except ValueError:
                if isinstance(float(self.entry1.get_text()), float):
                    self.label4.set_text("Enter natural number for time")
                else:
                    self.label4.set_text("Numbers only!")
                return
            
            if int(self.entry2.get_text()) <= int(self.entry3.get_text()):
                self.label4.set_text("Max value must be greater than min")
                return
                
            user_config = {'samplerate':str(self.entry1.get_text()), 'maxbrightness':str(self.entry2.get_text()), 'minbrightness':str(self.entry3.get_text())} 	
	    json.dump(user_config, open(config_addr, 'w'))	
	    self.label4.set_text("Updated!\nRestart the program\nto see changes")
	    pass

win = mainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()

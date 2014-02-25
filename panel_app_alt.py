#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk, AppIndicator3 as AppIndicator, GLib
from os import path, getenv, system
import wildguppy
from json import load

class AutoBrightnessIndicator():
    """An indicator for the AutoBrightness script"""
    def __init__(self):
        self.script_dir = path.split(path.realpath(__file__))[0]
        self.ind = AppIndicator.Indicator.new("AutoBrightness indicator",
                                              self.script_dir + "/fish.png",
                                              AppIndicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status(AppIndicator.IndicatorStatus.ACTIVE)

        self.config_path = getenv("HOME")+"/.config/wildguppy/config.json"

        self.menu = Gtk.Menu()

        self.startItem    = Gtk.MenuItem('Start')
        self.stopItem     = Gtk.MenuItem('Stop')
        self.restartItem  = Gtk.MenuItem('Restart')
        self.luckyItem    = Gtk.MenuItem('Feeling Lucky')
        self.quitItem     = Gtk.MenuItem('Quit')
        self.settingsItem = Gtk.MenuItem('Settings')
        self.aboutItem    = Gtk.MenuItem('About')
        self.levelItem    = Gtk.MenuItem('Brightness Levels')

        self.menu.append(self.startItem)
        self.menu.append(self.stopItem)
        self.menu.append(self.restartItem)
        self.menu.append(self.luckyItem)
        self.menu.append(self.levelItem)
        self.menu.append(self.settingsItem)
        self.menu.append(self.aboutItem)
        self.menu.append(self.quitItem)

        eachLevel = Gtk.Menu();
        self.levelItem.set_submenu(eachLevel)

        self.subLevels = {} 
        
        for i in range(10):
            subLevel = Gtk.MenuItem(str(i*10+10))
            self.subLevels[subLevel] = i*10+10
            eachLevel.append(subLevel)

        self.menu.show_all()
        self.ind.set_menu(self.menu)

        self.timeout_id = 0
        self.startItem.connect('activate', self.startProgram)
        self.stopItem.connect('activate', self.stopProgram)
        self.restartItem.connect('activate', self.restartProgram)
        self.luckyItem.connect('activate', self.luckMaker)
        self.aboutItem.connect('activate', self.aboutShow)
        self.settingsItem.connect('activate', self.settingsShow)
        for x in self.subLevels:
            x.connect('activate', self.brightnessSet, x)
        self.quitItem.connect('activate', self.quit)

        self.program = wildguppy.autoBrightness()

    def startProgram(self, widget):
        """Start the sampling and brightness setting"""
        self.ind.set_icon(self.script_dir + "/fish.png")
        config_file = load(open(self.config_path))
        self.program.samplerate = int(config_file['samplerate'])
        self.program.maxbr_ = int(config_file['maxbrightness'])
        self.program.minbr_ = int(config_file['minbrightness'])
        self.program.run_once()
        self.timeout_id = GLib.timeout_add((self.program.samplerate*1000), self.program.run_once)

    def stopProgram(self, widget):
        """Stop the sampling"""
        self.ind.set_icon(self.script_dir + "/fish.png")
        GLib.source_remove(self.timeout_id)

    def restartProgram(self, widget):
        """Restart the sampling"""
        self.stopProgram(widget)
        self.startProgram(widget)

    def settingsShow(self, widget):
        """Show the settings window"""
        system( self.script_dir + "/settings.py" )

    def luckMaker(self, widget):
        """Run the program once"""
        try:
            self.stopProgram(widget)
            self.program.run_once()
        except TypeError:
            self.program.run_once()

    def aboutShow(self, widget):
        """Show the About window"""
        system( self.script_dir + "/about.py" )

    def brightnessSet(self, widget, item):
        """Execute the command to set the screen brightness"""
        system("xbacklight -set " + str(self.subLevels[item]) )

    def quit(self, widget):
        """Quit the indicator"""
        Gtk.main_quit()

    def main(self):
        """Start the Gtk loop"""
        self.startProgram(None)
        Gtk.main()


if __name__ == "__main__":
    ind = AutoBrightnessIndicator().main()

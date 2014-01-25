#!/usr/bin/python

import appindicator
import gtk
import os
import wildguppy
import thread
import gobject
import json

gobject.threads_init()
file_path = "/opt/wildguppy/icon/fish.png"
config_path = os.getenv("HOME")+"/.config/wildguppy/config.json"
script_dir, script_name = os.path.split(os.path.realpath(__file__))

a = appindicator.Indicator('wildguppy', file_path, appindicator.CATEGORY_APPLICATION_STATUS)
a.set_status( appindicator.STATUS_ACTIVE )

m = gtk.Menu()
startItem = gtk.MenuItem('Start')
stopItem = gtk.MenuItem('Stop')
restartItem = gtk.MenuItem('Restart')
luckyItem = gtk.MenuItem('Feeling Lucky')
quitItem = gtk.MenuItem('Quit')
settingsItem = gtk.MenuItem('Settings')
aboutItem = gtk.MenuItem('About')
levelItem = gtk.MenuItem('Brightness Levels')


m.append(startItem)
m.append(stopItem)
m.append(restartItem)
m.append(luckyItem)
m.append(levelItem)
m.append(settingsItem)
m.append(aboutItem)
m.append(quitItem)

eachLevel = gtk.Menu()
levelItem.set_submenu(eachLevel)

subLevels = {} 
    
for i in xrange(10):
    subLevel = gtk.MenuItem(str(i*10+10))
    subLevels[subLevel] = i*10+10
    eachLevel.append(subLevel)
    subLevel.show()


a.set_menu(m)
startItem.show()
stopItem.show()
restartItem.show()
luckyItem.show()
levelItem.show()
settingsItem.show()
aboutItem.show()
quitItem.show()


program = wildguppy.autoBrightness()
samplerate = int(wildguppy.config_file['samplerate'])
maxbr_global = int(wildguppy.config_file['maxbrightness'])
minbr_global = int(wildguppy.config_file['minbrightness'])

x = 0
    
def startProgram(item):
    #sampling starts here
    global x 
    program.maxbr_ = maxbr_global
    program.minbr_ = minbr_global
    x = gobject.timeout_add((samplerate*1000), program.run_once)

startItem.connect('activate', startProgram)

def stopProgram(item):
    #sampling stops and retrieves new settings
    global maxbr_global, minbr_global, samplerate
    config_file = json.load(open(config_path))
    maxbr_global = int(config_file['maxbrightness'])
    minbr_global = int(config_file['minbrightness'])
    samplerate = int(config_file['samplerate'])
    gobject.source_remove(x)
    
stopItem.connect('activate', stopProgram)


def restartProgram(item):
    print "restarted"
    stopProgram(item)
    startProgram(item)
restartItem.connect('activate', restartProgram)

def quit(item):
    gtk.main_quit()
quitItem.connect('activate', quit)

def settingsShow(item):
	os.system("%s/settings.py" % script_dir)
settingsItem.connect('activate', settingsShow)

def luckMaker(item):
    try:
        stopProgram(item)
        program.run_once()
        pass
    except TypeError:
        program.run_once()
        pass
    
luckyItem.connect('activate', luckMaker)

def aboutShow(item):
    #about window
    os.system("%s/about.py" % script_dir)
aboutItem.connect('activate', aboutShow)

def brightnessSet(item):
    os.system("xbacklight -set %s" % subLevels[item])
for x in subLevels:
    x.connect('activate', brightnessSet)
    
gtk.main()


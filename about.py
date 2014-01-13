#!/usr/bin/python
from gi.repository import Gtk

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="WildGuppy 1.0")

        self.about_text = Gtk.Label("Name: WildGuppy 1.0")
        self.about_text.set_markup("Name: WildGuppy 1.0 \nDeveloper: Bilegt\n <a href=\"http://www.twitter.com/billyboar\" "
                 "title=\"My Twitter\">My Twitter</a> ")
        self.add(self.about_text)

    def on_button_clicked(self, widget):
        print("Hello World")

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()

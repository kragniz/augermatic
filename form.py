#!/usr/bin/python
from gi.repository import Gtk

class Form(Gtk.Box):
    def __init__(self, items):
        Gtk.Box.__init__(self, spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.button = Gtk.Button(label='Click this')
        self.pack_start(self.button, True, True, 6)

if __name__ == '__main__':
    win = Gtk.Window(title='Form test')
    form = Form(
                  [
                     ['database-no', 'Database Number'],
                     ['date', 'Date']
                  ]
               )
    win.add(form)
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()

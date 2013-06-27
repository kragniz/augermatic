#!/usr/bin/env python
from gi.repository import Gtk

class Form(Gtk.Box):
    def __init__(self, items):
        Gtk.Box.__init__(self, spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.fields = {}
        for item in items:
            box = Gtk.Box(spacing=6)
            label = Gtk.Label(item['label'])
            self.fields[item['id']] = Gtk.Entry()
            box.pack_start(label, False, False, 6)
            box.pack_start(self.fields[item['id']], True, True, 6)
            self.pack_start(box, False, True, 6)
        print self.fields

if __name__ == '__main__':
    win = Gtk.Window(title='Form test')
    form = Form(
                  [
                     {'id': 'database-no', 'label': 'Database Number'},
                     {'id': 'date', 'label': 'Date'}
                  ]
               )
    win.add(form)
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()

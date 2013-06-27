#!/usr/bin/env python
from gi.repository import Gtk

class Form(Gtk.Box):
    def __init__(self, items):
        Gtk.Box.__init__(self, spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.fields = {}
        for item in items:
            box = Gtk.Box()
            label = Gtk.Label(item['label'])
            self.fields[item['id']] = Gtk.Entry()
            box.pack_start(label, False, False, 10)
            box.pack_start(self.fields[item['id']], True, True, 6)
            self.pack_start(box, False, True, 4)
        print self.fields

    def print_data(self, event):
        for f in self.fields:
            print f, ':', self.fields[f].get_text()

if __name__ == '__main__':
    win = Gtk.Window(title='Form test')
    form = Form(
                  [
                     {'id': 'database-no', 'label': 'Database Number'},
                     {'id': 'name', 'label': 'Soil thing name'},
                     {'id': 'date', 'label': 'Date'}
                  ]
               )

    box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
    box.pack_start(form, True, True, 20)

    b = Gtk.Button(label='Show data')
    b.connect('clicked', form.print_data)
    box.pack_start(b, True, True, 6)
    win.add(box)
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()

#!/usr/bin/env python
from gi.repository import Gtk

class Form(Gtk.Box):
    def __init__(self, items):
        Gtk.Box.__init__(self, spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.fields = {}
        labelWidth = max([len(i[1]) for i in items])

        for item in items:
            if item[0] == 'separator':
                self.pack_start(Gtk.HSeparator(), False, False, 6)
            else:
                if item[0].startswith('float-'):
                    adjustment = Gtk.Adjustment(0, 0, 2**16, 1, 10, 0)
                    entry = Gtk.SpinButton()
                    entry.set_adjustment(adjustment)
                    entry.set_digits(5)
                else:
                    entry = Gtk.Entry()
                box = Gtk.Box()
                label = Gtk.Label(item[1] + ':')
                label.set_width_chars(labelWidth)
                label.set_alignment(0, 0.5)
                self.fields[item[0]] = entry
                box.pack_start(label, False, False, 10)
                box.pack_start(self.fields[item[0]], True, True, 6)
            self.pack_start(box, False, True, 4)

    def print_data(self, event):
        for f in self.fields:
            print f, ':', self.fields[f].get_text()
        print '-' * 80

if __name__ == '__main__':
    win = Gtk.Window(title='Form test')
    win.set_default_size(500, 300)
    b = Gtk.Box()
    form = Form(
                  (
                     ('database-no', 'Database Number'),
                     ('date', 'Date'),
                     ('time', 'Time'),
                     ('float-lat', 'Latitude (N/S)'),
                     ('float-lon', 'Longitude (E/W)'),
                     ('grid', 'Grid Reference'),
                     ('group', 'Sub Group'),
                     ('series', 'Series'),
                     ('landform', 'Landform'),

                     ('separator', ''),

                     ('slope-pos', 'Slope Position'),
                     ('sl-deg', 'Sl deg'),
                     ('aspect', 'Aspect')
                  )
               )

    form2 = Form(
                  (
                     ('date', 'Date'),
                     ('time', 'Time'),
                     ('grid', 'Grid Reference'),
                     ('series', 'Series'),
                     ('lat', 'Latitude (N/S)'),
                     ('lon', 'Longitude (E/W)'),
                     ('group', 'Sub Group'),
                     ('sl-deg', 'Sl deg'),
                     ('landform', 'Landform'),

                     ('separator', ''),

                     ('database-no', 'Database Number'),
                     ('slope-pos', 'Slope Position'),
                     ('aspect', 'Aspect')
                  )
               )

    #b.pack_start(form, True, True, 10)

    hb = Gtk.Box()

    hb.pack_start(form, True, True, 10)
    hb.pack_start(form2, True, True, 10)

    scroll = Gtk.ScrolledWindow()
    scroll.add(hb)
    box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
    box.pack_start(scroll, True, True, 20)

    b = Gtk.Button(label='Show data')
    b.connect('clicked', form.print_data)
    box.pack_start(b, False, True, 6)
    win.add(box)
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()

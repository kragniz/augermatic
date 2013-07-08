#!/usr/bin/env python
from gi.repository import Gtk

class Form(Gtk.VBox):
    def __init__(self, items):
        Gtk.VBox.__init__(self, spacing=6)
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
                elif item[0].startswith('date-'):
                    entry = DateBox()
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

    def get_fields(self, *args):
        self.set_editable(False)
        return {f:self.fields[f].get_text() for f in self.fields}

    def set_editable(self, value):
        for f in self.fields:
            field = self.fields[f]
            field.set_sensitive(value)

class DateBox(Gtk.Box):
    class CalendarPopup(Gtk.Window):
        def __init__(self, x=0, y=0):
            Gtk.Window.__init__(self, type=Gtk.WindowType.POPUP)
            self.move(x, y)
            self.cal = Gtk.Calendar()
            event = Gtk.EventBox()
            self.add(event)

            box = Gtk.VBox()
            event.add(box)
            box.pack_start(self.cal, False, False, 6)

            hbox = Gtk.Box()
            box.pack_start(hbox, True, True, 6)
            self.okbutton = Gtk.Button(stock=Gtk.STOCK_OK)
            hbox.pack_end(self.okbutton, False, False, 6)
            self.show_all()
            self.hide()
 
    def __init__(self):
        Gtk.Box.__init__(self)
        self.popup = self.CalendarPopup()
        self.popup.connect('leave-notify-event', self.leave_popup)
        self.popup.cal.connect('day-selected-double-click', self.selected_date)
        self.popup.okbutton.connect('clicked', self.selected_date)
        self.dateButton = Gtk.ToggleButton(label="Choose date")
        self.dateButton.connect('clicked', self.open_popup)
        self.pack_end(self.dateButton, False, False, 6)

        self.textbox = Gtk.Entry()
        self.pack_start(self.textbox, True, True, 0)
        self._popupOpen = False

    def open_popup(self, event):
        if not self._popupOpen:
            windowPos = self.dateButton.get_window().get_origin()[1:]
            allocation = self.dateButton.get_allocation()
            pos = (
                    allocation.x + windowPos[0],
                    allocation.y + allocation.height + windowPos[1]
                  )
            self.popup.move(*pos)
            self.popup.show()
            self._popupOpen = True
        else:
            self.leave_popup()

    def leave_popup(self, *args):
        self.popup.hide()
        #hack to stop the toggle events being fired whenever the mouse leaves
        self.dateButton.handler_block_by_func(self.open_popup)
        self.dateButton.set_active(False)
        self.dateButton.handler_unblock_by_func(self.open_popup)
        self._popupOpen = False

    def selected_date(self, event):
        date = self.popup.cal.get_date()
        self.textbox.set_text('-'.join([str(v) for v in date]))
        self.popup.hide()
        self.dateButton.set_active(False)

    def get_text(self):
        return self.textbox.get_text()

    def set_sensitive(self, value):
        self.textbox.set_sensitive(value)
        self.dateButton.set_sensitive(value)

if __name__ == '__main__':
    win = Gtk.Window(title='Form test')
    win.set_default_size(500, 300)
    b = Gtk.Box()
    form = Form(
                  (
                     ('database-no', 'Database Number'),
                     ('date-sample', 'Date'),
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
    box = Gtk.VBox()
    box.pack_start(scroll, True, True, 20)

    b = Gtk.Button(label='Show data')
    b.connect('clicked', form.get_fields)
    box.pack_start(b, False, True, 6)
    win.add(box)
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()

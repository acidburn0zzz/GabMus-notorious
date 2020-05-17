from gettext import gettext as _
from gi.repository import Gtk, Gdk, Pango
from os import remove
from notorious.confManager import ConfManager


class FileListboxRow(Gtk.ListBoxRow):
    def __init__(self, name, file_path, search_entry, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.confman = ConfManager()

        self.name = name
        self.file_path = file_path
        self.search_entry = search_entry

        self.name_label = Gtk.Label(self.name)
        self.name_label.set_hexpand(False)
        self.name_label.set_halign(Gtk.Align.START)
        self.name_label.set_margin_top(6)
        self.name_label.set_margin_bottom(6)
        self.name_label.set_margin_start(12)
        self.name_label.set_margin_end(12)
        self.name_label.set_ellipsize(
            Pango.EllipsizeMode.END
        )
        self.add(self.name_label)
        self.connect(
            'key-press-event',
            self.on_key_press_event
        )

    def on_key_press_event(self, widget, event):
        if event.keyval in (Gdk.KEY_Delete, Gdk.KEY_BackSpace):
            dialog = Gtk.MessageDialog(
                self.get_toplevel(),
                Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                Gtk.MessageType.QUESTION,
                Gtk.ButtonsType.YES_NO,
                _(
                    'Delete note `{0}`?'
                ).format(
                    self.name
                )
            )
            if dialog.run() == Gtk.ResponseType.YES:
                remove(self.file_path)
                self.confman.emit('notes_dir_changed', '')
            dialog.close()
        elif event.keyval == Gdk.KEY_Escape:
            self.search_entry.grab_focus()

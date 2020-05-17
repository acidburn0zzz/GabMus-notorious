from gi.repository import Gtk, Pango


class FileListboxRow(Gtk.ListBoxRow):
    def __init__(self, name, file_path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = name
        self.file_path = file_path

        self.name_label = Gtk.Label(self.name)
        self.name_label.set_hexpand(False)
        self.name_label.set_halign(Gtk.Align.START)
        self.name_label.set_margin_top(3)
        self.name_label.set_margin_bottom(3)
        self.name_label.set_margin_start(3)
        self.name_label.set_margin_end(3)
        self.name_label.set_ellipsize(
            Pango.EllipsizeMode.END
        )
        self.add(self.name_label)

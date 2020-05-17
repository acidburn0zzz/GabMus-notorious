from gi.repository import Gtk
from notorious.confManager import ConfManager
from notorious.headerbar import GHeaderbar
from notorious.main_ui import NotoriousUI


class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.confman = ConfManager()

        self.set_title('Notorious')
        self.set_icon_name('org.gabmus.notorious')

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.headerbar = GHeaderbar()
        self.set_titlebar(self.headerbar)

        self.main_ui = NotoriousUI(self.headerbar.search_entry)
        self.main_box.pack_start(self.main_ui, True, True, 0)

        self.add(self.main_box)

        # Why this -52?
        # because every time a new value is saved, for some reason
        # it's the actual value +52 out of nowhere
        # this makes the window ACTUALLY preserve its old size
        self.resize(
            self.confman.conf['windowsize']['width']-52,
            self.confman.conf['windowsize']['height']-52
        )
        self.size_allocation = self.get_allocation()
        self.connect('size-allocate', self.update_size_allocation)

        # accel_group is for keyboard shortcuts
        self.accel_group = Gtk.AccelGroup()
        self.add_accel_group(self.accel_group)
        shortcuts_l = [
            {
                'combo': 'F10',
                'cb': lambda *args: (
                    self.headerbar.menu_popover.popup
                    if not self.headerbar.menu_popover.is_visible()
                    else self.headerbar.menu_popover.popdown
                )()
            }
        ]
        for s in shortcuts_l:
            self.add_accelerator(s['combo'], s['cb'])

    def add_accelerator(self, shortcut, callback):
        if shortcut:
            key, mod = Gtk.accelerator_parse(shortcut)
            self.accel_group.connect(
                key, mod, Gtk.AccelFlags.VISIBLE, callback
            )

    def emit_destroy(self, *args):
        self.emit('destroy')

    def on_destroy(self, *args):
        self.main_ui.file_manager.save_current_file()
        self.confman.conf['windowsize'] = {
            'width': self.size_allocation.width,
            'height': self.size_allocation.height
        }
        self.confman.save_conf()

    def update_size_allocation(self, *args):
        self.size_allocation = self.get_allocation()

    def do_startup(self):
        pass

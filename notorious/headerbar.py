# from gettext import gettext as _
from gi.repository import Gtk, GObject, Handy
from notorious.confManager import ConfManager


class GHeaderbar(Handy.TitleBar):
    __gsignals__ = {
        'headerbar_squeeze': (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (bool,)
        )
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.builder = Gtk.Builder.new_from_resource(
            '/org/gabmus/notorious/ui/headerbar.glade'
        )
        self.builder.connect_signals(self)
        self.confman = ConfManager()
        self.headerbar = self.builder.get_object('headerbar')
        self.search_entry = self.builder.get_object('search_entry')

        self.add(self.headerbar)
        self.menu_btn = self.builder.get_object(
            'menu_btn'
        )
        self.menu_popover = Gtk.PopoverMenu()
        self.menu_builder = Gtk.Builder.new_from_resource(
            '/org/gabmus/notorious/ui/menu.xml'
        )
        self.menu = self.menu_builder.get_object('generalMenu')
        self.menu_popover.bind_model(self.menu)
        self.menu_popover.set_relative_to(self.menu_btn)
        self.menu_popover.set_modal(True)
        self.set_headerbar_controls()

    def set_headerbar_controls(self, *args):
        self.headerbar.set_show_close_button(True)
        # self.headerbar.set_title('Notorious')

    def on_menu_btn_clicked(self, *args):
        self.menu_popover.popup()

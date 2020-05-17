from gi.repository import Gtk, GtkSource
from notorious.file_manager import FileManager
from notorious.confManager import ConfManager


class NotoriousUI(Gtk.Bin):
    def __init__(self, search_entry, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.confman = ConfManager()
        self.builder = Gtk.Builder.new_from_resource(
            '/org/gabmus/notorious/ui/main_ui.glade'
        )
        self.ui_box = self.builder.get_object('ui_box')
        self.add(self.ui_box)

        self.search_entry = search_entry
        self.results_listbox = self.builder.get_object(
            'search_results_listbox'
        )

        self.source_style_scheme_manager = \
            GtkSource.StyleSchemeManager.get_default()
        self.source_language_manager = GtkSource.LanguageManager.get_default()
        self.source_lang_markdown = self.source_language_manager.get_language(
            'markdown'
        )
        # TODO: change color scheme depending on dark mode preference
        self.style_builder_dark = self.source_style_scheme_manager.get_scheme(
            'builder-dark'
        )
        self.source_buffer = GtkSource.Buffer()
        self.source_buffer.set_style_scheme(
            self.style_builder_dark
        )
        self.source_buffer.set_language(self.source_lang_markdown)
        self.on_enable_syntax_highlighting_changed()
        self.confman.connect(
            'markdown_syntax_highlighting_changed',
            self.on_enable_syntax_highlighting_changed
        )
        self.source_view = GtkSource.View.new_with_buffer(self.source_buffer)
        self.source_view.set_monospace(True)
        self.source_view.set_auto_indent(True)
        self.source_view.set_indent_on_tab(True)
        self.source_view.set_insert_spaces_instead_of_tabs(True)
        self.source_view.set_indent_width(4)
        self.source_view.set_tab_width(8)
        self.source_view.set_smart_backspace(True)
        # self.source_view.set_smart_home_end(GtkSource.SmartHomeEndType.ALWAYS)
        self.source_view.set_highlight_current_line(True)
        self.source_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.builder.get_object('source_view_box').add(
            self.source_view
        )

        self.file_manager = FileManager(
            self.search_entry, self.results_listbox, self.source_buffer
        )

    def on_enable_syntax_highlighting_changed(self, *args):
        self.source_buffer.set_highlight_syntax(
            self.confman.conf['show_markdown_syntax_highlighting']
        )

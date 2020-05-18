from gi.repository import Gdk, GLib
from notorious.confManager import ConfManager
from notorious.files_listbox_row import FileListboxRow
from os import listdir
from os.path import isfile


class FileManager:
    def __init__(self, search_entry, results_listbox,
                 source_buffer, source_view):
        self.currently_open_file = None
        self.search_entry = search_entry
        self.results_listbox = results_listbox
        self.source_buffer = source_buffer
        self.source_view = source_view
        self.confman = ConfManager()
        self.confman.connect(
            'sorting_method_changed',
            self.on_sorting_method_changed
        )
        self.on_sorting_method_changed()
        self.results_listbox.set_filter_func(
            self.results_filter_func, None, False
        )
        self.results_listbox.connect(
            'row_activated',
            self.on_results_listbox_row_activated
        )

        self.search_entry.connect('changed', self.on_search_changed)
        # activate called on Enter pressed
        self.search_entry.connect(
            'activate',
            self.on_search_entry_activate
        )
        self.search_entry.connect(
            'key-press-event',
            self.on_search_entry_key_press_event
        )
        self.confman.connect(
            'notes_dir_changed',
            self.populate_listbox
        )
        self.populate_listbox()

    def on_sorting_method_changed(self, *args):
        self.results_listbox.set_sort_func(
            self.results_sort_func_by_name
            if self.confman.conf['sorting_method'] == 'name'
            else self.results_sort_func_by_last_modified,
            None, False
        )

    def results_sort_func_by_name(self, row1, row2, data, notify_destroy):
        return row1.name > row2.name

    def results_sort_func_by_last_modified(self, row1, row2, data,
                                           notify_destroy):
        return row1.last_modified < row2.last_modified

    def results_filter_func(self, row, data, notify_destroy):
        return self.search_entry.get_text().lower().strip() in row.name.lower()

    def populate_listbox(self, *args):
        while True:
            row = self.results_listbox.get_row_at_index(0)
            if row:
                self.results_listbox.remove(row)
            else:
                break
        for f in listdir(self.confman.conf['notes_dir']):
            file_path = '{0}/{1}'.format(
                self.confman.conf['notes_dir'], f
            )
            if isfile(file_path):
                self.results_listbox.add(
                    FileListboxRow(f, file_path, self.search_entry)
                )
        self.results_listbox.show_all()

    def on_search_changed(self, *args):
        self.results_listbox.invalidate_filter()

    def on_search_entry_activate(self, *args):
        entry_text = self.search_entry.get_text().strip()
        if not entry_text:
            return
        file_path = '{0}/{1}'.format(
            self.confman.conf['notes_dir'],
            entry_text
        )
        self.open_file(file_path)

    def on_search_entry_key_press_event(self, entry, event):
        row = None
        if event.keyval == Gdk.KEY_Down:
            self.results_listbox.set_sensitive(False)
            row = self.results_listbox.get_row_at_y(0)
        elif event.keyval == Gdk.KEY_Up:
            self.results_listbox.set_sensitive(False)
            row = self.results_listbox.get_row_at_y(
                len(self.results_listbox.get_children()) - 1
            )
        elif event.keyval == Gdk.KEY_Escape:
            # weird way to select all
            self.search_entry.grab_focus()
            return
        if row is not None:
            self.results_listbox.select_row(row)
            self.results_listbox.set_sensitive(True)
            GLib.idle_add(lambda *args: row.grab_focus())

    def on_results_listbox_row_activated(self, listbox, row):
        if not row:
            return
        self.open_file(row.file_path)

    def save_current_file(self):
        if (
                self.currently_open_file is not None and
                isfile(self.currently_open_file)
        ):
            text_to_save = self.source_buffer.get_text(
                self.source_buffer.get_start_iter(),
                self.source_buffer.get_end_iter(),
                True
            )
            with open(self.currently_open_file, 'r') as fd:
                if fd.read() == text_to_save:
                    return
            with open(self.currently_open_file, 'w') as fd:
                fd.write(text_to_save)

    def open_file(self, file_path):
        self.save_current_file()
        self.currently_open_file = file_path
        if isfile(file_path):
            with open(file_path, 'r') as fd:
                self.source_buffer.set_text(fd.read())
        else:
            with open(file_path, 'w') as fd:
                fd.write('')
            self.populate_listbox()
            self.source_buffer.set_text('')
        self.source_view.grab_focus()

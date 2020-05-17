from notorious.confManager import ConfManager
from notorious.files_listbox_row import FileListboxRow
from os import listdir
from os.path import isfile


class FileManager:
    def __init__(self, search_entry, results_listbox, source_buffer):
        self.currently_open_file = None
        self.search_entry = search_entry
        self.results_listbox = results_listbox
        self.source_buffer = source_buffer
        self.confman = ConfManager()
        self.results_listbox.set_sort_func(
            self.results_sort_func, None, False
        )
        self.results_listbox.set_filter_func(
            self.results_filter_func, None, False
        )
        self.results_listbox.connect(
            'row_activated',
            self.on_results_listbox_row_activated
        )

        self.search_entry.connect('changed', self.on_search_changed)
        self.populate_listbox()

    def results_sort_func(self, row1, row2, data, notify_destroy):
        return row1.name > row2.name

    def results_filter_func(self, row, data, notify_destroy):
        return self.search_entry.get_text().lower() in row.name.lower()

    def populate_listbox(self):
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
                    FileListboxRow(f, file_path)
                )
        self.results_listbox.show_all()

    def on_search_changed(self, *args):
        self.results_listbox.invalidate_filter()

    def on_results_listbox_row_activated(self, listbox, row):
        if not row:
            return
        if (
                self.currently_open_file is not None and
                isfile(self.currently_open_file)
        ):
            with open(self.currently_open_file, 'w') as fd:
                fd.write(
                    self.source_buffer.get_text(
                        self.source_buffer.get_start_iter(),
                        self.source_buffer.get_end_iter(),
                        True
                    )
                )
        self.currently_open_file = row.file_path
        with open(row.file_path, 'r') as fd:
            self.source_buffer.set_text(fd.read())

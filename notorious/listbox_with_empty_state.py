from gi.repository import Gtk


class ListBoxWithEmptyState(Gtk.Stack):
    def __init__(self, icon_name, label, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_transition_type(
            Gtk.StackTransitionType.CROSSFADE
        )
        self.builder = Gtk.Builder.new_from_resource(
            '/org/gabmus/notorious/ui/listbox_with_empty_state.glade'
        )

        self.listbox_container = self.builder.get_object('listbox_container')
        self.listbox = self.builder.get_object('listbox')

        self.stack_add = super().add
        self.stack_remove = super().remove

        self.set_selection_mode = self.listbox.set_selection_mode
        self.set_header_func = self.listbox.set_header_func
        self.set_sort_func = self.listbox.set_sort_func
        self.get_row_at_index = self.listbox.get_row_at_index

        self.empty_state_img = self.builder.get_object('empty_state_img')
        self.empty_state_img.set_from_icon_name(
            icon_name, Gtk.IconSize.DIALOG
        )
        self.empty_state_label = self.builder.get_object('empty_state_label')
        self.empty_state_label.set_text(label)
        self.empty_state_container = self.builder.get_object(
            'empty_state_container'
        )
        self.stack_add(self.listbox_container)
        self.stack_add(self.empty_state_container)

    def set_show_empty_state(self, state):
        self.set_visible_child(
            self.empty_state_container if state else self.listbox_container
        )

    def empty(self, hide=True):
        hide and self.set_show_empty_state(True)
        while True:
            row = self.listbox.get_row_at_index(0)
            if row:
                self.listbox.remove(row)
            else:
                break

    def add(self, *args, **kwargs):
        self.set_show_empty_state(False)
        self.listbox.add(*args, **kwargs)
        self.listbox.show_all()

    def remove(self, *args, **kwargs):
        self.listbox.remove(*args, **kwargs)
        if len(self.listbox.get_children()) <= 0:
            self.set_show_empty_state(True)

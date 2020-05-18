from gettext import gettext as _
from pathlib import Path
from os.path import isfile, isdir
# from os import makedirs
from os import environ as Env
from os import system, makedirs
import json
from gi.repository import GObject, GLib
from notorious.singleton import Singleton

documents_dir = GLib.get_user_special_dir(
    GLib.UserDirectory.DIRECTORY_DOCUMENTS
)
if not documents_dir:
    system('xdg-user-dirs-update')
    documents_dir = GLib.get_user_special_dir(
        GLib.UserDirectory.DIRECTORY_DOCUMENTS
    )
    if not documents_dir:
        documents_dir = f'{Env.get("HOME")}/Documents'


class ConfManagerSignaler(GObject.Object):

    __gsignals__ = {
        'notes_dir_changed': (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str,)
        ),
        'markdown_syntax_highlighting_changed': (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str,)
        ),
        'dark_mode_changed': (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str,)
        ),
        'sorting_method_changed': (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str,)
        ),
    }


class ConfManager(metaclass=Singleton):

    BASE_SCHEMA = {
        'windowsize': {
            'width': 350,
            'height': 650
        },
        'notes_dir': '{0}/{1}'.format(documents_dir, _('Notes')),
        # 'max_search_results': 5,
        'show_markdown_syntax_highlighting': False,
        'dark_mode': False,
        'sorting_method': 'name'
    }

    def __init__(self):
        self.window = None
        self.signaler = ConfManagerSignaler()
        self.emit = self.signaler.emit
        self.connect = self.signaler.connect

        # check if inside flatpak sandbox
        self.is_flatpak = (
            'XDG_RUNTIME_DIR' in Env.keys() and
            isfile(f'{Env["XDG_RUNTIME_DIR"]}/flatpak-info')
        )

        if self.is_flatpak:
            self.path = Path(
                f'{Env.get("XDG_CONFIG_HOME")}/org.gabmus.notorious.json'
            )
        else:
            self.path = Path(
                f'{Env.get("HOME")}/.config/org.gabmus.notorious.json'
            )

        self.conf = None
        if isfile(str(self.path)):
            try:
                with open(str(self.path)) as fd:
                    self.conf = json.loads(fd.read())
                # verify that the file has all of the schema keys
                for k in ConfManager.BASE_SCHEMA:
                    if k not in self.conf.keys():
                        if isinstance(
                                ConfManager.BASE_SCHEMA[k], (list, dict)
                        ):
                            self.conf[k] = ConfManager.BASE_SCHEMA[k].copy()
                        else:
                            self.conf[k] = ConfManager.BASE_SCHEMA[k]
            except Exception:
                self.conf = ConfManager.BASE_SCHEMA.copy()
                self.save_conf()
        else:
            self.conf = ConfManager.BASE_SCHEMA.copy()
            self.save_conf()

        if not isdir(self.conf['notes_dir']):
            makedirs(self.conf['notes_dir'])

    def save_conf(self, *args):
        with open(str(self.path), 'w') as fd:
            fd.write(json.dumps(self.conf))

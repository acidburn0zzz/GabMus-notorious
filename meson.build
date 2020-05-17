project('notorious',
    version: '0.1',
    meson_version: '>= 0.50.0',
    license: 'GPL3'
)

description = 'Keyboard centric notes'
prettyname = 'Notorious'
prettylicense = 'GPL-3.0+'

author = 'gabmus'
authorfullname = 'Gabriele Musco'
authoremail = 'gabmus@disroot.org'
domain = 'org'
# app_id built as: domain.author.project_name
gitrepo = 'https://gitlab.com/'+author+'/'+meson.project_name()
website = 'http://'+meson.project_name()+'.'+author+'.org'

# NOTE: if you contributed, feel free to add your name and email address here
contributors = '\n'.join([
    'Gabriele Musco (GabMus) &lt;gabmus@disroot.org&gt;'
])

translators = '\n'.join([
    'Italian: Gabriele Musco (GabMus) &lt;gabmus@disroot.org&gt;'
])

designers = '\n'.join([
    'Icon, UI: Gabriele Musco (GabMus) &lt;gabmus@disroot.org&gt;'
])

i18n = import('i18n')
python = import('python3')
gnome = import('gnome')
prefix = get_option('prefix') # should be /usr
bindir = get_option('bindir') # should be bin
datadir = get_option('datadir') # should be /usr/share
pkgdatadir = join_paths(prefix, datadir, meson.project_name())
pythondir = join_paths(prefix, python.sysconfig_path('purelib'))
localedir = join_paths(prefix, get_option('localedir'))

install_subdir('notorious', install_dir: pythondir)
subdir('data')
subdir('bin')
subdir('po')

meson.add_install_script('meson_post_install.py')

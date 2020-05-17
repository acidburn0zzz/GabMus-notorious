# <a href="https://gabmus.gitlab.io/notorious"><img height="32" src="data/icons/org.gabmus.notorious.svg" /> Notorious</a>

Keyboard centric notes

![screenshot](https://gitlab.gnome.org/GabMus/notorious/raw/website/website/screenshots/mainwindow.png)

## Notes on the distribution of this app

I decided to target flatpak mainly. It's just another package manager at the end of the day, but
it's supported by many Linux distributions. It bundles all of the dependencies you need in one
package.

This helps a lot in supporting many different distros because I know which version of which
dependency you have installed, so I don't have to mess with issues caused by version mismatches.
If you want to report an issue, feel free to. But please at least first see if this issue happens
with the flatpak version as well.

As for development it's a similar story. I do most of my testing directly inside a flatpak sandbox
and you should do the same. It's easy to set up, just open up this repo in GNOME Builder and press
the run button. It will handle the rest.

## Installing from Flathub

You can install Notorious via [Flatpak](https://flathub.org/apps/details/org.gabmus.notorious).

## Installing from AUR

Notorious is available as an AUR package: [`notorious-git`](https://aur.archlinux.org/packages/notorious-git/).

<!--
## Installing from Fedora

Notorious is available in [Fedora repos](https://apps.fedoraproject.org/packages/notorious): `sudo dnf install notorious`
-->

# Building on different distributions

**Note**: these are illustrative instructions. If you're a developer or a package maintainer, they
can be useful to you. If not, just install the flatpak.

## Building on Ubuntu/Debian

```bash
git clone https://gitlab.gnome.org/GabMus/notorious
cd notorious
mkdir build
cd build
meson ..
meson configure -Dprefix=$PWD/testdir # use this line if you want to avoid installing system wide
ninja
ninja install
```

## Building on Arch/Manjaro

```bash
sudo pacman -S python-gobject

git clone https://gitlab.gnome.org/GabMus/notorious
cd notorious
mkdir build
cd build
meson ..
meson configure -Dprefix=$PWD/testdir # use this line if you want to avoid installing system wide
ninja
ninja install
```

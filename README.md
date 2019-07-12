# Software Boutique for Ubuntu MATE

An easy-to-use software distribution program for Ubuntu MATE. The team curates
a selection of tried & tested applications that integrate well with the Ubuntu
MATE desktop.

Complimentary to the [Welcome program](https://github.com/ubuntu-mate/ubuntu-mate-welcome).

This repository is the WebKitGTK front-end to [python3-libboutique](https://github.com/ubuntu-mate/python3-libboutique).

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/software-boutique)


## Features

* Install or remove software that meets [Ubuntu MATE's Tried & Tested Guidelines](https://ubuntu-mate.org/get-involved/guidelines/).
* [Presents a curated collection](https://github.com/ubuntu-mate/software-boutique-curated-apps).
* Supports the following packaging backends to search and manage software:
  * **apt**
  * **snapd**
* One-click fixes for common software issues.

The project aims to be modular. For instance, the software will still function if
the curated collection was excluded, or one of the supported packaging backends were not present.


## Building

After cloning the repository locally, you must build some assets.

To compile the visual styles - these are required:

    ./scripts/build-css.sh

To include the curated index, you'll need to clone
[software-boutique-curated-apps](https://github.com/ubuntu-mate/software-boutique-curated-apps)
into an adjacent directory.

    ./scripts/build-index.sh

To generate locales:

    ./scripts/build-locale-folder.sh


## Translations

The software itself can be translated on Transifex (which is not set up yet)

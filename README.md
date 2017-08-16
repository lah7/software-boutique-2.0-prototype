# Software Boutique for Ubuntu MATE

An easy-to-use curvated software collection for Ubuntu MATE users.
Complimentary of the [Welcome program](https://github.com/ubuntu-mate/ubuntu-mate-welcome).


## Features

* Install or remove software in the collection or searching the Ubuntu archives.
* One-click fixes for common software issues.
* Apt and Snap support.
* Securely downloads [an index of curvated applications](https://github.com/ubuntu-mate/ubuntu-mate.software).


## Building

After cloning the repository locally, you must build some assets. Run

    software-boutique-dev --build-only

For testing and making changes to the index, clone [`ubuntu-mate.software`](https://github.com/ubuntu-mate/ubuntu-mate.software)
and run this script in the background of that repository:

    ../ubuntu-mate.software/scripts/test-locally.sh

Then pass the `--use-local-index` to `software-boutique` or `software-boutique-dev`. If needed, also pass `--clear-cache` and
re-build the index if you're testing changes.


## Translations

The software itself can be translated on Transifex (when it's set up)

For translating the index itself, please do this in the [index repository](https://github.com/ubuntu-mate/ubuntu-mate.software) instead.

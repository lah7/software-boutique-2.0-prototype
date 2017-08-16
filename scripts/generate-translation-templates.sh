#!/bin/bash

bin_check="$(which pygettext)"
if [ ! $? == 0 ]; then
    echo "Please install gettext"
    exit 1
fi

cd "$(dirname $0)/../"

# Create POT for Software Boutique
echo -e "Generating POT for software-boutique..."
pygettext -d software-boutique software-boutique
mv software-boutique.pot sources/locale/software-boutique.pot


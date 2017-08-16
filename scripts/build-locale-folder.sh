#!/bin/bash

bin_check="$(which msgfmt)"
if [ ! $? == 0 ]; then
    echo "Please install gettext"
    exit 1
fi

cd "$(dirname $0)/../"

# Create POT for Software Boutique
echo -e "Generating locales..."
if [ -d "locale/" ]; then
    rm -r locale/
fi
mkdir locale/

for po_path in $(ls sources/locale/*.po); do
    locale=$(basename "$po_path")
    locale="${locale%.*}"
    echo "$locale"
    target_folder=locale/$locale/LC_MESSAGES
    mkdir -p $target_folder
    msgfmt $po_path -o $target_folder/software-boutique.mo
done


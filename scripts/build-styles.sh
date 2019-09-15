#!/bin/bash

cd "$(dirname $0)/../"

# Find an implementation of SASS to use.
sassc=$(which sassc 2>/dev/null)
sass=$(which sass 2>/dev/null)

if [ -z "$sass" ] && [ -z "$sassc" ]; then
    echo "Please install a package that provides 'sassc' or 'sass' and try again."
    echo "Try: sassc (from your distro's repositories); sass (npm) or Dart SASS."
    exit 1
fi

if [ ! -z "$sassc" ]; then
    echo "Compiling styling... (sassc)"
    sassc src/sass/boutique.scss data/view/boutique.css --sass --style compressed

elif [ ! -z "$sass" ]; then
    echo "Compiling styling... (sass)"
    sass src/sass/boutique.scss data/view/boutique.css --style=compressed --no-source-map
fi

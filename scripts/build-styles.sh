#!/bin/bash

cd "$(dirname $0)/../"

# Is a SASS compiler installed?
cmd=$(which sass)
if [ -z "$cmd" ]; then
    echo "Please install a package that provides 'sass' and try again."
    echo "For example, ruby-sass, sass (npm), sassc or Dart SASS."
    exit 1
fi

echo "Compiling styling..."
sass src/sass/boutique.scss data/view/boutique.css --scss --style=compressed --sourcemap=none

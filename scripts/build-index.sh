#!/bin/bash
#
# Prepares the index for use with the application, requires the index repository to
# be cloned adjacent to the 'software-boutique' repository folder.
#
cd "$(dirname $0)/../"

SB_DIR="$(pwd)"
INDEX_DIR="$(realpath ../software-boutique-curated-index)"

if [ ! -d "$INDEX_DIR" ]; then
    echo -e "\nTo build the index here, run:"
    echo "  git clone https://github.com/ubuntu-mate/software-boutique-curated-apps.git ../software-boutique-curated-index"
    echo -e "\nThe build will continue without (re)building the index.\n"
    exit 0
fi

rm -rf "$SB_DIR/data/index"
mkdir "$SB_DIR/data/index"

cd "$INDEX_DIR"
echo "Compiling index..."
./scripts/build.sh
if [ $? != 0 ]; then
    echo "Index failed to build."
    exit 1
fi

cp -r dist/* "$SB_DIR/data/index/"

#!/bin/bash

bin_check="$(which json2po)"
if [ ! $? == 0 ]; then
    echo "Please install translate-toolkit"
    exit 1
fi

bin_check="$(which pygettext)"
if [ ! $? == 0 ]; then
    echo "Please install gettext"
    exit 1
fi

cd "$(dirname $0)/../"

# Create POT for Software Boutique
echo -e "\033[94mGenerating POT for software-boutique...\033[91m"
pygettext -d software-boutique software-boutique
mv software-boutique.pot sources/locale/software-boutique.pot

# Create POT files for each application
echo -e "\033[94mGenerating POTs for curated applications...\033[91m"
for category in $(ls sources/apps/); do
    for app in $(ls sources/apps/$category/); do
        source="sources/apps/$category/$app/"
        target="sources/locale-metadata/$app/"
        mkdir -p $target
        json2po $source/metadata.json -P $target/$app.pot --filter name,summary,description,developer-name --progress none
    done
done

# Delete obsolete app locales
echo -e "\033[94mDeleting any obsolete app locales...\033[93m"
for app in $(ls sources/locale-metadata/); do
    results=$(find sources/apps/ -name "$app" | wc -l)
    if [ $results -eq 0 ]; then
        echo " -- Removed '$app'."
        rm -r sources/locale-metadata/$app
    fi
done

# Reset pretty colours
echo -ne "\033[00m"

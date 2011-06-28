#!/bin/bash

# Copyright (c) by Patryk Jaworski <skorpion9312@gmail.com>

AUTHOR="Patryk Jaworski <skorpion9312@gmail.com>"

find . -name '*.py' > tmp-list
xgettext -F -f tmp-list -o po/music-organizer.pot --package-name "Music Organizer" --package-version "$(cat VERSION)" --msgid-bugs-address "$AUTHOR" --copyright-holder "$AUTHOR"
rm tmp-list

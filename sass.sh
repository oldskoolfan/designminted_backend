#!/usr/bin/env bash

cd /Users/andrew/PycharmProjects/dmblogapi

echo "compiling sass..."

if [ $1 == 'watch' ]; then
    sass --watch sass:blogweb/static/blogweb/css
else
    sass sass/app.sass blogweb/static/blogweb/css/app.css
fi

echo "...done!"
exit 0
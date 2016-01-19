#!/usr/bin/env bash

cd /Users/andrew/PycharmProjects/dmblogapi

echo "compiling sass..."

sass blogwebapp/static/blogwebapi/sass/main.sass blogwebapp/static/blogwebapi/css/styles.css

echo "...done!"
exit 0
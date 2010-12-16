#!/bin/bash

make html || exit 1
rsync -u -r -v -x build/html/ herbie.asidev.net:/var/www/project-docs/varnishpurge/ 

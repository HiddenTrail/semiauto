#!/bin/sh
timestamp=$(date +"%Y%m%d_%H%M%S")
robot --outputdir ./$timestamp $@
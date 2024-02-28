#!/bin/sh
timestamp=$(date +"%Y%m%d_%H%M%S")
robot -L trace --outputdir ./results_$timestamp $@
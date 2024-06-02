#!/bin/bash

for year in "2012" "2015" "2018"; do
    echo "$year"

    gdalwarp -tr 200 200 -r average -tap "/home/juju/geodata/forest/in/forest_TCD_"$year"_100.tif" /home/juju/geodata/forest/in/forest_TCD_"$year"_200.tif
    gdalwarp -tr 500 500 -r average -tap /home/juju/geodata/forest/in/forest_TCD_"$year"_100.tif /home/juju/geodata/forest/in/forest_TCD_"$year"_500.tif
    gdalwarp -tr 1000 1000 -r average -tap /home/juju/geodata/forest/in/forest_TCD_"$year"_100.tif /home/juju/geodata/forest/in/forest_TCD_"$year"_1000.tif
    gdalwarp -tr 2000 2000 -r average -tap /home/juju/geodata/forest/in/forest_TCD_"$year"_100.tif /home/juju/geodata/forest/in/forest_TCD_"$year"_2000.tif
    gdalwarp -tr 5000 5000 -r average -tap /home/juju/geodata/forest/in/forest_TCD_"$year"_100.tif /home/juju/geodata/forest/in/forest_TCD_"$year"_5000.tif
    gdalwarp -tr 10000 10000 -r average -tap /home/juju/geodata/forest/in/forest_TCD_"$year"_100.tif /home/juju/geodata/forest/in/forest_TCD_"$year"_10000.tif
    gdalwarp -tr 20000 20000 -r average -tap /home/juju/geodata/forest/in/forest_TCD_"$year"_100.tif /home/juju/geodata/forest/in/forest_TCD_"$year"_20000.tif
    gdalwarp -tr 50000 50000 -r average -tap /home/juju/geodata/forest/in/forest_TCD_"$year"_100.tif /home/juju/geodata/forest/in/forest_TCD_"$year"_50000.tif

    gdalwarp -tr 200 200 -r mode -tap "/home/juju/geodata/forest/in/forest_DLT_"$year"_100.tif" /home/juju/geodata/forest/in/forest_DLT_"$year"_200.tif
    gdalwarp -tr 500 500 -r mode -tap /home/juju/geodata/forest/in/forest_DLT_"$year"_100.tif /home/juju/geodata/forest/in/forest_DLT_"$year"_500.tif
    gdalwarp -tr 1000 1000 -r mode -tap /home/juju/geodata/forest/in/forest_DLT_"$year"_100.tif /home/juju/geodata/forest/in/forest_DLT_"$year"_1000.tif
    gdalwarp -tr 2000 2000 -r mode -tap /home/juju/geodata/forest/in/forest_DLT_"$year"_100.tif /home/juju/geodata/forest/in/forest_DLT_"$year"_2000.tif
    gdalwarp -tr 5000 5000 -r mode -tap /home/juju/geodata/forest/in/forest_DLT_"$year"_100.tif /home/juju/geodata/forest/in/forest_DLT_"$year"_5000.tif
    gdalwarp -tr 10000 10000 -r mode -tap /home/juju/geodata/forest/in/forest_DLT_"$year"_100.tif /home/juju/geodata/forest/in/forest_DLT_"$year"_10000.tif
    gdalwarp -tr 20000 20000 -r mode -tap /home/juju/geodata/forest/in/forest_DLT_"$year"_100.tif /home/juju/geodata/forest/in/forest_DLT_"$year"_20000.tif
    gdalwarp -tr 50000 50000 -r mode -tap /home/juju/geodata/forest/in/forest_DLT_"$year"_100.tif /home/juju/geodata/forest/in/forest_DLT_"$year"_50000.tif

done

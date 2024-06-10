#!/bin/bash

for year in "2012" "2015" "2018"; do
    for res in "200" "500" "1000" "2000" "5000" "10000" "20000" "50000"; do
        echo "$year" "$res"

        gdalwarp -tr $res $res -r average -tap "/home/juju/geodata/forest/in/forest_TCD_"$year"_100.tif" /home/juju/geodata/forest/in/forest_TCD_"$year"_"$res".tif
        gdalwarp -tr $res $res -r mode -tap "/home/juju/geodata/forest/in/forest_DLT_"$year"_100.tif" /home/juju/geodata/forest/in/forest_DLT_"$year"_"$res".tif
done

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
.. _gridtiler_raster

.. Links
.. _Eurostat: http://ec.europa.eu/eurostat/web/main
.. |Eurostat| replace:: `Eurostat <Eurostat_>`_

Tile gridded data from raster files for visualisation with GridViz javascript library.

**Dependencies**

*require*:      :mod:`os`, :mod:`csv`, :mod:`math`, :mod:`json`, :mod:`rasterio`, :mod:`rasterio.transform `, :mod:`panda`

**Contents**
"""

# *credits*:      `jgaffuri <julien.gaffuri@ec.europa.eu>`_ 
# *since*:        May 2024

#%% Settings     


import rasterio
from math import ceil,floor
import os
import csv
import json
import pandas as pd
import concurrent.futures
import numpy as np
from datetime import datetime



def tiling_raster_fast(rasters, output_folder, crs="", tile_size_cell=128, format="csv", parquet_compression="snappy", num_processors_to_use=1):
    """Tile gridded statistics from raster files.

    Args:
        rasters (dict): A dictionnary with all data on the attributes and the raster file they are retrieved from.
        output_folder (str): The path to the output folder where to store the tiles.
        crs (str, optional): A text describing the grid CRS. Defaults to "".
        tile_size_cell (int, optional): The size of a tile, in number of cells. Defaults to 128.
        format (str, optional): The output file encodings format, either "csv" of "parquet". Defaults to "csv".
        parquet_compression (str, optional): The parquet compression. Be aware gridviz-parquet supports only snappy encodings, currently. Defaults to "snappy".

    Returns:
        _type_: _description_
    """

    #prepare and load raster file data
    resolution = None
    bounds = None
    width = None
    heigth = None
    for label in rasters:
        raster = rasters[label]
        #open file
        src = rasterio.open(raster["file"])

        if resolution==None: resolution = src.res[0]
        if bounds==None: bounds = src.bounds
        if width==None: width = src.width
        if heigth==None: heigth = src.width

        raster["src"] = src
        raster["nodata"] = src.meta["nodata"]
        raster["data"] = src.read(raster["band"])
        if not "no_data_values" in raster: raster["no_data_values"] = []

    x_min, y_min, x_max, y_max = bounds.left, bounds.bottom, bounds.right, bounds.top

    #tile frame caracteristics
    tile_size_geo = resolution * tile_size_cell
    tile_min_x = 0 #floor( (x_min - x_origin) / tile_size_geo )
    tile_min_y = 0 #floor( (y_min - y_origin) / tile_size_geo )
    tile_max_x = floor( (x_max - x_min) / tile_size_geo )
    tile_max_y = floor( (y_max - y_min) / tile_size_geo )

    #get keys
    keys = rasters.keys()

    #function to make cell template
    def build_cell(x,y):
        c = { "x":x, "y":y }
        for k in keys: c[k] = None
        return c

    #function to make a tile
    def make_tile(xyt):
        [xt, yt] = xyt
        print(datetime.now(), "tile", xt, yt)

        #prepare tile cells
        cells_index = {}

        #prepare raster data query window
        min_col = xt * tile_size_cell
        min_row = width - 1 - yt * tile_size_cell - tile_size_cell
        window = rasterio.windows.Window(min_col, min_row, tile_size_cell, tile_size_cell)

        print(min_col, min_row)


        for key in []: #keys:

            raster = rasters[key]
            src = raster["src"]
            data = src.read(1, window=window)

            for col in range(0, tile_size_cell):
                for row in range(0, tile_size_cell):

                    #get value
                    value = data[col,row]

                    #if no value, skip
                    if value == raster["nodata"] or value in raster["no_data_values"]: continue

                    #get cell from index. if it does not exists, create it
                    if col in cells_index: col_ = cells_index[col]
                    else: col_ = {}; cells_index[col] = col_
                    if row in col_: cell = col_[row]
                    else: cell = build_cell(col, tile_size_cell-row-1); col_[row] = cell

                    #set cell value
                    cell[key] = value

        #get cells as a list
        cells = [cell for col in cells_index.values() for cell in col.values()]
        del cells_index

        #if no cell within tile, skip
        if len(cells) == 0: return

        print(len(cells), "cells")

        #remove column with all values null
        #check columns
        for key in keys:
            #check if cells all have key as column
            toRemove = True
            for c in cells:
                if c[key]==None: continue
                toRemove = False
                break
            #remove column
            if toRemove:
                for c in cells: del c[key]

        #make csv header, ensuring x and y are first columns
        headers = list(cells[0].keys())
        headers.remove("x")
        headers.remove("y")
        headers.insert(0, "x")
        headers.insert(1, "y")

        #create output folder, if it does not already exists
        fo = output_folder + "/" + str(xt) + "/"
        if not os.path.exists(fo): os.makedirs(fo)

        #save as CSV file
        cfp = fo + str(yt) + ".csv"
        with open(cfp, 'w', newline='') as csv_file:
            #get writer
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            #write the header
            writer.writeheader()

            #write the cell rows
            for c in cells:
                writer.writerow(c)

        if format == "csv": return

        #csv to parquet

        #load csv file            
        df = pd.read_csv(cfp)
        #save as parquet            
        df.to_parquet(fo + str(yt) + ".parquet", engine='pyarrow', compression=parquet_compression, index=False)
        #delete csv file
        os.remove(cfp)

        return xyt







    #make list of tiles x,y
    pairs = []
    for xt in range(tile_min_x, tile_max_x+1):
        for yt in range(tile_min_y, tile_max_y+1):
            pairs.append([xt, yt])

    #make tiles, in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_processors_to_use) as executor:
        { executor.submit(make_tile, tile): tile for tile in pairs }

    #write info.json
    data = {
        "dims": [],
        "crs": crs,
        "tileSizeCell": tile_size_cell,
        "originPoint": {
            "x": x_min,
            "y": y_min
        },
        "resolutionGeo": resolution,
        "tilingBounds": {
            "xMin": 0,
            "yMin": 0,
            "xMax": tile_max_x,
            "yMax": tile_max_y
        }
    }

    if not os.path.exists(output_folder): os.makedirs(output_folder)

    with open(output_folder + '/info.json', 'w') as json_file:
        json.dump(data, json_file, indent=3)


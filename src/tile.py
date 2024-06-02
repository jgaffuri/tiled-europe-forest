from pygridmap import gridtiler_raster

input_data_folder = "/home/juju/geodata/forest/in/"

print("start")
for res in [50000, 20000, 10000, 5000, 2000, 1000, 500, 200, 100]:
    print(res)

    gridtiler_raster.tiling_raster(
        {
        "tcd_2012":{"file":input_data_folder+'forest_TCD_2012_'+str(res)+'.tif', "band":1, 'no_data_values':[255,254,0]},
        "tcd_2015":{"file":input_data_folder+'forest_TCD_2015_'+str(res)+'.tif', "band":1, 'no_data_values':[255,254,0]},
        "tcd_2018":{"file":input_data_folder+'forest_TCD_2018_'+str(res)+'.tif', "band":1, 'no_data_values':[255,254,0]},
        "dlt_2012":{"file":input_data_folder+'forest_DLT_2012_'+str(res)+'.tif', "band":1, 'no_data_values':[255,254,0]},
        "dlt_2015":{"file":input_data_folder+'forest_DLT_2015_'+str(res)+'.tif', "band":1, 'no_data_values':[255,254,0]},
        "dlt_2018":{"file":input_data_folder+'forest_DLT_2018_'+str(res)+'.tif', "band":1, 'no_data_values':[255,254,0]}
    },
    "../pub/parquet/"+str(res)+"/",
    res,
    900000,
    900000,
    7400000,
    5500000,
    tile_size_cell=256,
    format="parquet"
    )

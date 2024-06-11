import rasterio
import numpy as np
from scipy.ndimage import maximum_filter, binary_dilation



# Function to expand the 255 values to their 8 neighbors
def expand_255(data):
    # Create a mask of where the 255 values are
    mask = data == 255

    # Use maximum filter to expand the mask to 8 neighbors
    #expanded_mask = maximum_filter(mask, footprint=np.ones((3, 3)))
    # Set the values to 255 where the expanded mask is True
    #data[expanded_mask] = 255

    # Use binary dilation with a cross-shaped structuring element to expand the mask to 4 direct neighbors
    structuring_element = np.array([[0, 1, 0],
                                    [1, 1, 1],
                                    [0, 1, 0]])
    expanded_mask = binary_dilation(mask, structure=structuring_element)
    # Set the values to 255 where the expanded mask is True
    data[expanded_mask] = 255

    return data



def process(input_file, output_file):
    # Open the input GeoTIFF file
    with rasterio.open(input_file) as src:
        # Read the entire raster into a numpy array
        data = src.read(1)
        
        # Modify the pixel values: set all values > 100 to 255
        data[data > 100] = 255

        # Expand 255 values to their 8 neighbors
        data = expand_255(data)

        # Change 255 to 0
        data[data > 100] = 0

        # Update the metadata to be the same as the source, but update the dtype if necessary
        profile = src.profile
        profile.update(dtype=rasterio.uint8)  # Ensure the data type matches the new values

        # Write the modified data to a new GeoTIFF file
        with rasterio.open(output_file, 'w', **profile) as dst:
            dst.write(data, 1)



for type in ["TCD", "DLT"]:
    for year in [2012,2015,2018]:
        year = str(year)

        print(type, year)
        process('/home/juju/geodata/forest/forest_'+type+'_'+year+'_100_.tif', '/home/juju/geodata/forest/forest_'+type+'_'+year+'_100.tif')

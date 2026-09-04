import xarray as xr

file_path = (
    "data/rainfall/"
    "3B-DAY.MS.MRG.3IMERG.20130712-S000000-E235959.V07B.nc4.SUB.nc4"
)

# Open NASA NetCDF file
ds = xr.open_dataset(file_path)

print("=" * 60)
print("NASA IMERG RAINFALL FILE")
print("=" * 60)

print("\nDataset:")
print(ds)

print("\nVariables:")
print(list(ds.data_vars))

print("\nCoordinates:")
print(list(ds.coords))

print("\nPrecipitation information:")
print(ds["precipitation"])

ds.close()
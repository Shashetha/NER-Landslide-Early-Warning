import os
import glob
import rasterio


DEM_DIR = "data/terrain/dem"

files = sorted(glob.glob(os.path.join(DEM_DIR, "*.tif")))

print("=" * 60)
print("COPERNICUS DEM VALIDATION")
print("=" * 60)

print(f"DEM files found: {len(files)}")
print()

if len(files) != 30:
    print("WARNING: Expected 30 DEM files.")
else:
    print("✓ Correct number of DEM tiles found.")

print()

failed = []

for i, file in enumerate(files, 1):

    name = os.path.basename(file)

    try:
        with rasterio.open(file) as src:

            width = src.width
            height = src.height
            crs = src.crs
            resolution = src.res
            bounds = src.bounds

            # Read elevation data
            data = src.read(1, masked=True)

            valid_pixels = data.compressed()

            if len(valid_pixels) == 0:
                raise ValueError("No valid elevation pixels")

            min_elevation = valid_pixels.min()
            max_elevation = valid_pixels.max()

            print(f"[{i:02d}/30] {name}")
            print(f"      CRS: {crs}")
            print(f"      Resolution: {resolution}")
            print(f"      Size: {width} x {height}")
            print(
                f"      Elevation: "
                f"{min_elevation:.2f} to {max_elevation:.2f} m"
            )
            print()

    except Exception as e:

        print(f"[{i:02d}/30] FAILED: {name}")
        print(f"      Error: {e}")
        print()

        failed.append(name)


print("=" * 60)
print("VALIDATION SUMMARY")
print("=" * 60)

print(f"Total files: {len(files)}")
print(f"Valid files: {len(files) - len(failed)}")
print(f"Failed files: {len(failed)}")

if failed:
    print()
    print("Failed tiles:")
    for name in failed:
        print(f"  - {name}")
else:
    print()
    print("✓ ALL 30 DEM TILES ARE VALID")
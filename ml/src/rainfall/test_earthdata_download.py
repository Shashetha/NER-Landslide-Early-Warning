import earthaccess

print("=" * 60)
print("NASA EARTHDATA DOWNLOAD TEST")
print("=" * 60)

# Login
auth = earthaccess.login()

print("\nAuthentication successful!")

# Search for one IMERG daily file
results = earthaccess.search_data(
    short_name="GPM_3IMERGDF",
    version="07",
    temporal=("2013-07-12", "2013-07-12"),
    bounding_box=(94.05, 25.57, 94.17, 25.68),
)

print(f"\nFiles found: {len(results)}")

if results:
    print("\nFirst result:")
    print(results[0])

    print("\nDownloading test file...")

    files = earthaccess.download(
        results[0],
        "data/rainfall"
    )

    print("\nDownload completed!")
    print(files)
else:
    print("\nNo files found.")
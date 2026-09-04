import earthaccess
from harmony import Client, Request, Collection, BBox
from datetime import datetime
import os

OUTPUT_DIR = "data/rainfall/harmony_test"
os.makedirs(OUTPUT_DIR, exist_ok=True)

client = Client(token=earthaccess.get_edl_token())

collection = Collection(id="C2723754864-GES_DISC")

request = Request(
    collection=collection,
    spatial=BBox(92.0, 22.0, 96.0, 29.0),
    temporal={
        "start": datetime(2010, 6, 1),
        "stop": datetime(2010, 6, 2),
    },
    variables=["precipitation"],
    format="application/netcdf",
)

print("Request valid:", request.is_valid())

if not request.is_valid():
    print("Request errors:")
    print(request.errors)
    raise SystemExit(1)

print("Submitting Harmony request...")
job_id = client.submit(request)

print("Job ID:", job_id)
print("Waiting for NASA Harmony...")

client.result_json(job_id, show_progress=True)

print("Downloading result...")

files = client.download_all(
    job_id,
    directory=OUTPUT_DIR,
    overwrite=True
)

for f in files:
    print("Downloaded:", f.result())

print("DONE")

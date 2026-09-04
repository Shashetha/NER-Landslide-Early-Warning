import requests

url = "https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGDF.07/2013/07/12/3B-DAY.MS.MRG.3IMERG.20130712-S000000-E235959.V07B.1day.tif"

response = requests.get(url)

print("HTTP status:", response.status_code)
print("Content type:", response.headers.get("Content-Type"))
print("File size:", len(response.content), "bytes")
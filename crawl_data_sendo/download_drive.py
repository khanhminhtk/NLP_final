import wget
import zipfile
import os


version_number = "131.0.6778.87"
download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{version_number}/win64/chromedriver-win64.zip"
latest_driver_zip = wget.download(download_url,'chromedriver.zip')

with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
    zip_ref.extractall(r"./chrome_driver")
os.remove(latest_driver_zip)
"""
KoeBridge for Zoom — Argos Translate EN->JA Package Installer & Verification
"""

import urllib.request
import hashlib
import json
import zipfile
import argostranslate.package
import argostranslate.translate

URL = "https://argos-net.com/v1/translate-en_ja-1_1.argosmodel"
LOCAL_PATH = "translate-en_ja-1_1.argosmodel"

print(f"Downloading {URL}...")
req = urllib.request.Request(URL, headers={"User-Agent": "KoeBridge/1.0"})
with urllib.request.urlopen(req) as resp, open(LOCAL_PATH, "wb") as f:
    f.write(resp.read())

# Compute SHA-256 and size
with open(LOCAL_PATH, "rb") as f:
    data = f.read()
    size_mb = len(data) / (1024 * 1024)
    sha256 = hashlib.sha256(data).hexdigest()

print(f"Downloaded artifact size: {size_mb:.2f} MB")
print(f"Artifact SHA-256: {sha256}")

# Inspect archive contents
with zipfile.ZipFile(LOCAL_PATH, "r") as z:
    names = z.namelist()
    print("Files in archive:", names)
    if "metadata.json" in names:
        meta = json.loads(z.read("metadata.json").decode())
        print("metadata.json:")
        print(json.dumps(meta, indent=2))

# Install into argostranslate local cache
print("Installing model into local argostranslate repository...")
argostranslate.package.install_from_path(LOCAL_PATH)

installed = argostranslate.translate.get_installed_languages()
print("Installed languages:", [f"{lang.name} ({lang.code})" for lang in installed])

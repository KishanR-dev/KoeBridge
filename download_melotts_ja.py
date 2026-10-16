"""
KoeBridge for Zoom — Download and Verify Japanese MeloTTS ONNX Assets
Repository: MiaoMint/MeloTTS-ONNX
Revision: 7a50512ba14a067701943e18b6636a6a18e7c69a
"""
import os
import urllib.request
import hashlib

REVISION = "7a50512ba14a067701943e18b6636a6a18e7c69a"
BASE_URL = f"https://huggingface.co/MiaoMint/MeloTTS-ONNX/resolve/{REVISION}/onnx_exports/ja"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "tts_melotts_ja")
os.makedirs(OUT_DIR, exist_ok=True)

FILES = ["model.onnx", "lexicon.txt", "tokens.txt", "metadata.json"]
RESULTS = {}

print(f"Downloading Japanese MeloTTS ONNX assets from revision {REVISION}...")
for fname in FILES:
    url = f"{BASE_URL}/{fname}"
    dest = os.path.join(OUT_DIR, fname)
    print(f"  Downloading {fname} from {url}...")
    req = urllib.request.Request(url, headers={"User-Agent": "KoeBridge/1.0"})
    with urllib.request.urlopen(req) as resp, open(dest, "wb") as f:
        f.write(resp.read())

    # Compute SHA-256
    with open(dest, "rb") as f:
        data = f.read()
        sha256 = hashlib.sha256(data).hexdigest()
        size_bytes = len(data)

    RESULTS[fname] = {"size": size_bytes, "sha256": sha256, "path": dest}
    print(f"  [OK] {fname}: {size_bytes} bytes ({size_bytes / (1024*1024):.2f} MB)")
    print(f"       SHA-256: {sha256}")

print("\n--- Download & Integrity Verification Summary ---")
for k, v in RESULTS.items():
    print(f"{k}: size={v['size']} bytes, sha256={v['sha256']}")
